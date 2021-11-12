import os, sys
from PIL import Image

'''
python3 resizer infile width*height
'''

class Resizer(object):
    def __init__(self):
        pass

    def get_outfile(self, infile, width, height):
        root, ext = os.path.splitext(infile)
        # Image.NEAREST (0), Image.LANCZOS (1), Image.BILINEAR (2), Image.BICUBIC (3), Image.BOX (4) or Image.HAMMING (5)
        outfile = Image.open(infile).resize((width, height), Image.NEAREST)
        outfile.save('{}_out{}'.format(root, ext))
        return outfile

    def resize_image(self, infile_or_indir, width_height):
        (width, height) = width_height.split('*')
        (width, height) = (int(width), int(height))
        if os.path.isfile(infile_or_indir):
            infile = infile_or_indir
            self.get_outfile(infile, width, height)
        elif os.path.isdir(infile_or_indir):
            indir = infile_or_indir
            for root, dirs, files in os.walk(indir):
                for file in files:
                    infile = os.path.join(root, file)
                    self.get_outfile(infile, width, height)
        else:
            return 1

        return 0


if __name__ == '__main__':
    r = Resizer()
    r.resize_image(sys.argv[1], sys.argv[2])
