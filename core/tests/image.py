from io import BytesIO
from PIL import Image
from django.core.files.base import File


def get_image_file(name='test.png', ext='png', size=(1, 1), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)
