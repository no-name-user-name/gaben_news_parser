import re
from io import BytesIO

from PIL import Image

from config import tags, admins
from gaben.bot import get_bot


def clear_text_format(txt):
    txt = txt.strip()
    txt = txt.replace('\n\n', '\n').replace('\t', '')
    if txt[0:1] == '\n':
        txt = txt[1:]

    while txt[-1] == '\n':
        txt = txt[0:-1]

    while txt[-1] == ' ':
        txt = txt[0:-1]

    while txt[0] == ' ':
        txt = txt[1:]

    return txt


def set_tags(data):
    data_tags = []
    out = ''
    for each_tag in tags:
        if re.search(each_tag, data):
            data_tags.append(tags[each_tag])
    x = data_tags
    data_tags = sorted(set(x), key=lambda d: x.index(d))
    for each in data_tags:
        out = out + each + ' '
    return out


def image_to_byte_array(image: Image) -> bytes:
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


def catcherError(func):
    def f(*args, **kwargs):
        try:
            out = func(*args, **kwargs)
            return out
        except Exception as e:
            msg = f"[!] Error in {func.__name__}: {e}"
            get_bot().send_message(admins[0], msg)
            print(msg)

    return f
