# -*- coding: utf-8 -*-

class ServiceError(Exception):
    """Base class for service errors"""


class DeviceAlreadyExistsError(ServiceError):
    """Raised when creating a device that already exists"""


class DeviceDeletionError(ServiceError):
    """Raised when a device could not be deleted"""


class DeviceDoesNotExistError(ServiceError):
    """Raised when trying to access a device that does not exist"""
