import time
import os
from pandas.core.tools.datetimes import to_datetime
import pip
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import re
from product.models import *

# ignore future warnings
warnings.filterwarnings("ignore")


# call for pip command
def install(package):
    pip.main(['install', package])


# pandas, bs4, selenium, webdriver-manager, ftfy packages
def requirements_check(package):
    try:
        __import__("pandas")
        __import__("bs4")
        __import__("selenium")
        __import__("webdriver_manager")
        __import__("ftfy")
        __import__("numpy")
    except:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pandas"])
        __import__("pandas")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
        __import__("bs4")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "selenium"])
        __import__("selenium")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "webdriver-manager"])
        __import__("webdriver_manager")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "ftfy"])
        __import__("ftfy")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "numpy"])


requirements_check("pandas")
requirements_check("bs4")
requirements_check("selenium")
requirements_check("webdriver_manager")
requirements_check("ftfy")
requirements_check("numpy")

# Import packages
import pandas as pd
from selenium import webdriver
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ftfy import fix_encoding
import numpy as np
from webdriver_manager.utils import ChromeType

from urllib.parse import urlparse
import urllib.request as urllib2
from django.core.files import File
from django.core.files.base import ContentFile
import io
from selenium.webdriver.common.keys import Keys
from django.template.defaultfilters import slugify



from django.contrib.auth.models import User

def data_scrap():
    # Empty lists for storing information
    list_of_product= []
    list_of_price = []
    list_of_image= []
    list_of_category = []
    list_of_service = []
    # Driver
    global driver

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options,)
    page = 1
    while(page<=8):
        driver.get(str("https://seller5theway.com/shop/page/"+str(page)+"/"))
        time.sleep(5)
 
        # Get author name, article name, year, total citation
        htmlSource = driver.page_source
        only_class = SoupStrainer("div", {"class": "products row row-small large-columns-5 medium-columns-3 small-columns-3"})
        list_product = BeautifulSoup(htmlSource, "html.parser", parse_only=only_class)
        print(list_product)
        for item in list_product.findAll("div", {"class": "product-small"}):
            name = str(item.find("a", attrs={"class": "woocommerce-LoopProduct-link woocommerce-loop-product__link"}).text)
            list_of_product.append(name)
            service = str(item.find("p", attrs={"class": "category uppercase is-smaller no-text-overflow product-cat op-7"}).text)
            list_of_service.append(service)
            price = int(re.sub("[^0-9]", "", str(item.find("span",attrs={"class" :"woocommerce-Price-amount"}).text)))
            list_of_price.append(price)
            image = item.find("div", attrs={"class": "image-fade_in_back"})
            currentImg = str(image.find("img").get("src"))
            imageStr = str(image.find("img").get("src")).replace("-300x300.", "-600x600.")
            list_of_image.append(imageStr)
            listCategory = re.sub("\s+"," ",name).split(" ")
            category = listCategory[-3]
            category = re.sub("[^A-Z]","",category)
            print(name +" " + str(price) +" " + service + " "+ imageStr+" "+ category)
            try:
                hasCategory = Category.objects.get(name=category)
            except:
                hasCategory = Category.objects.create(name=category)
            try:
                hasService = Service.objects.get(name=service)
            except:
                hasService = Service.objects.create(name=service)
            product = Product.objects.create(category = hasCategory, service=hasService, title = name, price = price)
            try:
                img_url = imageStr
                name_image = urlparse(img_url).path.split('/')[-1]
                content = io.BytesIO(urllib2.urlopen(img_url).read())
            except:
                img_url = currentImg
                name_image = urlparse(img_url).path.split('/')[-1]
                content = io.BytesIO(urllib2.urlopen(img_url).read())
            product.image.save(name_image, content, save=True)
            time.sleep(0.5)
        time.sleep(1)
        page=page+1
    driver.close()
   
   

