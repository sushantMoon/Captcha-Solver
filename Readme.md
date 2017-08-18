# Objective :

This is an attempt to solve the capthca given out in www.mca.gov.in
Note : Few of the steps are mentioned in `KarzaTest.pdf`


# crawler.py :

Script using the following tech stack, no machine learning and not much of opencv stuff. 

## Technologies :

* Python
* Selenium 
* Tesseract-ORC

## Script Logic :

1. Script simulate the chrome browser using selenium and open the link - http://www.mca.gov.in/
2. Once the page is loaded, we click on "View Company or LLP Master Data". This opens a new tab. We switch to the newly opened tab.
3. The script then takes screenshot of the captcha, and attempts at solving it using tesseract-ocr.
4. If it succeeds, we download the data loaded by website using export to excel. And If it fails, we re-try solving. If the second attemp fails, script closes the browser and again start form Step 1.
5. This is repeated till we get data for all the Complany CINs of our interset.


# captcha.py | cv-crawler.py | parse_captcha.py :

Testing and Reference Script for OpenCV and Machine learning 

## Technologies :

* Python
* opencv3
