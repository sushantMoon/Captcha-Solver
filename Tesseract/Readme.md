# Installing Tesseract 

## Dependencies 

```sh
sudo apt-get install libpng-dev libjpeg-dev libtiff-dev zlib1g-dev
sudo apt-get install gcc g++
sudo apt-get install autoconf automake libtool
sudo apt-get install autoconf-archive zlib1g-dev libtiff5-dev libjpeg8-dev pkg-config libpng12-dev libleptonica-dev
```

For Training Tools 

```sh
sudo apt-get install libicu-dev libpango1.0-dev libcairo2-dev
```

### Leptonica 

[Image Processing Toolkit](http://leptonica.com/) required to build Tesseract. 

#### Installing Leptonica 

```sh
cd "/media/feliz/Safira/GitHub/Captcha-Solver/Tesseract/"
wget https://github.com/DanBloomberg/leptonica/releases/download/1.74.4/leptonica-1.74.4.tar.gz
tar -zxvf leptonica-1.74.4.tar.gz
cd leptonica-1.74.4
./configure
make
sudo checkinstall
sudo ldconfig
```

This installed the Leptonica as a Package, giving it nice properties like install/uninstall using dpkg package manager.
To remove use command `dpkg -r leptonica`

## Tesseract 

Date: 20 August 2017
Version : Tesseract 4.0.0 - alpha

```sh
cd /media/feliz/Safira/GitHub/Captcha-Solver/Tesseract
git clone https://github.com/tesseract-ocr/tesseract.git
cd tesseract
./autogen.sh
./configure
make
sudo make install
sudo ldconfig
make training
sudo make training-install 
sudo ldconfig
```

### Language Data :

```sh
cd tessdata
wget https://github.com/tesseract-ocr/tessdata/raw/4.00/eng.traineddata
sudo mkdir /usr/local/share/tessdata
cd ..
sudo cp -r tessdata/* /usr/local/share/tessdata
```

Add the following line to ~/.bashrc file

```vim
export TESSDATA_PREFIX=/usr/local/share/
```

# Reference 

* https://github.com/tesseract-ocr/tesseract/blob/master/INSTALL.GIT.md
* https://github.com/tesseract-ocr/tesseract/wiki/Compiling
* https://www.linux.com/blog/using-tesseract-ubuntu
* https://github.com/tesseract-ocr/tesseract/wiki/Data-Files
* https://github.com/tesseract-ocr/tesseract