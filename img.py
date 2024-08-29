from io import BytesIO
from PIL import Image
import requests
from hoshino import R, log
from hoshino.typing import MessageSegment
from hoshino.util import pic2b64

logger = log.new_logger('wiki')
UNKNOWN = 1000

def download_icon(num, types):
    url = f'https://redive.estertion.win/icon/{types}/{num}.webp'
    save_path = R.img(f'priconne/{types}/icon_{types}_{num}.png').path
    logger.info(f'Downloading {types} icon from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=5)
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        logger.exception(e)
    if 200 == rsp.status_code:
        img = Image.open(BytesIO(rsp.content))
        img.save(save_path)
        logger.info(f'Saved to {save_path}')
    else:
        logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')

def icon(num, types):
    res = R.img(f'priconne/{types}/icon_{types}_{num}.png')
    if not res.exist:
        download_icon(num, types)
        res = R.img(f'priconne/{types}/icon_{types}_{num}.png')
    if not res.exist:
        res = R.img(f'priconne/unit/icon_unit_{UNKNOWN}31.png')
    return res

def resize_icon(num,size=64,types='skill'):
    pic = icon(num,types).open().convert('RGBA').resize((size, size), Image.LANCZOS)
    return str(MessageSegment.image(pic2b64(pic)))