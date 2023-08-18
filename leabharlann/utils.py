from io import BytesIO
from PIL import Image
from django.core.files import File


def edit_image(image, width, height):
    """
    Function to edit an image to a specified width and height.
    """
    img = Image.open(image)
    new_img = img.resize((width, height), Image.ANTIALIAS)
    new_img_io = BytesIO()
    new_img.save(new_img_io, format="JPEG", quality=100)
    new_image = File(new_img_io, name=image.name)
    return new_image
