from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry
import time
import os

filepath = "C:/Temp/credentials.txt"

def save_credentials(email, password):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            file.write("")
    
    with open(filepath, "w") as file:
        file.write(f"{email}\n")
        file.write(f"{password}")

def load_credentials():
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()
            email = lines[0].strip()
            password = lines[1].strip()
            return email, password
    else:
        return "", ""

def gb_aanvraag(amount, email, password):
    counter = 0

    driver = webdriver.Firefox()
    driver.get("https://mijn.kpn.com/classic/#/abonnement")

    wait = WebDriverWait(driver, 10)

    reject_cookies = wait.until(EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler")))
    reject_cookies.click()
    login_email = wait.until(EC.presence_of_element_located((By.ID, "email")))
    login_email.send_keys(email)
    login_password = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_password.send_keys(password)
    time.sleep(2)
    log_in = wait.until(EC.element_to_be_clickable((By.NAME, "inloggen")))
    log_in.click()
    time.sleep(12)
    producten = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ProductenTab")))
    producten.click()
    mobiel = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Mobiel']")))
    mobiel.click()
    mb_kopen = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Extra MB\'s en bundels bijkopen"]')))
    mb_kopen.click()
    extra_mb = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Extra MB\'s/min/sms"]')))
    extra_mb.click()

    while counter < amount:
        optie_2gb = wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="2 GB extra dagbundel"]')))
        optie_2gb.click()
        print("optie 2gb")
        time.sleep(1)
        ik_ga_akkoord = wait.until(EC.presence_of_element_located((By.ID, 'agree')))    
        driver.execute_script("arguments[0].click();", ik_ga_akkoord)
        print("ik ga akkoord")
        time.sleep(1)
        zet_extra_optie_aan = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Zet extra optie aan"]')))
        zet_extra_optie_aan.click()
        print("zet extra optie aan")
        counter += 1
        print(f"{counter}/{amount}")
        try:
            extra_mb = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Extra MB\'s/min/sms"]')))
            extra_mb.click()
            time.sleep(1)
            print("extra mb try 1")
        except:
            try:
                terug = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "link_back")))
                terug.click()
                amount += 1
                print("terug try 2")
                time.sleep(1)
                continue
            except:
                producten = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ProductenTab")))
                producten.click()
                print("producten except 2")
                mobiel = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Mobiel']")))
                mobiel.click()
                print("mobiel except 2")
                mb_kopen = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Extra MB\'s en bundels bijkopen"]')))
                mb_kopen.click()
                print("mb kopen except 2")
                extra_mb = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Extra MB\'s/min/sms"]')))
                extra_mb.click()
                print("extra mb except 2")
                continue

    driver.quit()

def app():
    root = CTk()
    root.title("KPN GB aanvrager")
    root.geometry("400x350")

    email_label = CTkLabel(root, text="Email")
    email_label.pack(pady=2)
    email_entry = CTkEntry(root, width=200)
    email_entry.pack(pady=2)

    password_label = CTkLabel(root, text="Wachtwoord")
    password_label.pack(pady=2)
    password_entry = CTkEntry(root, width=200)
    password_entry.pack(pady=2)

    amount_label = CTkLabel(root, text="Hoevaak wil je 2GB aanvragen?")
    amount_label.pack(pady=6)
    amount_entry = CTkEntry(root, width=200)
    amount_entry.pack(pady=6)

    email, password = load_credentials()
    email_entry.insert(0, email)
    password_entry.insert(0, password)

    def set_amount():
        if int(amount_entry.get()) >= 0:
            amount = int(amount_entry.get())
            print(amount)
            save_credentials(email_entry.get(), password_entry.get())
            gb_aanvraag(amount, email, password)
        else:
            pass

    submit_button = CTkButton(root, text="Submit", command=set_amount)
    submit_button.pack(pady=45)

    root.mainloop()

if __name__ == "__main__":
    app()