class NotifyCallbackError(Exception):
    def __init__(self, message, error, error_description):
        super().__init__(message)
        self.message = message
        self.error = error
        self.error_description = error_description

    def getMessage(self):
        alert_message = {
            'message': self.message,
            'error' : self.error,
            'error_description': self.error_description
        }
        return alert_message