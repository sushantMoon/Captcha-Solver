import sys
import os
import re
import subprocess
import tempfile
from PIL import Image


def parse_captcha(filename):
    """Return the text for thie image using Tesseract
    """
    img = threshold(filename)
    return tesseract(img)


def threshold(filename, limit=100):
    """Make text more clear by thresholding all pixels above / below this limit to white / black
    """
    # read in colour channels
    img = Image.open(filename)
    # resize to make more clearer
    m = 1.5
    img = img.resize((int(img.size[0]*m), int(img.size[1]*m))).convert('RGBA')
    pixdata = img.load()

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < limit:
                # make dark color black
                pixdata[x, y] = (0, 0, 0, 255)
            else:
                # make light color white
                pixdata[x, y] = (255, 255, 255, 255)
    img.save('tmp/threshold_' + filename)
    return img.convert('L') # convert image to single channel greyscale



def call_command(*args):
    """call given command arguments, raise exception if error, and return output
    """
    c = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = c.communicate()
    if c.returncode != 0:
        if error:
            print error
        print "Error running `%s'" % ' '.join(args)
    return output


def tesseract(image):
    """Decode image with Tesseract  
    """
    # create temporary file for tiff image required as input to tesseract
    input_file = tempfile.NamedTemporaryFile(suffix='.tif')
    image.save(input_file.name)

    # perform OCR
    output_filename = input_file.name.replace('.tif', '.txt')
    call_command('tesseract', input_file.name, output_filename.replace('.txt', ''))
    
    # read in result from output file
    result = open(output_filename).read()
    os.remove(output_filename)
    return clean(result)


def gocr(image):
    """Decode image with gocr
    """
    input_file = tempfile.NamedTemporaryFile(suffix='.ppm')
    image.save(input_file.name)
    result = call_command('gocr', '-i', input_file.name)
    return clean(result)
     

def ocrad(image):
    """Decode image with ocrad
    """
    input_file = tempfile.NamedTemporaryFile(suffix='.ppm')
    image.save(input_file.name)
    result = call_command('ocrad', input_file.name)
    return clean(result)


def clean(s):
    """Standardize the OCR output
    """
    # remove non-alpha numeric text
    return re.sub('[\W]', '', s)



if __name__ == '__main__':
    filenames = sys.argv[1:]
    if filenames:
        for filename in filenames:
            img = threshold(filename)
            print filename
            print 'Tesseract:', tesseract(img)
            print 'Gocr:', gocr(img)
            print 'Ocrad:', ocrad(img)
            print
    else:
        print 'Usage: %s [image1] [image2] ...' % sys.argv[0]
