
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os 
import wget
import time
import urllib
import re
from bs4 import BeautifulSoup


#Esta es la direccion donde esta guardado el driver de chrome previamente descargado, para poder monitorizar las tareas.

DRIVER_PATH = "C:/Users/gonin/chromedriver_win32/chromedriver.exe"


USERNAME = "Nombre del usuario"
PASSWD = "Contraseña del usuario"

driver = webdriver.Chrome(DRIVER_PATH)
driver.get("https://www.instagram.com/")
NUM_IMG = 0

#Estos pasos son para autenticarte y entrar en la pagina
time.sleep(2)
def login():
    accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar todas')]"))).click()

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'password']")))

    username.clear()
    password.clear()
    username.send_keys(USERNAME)
    password.send_keys(PASSWD)
    time.sleep(1)
    log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(5)
    accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ahora no')]"))).click()
    time.sleep(3)
    accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ahora no')]"))).click()
    
#Llamamos al metodo login para entrar en la app y buscamos en el buscador interno el perfil al cual queremos realizar un scraping.  
   
login()
searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Busca']")))
searchbox.clear()
#Nombre del perfil a realizar el scrapping
searchbox.send_keys("NOMBRE_DEL _PERFIL")
searchbox.send_keys(Keys.ENTER)
time.sleep(2)
searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div"))).click()
time.sleep(2)


#Crea la carpeta donde se guradaran las imagenes descargadas.

path = os.getcwd()
path = os.path.join(path,"Imagenes")
os.mkdir(path)
path


#Obtenemos el numero de publicacions, usuarios seguidores y usuarios seguidos.

soup = BeautifulSoup(driver.page_source, 'html.parser')
datos = soup.find_all('span', {"class":"g47SY"})

publicaciones = str(datos[0])
seguidores = str(datos[1])
seguidos = str(datos[2])

n = int(publicaciones.find('>'))
p = int(publicaciones.rfind('<'))
numeroPublicaciones = int(publicaciones[n+1:p])
print(f'Publicaciones: {publicaciones[n+1:p]}')


n = int(seguidores.find('>'))
p = int(seguidores.rfind('<'))
print(f'Seguidores: {seguidores[n+1:p]}')

n = int(seguidos.find('>'))
p = int(seguidos.rfind('<'))
print(f'Seguidos: {seguidos[n+1:p]}')

#Metodo para descargar las imagenes

def download_image(url, NUM_IMG, destination = path):
    resource = urllib.request.urlopen(url)
    n = str(NUM_IMG)
    d = os.path.join(destination,"Imagenes")
    filename = d + n + ".jpg"
    #print(filename)
    output = open(filename,"wb")
    output.write(resource.read())
    output.close()

    
#PObtenemos las referancios de las imagenes del perfil y las descargamos.    


image_link = []

i = 0
j = 400

nScrolls = 0

if numeroPublicaciones < 6:
    nScrolls = 1
elif numeroPublicaciones < 12:
    nScrolls = 2
else:
    nScrolls = 3

for h in range(0, nScrolls):
    ws = "window.scroll(" + str(i) + "," + str(j) + ");"
    driver.execute_script(ws)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/p'):
            #En esta direccion hay que poner el nombre del perfil con el que has accedido a instagram.
            image_link.append("https://www.instagram.com/NOMBRE_PERFIL"+a['href'])
            #print("Found the URL:", "https://www.instagram.com/gonzalo_iniesta" +a['href'])
    i = j
    j = j*2
    time.sleep(2)



    
    
    
    
    
    
