import customtkinter
import os
from PIL import Image
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.captcha import CaptchaWindow
from colorama import init, Fore
import logging

logging.getLogger("uc").setLevel(logging.CRITICAL)
root = customtkinter.CTk()
root.withdraw()
init()

def logo():
    print("")
    print(Fore.CYAN + " ███████████ ██║ ███ " + Fore.RESET + Fore.MAGENTA + "███████╗██████╗ ██████╗██╗          " + Fore.RESET)
    print(Fore.CYAN + " ╚══██╔══ ██ ██║ ██╔ " + Fore.RESET + Fore.MAGENTA + "╚══██╔══██╔═══████╔═══████║         " + Fore.RESET)
    print(Fore.CYAN + "    ██║   ██ █████╔╝ " + Fore.RESET + Fore.MAGENTA + "   ██║  ██║   ████║   ████║         " + Fore.RESET)
    print(Fore.CYAN + "    ██║   ██ ██╔═██╗ " + Fore.RESET + Fore.MAGENTA + "   ██║  ██║   ████║   ████║         " + Fore.RESET)
    print(Fore.CYAN + "    ██║   ██ ██║  ██╗" + Fore.RESET + Fore.MAGENTA + "   ██║  ╚██████╔╚██████╔███████╗    " + Fore.RESET)
    print(Fore.CYAN + "    ╚═╝   ╚═ ╚═╝  ╚═╝" + Fore.RESET + Fore.MAGENTA + "   ╚═╝   ╚═════╝ ╚═════╝╚══════╝    " + Fore.RESET)
    print()
    print()
    print()

def openTiktokSites():
    os.system('cls')
    global zefoy_driver
    global nreer_driver
    logo()
    print("""    COMPLETE THE 2 CAPTCHAS THAT APPEAR ON YOUR SCREEN.
    IF YOU GET THE SECOND WRONG, RESTART THE PROGRAM.""")
    zefoy_options = uc.ChromeOptions()
    nreer_options = uc.ChromeOptions()
    zefoy_options.add_argument("--headless")
    nreer_options.add_argument("--headless")
    zefoy_options.add_argument("--disable-notifications")
    nreer_options.add_argument("--disable-notifications")
    zefoy_driver = uc.Chrome(options=zefoy_options)
    nreer_driver = uc.Chrome(options=nreer_options)    
    try:
        zefoy_driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["https://fundingchoicesmessages.google.com/*"]})
        zefoy_driver.execute_cdp_cmd("Network.enable", {})
        nreer_driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["https://fundingchoicesmessages.google.com/*"]})
        nreer_driver.execute_cdp_cmd("Network.enable", {})
    except Exception as cdp_err:
        print(f"    Warning: Could not set CDP network blocking: {cdp_err}")

    zefoy_driver.get("https://zefoy.com/")
    nreer_driver.get("https://nreer.com/")
    try:
        if zefoyCaptcha():
            print("    Zefoy Captcha Successful.")
            time.sleep(1)
    except:
        print("    Error communication with Zefoy")
        zefoy_driver.quit()
    try:
        if nreerCaptcha():
            print("    Nreer Captcha Successful.")
            use = nreer_driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block')

            use.click()
            time.sleep(1)
    except:
        print("    Error communication with Nreer")
        nreer_driver.quit()
    chooseTiktok()
    
    
    
    

def nreerCaptcha():
    global nreer_driver
    inputBox = nreer_driver.find_element(By.XPATH, '//*[@id="cat"]/input')
    solutionNreer = captchaSaveNreer(is_retry=False)
    if solutionNreer is None:
        print("    Captcha solving cancelled or failed.")
        return False
    inputBox.send_keys(solutionNreer)
    time.sleep(1)
    submit = nreer_driver.find_element(By.XPATH, "//button[contains(@class, 'btn-dark') and contains(@class, 'btn-block')]").click()



def zefoyCaptcha():
    """Original captcha function structure."""
    global zefoy_driver
    is_retry = False
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        attempts+=1
        try:

            time.sleep(1) 
            input_field = zefoy_driver.find_element(By.ID, "captchatoken") 
            input_field.clear()
            solution = captchaSaveZefoy(is_retry)
            if solution is None: 
                print("    Zefoy solving cancelled or failed.")
                return False

            input_field.send_keys(solution)
            time.sleep(1)

            submit_button = zefoy_driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-lg.btn-block.rounded-0.submit-captcha[type="submit"]')
            submit_button.click()
            time.sleep(3) 


            try:
                error_popup_close_button = zefoy_driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[3]/button") 
                error_popup_close_button.click()
                time.sleep(1)
                is_retry = True
                print("    Captcha incorrect, retrying...")
                time.sleep(2)
                continue 
            except:
                try:
                    zefoy_driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]') 
                    print("    Captcha likely successful.")
                    return True 
                except:
                    print("    Captcha state uncertain, assuming retry needed...")
                    is_retry = True
                    time.sleep(2)
                    continue 
        except Exception as e:
             print(f"    Error during captcha attempt {attempts}: {e}")

             time.sleep(5)
             is_retry = True 
             continue 
    print("    Failed to solve captcha after multiple attempts.")
    return False 


