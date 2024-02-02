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
import inspect
import pprint

from django.conf import settings

from govtech_csg_xcg.dangerousrequests.advocate import AddrValidator, RequestsAPIWrapper


def is_disabled(sig):
    """not implemented. this function is to check whether the specified function is disabled"""
    return True
    # TODO: check whether sig is disabled
    # return sig in black_list


def get_strategy(sig):
    """get the strategy for the specified function"""
    if not hasattr(settings, "XCG_SECURITY"):
        middleware_settings = {}
    else:
        middleware_settings = settings.XCG_SECURITY
    return middleware_settings.get(sig, {})


def get_validator_setting():
    return get_strategy("requests")


def debug():
    """print stack information"""
    stack_info = inspect.stack()
    for stack in stack_info:
        pprint.pprint(stack)


def get_info_from_stack():
    """get source code information from `inspect.stack()`"""
    stack_info = inspect.stack()
    target_frame = stack_info[2]
    return (
        target_frame.filename,
        target_frame.lineno,
        target_frame.function,
        target_frame.code_context,
    )


def in_scope(filename: str) -> bool:
    """determine whether the file is inside the django project"""
    if filename is None:
        return False
    return filename.startswith(str(settings.BASE_DIR))


def get_validator():
    """get the validator for advocate"""
    return AddrValidator(**get_validator_setting())


def get_requests_handle():
    """get the advocate api wrapper with validator"""
    return RequestsAPIWrapper(get_validator())
