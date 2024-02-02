from .default_config import *  # noqa: F401, F403

XCG_SECURITY = {
    "requests": {
        "request_blacklist": {"httpbin.org", ("httpbin.org", "POST", "/anything")},
        "request_whitelist": {("httpbin.org", "POST", "/anything")},
    }
}
