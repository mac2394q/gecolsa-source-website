import os
import uuid


def get_upload_path(instance, filename):
    """Return a obscured path to upload files
    """
    return os.path.join(
        instance._meta.object_name.lower(),
        uuid.uuid4().hex,
        filename,
    )
