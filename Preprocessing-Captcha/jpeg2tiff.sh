
# Data Prepration Script
# Steps executed are :
# 1. Rescaling the DPI 
# 2. Converting JPG format to TIFF 
# 3. Generates the corresponding Box File which we shall correct using jTessBoxEditor 2.0 Beta



inputFolder='/media/feliz/Safira/GitHub/Captcha-Solver/Data/PrivateCircle/Kushal/Captchas'
outputFolder='/media/feliz/Safira/GitHub/Captcha-Solver/Data/PrivateCircle/Box-Tiff'
currentFolder=`pwd`

counter=0
cd $inputFolder

for f in `ls *jpg`
do 
	echo "Operating on file : "$f
	path=$outputFolder"/"$counter
  	convert -compress none \
    	    -units PixelsPerInch \
          	-monochrome \
          	-format tiff \
          	-density 300 \
          	$f $path".tif"
	# echo $path
	tesseract $path".tif" $path batch.nochop makebox
	echo "Generated Tif/Box : "$counter".tif"
    ((counter+=1))
done

cd $currentFolder