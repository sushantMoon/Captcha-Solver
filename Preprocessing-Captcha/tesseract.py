import subprocess
import os
import re


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

def clean(s):
	"""Standardize the OCR output
	"""
	# remove non-alpha numeric text
	return re.sub('[\W]', '', s)

def tesseract(imagePath):
	"""Decode image with Tesseract  
	"""
	# perform OCR
	output_filename = imagePath.replace('.jpg', '.txt')
	call_command('tesseract', imagePath, output_filename.replace('.txt', ''), '--oem 2')
	
	# read in result from output file
	result = open(output_filename).read()
	os.remove(output_filename)
	return clean(result)


if __name__ == '__main__':
	print "This script is to be imported and not to be called directly"