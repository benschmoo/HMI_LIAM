from tkinter import *
from neopixel import *
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

# LED config für beide PWM Signale
LED_COUNT = 128
LED_PIN_18 = 18
LED_PIN_19 = 19
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL_0 = 0
LED_CHANNEL_1 = 1
BlinkNum = 0
strip18 = Adafruit_NeoPixel(LED_COUNT, LED_PIN_18, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_0)
strip18.begin()
strip19 = Adafruit_NeoPixel(LED_COUNT, LED_PIN_19, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_1)
strip19.begin()
BlinkArray1 = [5, 6, 7, 13, 14, 15, 21, 22, 23, 29, 30, 31, 37, 38, 39, 45, 46, 47, 53, 54, 55, 61, 62, 63]
BlinkArray2 = [64, 65, 66, 72, 73, 74, 80, 81, 82, 88, 89, 90, 96, 97, 98, 104, 105, 106, 112, 113, 114, 120, 121, 122]
Chairstate = 0  # if chair turned 180° state = 1
global FrameDestroy
global switch  # switch for Indicators

root = Tk()  # Fenster erstellen
root.wm_title("LIAM'S HMI")  # Fenster Titel
root.config(background="#FFFFFF")  # Hintrgrundfarbe des Fensters

# Hier kommen die Elemente hin
leftFrame = Frame(root, width=200, height=400)
leftFrame.grid(row=0, column=0, padx=10, pady=3)



# imageEx = PhotoImage(file='200x200')
# Label(leftFrame, image=imageEx).grid(row=2, column=0, padx=10, pady=3)

rightFrame = Frame(root, width=400, height=400)
rightFrame.grid(row=0, column=1, padx=10, pady=3)


buttonFrame = Frame(rightFrame)
DashboardFrame = Frame(rightFrame)
StairClimbFrame = Frame(rightFrame)
SensorsFrame = Frame(rightFrame)


for frame in (buttonFrame, DashboardFrame, StairClimbFrame, SensorsFrame):
    frame.grid(row=1, column=0, padx=10, pady=3)

def raise_frame(frame):
    buttonFrame.grid_remove()
    DashboardFrame.grid_remove()
    StairClimbFrame.grid_remove()
    SensorsFrame.grid_remove()
    time.sleep(0.5)
    frame.grid()
    frame.tkraise()

def LightOFF():
    global switch
    switch = False
    for i in range(0, LED_COUNT, 1):
        strip18.setPixelColorRGB(i, 0, 0, 0)
        strip19.setPixelColorRGB(i, 0, 0, 0)
        strip18.show()
        strip19.show()


def StandingLight():
    for i in range(0, LED_COUNT, 1):
        strip18.setPixelColorRGB(i, 0, 0, 0)
        strip19.setPixelColorRGB(i, 0, 0, 0)
    T = [3, 4, 11, 12, 19, 20, 27, 28, 35, 36, 43, 44, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
         62, 63]
    H = [64, 65, 70, 71, 72, 73, 78, 79, 80, 81, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
         100, 101, 102, 103, 104, 105, 110, 111, 112, 113, 118, 119, 120, 121, 126, 127]
    R = [0, 1, 5, 6, 9, 10, 13, 14, 18, 19, 21, 22, 27, 28, 29, 30, 34, 35, 36, 37, 38, 41, 42, 45, 46,
         49, 50, 51, 52, 53, 54, 58, 59, 60, 61, 62]
    O = [66, 67, 68, 69, 73, 74, 75, 76, 77, 78, 80, 81, 82, 85, 86, 87, 88, 89, 94, 95, 96, 97, 102, 103,
         104, 105, 106, 109, 110, 111, 113, 114, 115, 116, 117, 118, 122, 123, 124, 125]
    if Chairstate == 0:
        for i in T:
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in H:
            strip18.setPixelColorRGB(j, 255, 255, 255)
        for k in R:
            strip19.setPixelColorRGB(k, 0, 255, 0)
        for l in O:
            strip19.setPixelColorRGB(l, 0, 255, 0)
    elif Chairstate == 1:
        for i in T:
            strip19.setPixelColorRGB(i, 255, 255, 255)
        for j in H:
            strip19.setPixelColorRGB(j, 255, 255, 255)
        for k in R:
            strip18.setPixelColorRGB(k, 0, 255, 0)
        for l in O:
            strip18.setPixelColorRGB(l, 0, 255, 0)
    else:
        callback2()
    strip18.setBrightness(20)
    strip19.setBrightness(20)
    strip18.show()
    strip19.show()


def LightON():
    for i in range(0, 128):
        strip18.setPixelColorRGB(i, 255, 255, 255)
    for j in range(0, 128):
        strip19.setPixelColorRGB(j, 0, 255, 0)
    strip18.setBrightness(50)
    strip19.setBrightness(50)
    strip18.show()
    strip19.show()


def callback2():
    print(1 + 1)
    for i in range(0, 64):
        strip18.setPixelColorRGB(i, 150, 150, 1500)
    for j in range(65, 128):
        strip18.setPixelColorRGB(j, 0, 150, 0)
    strip18.show()