def captchaSaveZefoy(is_retry=False):
    """Original captchaSave function structure."""
    global zefoy_driver
    time.sleep(1)
    possible_div_numbers = [4, 5, 6] 
    for div_num in possible_div_numbers:
        xpath = f'/html/body/div[{div_num}]/div[2]/form/div/div/img' 
        try:
            l = zefoy_driver.find_element(By.XPATH, xpath)
            captcha_file = 'captcha.png'
            with open(captcha_file, 'wb') as file:
                file.write(l.screenshot_as_png)
            captcha_window = CaptchaWindow(is_retry) 
            return captcha_window.result
        except Exception as e: 
            continue 

    print("    Could not find captcha image after trying multiple XPaths.")
    return None 

def captchaSaveNreer(is_retry=False):
    global nreer_driver
    time.sleep(1)
    xpath = '//*[@id="msg"]/div[2]/img'
    try:
        l = nreer_driver.find_element(By.XPATH, xpath)
        captcha_file = 'captcha.png'
        with open(captcha_file, 'wb') as file:
            file.write(l.screenshot_as_png)
        captcha_window = CaptchaWindow(is_retry) 
        return captcha_window.result
    except Exception as e:
        print(f"    Error capturing CAPTCHA: {e}")
        return None


def chooseSocial():
    os.system('cls')
    logo()
    print("""    Please choose an option.  [e.g 1]""")
    print()
    print("    1. TIKTOK  " + Fore.GREEN + "[WORKING]" + Fore.RESET)
    print("    2. INSTAGRAM  " + Fore.YELLOW + "[RELEASING AT 150 STARS]" + Fore.RESET)
    print()
    try:
        choice = int(input("    CHOICE: "))
    except:
        chooseSocial()
    if (choice == 1):
          openTiktokSites()
    elif (choice == 2):
        chooseSocial()
    else:
        chooseSocial()

def chooseTiktok():
    global zefoy_driver, zefoy_input, URL
    os.system('cls')

    viewsTabZefoy = zefoy_driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-views-button']")
    likesTabZefoy = zefoy_driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-hearts-button']")
    sharesTabZefoy = zefoy_driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-shares-button']")
    favouriteTabZefoy = zefoy_driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-favorites-button']")

    logo()

    print("""    Please choose an option.  [e.g 1]""")
    print()
    if viewsTabZefoy.is_enabled():
        print("    1. Views  " + Fore.GREEN + "[WORKING]" + Fore.RESET)
    else:
         print("    1. Views  " + Fore.RED + "[DOWN]" + Fore.RESET)
    if likesTabZefoy.is_enabled():
        print("    2. Likes  " + Fore.GREEN + "[WORKING]" + Fore.RESET)
    else:
         print("    2. Likes  " + Fore.RED + "[DOWN]" + Fore.RESET)
    if sharesTabZefoy.is_enabled():
        print("    3. Shares  " + Fore.GREEN + "[WORKING]" + Fore.RESET)
    else:
         print("    3. Shares  " + Fore.RED + "[DOWN]" + Fore.RESET)
    if favouriteTabZefoy.is_enabled():
        print("    4. Favourites  " + Fore.GREEN + "[WORKING]" + Fore.RESET)
    else:
         print("    4. Favourites  " + Fore.RED + "[DOWN]" + Fore.RESET)
    print()

    try:
        choice = int(input("    CHOICE: "))
    except:
        chooseTiktok()

    if (choice == 1):
        if viewsTabZefoy.is_enabled():
            viewsTabZefoy.click()
            zefoy_input = zefoy_driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
            URL = input("    Enter your video URL: ")
            viewBot()
        else:
            chooseTiktok()
    elif (choice == 2):
        if likesTabZefoy.is_enabled():
            likesTabZefoy.click()
            zefoy_input = zefoy_driver.find_element(By.XPATH, '/html/body/div[8]/div/form/div/input')
            URL = input("    Enter your video URL: ")
            likeBot()
        else:
            chooseTiktok()
    elif (choice == 3):
        if sharesTabZefoy.is_enabled():
            sharesTabZefoy.click()
            zefoy_input = zefoy_driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/input')
            URL = input("    Enter your video URL: ")
            shareBot()
        else:
            chooseTiktok()
    elif (choice == 4):
        if favouriteTabZefoy.is_enabled():
            favouriteTabZefoy.click()
            zefoy_input = zefoy_driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/input')
            URL = input("    Enter your video URL: ")
            favouriteBot()
        else:
            chooseTiktok()
    elif (choice == 5):
        chooseTiktok()
    else:
        chooseTiktok()




