from tkinter import *
from neopixel import *
import RPi.GPIO as GPIO
import time
import smbus2
import bme280
import threading
from PIL import Image, ImageTk

Sensor1 = 16
Sensor2 = 18
HornSignal = 31
Red = 32
Green = 38 
Blue = 40

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(Sensor1, GPIO.IN,
           pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(Sensor2, GPIO.IN,
           pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(HornSignal, GPIO.OUT) # set a port/pin as an output
GPIO.setup(Red, GPIO.OUT) # set a port/pin as an output
GPIO.setup(Green, GPIO.OUT) # set a port/pin as an output
GPIO.setup(Blue, GPIO.OUT) # set a port/pin as an output

# I2c communication
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)

# temperature,pressure,humidity = bme280.readBME280All()

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
global FrameDestroy
global switch  # switch for Indicators
global Chairstate

# Logic for Chairstate
def getChairstate():
    global Chairstate                     # defining global variable for usage in all functions
    if GPIO.input(Sensor1) == GPIO.HIGH:  # only sensor1 connected to GPIO 16 is HIGH
        if GPIO.input(Sensor2) == GPIO.LOW:
            Chairstate = 1
            print(Chairstate)
            return Chairstate
    elif GPIO.input(Sensor2) == GPIO.HIGH:  # only sensor2 connected to GPIO 18 is HIGH
        if GPIO.input(Sensor1) == GPIO.LOW:
            Chairstate = 0
            return Chairstate
    else:
        ERROR()                             # if both GPIO are HIGH or LOW --> Error --> WarningLight
        print("IOError")


root = Tk()  # Fenster erstellen
root.wm_title("LIAM'S HMI")  # Fenster Titel
root.config(background="#000000")  # Hintrgrundfarbe des Fensters
root.attributes('-zoomed', True)

# Hier kommen die Elemente hin
leftFrame = Frame(root, width=200, height=400, background="#000000")
leftFrame.grid(row=0, column=0, padx=10, pady=3)

# Image import and resize using PIL
IndLeftOrig = Image.open("/home/pi/repos/HMI_LIAM/HMI/venv/Pictures/IndLeft.png")
IndLeftResize = IndLeftOrig.resize((140,90), Image.ANTIALIAS)
IndLeft = ImageTk.PhotoImage(IndLeftResize)
IndRightOrig = Image.open("/home/pi/repos/HMI_LIAM/HMI/venv/Pictures/IndRight.png")
IndRightResize = IndRightOrig.resize((140,90), Image.ANTIALIAS)
IndRight = ImageTk.PhotoImage(IndRightResize)
WarnLightOrig = Image.open("/home/pi/repos/HMI_LIAM/HMI/venv/Pictures/Warnblinker.png")
WarnLightResize = WarnLightOrig.resize((100,90), Image.ANTIALIAS)
WarnLight = ImageTk.PhotoImage(WarnLightResize)
HornOrig = Image.open("/home/pi/repos/HMI_LIAM/HMI/venv/Pictures/Horn.png")
HornResize = HornOrig.resize((130,70), Image.ANTIALIAS)
Horn = ImageTk.PhotoImage(HornResize)

WheelchairOrig = Image.open("/home/pi/repos/HMI_LIAM/HMI/venv/Pictures/Wheelchair.jpg")
WheelchairResize = WheelchairOrig.resize((400,400), Image.ANTIALIAS)
Wheelchair = ImageTk.PhotoImage(WheelchairResize)


#defining of frames for the right side of the HMI layout
rightFrame = Frame(root, width=400, height=400, background="#000000")
rightFrame.grid(row=0, column=1, padx=10, pady=3)

buttonFrame = Frame(rightFrame, bg="#000000")
DashboardFrame = Frame(rightFrame, bg="#000000")
StairClimbFrame = Frame(rightFrame, bg="#000000")
SensorsFrame = Frame(rightFrame, bg="#000000")

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

# functions for the light options and the horn following
def LightOFF():
    global switch
    switch = False
    LightOFF.configure(bg="yellow")
    LightON.configure(bg="#FD6A02")
    THRO.configure(bg="#FD6A02")
    for i in range(0, LED_COUNT, 1):
        strip18.setPixelColorRGB(i, 0, 0, 0)
        strip19.setPixelColorRGB(i, 0, 0, 0)
        strip18.show()
        strip19.show()


def StandingLight():
    global Chairstate
    getChairstate()
    LightOFF.configure(bg="#FD6A02")
    LightON.configure(bg="#FD6A02")
    THRO.configure(bg="yellow")
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
    if Chairstate == 1:
        for i in T:
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in H:
            strip18.setPixelColorRGB(j, 255, 255, 255)
        for k in R:
            strip19.setPixelColorRGB(k, 0, 255, 0)
        for l in O:
            strip19.setPixelColorRGB(l, 0, 255, 0)
    elif Chairstate == 0:
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
    global Chairstate
    getChairstate()     # get current chairstate
    LightOFF.configure(bg="#FD6A02")    # lowlight "OFF" button
    LightON.configure(bg="yellow")      # highligt "ON" button
    THRO.configure(bg="#FD6A02")        # lowlight "Stand" button
    if Chairstate == 0:             # ask chairstate
        for i in range(0, 128):     # LED range first led matrix
            strip19.setPixelColorRGB(i, 255, 255, 255)      # set color white
        for j in range(0, 128):     # LED range second LED matrix
            strip18.setPixelColorRGB(j, 0, 255, 0)      # set color red
    if Chairstate == 1:
        for i in range(0, 128):
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in range(0, 128):
            strip19.setPixelColorRGB(j, 0, 255, 0)
    strip18.setBrightness(50)       # set brightness LED matrix
    strip19.setBrightness(50)
    strip18.show()                  # show new config
    strip19.show()


def callback2():
    print(1 + 1)
    for i in range(0, 64):
        strip18.setPixelColorRGB(i, 150, 150, 1500)
    for j in range(65, 128):
        strip18.setPixelColorRGB(j, 0, 150, 0)
    strip18.show()


def BlinkRight():
    global Chairstate
    getChairstate()
    global switch
    switch = False  # to shutdown all other blinkers
    time.sleep(0.1)
    switch = True
    while switch:
        if Chairstate == 0:
            for i in range(0, 128):
                strip19.setPixelColorRGB(i, 255, 255, 255)
            for j in range(0, 128):
                strip18.setPixelColorRGB(j, 0, 255, 0)
        if Chairstate == 1:
            for i in range(0, 128):
                strip18.setPixelColorRGB(i, 255, 255, 255)
            for j in range(0, 128):
                strip19.setPixelColorRGB(j, 0, 255, 0)
        strip18.setBrightness(25)
        strip19.setBrightness(25)
        strip18.show()
        strip19.show()
        time.sleep(0.6)

        root.update()
        if not switch:
            break

        if Chairstate == 1:
            for t in BlinkArray1:
                strip18.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip19.setPixelColorRGB(z, 20, 60, 0)
        elif Chairstate == 0:
            for t in BlinkArray1:
                strip19.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip18.setPixelColorRGB(z, 20, 60, 0)
        strip18.setBrightness(25)
        strip19.setBrightness(25)
        strip18.show()
        strip19.show()
        time.sleep(0.6)


def BlinkLeft():
    global Chairstate
    getChairstate()
    global switch
    switch = False  # to shutdown all other blinkers
    time.sleep(0.1)
    switch = True
    while switch:
        if Chairstate == 0:
            for i in range(0, 128):
                strip19.setPixelColorRGB(i, 255, 255, 255)
            for j in range(0, 128):
                strip18.setPixelColorRGB(j, 0, 255, 0)
        if Chairstate == 1:
            for i in range(0, 128):
                strip18.setPixelColorRGB(i, 255, 255, 255)
            for j in range(0, 128):
                strip19.setPixelColorRGB(j, 0, 255, 0)
        strip18.setBrightness(25)
        strip19.setBrightness(25)
        strip18.show()
        strip19.show()
        time.sleep(0.6)

        root.update()
        if not switch:
            break

        if Chairstate == 1:
            for t in BlinkArray1:
                strip19.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip18.setPixelColorRGB(z, 20, 60, 0)
        elif Chairstate == 0:
            for t in BlinkArray1:
                strip18.setPixelColorRGB(t, 20, 60, 0)
            for z in BlinkArray2:
                strip19.setPixelColorRGB(z, 20, 60, 0)
        strip18.setBrightness(25)
        strip19.setBrightness(25)
        strip18.show()
        strip19.show()
        time.sleep(0.6)


def WarningLight():
    getChairstate()
    global switch
    switch = False  # to shutdown all other blinkers
    time.sleep(0.1)
    switch = True
    while switch:
        if Chairstate == 0:
            for i in range(0, 128):
                strip19.setPixelColorRGB(i, 255, 255, 255)
            for j in range(0, 128):
                strip18.setPixelColorRGB(j, 0, 255, 0)
        if Chairstate == 1:
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

# following 2 functions need connection and data with/of SPS
def ReverseLight():
    global Chairstate
    getChairstate()     # get current chairstate
    LightOFF.configure(bg="#FD6A02")    # lowlight "OFF" button
    LightON.configure(bg="yellow")      # highligt "ON" button
    THRO.configure(bg="#FD6A02")        # lowlight "Stand" button
    if Chairstate == 0:             # ask chairstate
        for i in range(0, 128):     # LED range first led matrix
            strip19.setPixelColorRGB(i, 255, 255, 255)      # set color white
        for j in range(0, 63):     # LED range second LED matrix
            strip18.setPixelColorRGB(j, 0, 255, 0)      # set color red
        for k in range(64, 128):     # LED range second LED matrix
            strip18.setPixelColorRGB(j, 255, 255, 255)      # set color white one panel --> reverse light
    if Chairstate == 1:
        for i in range(0, 128):
            strip18.setPixelColorRGB(i, 255, 255, 255)
        for j in range(0, 63):
            strip19.setPixelColorRGB(j, 0, 255, 0)
        for k in range(64, 128):     # LED range second LED matrix
            strip18.setPixelColorRGB(j, 255, 255, 255)      # set color white one panel --> reverse light
    strip18.setBrightness(50)       # set brightness LED matrix
    strip19.setBrightness(50)
    strip18.show()                  # show new config
    strip19.show()


def BreakingLight():
    global Chairstate
    getChairstate()     # get current chairstate
    LightOFF.configure(bg="#FD6A02")    # lowlight "OFF" button
    LightON.configure(bg="yellow")      # highligt "ON" button
    THRO.configure(bg="#FD6A02")        # lowlight "Stand" button
    if Chairstate == 0:             # ask chairstate
        for i in range(0, 128):     # LED range first led matrix
            strip19.setPixelColorRGB(i, 255, 255, 255)      # set color white
            strip19.setBrightness(50)   # brightness normal
        for j in range(0, 128):     # LED range second LED matrix
            strip18.setPixelColorRGB(j, 0, 255, 0)      # set color red
            strip18.setBrightness(80)   # higher brightness breaking light
    if Chairstate == 1:
        for i in range(0, 128):
            strip18.setPixelColorRGB(i, 255, 255, 255)
            strip18.setBrightness(50)   # brightness normal
        for j in range(0, 128):
            strip19.setPixelColorRGB(j, 0, 255, 0)
            strip19.setBrightness(80)   # higher brightness breaking light
    strip18.show()                  # show new config
    strip19.show()

def ERROR():
    getChairstate()
    global switch
    global switch
    switch = False
    for i in range(0, LED_COUNT, 1):
        strip18.setPixelColorRGB(i, 0, 0, 0)
        strip19.setPixelColorRGB(i, 0, 0, 0)
        strip18.show()
        strip19.show()
        time.sleep(0.6)

    for j in range(0, LED_COUNT, 1):
        strip18.setPixelColorRGB(j, 20, 60, 0)
        strip19.setPixelColorRGB(j, 20, 60, 0)
        strip18.show()
        strip19.show()
        time.sleep(0.6)


def blinkOff():
    global switch
    switch = False

def start_Horn(event):
    global beeping
    beeping = True
    GPIO.output(31,1)
    print("starting horn...")

def stop_Horn(event):
    global beeping
    GPIO.output(31,0)
    print("stopping horn...")
    beeping = False

def UnderfloorLight():
    GPIO.output(Red,1)
    GPIO.output(Green,1)
    GPIO.output(Blue,1)


temp = str(data.temperature)

# Dashboard Frame --> just picture and temp/humidity/hight is mentioned
WheelChairIMG = Label(DashboardFrame, image=Wheelchair, bg="#FFFFFF", pady=20)
WheelChairIMG.grid(row=0, column=0, padx=10, pady=3)

Temperature = Label(DashboardFrame, text="Temperature: %.2f °C" % data.temperature, bg="#FFFF00")
Temperature.grid(row=0, column=0, padx=10, pady=3)

# Light Buttons/Frame
# buttonFrame = Frame(rightFrame)
# buttonFrame.grid(row=1, column=0, padx=10, pady=3)

LightOFF = Button(buttonFrame, text="OFF", bg="#FD6A02", pady=30, padx=60, command=LightOFF)
LightOFF.grid(row=0, column=0, padx=5, pady=3)

THRO = Button(buttonFrame, text="Standing light", bg="#FD6A02",pady=30, padx=60, command=StandingLight)
THRO.grid(row=0, column=1, padx=5, pady=3)

LightON = Button(buttonFrame, text="LIGHT", bg="#FD6A02", pady=30, padx=60, command=LightON)
LightON.grid(row=0, column=2, padx=5, pady=3)

Warning_Lights = Button(buttonFrame, image=WarnLight, bg="#FFF000", pady=30, padx=60, command=WarningLight)
Warning_Lights.grid(row=1, column=1, padx=5, pady=3)

Indicator_Left = Button(buttonFrame, image=IndLeft, text="Indicator Left", bg="#FFF000", pady=30, padx=60, command=BlinkLeft)
Indicator_Left.grid(row=2, column=0, padx=5, pady=3)

Indicators_OFF = Button(buttonFrame, text="Indicator OFF", bg="#FD6A02", pady=30, padx=60, command=blinkOff)
Indicators_OFF.grid(row=2, column=1, padx=5, pady=3)

Indicator_Right = Button(buttonFrame, image=IndRight, text="Indicator Right", bg="#FFF000", pady=30, padx=60, command=BlinkRight)
Indicator_Right.grid(row=2, column=2, padx=5, pady=3)

HornButton = Button(buttonFrame, image=Horn, bg="#FFF000", pady=30, padx=60)
HornButton.grid(row=3, column=1, padx=5, pady=3)
HornButton.bind('<ButtonPress-1>',start_Horn)
HornButton.bind('<ButtonRelease-1>',stop_Horn)

Underfloor = Button(buttonFrame, text="Underfloor", bg="#FD6A02", pady=20, padx=40, command=UnderfloorLight)
Underfloor.grid(row=3, column=2, padx=5, pady=3)

# Stairclimb Frame --> just an idea actually, has to improved in further developments,

moveOut = Button(StairClimbFrame, text="MOVE OUT", bg="#FD6A02", pady=60, padx=60)
moveOut.grid(row=0, column=0, padx=10, pady=5)

upStairs = Button(StairClimbFrame, text="UPSTAIRS", bg="#FD6A02",pady=60, padx=60)
upStairs.grid(row=0, column=1, padx=10, pady=5)

moveIn = Button(StairClimbFrame, text="MOVE IN", bg="#FD6A02", pady=60, padx=60)
moveIn.grid(row=2, column=0, padx=10, pady=5)

downStairs = Button(StairClimbFrame, text="UPSTAIRS", bg="#FD6A02",pady=60, padx=60)
downStairs.grid(row=2, column=1, padx=10, pady=5)

Slider = Scale(StairClimbFrame, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=400)
Slider.grid(row=2, column=0, padx=10, pady=3)

# Sensors Frame
# nothing here right now....


# Menubuttons

menuFrame = Frame(leftFrame, bg="#000000")
menuFrame.grid(row=1, column=0, padx=10, pady=3)

Dashboard = Button(menuFrame, text="Overview", bg="#FD6A02", width=20, height=3,
                   command=lambda: raise_frame(DashboardFrame)).pack()
Label(menuFrame).pack()

Lights = Button(menuFrame, text="Lights", bg="#FD6A02", width=20, height=3,
                command=lambda: raise_frame(buttonFrame)).pack()
Label(menuFrame).pack()

StairClimber = Button(menuFrame, text="Stairclimber", bg="#FD6A02", width=20, height=3,
                      command=lambda: raise_frame(StairClimbFrame)).pack()
Label(menuFrame).pack()

Sensors = Button(menuFrame, text="Sensors", bg="#FD6A02", width=20, height=3,
                 command=lambda: raise_frame(SensorsFrame)).pack()
Label(menuFrame).pack()

raise_frame(DashboardFrame) # initial frame after startup
root.mainloop()  # GUI wird upgedatet. Danach keine Elemente setzen
