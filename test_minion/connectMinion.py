import salt.client


from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement as webelement


#from webdriver_manager.chrome import ChromeDriverManager

#If successfully logged in, expect new user profile dir, if not.. just log in and go to meeting url 
def login_headless(email,password):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximizes')
    driver = webdriver.Chrome(options=options) #driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    #driver.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    #driver.get('https://accounts.google.com/signin')
    driver.get('https://us04web.zoom.us/signin')

    #TODO: if already logged in 

    account = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "email")))
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='identifierId']")))
    account.send_keys(email)
    #driver.find_element_by_id("next").click() #identifierNext
    passwrd = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))
    passwrd.send_keys(password)
    # print("element name : ", driver.find_elements_by_class_name('signin'), "\n-----")
    # print("\nelement from button path : ", driver.find_elements(By.XPATH, '//button'))
    # element = driver.find_elements_by_class_name('signin')[0]['element']
    # print("extracted : ", element)
    #driver.find_element_by_id("SignIn").click()
    
    print("--- ", driver.find_elements_by_class_name("signin"))
    print("@@@ ", driver.find_elements_by_xpath("//div[contains(@class, 'signin')]"))
    # obj = driver.find_elements_by_xpath("//div[contains(@class, 'signin')]")
    # obj[0].click()
    # print("** ", obj[0].text)

    # for i in obj:
    #     print("\n  -  ", i.text)

    #driver.find_element_by_xpath('//button[contains(text(), "Sign In")]').click() #-> throws http 401 error
    #driver.find_element_by_xpath("//div[@class='signin']/button[@class='btn btn-primary signin user']").click() #-> throws http 401 error
    #driver.find_element_by_xpath("//div[@class='btn btn-primary signin user']").click() #-> throws http 401 error
    #driver.find_element_by_xpath("//div[@class='signin']/button[.='Sign In']").click() #-> throws http 401 error
    #driver.find_element_by_xpath("//div[@class='signin']/button").click() #-> throws http 401 error
    
    #driver.find_element_by_xpath("//div[@class='signin']/button[@type='submit']").click()
    
    WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//div[@class='signin']")))
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(By.XPATH, "//button[@class='btn btn-primary signin user']")).click()

    ### trying with action chains ####

    #element = driver.find_element_by_xpath("//*[text()='Sign In']") #-> throws http 401 error
    #element = driver.find_element_by_xpath('//button[@class="btn btn-primary signin user"]/parent::div[@class="signin"]')  #-> throws http 401 error
    
    # action = ActionChains(driver)
    # print("!!! ", element)
    # action.click(on_element=element).perform()

    ### action chain attemps end here ####

    #driver.find_elements_by_xpath("//div[contains(@class, 'signin')]").click()
    #print("%% ", driver.find_element(By.XPATH('//div[@class="signin"]')))
    # q4 = driver.find_element_by_xpath('//button[@class="btn btn-primary signin user"]/parent::div[@class="signin"]')
    # driver.move_to_element(q4[0]).click()
    # for i in q4:
    #     print("\nq4: ", i.text)
    # print("\nfirst elem: ", q4[0].text)

    # time.sleep(2)

    # driver.get_screenshot_as_file("login.png")
    # print(dir(driver))

    #If need to verify
    if (len(driver.find_elements(By.XPATH, '//button')) != 5):
        #driver.get_screenshot_as_file("login.png")
        print("Successfully logged in!..1")
        driver.close()
    else: 
        print("Need verification...")
        verifyByTxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button')))
        verifyByTxt.click()

        #Ask user for 
        veriCode = input("Enter the 6-digit verification code from Google: ")
        actions = ActionChains(driver)
        actions.send_keys(veriCode)
        actions.perform()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit"))).click()

        #TODO: if wrong verification code 
        print("Successfully logged in!..2")
        driver.close()

    driver.quit()


def connect():
    print("Id: ", minion_id)
    local = salt.client.LocalClient()
    status = local.cmd(minion_id, 'test.ping')
    print("Ping status : ", status)

def runCommand():
    local = salt.client.LocalClient()
    output = local.cmd(minion_id, 'cmd.run', ["uname -a"])
    print("Command results: ", output)

def main():
    #init()
    connect()
    runCommand()
    login_headless(email,password)

if __name__ == '__main__':
    minion_id = "raspi-e4:5f:01:56:d8:cd"
    local = None
    email = "vinothinisekar.g@gmail.com" #"ucsbsnl2@gmail.com"
    password = "zoomData@123" #"ABCdef123!!!"
    main()
