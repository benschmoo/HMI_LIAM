from tkinter import *
from neopixel import *
import RPi.GPIO as GPIO
import time
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

p = GPIO.PWM(23, 800000)
p.start(1)
# LED config
LED_COUNT = 128
LED_PIN = 23
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 0
BlinkNum= 0
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA , LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


root = Tk()  # Fenster erstellen
root.wm_title("Raspberry Pi GUI")  # Fenster Titel
root.config(background="#FFFFFF")  # Hintergrundfarbe des Fensters

# Hier kommen die Elemente hin
leftFrame = Frame(root, width=200, height=400)
leftFrame.grid(row=0, column=0, padx=10, pady=3)

leftLabel1 = Label(leftFrame, text="Platzhalter Text")
leftLabel1.grid(row=0, column=0, padx=10, pady=3)
leftLabel2 = Label(leftFrame, text="Dies ist ein Text\nmit mehreren Zeilen.")
leftLabel2.grid(row=1, column=0, padx=10, pady=3)

#imageEx = PhotoImage(file='200x200')
#Label(leftFrame, image=imageEx).grid(row=2, column=0, padx=10, pady=3)

rightFrame = Frame(root, width=400, height=400)
rightFrame.grid(row=0, column=1, padx=10, pady=3)

E1 = Entry(rightFrame, width=50)
E1.grid(row=0, column=0, padx=10, pady=3)


def callback1():
    print(E1.get())
    TH = [3, 4, 11, 12, 19, 20, 27, 28, 35, 36, 43, 44, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
          62, 63]
    RO = [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 83, 84, 91, 92, 99, 100, 107, 108,
          112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]
    for i in TH:
        strip.setPixelColorRGB(i, 0, 255, 255)
    for j in RO:
        strip.setPixelColorRGB(j, 0, 0, 255)
    strip.show()


def callback2():
    print(1 + 1)    
    for i in range(0,64):
        strip.setPixelColorRGB(i, 150, 150, 1500)
    for j in range(65, 128):
        strip.setPixelColorRGB(j, 0, 150, 0)
    strip.show()
    
def scoreUp(BlinkNum):
    #BlinkNum += 1
    print(BlinkNum)
    return BlinkNum + 1

def callback3():
    def run():
        while (switch == True) :
            for x in range (0,10):    
                for i in range(0,64):
                    strip.setPixelColorRGB(i, 30, 30, 30)
                for j in range(65, 128):
                    strip.setPixelColorRGB(j, 0, 30, 0)
                strip.show()
                time.sleep(0.3)

                for i in range(0,40):
                    strip.setPixelColorRGB(i, 30, 30, 30)
                for t in range(40, 64):
                    strip.setPixelColorRGB(t, 20, 60, 0)
                for j in range(64,104):
                    strip.setPixelColorRGB(j, 0, 30, 0)
                for z in range(104, 128):
                    strip.setPixelColorRGB(z, 20, 60, 0)
                    
                strip.show()
                time.sleep(0.3)
                if switch == False:
                    break
    thread = threading.Thread(target=run)
    thread.start()

def blinkon():
    global switch
    switch = True
    callback3()

def blinkoff():
    global switch
    switch = False

buttonFrame = Frame(rightFrame)
buttonFrame.grid(row=1, column=0, padx=10, pady=3)

B1 = Button(buttonFrame, text="Button 1", bg="#FF0000", width=15, command=callback1)
B1.grid(row=0, column=0, padx=10, pady=3)

B2 = Button(buttonFrame, text="Button 2", bg="#FFFF00", width=15, command=blinkoff)
B2.grid(row=0, column=1, padx=10, pady=3)


B3 = Button(buttonFrame, text="Blink", bg="#FFF000", width=15, command=blinkon)
B3.grid(row=0, column=2, padx=10, pady=3)


Slider = Scale(rightFrame, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=400)
Slider.grid(row=2, column=0, padx=10, pady=3)

root.mainloop()  # GUI wird upgedatet. Danach keine Elemente setzen

