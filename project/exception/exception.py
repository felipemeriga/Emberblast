#  We want to keep development and programming errors away from the user, and show
#  custom error messages, while the application runtime errors will be saved in the log.
class ConfigFileError(Exception):
    """Base class for other exceptions"""
    pass