def BlinkRight():
    global switch
    switch = False  # to shutdown all other blinkers
    time.sleep(0.6)
    switch = True
    while switch:
        for i in range(0, 128):
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in range(0, 128):
            strip19.setPixelColorRGB(j, 0, 255, 0)
        strip18.setBrightness(50)
        strip19.setBrightness(50)
        strip18.show()
        strip19.show()
        time.sleep(0.6)

        root.update()
        if not switch:
            break

        if Chairstate == 0:
            for t in BlinkArray1:
                strip18.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip19.setPixelColorRGB(z, 20, 60, 0)
        elif Chairstate == 1:
            for t in BlinkArray1:
                strip19.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip18.setPixelColorRGB(z, 20, 60, 0)
        strip18.setBrightness(50)
        strip19.setBrightness(50)
        strip18.show()
        strip19.show()
        time.sleep(0.6)


def BlinkLeft():
    global switch
    switch = False  # to shutdown all other blinkers
    time.sleep(0.6)
    switch = True
    while switch:
        for i in range(0, 128):
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in range(0, 128):
            strip19.setPixelColorRGB(j, 0, 255, 0)
        strip18.setBrightness(50)
        strip19.setBrightness(50)
        strip18.show()
        strip19.show()
        time.sleep(0.6)

        root.update()
        if not switch:
            break

        if Chairstate == 0:
            for t in BlinkArray1:
                strip19.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip18.setPixelColorRGB(z, 20, 60, 0)
        elif Chairstate == 1:
            for t in BlinkArray1:
                strip18.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip19.setPixelColorRGB(z, 20, 60, 0)
        strip18.setBrightness(50)
        strip19.setBrightness(50)
        strip18.show()
        strip19.show()
        time.sleep(0.6)


def WarningLight():
    global switch
    switch = False  # to shutdown all other blinkers
    time.sleep(0.6)
    switch = True
    while switch:
        for i in range(0, 128):
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in range(0, 128):
            strip19.setPixelColorRGB(j, 0, 255, 0)
        strip18.setBrightness(50)
        strip19.setBrightness(50)
        strip18.show()
        strip19.show()
        time.sleep(0.6)

        root.update()
        if not switch:
            break

        if Chairstate == 0:
            for t in BlinkArray1:
                strip18.setPixelColorRGB(t, 20, 60, 0)
                strip19.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip18.setPixelColorRGB(z, 20, 60, 0)
                strip19.setPixelColorRGB(z, 20, 60, 0)
        strip18.setBrightness(50)
        strip19.setBrightness(50)
        strip18.show()
        strip19.show()
        time.sleep(0.6)


def blinkOff():
    global switch
    switch = False

# Dashboard Frame
TestBTN = Button(DashboardFrame, text="Testomania", bg="#FFFFF0", width=15, height=10, command=LightOFF)
TestBTN.grid(row=0, column=0, padx=10, pady=3)

# Light Buttons/Frame
#buttonFrame = Frame(rightFrame)
#buttonFrame.grid(row=1, column=0, padx=10, pady=3)

LightOFF = Button(buttonFrame, text="OFF", bg="#FF0000", width=15, height=5, command=LightOFF)
LightOFF.grid(row=0, column=0, padx=10, pady=3)

THRO = Button(buttonFrame, text="Standing light", bg="#FF0000", width=15, height=5, command=StandingLight)
THRO.grid(row=0, column=1, padx=10, pady=3)

LightON = Button(buttonFrame, text="LIGHT", bg="#FF0000", width=15, height=10, command=LightON)
LightON.grid(row=0, column=2, padx=10, pady=3)

Warning_Lights = Button(buttonFrame, text="Warning Lights", bg="#FFF000", width=15, height=5, command=WarningLight)
Warning_Lights.grid(row=1, column=1, padx=10, pady=3)

Indicator_Left = Button(buttonFrame, text="Indicator Left", bg="#FFF000", width=15, height=5, command=BlinkLeft)
Indicator_Left.grid(row=2, column=0, padx=10, pady=3)

Indicators_OFF = Button(buttonFrame, text="Indicator OFF", bg="#FFFF00", width=15, height=5, command=blinkOff)
Indicators_OFF.grid(row=2, column=1, padx=10, pady=3)

Indicator_Right = Button(buttonFrame, text="Indicator Right", bg="#FFF000", width=15, height=5, command=BlinkRight)
Indicator_Right.grid(row=2, column=2, padx=10, pady=3)


# Stairclimb Frame

Slider = Scale(StairClimbFrame, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=400)
Slider.grid(row=2, column=0, padx=10, pady=3)


# Sensors Frame

# Menubuttons

menuFrame = Frame(leftFrame)
menuFrame.grid(row=1, column=0, padx=10, pady=3)

Dashboard = Button(menuFrame, text="Overview", bg="#FF0000", width=15, height=5, command=lambda: raise_frame(DashboardFrame)).pack()
Dashboard.grid(row=0, column=0, padx=10, pady=3)
Label(menuFrame).pack()

Lights = Button(menuFrame, text="Lights", bg="#FF0000", width=15, height=5, command=lambda: raise_frame(buttonFrame)).pack()
Lights.grid(row=1, column=0, padx=10, pady=3)
Label(menuFrame).pack()

StairClimber = Button(menuFrame, text="Stairclimber", bg="#FF0000", width=15, height=5, command=lambda: raise_frame(StairClimbFrame)).pack()
StairClimber.grid(row=2, column=0, padx=10, pady=3)

StairClimber(menuFrame).pack()

Sensors = Button(menuFrame, text="Sensors", bg="#FF0000", width=15, height=5, command=lambda: raise_frame(SensorsFrame)).pack()
Sensors.grid(row=3, column=0, padx=10, pady=3)

Sensors(menuFrame).pack()

raise_frame(DashboardFrame)
root.mainloop()  # GUI wird upgedatet. Danach keine Elemente setzen
