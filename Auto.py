import pyautogui
import time

################################################
def open_Terminal():                           #
    pyautogui.keyDown('ctrl')                  #
    pyautogui.keyDown('alt')                   #
    pyautogui.keyDown('t')                     #
    pyautogui.keyUp('ctrl')                    #
    pyautogui.keyUp('alt')                     #
    pyautogui.keyUp('t')                       #
    time.sleep(0.5)                            #
################################################

################################################
def command():                                 #
    time.sleep(3)                              #
    pyautogui.typewrite('turtlebot\n')         #
    time.sleep(1)                              #
    pyautogui.typewrite('cd Desktop\n')        #
    time.sleep(1)                              #
    pyautogui.typewrite('python When4.py\n')   #
    time.sleep(1)                              #
################################################

print("Waiting for get wifi on pi")
time.sleep(6)

pyautogui.click(x=100, y=100)
time.sleep(0.5)

print("############")
print("#####R1#####")
print("############")
print("")
open_Terminal()
pyautogui.typewrite('ssh pi@192.168.0.20\n')
command()

print("############")
print("#####R2#####")
print("############")
print("")
open_Terminal()
pyautogui.typewrite('ssh pi@192.168.0.23\n')
command()

print("############")
print("#####R3#####")
print("############")
print("")
open_Terminal()
pyautogui.typewrite('ssh pi@192.168.0.24\n')
command()

print("############")
print("#####R4#####")
print("############")
print("")
open_Terminal()
pyautogui.typewrite('ssh pi@192.168.0.25\n')
command()