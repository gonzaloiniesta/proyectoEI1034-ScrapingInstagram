from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


class Scraping():
    def __init__(self, username: str, userPassword: str) -> None:
        
        self.driverPath = "C:/Users/gonin/chromedriver_win32/chromedriver.exe" #CAMBIAR POR LA DIRECCIÓN DONDE TENGAS EL CHROMEDRIVER
        self.username = username
        self.userPassword = userPassword
        self.driver = webdriver.Chrome(self.driverPath)
        
    def openChrome(self):
        try:
            self.driver = webdriver.Chrome(self.driverPath)
        except Exception as exc:
            print(f'Error al abrir en navegador Google Chrome: {str(exc)}')

    def login_instagram(self):
        try: 
            self.driver.get("https://www.instagram.com/")
            
            #Aceptar Cookies
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar todas')]"))).click()
            usernameBox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'username']")))
            passwordBox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'password']")))
            usernameBox.clear()
            passwordBox.clear()
            usernameBox.send_keys(self.username)
            passwordBox.send_keys(self.userPassword)
            time.sleep(1)

            #Login en Instagram
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            time.sleep(5)
            #Aceptar Cookies
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ahora no')]"))).click()
            time.sleep(3)
            #Aceptar Cookies
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ahora no')]"))).click()
        except Exception as exc:
            print(f'Error durante el login en Instagram: {str(exc)}')

    def get_information(self, user: str):
        searchbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Busca']")))
        searchbox.clear()
        searchbox.send_keys(user)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(2)
        searchbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div"))).click()
        time.sleep(2)
        
