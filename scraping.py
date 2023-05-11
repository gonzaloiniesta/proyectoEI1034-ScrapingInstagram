from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

import time
import os
import urllib
import requests


class Operations:
    def __init__(self) -> None:
        self.path= ''
    
    def createDitectory(self, directoryName: str):
        self.path = os.getcwd()
        self.path = os.path.join(self.path, directoryName)
        os.mkdir(self.path)

    def download_image(url, NUM_IMG, path):
        resource = urllib.request.urlopen(url)
        n = str(5)
        d = os.path.join(path,"Imagenes")
        filename = d + n + ".jpg"
        output = open(filename,"wb")
        output.write(resource.read())
        output.close()


class Scraping():
    def __init__(self, username: str, userPassword: str) -> None:
        
        self.driverPath = "C:/Users/gonin/chromedriver_win32/chromedriver.exe" #CAMBIAR POR LA DIRECCIÓN DONDE TENGAS EL CHROMEDRIVER
        self.username = username
        self.userPassword = userPassword
        self.driver = self.openChrome()
        self.operations = Operations()
        
    def openChrome(self):
        try:
            return webdriver.Chrome(self.driverPath)
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

    def search(self, user: str):
        searchbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Busca']")))
        searchbox.clear()
        searchbox.send_keys(user)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(2)
        searchbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div"))).click()
        time.sleep(2)

    def get_information(self):
        soup = BeautifulSoup(self.driver, 'html.parser')
        data = soup.find_all('span', {"class":"g47SY"})
        res = ''

        publications = str(data[0])
        followers = str(data[1])
        following = str(data[2])

        n = int(publications.find('>'))
        p = int(publications.rfind('<'))
        numeroPublicaciones = int(publications[n+1:p])
        res = f'{res}Publications: {publications[n+1:p]} \n'


        n = int(followers.find('>'))
        p = int(followers.rfind('<'))
        res = f'{res}Seguidores: {followers[n+1:p]} \n'

        n = int(following.find('>'))
        p = int(following.rfind('<'))
        res = f'{res}Seguidos: {following[n+1:p]} \n'

        return res
        
    def get_images(self):

        image_link = []

        for h in range(0, 3):
            ws = "window.scroll(" + str(i) + "," + str(j) + ");"
            self.driver.execute_script(ws)
            soup = BeautifulSoup(self.driver, "html.parser")
            for a in soup.find_all('a', href=True):
                if a['href'].startswith('/p'):
                    #En esta direccion hay que poner el nombre del perfil con el que has accedido a instagram.
                    image_link.append("https://www.instagram.com/NOMBRE_PERFIL"+a['href'])
                    #print("Found the URL:", "https://www.instagram.com/gonzalo_iniesta" +a['href'])
            i = j
            j = j*2
            time.sleep(2)


        def incrementar(n):
            p = n + 1
            return p

        veces = 0
        '''
        for i in range(len(image_link)):
            print(image_link[i])
        '''
        for link in image_link:
            #print(link)
            driver.get(link)
            soup_i = BeautifulSoup(driver.page_source, "html.parser")
            #print(soup_i)
            #print(soup_i.find_all('div', {"class":"KL4Bh"}) )
            down = soup_i.find_all('div',{"class":"KL4Bh"})[0].find_all('img')[0].get('src')
            #print(down)
            download_image(down, NUM_IMG)
            NUM_IMG = incrementar(NUM_IMG)
            veces += 1
            if numeroPublicaciones < 15:
                if veces - 1 == numeroPublicaciones:
                    break
            if veces == 15:
                break

        


                
