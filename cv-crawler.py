#Info : 
# This script attempts as breaking the captcha using opencv techinques more info in readme.md
#
##### How to use the Script #######
# nohup python crawler.py &
#####################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import cv2
from PIL import Image
import tesserocr
from pprint import pprint


loggingFileName = 'Runtime-Karza.log'
URL = "http://www.mca.gov.in/"
outputFileName = "Karza-DataFile"


class Sel():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", {
          "download.default_directory": "/Volumes/Work/Personal-Development/Karza/",
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(chrome_options=self.options)
        # self.driver = webdriver.PhantomJS()
        # self.driver.set_window_size(1120, 550)
        # self.driver.implicitly_wait(30) 
        self.base_url = URL
        self.verificationErrors = []
        self.accept_next_alert = True
        logging.info("Initialization Completed")

    def __del__(self):
        self.driver.close()
        self.driver.quit()
        logging.info("Cleaned and Deleted the Webdriver Instance")

    def crawl(self,cin,count):
        browser = self.driver
        browser.get(self.base_url)
        delay = 10 # Seconds
        try:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,"//button")))
        except Exception as e:
            logging.exception("Took Too much of time to load, the error is: %s",e)

        button = browser.find_element(By.XPATH,"//button")
        button.click()

        # Delay for page to load
        wait = WebDriverWait(browser,delay)
        # Opening the required second page 
        browser.find_element_by_link_text("View Company or LLP Master Data").click()
        time.sleep(3)

        # Focusing on the newly opened page
        browser.switch_to_window(browser.window_handles[1])
        # Waiting for the page to load
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID,"captcha")))
        captcha_dimension = browser.find_element(By.ID,"captcha")
        location = captcha_dimension.location
        size = captcha_dimension.size

        # Taking the Screenshot
        logging.info("Taking Screen Shot for Captcha")
        browser.save_screenshot('screenshot.png')


        # Reading the Screenshot
        img = cv2.imread("/Volumes/Work/Personal-Development/Karza/screenshot.png")
        # width = 1050
        # height = 655
        # print img.shape
        logging.info("Cropping Screen Shot to extract Captcha")
        # NOTE: its img[y: y + h, x: x + w]
        x = int(location['x'])+ 2
        y = int(location['y'])+ 2
        width = int(size['width']) - 3
        height = int(size['height']) - 3
        crop_img = img[y: y + height, x:x + width]
        # logging.info("Saving the cropped Captcha Image")
        cv2.imwrite('Data/captcha_'+str(count)+'.png',crop_img)
        # cv2.imshow("Captcha", crop_img)
        # if (cv2.waitKey(0)):
        #     return

        # Uncomment below
        # image = Image.open('captcha.png')
        
        # Solving the Captcha
        # logging.info("Decrypting the Captcha")
        # captcha = tesserocr.image_to_text(image).strip().lower()  # print ocr text from image
        
        
        # companyID = browser.find_element_by_id("companyID")
        # userEnteredCaptcha = browser.find_element_by_id("userEnteredCaptcha")
        # # logging.info("Entering the values in the fields")
        # companyID.send_keys(cin)
        # # userEnteredCaptcha.send_keys(captcha)
        # userEnteredCaptcha.send_keys(count)

        # browser.find_element_by_id("companyLLPMasterData_0").click()

        # WebDriverWait(browser, delay)
        # try:
        #     logging.info("Checking for successful Captcha breakthrough")
        #     browser.find_element_by_id("exportCompanyMasterData_0")
        # except:
        #     companyID = ''
        #     userEnteredCaptcha = ''
        #     captcha = ''
        #     time.sleep(5)
        #     WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.ID,"msgboxclose")))
        #     browser.find_element_by_id("msgboxclose").click()

        #     logging.exception("Capcha Failed..... Re-Trying for Second Time")
        #     WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID,"companyID")))
        #     logging.info("Taking Screen Shot once again")
        #     browser.save_screenshot('screenshot.png')

        #     # Reading the Screenshot
        #     img = cv2.imread("/Volumes/Work/Personal-Development/Karza/screenshot.png")
        #     logging.info("Cropping Screen Shot to extract Captcha")
        #     crop_img = img[390:500, 550:855]
        #     # Saving the cropped captcha
        #     logging.info("Saving the cropped Captcha Image")
        #     cv2.imwrite('Data/captcha_failed'+str(count)+'.png',crop_img)
        return 
        #     image = Image.open('captcha.png')
            
        #     # Solving the captcha
        #     logging.info("Decrypting the Captcha")
        #     captcha = tesserocr.image_to_text(image).strip().lower()  # print ocr text from image
            
        #     WebDriverWait(browser, delay)
        #     companyID = browser.find_element_by_id("companyID")
        #     userEnteredCaptcha = browser.find_element_by_id("userEnteredCaptcha")
        #     logging.info("Entering the values in the fields")
        #     # companyID.send_keys(cin)
        #     userEnteredCaptcha.send_keys(captcha)
        #     time.sleep(3)
        #     browser.find_element_by_id("companyLLPMasterData_0").click()
        #     try :
        #         browser.find_element_by_id("exportCompanyMasterData_0")
        #     except:
        #         logging.exception("Failed to solve the captcha for second time for CIN no %s, would close down the browser instance and restart from fresh browser",cin)
        #         return False
        # logging.info("Saving the Data via Export Excel File for CIN %s",cin)
        # browser.find_element_by_id("exportCompanyMasterData_0").click()
        # time.sleep(5)
        # return True



def main():
    # cinList = ['U51101RJ2005PTC020462','U85110KA1989PLC013224','U85110MH2000PLC128425']
    # for cin in cinList:
    #     success = False
    #     while not success:
    #         selenium = Sel()
    #         success = selenium.crawl(cin)
    #         time.sleep(10)
    count = 61
    while True:
        selenium = Sel()
        cin = 'U51101RJ2005PTC020462'
        selenium.crawl(cin,count)
        count += 1
        time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=loggingFileName , format='[%(levelname)s] (%(threadName)-10s) %(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Starting ... ")
    main()
    logging.info("Exting the code")

