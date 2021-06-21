import os.path
import secrets

from manage import app


def save_user_account_image(image):
    random_hex = secrets.token_hex(16)
    _, extension = os.path.splitext(image.filename)
    image_filename = random_hex + extension
    image_path = os.path.join(app.root_path, 'static/media/users', image_filename)
    image.save(image_path)
    return image_filename
