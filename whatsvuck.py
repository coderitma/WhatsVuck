"""
WhatsVuck
=========
develop by Yanzen (yanwarsolah@gmail.com)
MIT License

This is an application that sends messages via whatsapp as an 
alternative to premium use published by some people with special services.
"""

import time
import _thread
import os
import io
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import qrcode
import config

from flask import Flask, request
app = Flask(__name__)

options = Options()
driver = None


def whatsvuck_build():
  global driver
  options.add_argument(config.WA_HEADLESS)
  options.add_argument(config.WA_DISABLE_INFOBAR)
  options.add_argument(config.WA_ENABLE_COOKIE)
  options.add_argument(config.WA_USER_AGENT)
  driver = webdriver.Chrome(config.WA_DRIVER, chrome_options=options)
  driver.get(config.WA_ME_URL)

def whatsvuck_start(*args):
  whatsvuck_build()
  global deriver
  start = True
  time.sleep(5)
  while start:
    os.system("cls")
    try:
      myqr = qrcode.QRCode()
      print("waiting moment!")
      qr_data = WebDriverWait(driver, config.WA_DELAY_TIME)\
        .until(lambda driver: driver.find_element("xpath", config.WA_XPATH_QR))
      myqr.add_data(qr_data.get_attribute(config.WA_DATA_REF))
      print("get xpath done!")
      f = io.StringIO()
      myqr.print_ascii(out=f)
      f.seek(0)
      print(f.read())
      time.sleep(config.WA_LOGIN_TIMING)
    except TimeoutException:
      start = False


def whatsvuck_send(phone, message):
  time.sleep(3)
  global driver
  text = message
  input_box_search = WebDriverWait(driver, config.WA_DELAY_TIME)\
    .until(lambda driver: driver.find_element("xpath", config.WA_SEARCH_BOX))
  input_box_search.click()
  input_box_search.send_keys(phone)

  selected_contact = WebDriverWait(driver, config.WA_DELAY_TIME)\
    .until(lambda driver: driver.find_element('xpath', config.WA_CONTACT_LIST.format(phone=phone)))
  print(selected_contact.text)
  selected_contact.click()

  input_box = WebDriverWait(driver, config.WA_DELAY_TIME)\
    .until(lambda driver: driver.find_element('xpath', config.WA_INPUT_BOX))
  input_box.send_keys(message + Keys.ENTER)
  
def whatsvuck_sending(phone, message):
  driver.get(f"https://api.whatsapp.com/send?phone={phone}")
  download = WebDriverWait(driver, config.WA_DELAY_TIME)\
        .until(lambda driver: driver.find_element("xpath", '//*[@id="action-button"]'))
  # download.click()
  driver.execute_script("arguments[0].click();", download)

  download = WebDriverWait(driver, config.WA_DELAY_TIME)\
        .until(lambda driver: driver.find_element("xpath", "//span[contains(text(), 'use WhatsApp Web')]"))
  # download.click()
  driver.execute_script("arguments[0].click();", download)
  
  time.sleep(5)
  input_box = WebDriverWait(driver, config.WA_DELAY_TIME)\
    .until(lambda driver: driver.find_element('xpath', config.WA_INPUT_BOX))
  input_box.send_keys(message + Keys.ENTER)

@app.route('/send', methods=['POST'])
def send():
  try:
    phone = request.json.get('phone')
    message = request.json.get('message')
    message = f"{message} {config.WA_SHIFT_ENTER*2}_powered by *whatsvuck*._"
    _thread.start_new_thread(whatsvuck_sending, (phone, message,))
    return jsonify({
      "status": "sending",
      "data": request.json
    })
  except Exception as e:
    return jsonify({"message": e})


if __name__ == "__main__":
  _thread.start_new_thread(whatsvuck_start, (None,))
  app.run()
