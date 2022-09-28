from selenium.webdriver.common.keys import Keys

WA_ME_URL = "https://web.whatsapp.com"
WA_SEND_URL = "https://web.whatsapp.com/send/?phone={phone}&text={message}"
WA_USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
WA_HEADLESS = "headless"
WA_DRIVER = r"C:\webdrivers\chromedriver106.exe"
WA_XPATH_ACTION ="//a[@id='action-button']"
WA_XPATH_SENDER = "//h4/a[@href='{url}']"
WA_XPATH_QR = '//div[@data-testid="qrcode"]'
WA_DATA_REF = "data-ref"
WA_LOGIN_TIMING = 7
WA_INPUT_CONVERSATION = "//div[@data-testid='conversation-compose-box-input']"

WA_SEARCH_BOX = "//div[@data-testid='chat-list-search']"
WA_CONTACT_LIST = "//span[contains(@title,'{phone}')]"
WA_INPUT_BOX = "//div[@data-testid='conversation-compose-box-input']"
WA_DELAY_TIME = 30
WA_DISABLE_INFOBAR = "--disable-infobars"
WA_ENABLE_COOKIE = "--enable-file-cookies"
WA_SHIFT_ENTER = (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT)