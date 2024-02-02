import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from typing import Any
from unittest import skipUnless

from django.test import SimpleTestCase
from parameterized import parameterized

from govtech_csg_xcg.dangerousrequests.advocate.exceptions import (
    UnacceptableAddressException,
    UnacceptableRequestException,
)

SETTINGS_MODULE_NAME = os.environ["DJANGO_SETTINGS_MODULE"].split(".")[-1]
RUN_FLAKY_TESTS = os.getenv("DANGEROUS_REQUESTS_RUN_FLAKY_TESTS", False)


class SilentHttpRequestHandler(SimpleHTTPRequestHandler):
    """Override the log_message method to turn off logging so as to not clutter the test logs."""

    def log_message(self, format: str, *args: Any) -> None:
        pass


def start_threaded_http_server(port):
    """Start a HTTP server on localhost at the specified port
    in a separate thread, for testing certain requests."""

    def serve_forever(server):
        with server:
            server.serve_forever()

    server = HTTPServer(("127.0.0.1", port), SilentHttpRequestHandler)
    Thread(target=serve_forever, args=(server,), daemon=True).start()
    return server


class TestDangerousRequests(SimpleTestCase):
    """Tests for the govtech_csg_xcg.dangerousrequests app."""

    def setUp(self):
        # Import the requests package here so that
        # the dangerousrequests package can patch
        # the requests module - happens when the Django
        # app is fully loaded.
        import requests

        self.requests = requests

    def tearDown(self):
        # Make sure to tear down any test HTTP servers that
        # were set up during the tests. This prevents a situation
        # where an exception occurs during the test and the
        # server is just left running.
        if hasattr(self, "http_server"):
            self.http_server.shutdown()

    # Request blacklist should be used to blacklist entire "sets" of requests.
    # E.g. Requests to https://httpbin.org/anything with any method. On the other hand,
    # request whitelist can be used to make exceptions for specific requests, e.g.
    # POST requests to https://httpbin.org/anything
    @parameterized.expand(
        [
            ("GET", "https://httpbin.org/anything"),
            ("OPTIONS", "https://httpbin.org/anything"),
            ("HEAD", "https://httpbin.org/anything"),
            ("PUT", "https://httpbin.org/anything"),
            ("PATCH", "https://httpbin.org/anything"),
            ("DELETE", "https://httpbin.org/anything"),
        ]
    )
    @skipUnless(SETTINGS_MODULE_NAME == "test_request_black_and_whitelist", "")
    def test_request_blacklist_denies_blacklisted_requests(self, method, url):
        with self.assertRaises(UnacceptableRequestException):
            self.requests.request(method, url)

    @skipUnless(
        SETTINGS_MODULE_NAME == "test_request_black_and_whitelist" and RUN_FLAKY_TESTS,
        "",
    )
    def test_request_whitelist_overrides_blacklist(self):
        # We make an actual request here because we can't
        # use "request_whitelist" to whitelist "localhost" - the
        # request will get past the "request filter" but will still
        # be denied at the IP level.
        response = self.requests.post("http://httpbin.org/anything")
        self.assertGreaterEqual(response.status_code, 200)

    @skipUnless(SETTINGS_MODULE_NAME == "test_hostname_blacklist", "")
    def test_hostname_blacklist_denies_blacklisted_hostname(self):
        with self.assertRaises(UnacceptableAddressException):
            self.requests.post("https://google.com")

    @skipUnless(SETTINGS_MODULE_NAME == "test_hostname_blacklist", "")
    def test_hostname_blacklist_overrides_request_whitelist(self):
        with self.assertRaises(UnacceptableAddressException):
            self.requests.post("https://httpbin.org/anything")

    @parameterized.expand(
        [
            ("1",),
            ("81",),
            ("444",),
            ("8001",),
            ("8444",),
            ("9999",),
            ("10423",),
            ("65535",),
        ]
    )
    @skipUnless(SETTINGS_MODULE_NAME == "default_config", "")
    def test_all_ports_blacklisted_by_default(self, port_str):
        """All ports are rejected unless explicitly (or by default) whitelisted."""
        with self.assertRaises(UnacceptableAddressException):
            self.requests.get(f"http://127.0.0.1:{port_str}")

    @skipUnless(SETTINGS_MODULE_NAME == "test_port_black_and_whitelist", "")
    def test_explicit_port_whitelist_allows_request_to_target_port(self):
        self.server = start_threaded_http_server(9999)
        try:
            response = self.requests.get("http://127.0.0.1:9999")
        except Exception as err:
            self.assertFalse(isinstance(err, UnacceptableAddressException))
            raise err
        else:
            self.assertEqual(response.status_code, 200)

    @skipUnless(SETTINGS_MODULE_NAME == "test_port_black_and_whitelist", "")
    def test_explicit_port_blacklist_overrides_explicit_whitelist(self):
        with self.assertRaises(UnacceptableAddressException):
            self.requests.get("http://127.0.0.1:9998")

    @parameterized.expand(
        [
            ("127.0.0.1",),
            ("0.0.0.0",),
        ]
    )
    @skipUnless(SETTINGS_MODULE_NAME == "default_config", "")
    def test_loopback_ips_blocked_by_default(self, local_ip):
        with self.assertRaises(UnacceptableAddressException):
            self.requests.get(f"http://{local_ip}:80")

    @parameterized.expand(
        [
            ("169.254.169.254",),
            ("1.0.0.1",),
            ("1.1.1.0",),
        ]
    )
    @skipUnless(SETTINGS_MODULE_NAME == "test_ip_black_and_whitelist", "")
    def test_explicit_ip_blacklist_denies_request_to_target_ip(self, blacklisted_ip):
        with self.assertRaises(UnacceptableAddressException):
            self.requests.get(f"http://{blacklisted_ip}")

    @skipUnless(
        SETTINGS_MODULE_NAME == "test_ip_black_and_whitelist" and RUN_FLAKY_TESTS, ""
    )
    def test_explicit_ip_whitelist_overrides_explicit_blacklist(self):
        try:
            # Use Cloudflare's DNS resolver website for testing.
            # We make an actual request here because testing with
            # a loopback IP address might confound the testing, since
            # the default behaviour is to deny loopback addresses. It
            # feels cleaner to use a known public IP that is included
            # in the explicit blacklist range, but also explicitly included
            # in the explicit whitelist.
            response = self.requests.get("https://1.1.1.1")
        except Exception as err:
            self.assertFalse(isinstance(err, UnacceptableAddressException))
            raise err
        else:
            self.assertEqual(response.status_code, 200)
