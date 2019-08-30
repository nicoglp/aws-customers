class ServiceException(Exception):

    def __init__(self, message):
        super(ServiceException, self).__init__()
        self.message = message

    def __str__(self):
        return repr('Service exception - {}'.format(self.message))


class ValidationError(ServiceException):
    """
    REST - 400
    """
    def __init__(self, errors=None, warnings=None):
        super(ValidationError, self).__init__("Validation errors")
        self.warnings = warnings if warnings else []
        self.errors = errors if errors else []


class EntityNotFoundError(ServiceException):
    """
    REST - 404
    """
    def __init__(self, id):
        super(EntityNotFoundError, self).__init__("Entity with id {} does not exist".format(id))
        self.id = id
