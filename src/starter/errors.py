#!/usr/bin/env python


class Error(Exception):
    """
    Base class for starter-specific errors
    """
    def __init__(self, message: str=""):
        self.message = message


class WrongConfiguration(Error):
    def __init__(self, message, payload):
        self.message = message
        self.payload = payload
