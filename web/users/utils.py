import os.path
import secrets

from PIL import Image

from services import app


def save_user_account_image(image):
    random_hex = secrets.token_hex(16)
    _, extension = os.path.splitext(image.filename)
    image_filename = random_hex + extension
    image_path = os.path.join(app.root_path, 'static/media/users', image_filename)

    output_size = (256, 256)
    i = Image.open(image)
    i.thumbnail(output_size)

    i.save(image_path)
    return image_filename
