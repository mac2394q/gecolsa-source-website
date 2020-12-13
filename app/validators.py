from django.core.validators import BaseValidator


class FileSizeValidator(BaseValidator):
    """Validate a file size. Size must be given in Kb."""
    message = 'El peso del archivo debe ser menor al máximo permitido'
    code = 'file_size'

    def compare(self, a, b):
        return a.size > 1024 * b
