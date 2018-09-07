import numpy as np
import mrcfile
import imageio
from PIL import Image

def image_read(image_path, region=None):
    image_path = str(image_path)
    if image_path.endswith(("jpg", "png")):
        if not is_single_channel(image_path):
            raise Exception("Not supported image format. Movie files are not supported")
            return None
        img = imageio.imread(image_path, pilmode="L", as_gray=True)
        img = img.astype(np.uint8)
    elif image_path.endswith(("tiff", "tif")):
        img = imageio.imread(image_path)
       # img = np.flipud(img)
    elif image_path.endswith("mrc"):
        if not is_single_channel(image_path):
            raise Exception("Not supported image format. Movie files are not supported")
            return None

        img = read_mrc(image_path)
        img = np.squeeze(img)
        if np.issubdtype(img.dtype, np.integer):
            img = img.astype(dtype=np.uint8)
    else:
        raise Exception("Not supported image format: " + image_path)

    # OpenCV has problems with some datatypes
    if np.issubdtype(img.dtype, np.uint32):
        img = img.astype(dtype=np.float64)

    if np.issubdtype(img.dtype, np.float16):
        img = img.astype(dtype=np.float32)

    if region is not None:
        return img[region[1], region[0]]
    return img

def is_single_channel(image_path):
    if image_path.endswith(("jpg", "png", "tiff", "tif")):
        im = Image.open(image_path)
        if len(im.size) > 2:
            return False

    if image_path.endswith("mrc"):
        with mrcfile.open(image_path, permissive=True) as mrc:
            if mrc.header.nz > 1:
                return False

    return True

def read_mrc(image_path):
    with mrcfile.open(image_path, permissive=True) as mrc:
        mrc_image_data = np.copy(mrc.data)
    mrc_image_data = np.flipud(mrc_image_data)

    return mrc_image_data
