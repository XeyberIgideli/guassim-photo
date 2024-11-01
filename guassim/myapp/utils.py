import os
import uuid

def unique_image_path(instance, filename,folder_name):
    """
    Generate a unique filename for uploaded images
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(folder_name + '/', unique_filename)