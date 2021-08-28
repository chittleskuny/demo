import os, sys
from PIL import Image

'''
python3 resizer infile width*height
'''


def get_outfile(infile):
    root, ext = os.path.splitext(infile)
    outfile = '{}_out{}'.format(root, ext)
    return outfile


def resize_image(infile, width_height):
    (width, height) = width_height.split('*')
    out = Image.open(infile).resize((int(width), int(height)), Image.ANTIALIAS)
    out.save(get_outfile(infile))


if __name__ == '__main__':
    resize_image(sys.argv[1], sys.argv[2])