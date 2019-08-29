class ServiceException(Exception):

    def __init__(self, message):
        super(ServiceException, self).__init__()
        self.message = message

    def __str__(self):
        return repr('Service exception - {}'.format(self.message))
