import ipaddress

from .default_config import *  # noqa: F401, F403

XCG_SECURITY = {
    "requests": {
        "ip_whitelist": {ipaddress.ip_network("127.0.0.1")},
        "port_blacklist": {9998},
        "port_whitelist": {9998, 9999},
    }
}
