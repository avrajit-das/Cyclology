from PIL import Image
import os

INPUT_DIR = "images"
OUTPUT_DIR = "watermarked_images"
WATERMARK_FILE = "molex.png"
# The watermark will take up 15% of the horizontal space on landscape images
LANDSCAPE_SCALE_FACTOR = 0.15
# 30% on portrait images
PORTRAIT_SCALE_FACTOR = 0.30
# 20% on images of equal size
EQUAL_SCALE_FACTOR = 0.20
# Min and max values the watermark is allowed to be scaled
MIN_SCALE_FACTOR = 0.5
MAX_SCALE_FACTOR = 3
# Padding TODO: Make fluid
PADX = 20
PADY = 5


def clamp(val, _min, _max):
    """Keep a value within a certain limit"""
    if val < _min:
        return _min
    elif val > _max:
        return _max
    else:
        return val


os.makedirs(OUTPUT_DIR, exist_ok=True)

watermark = Image.open(WATERMARK_FILE)
watermark_ratio = watermark.size[0]/watermark.size[1]

image_paths = os.listdir(INPUT_DIR)

for image_path in image_paths:
    try:
        image = Image.open(os.path.join(INPUT_DIR, image_path))
    except OSError:
        print("Bad image, skipping")
        continue

    image_width, image_height = image.size
    # Determine the images postion and then the watermark's new size
    # Image is in the landscape position
    if image_width > image_height:
        # Scales the width of the watermark based on the width of the image
        # while keeping within min/max values
        new_width = int(clamp(image_width * LANDSCAPE_SCALE_FACTOR,
                              watermark.size[0] * MIN_SCALE_FACTOR,
                              watermark.size[0] * MAX_SCALE_FACTOR))
        # Determine height from new width and old height/width ratio
        new_height = int(new_width / watermark_ratio)
    # Image is in the portrait position
    elif image_width < image_height:
        new_width = int(clamp(image_width * PORTRAIT_SCALE_FACTOR,
                              watermark.size[0] * MIN_SCALE_FACTOR,
                              watermark.size[0] * MAX_SCALE_FACTOR))
        new_height = int(new_width / watermark_ratio)
    # Image is equal sided
    else:
        new_width = int(clamp(image_width * EQUAL_SCALE_FACTOR,
                              watermark.size[0] * MIN_SCALE_FACTOR,
                              watermark.size[0] * MAX_SCALE_FACTOR))
        new_height = int(new_width / watermark_ratio)

    # Resize watermark
    watermark_copy = watermark.copy().resize((new_width, new_height))
    print("New size: {}x{}".format(watermark_copy.size[0],
                                   watermark_copy.size[1]))

    # Calculate position for watermark
    logo_x = image_width - watermark_copy.size[0] - PADX
    logo_y = image_height - watermark_copy.size[1] - PADY
    print("Putting logo at: {}x{}".format(logo_x, logo_y))
    # Paste the resized watermark at the calculated position and save
    output_path = os.path.join(OUTPUT_DIR, image_path)
    print("Applying watermark and saving to to: " + output_path)
    try:
        image.paste(watermark_copy, box=(logo_x, logo_y), mask=watermark_copy)
    except ValueError:
        image.paste(watermark_copy, box=(logo_x, logo_y))
    image.save(output_path)