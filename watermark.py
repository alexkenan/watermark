"""
Module that adds a Text watermark to an image
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont


def watermark(image_before, text, font, newpath, coords=None, color=(255, 255, 255)):
    """
    Main watermark program
    :param image_before: (str) Path to an image to insert the watermark
    :param text: (str) Text to be inserted into the image
    :param font: (tup of ImageFont and int) Font of the text to be inserted and size
    as (Font, Size)
    :param newpath: (str) New path to directory of watermarked images
    :param coords: (tup) Coordinates to insert the text into the image (X, Y)
    :param color: (tup) RGBA tuple for a font color
    :return: None
    """
    image = Image.open(image_before)
    width, height = image.size

    draw = ImageDraw.Draw(image)

    __, textheight = draw.textsize(text, font)

    # Use the given coordinates
    if coords:
        x = coords[0]
        y = coords[1]
    else:
        # calculate the x,y coordinates of the text
        margin = 5
        x = 0 + margin
        y = height - textheight - margin

    if x > width:
        raise Exception("Given x coordinate ({}) is greater than image width ({})".format(x, width))
    if y > height:
        raise Exception("Given y coordinate ({}) is greater than image height ({})".format(y, height))

    # draw watermark in the bottom right corner
    draw.text((x, y), text, font=font, fill=color)

    newname = os.path.join(newpath, image_before)

    image.save('{}'.format(newname))
    print("Watermarked {}".format(os.path.basename(image_before)))


def main():
    """
    Do some managing
    :return: None
    """
    # Go to the correct directory for the images
    while True:
        folderpaths = input('What is the absolute folder path of the pictures? ')
        if not os.path.exists(folderpaths):
            print('"{}" isn\'t a valid folder path!'.format(folderpaths))
        else:
            break
    base = os.path.split(folderpaths)[0]
    newfolderpath = os.path.join(base, 'watermarked')
    os.mkdir(newfolderpath)
    os.chdir(newfolderpath)

    # Set up the parameters
    img_font = ImageFont.truetype('/Library/Fonts/Bradley Hand Bold.ttf', 36)
    waterm = "Alex Kenan 2017"

    # Copy old photos into new folder
    for photo in os.listdir(folderpaths):
        if 'DS_Store' not in photo and '.' in photo:
            shutil.copy(os.path.join(folderpaths, photo), os.path.join(newfolderpath, photo))

    i = 1
    for photo in os.listdir(newfolderpath):
        if 'DS_Store' not in photo and '.' in photo:
            watermark(os.path.join(newfolderpath, photo), waterm, img_font, newfolderpath)
            i += 1
    print('Watermarked {} images!'.format(i))
    print('New images located in {}'.format(newfolderpath))

if __name__ == '__main__':
    main()
