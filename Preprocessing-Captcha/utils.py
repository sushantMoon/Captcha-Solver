from PIL import Image
import cv2
import numpy as np

def downscaleImage(im, max_dim=2048):
	"""
	Shrink image(im) until its longest dimension is <= max_dim.
	Input params
	 1. Image object of PIL.Image type  
	 2. Max Dimension  (default value 2048)
	Output params
	 1. Scale (where scale <= 1).
	 2. Rescaled new Image 
	"""
	a, b = im.size
	if max(a, b) <= max_dim:
		return 1.0, im
	scale = 1.0 * max_dim / max(a, b)
	new_im = im.resize((int(a * scale), int(b * scale)), Image.ANTIALIAS)
	return scale, new_im

def saveImage(img, path, xdpi=300, ydpi=300):
	"""
	This function expects img object of type PIL.Image and saves on the defined path which contains file name.
	Input params
	 1. Image object of PIL.Image type 
	 2. Complete Path along with the file name where the image needs to be saved
	 3. xDPI , yDPI required to be along x,y dimensions respectively (both defaults to 300)   
	"""
	img.save(path, dpi=(xdpi,ydpi))

def rescaleImage(im, type, scale=1, height=150, width=500):
	"""
	This function rescales the image(im) in multiples of scale if salar or height and width if skewed.
	Input params
	 1. Image object of PIL.Image type  
	 2. scale (default value 1)
	Output params
	 1. Rescaled new Image 
	"""
	if type == 'scalar' :
		return im.resize((im.size[0] * scale, im.size[1] * scale) , Image.ANTIALIAS)
	if type == 'skewed' :
		return im.resize((width, height) , Image.ANTIALIAS)

def dilate(ary, N, iterations): 
	"""Dilate using an NxN '+' sign shape. ary is np.uint8."""
	kernel = np.zeros((N,N), dtype=np.uint8)
	kernel[(N-1)/2,:] = 1
	dilated_image = cv2.dilate(ary / 255, kernel, iterations=iterations)
	kernel = np.zeros((N,N), dtype=np.uint8)
	kernel[:,(N-1)/2] = 1
	dilated_image = cv2.dilate(dilated_image, kernel, iterations=iterations)
	return dilated_image

def find_components(edges, max_components=16):
	"""Dilate the image until there are just a few connected components.

	Returns contours for these components."""
	# Perform increasingly aggressive dilation until there are just a few
	# connected components.
	count = 21
	dilation = 5
	n = 1
	while count > 16:
		n += 1
		dilated_image = dilate(edges, N=3, iterations=n)
		_ , contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		count = len(contours)
	# print dilation
	# Image.fromarray(edges).show()
	# Image.fromarray(255 * dilated_image).show()
	return contours

def props_for_contours(contours, ary):
	"""Calculate bounding box & the number of set pixels for each contour."""
	c_info = []
	for c in contours:
		x,y,w,h = cv2.boundingRect(c)
		c_im = np.zeros(ary.shape)
		cv2.drawContours(c_im, [c], 0, 255, -1)
		c_info.append({
			'x1': x,
			'y1': y,
			'x2': x + w - 1,
			'y2': y + h - 1,
			'sum': np.sum(ary * (c_im > 0))/255
		})
	return c_info

def crop_area(crop):
	x1, y1, x2, y2 = crop
	return max(0, x2 - x1) * max(0, y2 - y1)

def union_crops(crop1, crop2):
	"""Union two (x1, y1, x2, y2) rects."""
	x11, y11, x21, y21 = crop1
	x12, y12, x22, y22 = crop2
	return min(x11, x12), min(y11, y12), max(x21, x22), max(y21, y22)

def intersect_crops(crop1, crop2):
	x11, y11, x21, y21 = crop1
	x12, y12, x22, y22 = crop2
	return max(x11, x12), max(y11, y12), min(x21, x22), min(y21, y22)

