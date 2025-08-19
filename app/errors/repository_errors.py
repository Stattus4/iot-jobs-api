# -*- coding: utf-8 -*-

class RepositoryError(Exception):
    """Base class for repository errors"""


class DeviceNotFoundError(RepositoryError):
    """Raised when a device is not found in the database"""


class DuplicateDeviceError(RepositoryError):
    """Raised when a device with the same IMEI already exists"""
