__version__ = "1.0.0"

from requests import utils
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    RequestException,
    Timeout,
    TooManyRedirects,
    URLRequired,
)
from requests.models import PreparedRequest, Request, Response
from requests.status_codes import codes

from .adapters import ValidatingHTTPAdapter
from .addrvalidator import AddrValidator
from .api import *
from .exceptions import UnacceptableAddressException