def viewBot():
    global URL
    viewStats = 0
    zefoy_input.send_keys(URL)
    while True:
        os.system('cls')
        logo()
        print(Fore.CYAN + f"    {viewStats}" + Fore.RESET + Fore.MAGENTA +" views sent in total." + Fore.RESET)
        print("    Press CTRL+C to stop.")
        try:
            search_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button').click()
            time.sleep(1)
            try:
                target_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button')
                target_button.click()
                viewStats += 500
            except:
                time.sleep(3)
        except:
            time.sleep(1)
        try:
            use_button = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div[1]/div[3]/div/div/button').click()
            time.sleep(3)
            enterURL = enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
            enterURL.send_keys(URL)
            time.sleep(1)
            search = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button').click()
            time.sleep(2)
            viewButton = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div/div[1]/button[4]').click()
            time.sleep(5)
            close = nreer_driver.find_element(By.XPATH, '/*[@id="bootstrap-show-modal-0"]/div/div/div[1]/button').click()
            viewStats += 500
        except:
            time.sleep(1)

                    
    

    
def likeBot():
    global URL
    likeStats = 0
    zefoy_input.send_keys(URL)
    while True:
        os.system('cls')
        logo()
        print(f"    {likeStats} likes sent in total.")
        print("    Press CTRL+C to stop.")
        try:
            search_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[8]/div/form/div/div/button').click()
            time.sleep(1)
            try:
                target_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[1]/div/form/button')
                target_button.click()
                likeStats += 10
            except:
                time.sleep(3)
        except:
            time.sleep(3)
            
        try:
            use_button = nreer_driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block').click()
            time.sleep(3)
            enterURL = enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
            enterURL.send_keys(URL)
            time.sleep(1)
            search = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button').click()
            time.sleep(2)
            likeButton = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div/div[1]/button[3]').click()
            if likeButton:
                likeStats += 25
            close = nreer_driver.find_element(By.XPATH, '/*[@id="bootstrap-show-modal-0"]/div/div/div[1]/button').click()
        except:
            time.sleep(1)

    
def shareBot():
    global URL
    shareStats = 0
    zefoy_input.send_keys(URL)
    while True:
        os.system('cls')
        logo()
        print(f"    {shareStats} likes sent in total.")
        print("    Press CTRL+C to stop.")
        try:
            search_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/div/button').click()
            time.sleep(1)
            try:
                target_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/div/form/button')
                target_button.click()
                shareStats += 200
            except:
                time.sleep(3)
        except:
            time.sleep(3)
        try:
            use_button = nreer_driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block').click()
            time.sleep(3)
            enterURL = enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
            enterURL.send_keys(URL)
            time.sleep(1)
            search = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button').click()
            time.sleep(2)
            shareButton = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div/div[1]/button[6]').click()
            close = nreer_driver.find_element(By.XPATH, '/*[@id="bootstrap-show-modal-0"]/div/div/div[1]/button').click()
            shareStats += 200
        except:
            time.sleep(1)
    

def favouriteBot():
    global URL
    favStats = 0
    zefoy_input.send_keys(URL)
    while True:
        os.system('cls')
        logo()
        print(f"    {favStats} favourites sent in total.")
        print("    Press CTRL+C to stop.")
        try:
            search_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/div/button').click()
            time.sleep(1)
            try:
                target_button = zefoy_driver.find_element(By.XPATH, '/html/body/div[12]/div/div/div[1]/div/form/button')
                target_button.click()
                favouriteStats += 90
            except:
                time.sleep(3)
        except:
            time.sleep(3)
        try:
            use_button = nreer_driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block').click()
            time.sleep(3)
            enterURL = enterURL = nreer_driver.find_element(By.CSS_SELECTOR, '.form-control.form-control-lg')
            enterURL.send_keys(URL)
            time.sleep(1)
            search = nreer_driver.find_element(By.XPATH, '//*[@id="form1"]/div/div/button').click()
            time.sleep(2)
            shareButton = nreer_driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div/div/div[1]/button[6]').click()
            close = nreer_driver.find_element(By.XPATH, '/*[@id="bootstrap-show-modal-0"]/div/div/div[1]/button').click()
            favouriteStats += 100
        except:
                time.sleep(1)

    

def commentBot():
    os.system('cls')


os.system('cls')
os.system("title TikTool")
time.sleep(3)
chooseSocial()
