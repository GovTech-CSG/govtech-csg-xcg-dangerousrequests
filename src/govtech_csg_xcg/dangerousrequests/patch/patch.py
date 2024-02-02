# ------------------------------------------------------------------------
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# This file incorporates work covered by the following copyright:
#
# Copyright (c) 2023 Agency for Science, Technology and Research (A*STAR).
#   All rights reserved.
# Copyright (c) 2023 Government Technology Agency (GovTech).
#   All rights reserved.
# ------------------------------------------------------------------------
import requests

from .utils import get_requests_handle


class Patcher:
    """this class will do the patching and reverting of dangerous functions"""

    @classmethod
    def do_patch(cls):
        """this function will monkey patch dangerous functions"""

        patched_requests = get_requests_handle()
        requests.get = patched_requests.get
        requests.delete = patched_requests.delete
        requests.head = patched_requests.head
        requests.post = patched_requests.post
        requests.put = patched_requests.put
        requests.session = patched_requests.session
        requests.options = patched_requests.options
        requests.patch = patched_requests.patch
        requests.request = patched_requests.request
        requests.Session = patched_requests.Session

    @classmethod
    def revert(cls):
        """this function will revert back the original functions"""
        pass
