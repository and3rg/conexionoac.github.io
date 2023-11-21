try:
    import usocket as socket
except:
    import socket

import network
from machine import Pin, I2C
import bme280

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

ssid = 'COWIFI250723930/0'
password = 'WiFi-88398745'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Conexion correcta')
print(station.ifconfig())

bme = bme280.BME280(i2c=i2c)


def leer_sensor():
    global temp, hum, pres
    temp = bme.values[0]
    pres = bme.values[1]
    hum = bme.values[2]
    return ()


def cargar_html():
    try:
        with open('index.html', 'r') as file:
            return file.read()
    except Exception as e:
        print("Error al cargar el archivo HTML:", str(e))
        return ""


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conexion, direccion = s.accept()
    request = conexion.recv(1024)
    leer_sensor()
    respuesta = cargar_html()
    conexion.send('HTTP/1.1 200 OK\n')
    conexion.send('Content-Type: text/html\n')
    conexion.send('Connection: close\n\n')
    conexion.sendall(respuesta)
    conexion.close()
