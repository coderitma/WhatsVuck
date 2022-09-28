"""
WhatsVuck
=========
develop by Yanzen (yanwarsolah@gmail.com)
MIT License

This is an application that sends messages via whatsapp as an 
alternative to premium use published by some people with special services.
"""
from threading import Thread
import time
import _thread
import sys
import os
import io
import logging
from tqdm import tqdm
from art import tprint
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import qrcode
import config

# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
logging.basicConfig()

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
logging.root.setLevel(logging.INFO)

# The following line sets the root logger level as well.
# It's equivalent to both previous statements combined:
logging.basicConfig(level=logging.NOTSET)

log = logging.getLogger("WHATSVUCK-LOG")


from flask import Flask, request
app = Flask(__name__)

options = Options()
driver = None

tasks = []


def message_clear(message):
  data = message.replace("\n", config.WA_SHIFT_ENTER)
  print(data)
  return data


def whatsvuck_build():
  global driver
  log.info("whatsvuck build")
  options.add_argument(config.WA_HEADLESS)
  options.add_argument(config.WA_DISABLE_INFOBAR)
  options.add_argument(config.WA_ENABLE_COOKIE)
  options.add_argument(config.WA_USER_AGENT)
  driver = webdriver.Chrome(config.WA_DRIVER, chrome_options=options)
  driver.get(config.WA_ME_URL)

def whatsvuck_start(*args):
  whatsvuck_build()
  global deriver
  log.info("whatsvuck start")
  start = True
  # before start, we can check qr_data is available
  try:
    qr_data = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, config.WA_XPATH_QR))
    )
  except TimeoutException as e:
    driver.exit()
    sys.exit()
  
  while start:
    os.system("cls")
    log.info("whatsvuck waiting for login.")
    try:
      myqr = qrcode.QRCode()
      qr_data = WebDriverWait(driver, config.WA_DELAY_TIME)\
        .until(lambda driver: driver.find_element("xpath", config.WA_XPATH_QR))
      myqr.add_data(qr_data.get_attribute(config.WA_DATA_REF))
      f = io.StringIO()
      myqr.print_ascii(out=f)
      f.seek(0)
      print(f.read())
      time.sleep(config.WA_LOGIN_TIMING)
    except TimeoutException:
      log.info("whatsvuck time done.")
      start = False
    finally:
      log.info("Yeah, whatsvuck ready!")


def whatsvuck_send(phone, message):
  log.info("whatsvuck send")
  global driver
  text = message_clear(message)
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
  
def whatsvuck_sending():
  log.info("whatsvuck send")
  global driver
  global tasks
  while True:
    if tasks:
      try:
        log.info("whatsvuck send message")
        time.sleep(5)
        phone, message = tasks.pop()
        message = f"{message} {config.WA_SHIFT_ENTER*2}_powered by *whatsvuck*._"
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

        log.info('whatsvuck sending success')
      except TimeoutException as e:
        log.info('whatsvuck sending failed')

@app.route('/send', methods=['POST'])
def send():
  global tasks
  try:
    log.info(f"data send: {request.json}")
    priority = len(tasks) + 1
    tasks.append([request.json.get('phone'),request.json.get('message')])
    return jsonify({
      "status": "sending",
      "data": request.json,
      "priority": priority
    })
  except Exception as e:
    log.info("whatsvuck send error")
    return jsonify({"message": e})


if __name__ == "__main__":
  os.system("cls")
  tprint("WhatsVuck")
  print("1.0.0 Beta,\nDeveloped by Yanzen. Coderitma")
  print("")
  print("This is an application that sends messages"
  "via whatsapp as an alternative to" 
  "premium use published by some people with special services.")
  print("\n\n")
  thread = Thread(target=whatsvuck_start)
  thread.daemon = True
  thread.start()

  thread2 = Thread(target=whatsvuck_sending)
  thread2.daemon = True
  thread2.start()
  app.run()
