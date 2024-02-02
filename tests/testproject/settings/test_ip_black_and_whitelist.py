import ipaddress

from .default_config import *  # noqa: F401, F403

XCG_SECURITY = {
    "requests": {
        "ip_blacklist": {
            ipaddress.ip_network("169.254.169.254"),
            ipaddress.ip_network("1.0.0.0/8"),
        },
        "ip_whitelist": {ipaddress.ip_network("1.1.1.1")},
    }
}
