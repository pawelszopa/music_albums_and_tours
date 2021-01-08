import os
from datetime import datetime
from secrets import token_hex

from werkzeug.utils import secure_filename

from setup import app




def save_image_upload(image):
    date_format = '%Y%m%dT%H%M%S'
    now = datetime.utcnow().strftime(date_format)
    random_string = token_hex(2)  # how many bytes
    file_name = random_string + '_' + now + '_' + image.data.filename
    # w data jest file
    file_name = secure_filename(file_name)
    image.data.save(os.path.join(app.config['IMAGE_UPLOADS'], file_name))
    return file_name
