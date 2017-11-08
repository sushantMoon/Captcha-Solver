import cv2
from utils import *
from scipy.ndimage.filters import rank_filter
import random

# Imported in Utils.py
# from PIL import Image

# Tesseract 
from tesseract import *

# Debug
DEBUG=True

def extraction(imgpath):
	orig_im = Image.open(imgpath)
	scale, im = downscaleImage(orig_im)
	# if DEBUG:
	# 	im.show(title="Downscaled")										# waits indefinitely till one presses anything (prefereably ESC)

	edges = cv2.Canny(np.asarray(im), 100, 200)
	# if DEBUG:
	# 	cv2.imshow("Edges",edges)
	# 	cv2.waitKey(0)								# waits indefinitely till one presses anything (prefereably ESC)
	# 	cv2.destroyAllWindows()

	significantContours = find_components(edges)
	if len(significantContours) == 0:
		print '%s -> No Captcha Found!!!' % imgpath
		return

	crop = find_optimal_components_subset(significantContours, edges)
	crop = pad_crop(crop, significantContours, edges, None)

	crop = [int(x / scale) for x in crop]
	im_cropped = orig_im.crop(crop)
	# if DEBUG:
	# 	im_cropped.show(title="Cropped")

	width = 500
	height = 150
	im_rescaled = rescaleImage(im_cropped,'skewed',1,height,width)
	# if DEBUG:
	# 	im_rescaled.show()										# waits indefinitely till one presses anything (prefereably ESC)
	
	im_threshold = Image.fromarray(threshold(np.asarray(im_rescaled))) 
	if DEBUG:
		im_threshold.show()

	# Sliding Window 
	windowWidth = 100
	for i in range(0,width,windowWidth/2):
		if i <= width - windowWidth:
			crop = im_threshold.crop((i,0,windowWidth+i,height)) # left upper, right lower box # number starts from left upper part of image, i.e left upper pixel is 0,0
			crop.show()
		# break

	# Path to save the image/ Folder Name is specified at the 2nd replace command
	# outpath = imgpath.replace('.jpg', '.cropped.jpg').replace('Captchas','CroppedCaptchas')

	# Saving the pocessed image
	# print outpath
	# saveImage(im_rescaled,outpath)

	# Tesing Tesseract on the precoessed image
	# print tesseract(outpath)
	# os.remove(outpath)

def main():
	# Path for the Captcha Repo/Data/Images 
	path = "/media/feliz/Safira/GitHub/Captcha-Solver/Data/PrivateCircle/Captchas/"
	# Selecting a Random Image
	imgpath = path + str(os.listdir(path)[random.randint(1, 960)])
	extraction(imgpath)
	# imgpath = path + "20170720143854_getCapchaImage.do.jpg"

	# files = os.listdir(path)
	# for i in files:
	# 	if len(i) > 1:
	# 		imgpath = path + i
	# 		print "Image : ",imgpath
	# 		extraction(imgpath)
	# 		if DEBUG:
	# 			break

if __name__ == '__main__':
	main()
else :
	print "This file is not supposed to be imported."
