from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import re
import warnings
warnings.filterwarnings('ignore')

def get_member(id_groups, email, password):
    # how to hide pop up chrome
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--log-level=3')

    # open facebook link with selenium
    browser = webdriver.Chrome(executable_path ="lookup/chromedriver", chrome_options=chrome_options)
    browser.get("https://www.facebook.com/")
    sleep(1)

    # how login to facebook
    username_box = browser.find_element_by_id('email')
    username_box.send_keys(email)
    print("Email Id entered")
    sleep(1)

    password_box = browser.find_element_by_id('pass')
    password_box.send_keys(password)
    print("Password entered")

    login_box = browser.find_element_by_id('loginbutton')
    login_box.click()

    browser.get("https://www.facebook.com/groups/{}/members".format(id_groups))
    sleep(5)

    # how to scroll facebook page
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        sleep(3)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # how to get username, id member from page facebook
    data_akun = []
    data = browser.find_elements_by_class_name('_21m-')
    for datas in data:
        firstGet = datas.find_element_by_class_name('_4ks')
        for akun in firstGet.find_elements_by_class_name('_gse'):
            tes = akun.find_element_by_class_name('_ohe')
            ids = tes.get_attribute('data-hovercard')
            ids = re.findall(r"id=\w+", ids)
            data_akun.append({'username': re.findall(r"com[\/\.\w]+", tes.get_attribute('href'))[0].replace("com/", ""),
                              "id": ids[0].replace('id=', ''),
                              "fullname": tes.get_attribute('title'),
                              "class": datas.get_attribute('id').replace('groupsMemberSection_', '')})

        for nexts in datas.find_elements_by_class_name('expandedList'):
            cek = nexts.find_element_by_class_name('_4ks')
            for akun in cek.find_elements_by_class_name('_gse'):
                tes = akun.find_element_by_class_name('_ohe')
                ids = tes.get_attribute('data-hovercard')
                ids = re.findall(r"id=\w+", ids)
                data_akun.append({'username': re.findall(r"com[\/\.\w]+", tes.get_attribute('href'))[0].replace("com/", ""),
                                  "id": ids[0].replace('id=', ''),
                                  "fullname": tes.get_attribute('title'),
                                  "class": datas.get_attribute('id').replace('groupsMemberSection_', '')})

    # how to dump member group
    with open("{}_member_group.json", "w") as f:
        for i in data_akun:
            f.write(json.dumps(i),"+\n")
    f.close()

if __name__ == '__main__':
    get_member(id_groups=None, email=None, password=None)