def find_optimal_components_subset(contours, edges):
	"""Find a crop which strikes a good balance of coverage/compactness.

	Returns an (x1, y1, x2, y2) tuple.
	"""
	c_info = props_for_contours(contours, edges)
	c_info.sort(key=lambda x: -x['sum'])
	total = np.sum(edges) / 255
	area = edges.shape[0] * edges.shape[1]
	c = c_info[0]
	del c_info[0]
	this_crop = c['x1'], c['y1'], c['x2'], c['y2']
	crop = this_crop
	covered_sum = c['sum']
	while covered_sum < total:
		changed = False
		recall = 1.0 * covered_sum / total
		prec = 1 - 1.0 * crop_area(crop) / area
		f1 = 2 * (prec * recall / (prec + recall))
		#print '----'
		for i, c in enumerate(c_info):
			this_crop = c['x1'], c['y1'], c['x2'], c['y2']
			new_crop = union_crops(crop, this_crop)
			new_sum = covered_sum + c['sum']
			new_recall = 1.0 * new_sum / total
			new_prec = 1 - 1.0 * crop_area(new_crop) / area
			new_f1 = 2 * new_prec * new_recall / (new_prec + new_recall)
			# Add this crop if it improves f1 score,
			# _or_ it adds 25% of the remaining pixels for <15% crop expansion.
			# ^^^ very ad-hoc! make this smoother
			remaining_frac = c['sum'] / (total - covered_sum)
			new_area_frac = 1.0 * crop_area(new_crop) / crop_area(crop) - 1
			if new_f1 > f1 or (
					remaining_frac > 0.25 and new_area_frac < 0.15):
				print '%d %s -> %s / %s (%s), %s -> %s / %s (%s), %s -> %s' % (
						i, covered_sum, new_sum, total, remaining_frac,
						crop_area(crop), crop_area(new_crop), area, new_area_frac,
						f1, new_f1)
				crop = new_crop
				covered_sum = new_sum
				del c_info[i]
				changed = True
				break
		if not changed:
			break
	return crop


def pad_crop(crop, contours, edges, border_contour, pad_px=15):
	"""Slightly expand the crop to get full contours.

	This will expand to include any contours it currently intersects, but will
	not expand past a border.
	"""
	bx1, by1, bx2, by2 = 0, 0, edges.shape[0], edges.shape[1]
	if border_contour is not None and len(border_contour) > 0:
		c = props_for_contours([border_contour], edges)[0]
		bx1, by1, bx2, by2 = c['x1'] + 5, c['y1'] + 5, c['x2'] - 5, c['y2'] - 5
	def crop_in_border(crop):
		x1, y1, x2, y2 = crop
		x1 = max(x1 - pad_px, bx1)
		y1 = max(y1 - pad_px, by1)
		x2 = min(x2 + pad_px, bx2)
		y2 = min(y2 + pad_px, by2)
		return crop
	crop = crop_in_border(crop)
	c_info = props_for_contours(contours, edges)
	changed = False
	for c in c_info:
		this_crop = c['x1'], c['y1'], c['x2'], c['y2']
		this_area = crop_area(this_crop)
		int_area = crop_area(intersect_crops(crop, this_crop))
		new_crop = crop_in_border(union_crops(crop, this_crop))
		if 0 < int_area < this_area and crop != new_crop:
			print '%s -> %s' % (str(crop), str(new_crop))
			changed = True
			crop = new_crop
	if changed:
		return pad_crop(crop, contours, edges, border_contour, pad_px)
	else:
		return crop

def threshold(image):
	"""
	Binary Thresholding after grayscaling it.
	Input Param:
		Image Object of type Numpy Array which can be opened with CV2.imshow()
	Output Param:
		Image Object of type Numpy Array which can be opened with CV2.imshow()
	"""
	img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	# Image.fromarray(img).show("Threshold GrayScale")
	img = cv2.medianBlur(img,7)
	# Image.fromarray(img).show("Threshold Blur")
	ret,binaryth = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
	# return adaptiveth
	return binaryth

if __name__ == '__main__':
	print "This script is to be imported and not to be called directly"