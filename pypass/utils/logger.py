# -*- coding: utf-8 -*-
"""
    logger
    ~~~~~~
    
    This module contains utilities for logging
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv2, see LICENSE for more details.
"""
import logging
from flask import _request_ctx_stack


class CtxFilter(logging.Filter):
    """
        A filter that injects request information to a log record
    """

    def filter(self, record):
        """
            Injects information to log record
        :param record:
        """
        record.path = ''
        record.method = ''
        record.ip = ''
        record.user_agent = ''
        record.url = ''

        # FIXME: use request correctly
        ctx = _request_ctx_stack.top
        if ctx is not None:
            record.path = ctx.request.path
            record.url = ctx.request.url
            record.method = ctx.request.method
            record.ip = ctx.request.remote_addr
            record.user_agent = ctx.request.headers.get('user-agent', '')
        return True
