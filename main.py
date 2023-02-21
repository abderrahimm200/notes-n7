import time, random, traceback, os, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import telepot
from pathlib import Path

"""
from server import alive
# keep the script running
alive()
"""

# user's info
user = os.environ['user']
password = os.environ['password']
token = os.environ['token']  # telegram token
receiver_id = os.environ['receiver_id']

bot = telepot.Bot(token)


# create resultats.txt file
open('resultats.txt','w+') 


def wait_id(id_, driver):
    return WebDriverWait(driver,
                         20).until(EC.presence_of_element_located(
                             (By.ID, id_)))


# run chrome in background
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


def refresh(i):
    driver.get('https://mdw.inp-toulouse.fr/mdw3/#!notesView')
    try:
        wait_id('username', driver).send_keys(user)
        wait_id('password', driver).send_keys(password + Keys.ENTER)
        time.sleep(1)
        driver.back()
    except:
        pass
    time.sleep(3)
    try:
        driver.execute_script(
            "document.getElementsByClassName('v-button-wrap')[1].click()")
    except:
        pass
    time.sleep(1)
    driver.execute_script(
        "document.getElementsByClassName('v-button-wrap')[4].click()")
    table = driver.find_elements(By.CLASS_NAME,'v-table-table')[2]
    for _ in range(i % 10):
        rows = table.find_elements(By.TAG_NAME,'tr')
        ActionChains(driver).move_to_element(rows[-1]).perform()
        time.sleep(1)
    time.sleep(3)
    table = driver.find_elements(By.CLASS_NAME,'v-table-table')[2]
    rows = table.find_elements(By.TAG_NAME,'tr')

    message = ''
    resultats = open("resultats.txt").read().split("\n")
    write = False
    s_notes = {"Session1": {}, "Session2": {}}
    for row in rows:
        code = row.find_elements(By.CLASS_NAME,
            'v-table-cell-content')[0].text + "\t"
        module = row.find_elements(By.CLASS_NAME,
            'v-table-cell-content')[1].text.strip()
        note = row.find_elements(By.CLASS_NAME,'v-table-cell-content')[2].text
        if note:
            s_notes["Session1"][code + module] = note
        note2 = row.find_elements(By.CLASS_NAME,'v-table-cell-content')[4].text
        if note2:
            s_notes["Session2"][code + module] = note2

    for session in s_notes:
        for c_module in s_notes[session]:
            note = s_notes[session][c_module]
            s_c_m = session + "\t" + c_module
            if s_c_m in resultats:
                i = resultats.index(s_c_m)
                if resultats[i + 1] != note:
                    resultats[i + 1] = note
                    message += session + "\n" + c_module.split(
                        "\t")[-1] + "\n" + note + "\n\n"
                    write = True
            else:
                resultats.append(s_c_m + "\n" + note)
                message += session + "\n" + c_module.split(
                    "\t")[-1] + "\n" + note + "\n\n"
                write = True

    if write:
        #bot.sendMessage(receiver_id, message)
        print(message)
        with open("resultats.txt", "w") as f:
            f.write("\n".join(resultats))

    return message


print("Starting .. ")
i = 0
while True:
    print(f"refresh n {i}")
    i += 1
    try:
        message = refresh(i)
        time.sleep(random.randint(10, 40))
    except Exception:
        print(traceback.format_exc())
