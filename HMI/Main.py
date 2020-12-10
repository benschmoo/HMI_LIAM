from tkinter import *
from rpi_ws281x import *

# LED config
LED_COUNT = 64
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

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
    for i in range(0,64):
        strip.setPixelColorRGB(i, 0, 255, 255)
    strip.show()


def callback2():
    print(1 + 1)    
    for i in range(0,64):
        strip.setPixelColorRGB(i, 255, 0, 0)
    strip.show()

buttonFrame = Frame(rightFrame)
buttonFrame.grid(row=1, column=0, padx=10, pady=3)

B1 = Button(buttonFrame, text="Button 1", bg="#FF0000", width=15, command=callback1)
B1.grid(row=0, column=0, padx=10, pady=3)

B2 = Button(buttonFrame, text="Button 2", bg="#FFFF00", width=15, command=callback2)
B2.grid(row=0, column=1, padx=10, pady=3)

Slider = Scale(rightFrame, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=400)
Slider.grid(row=2, column=0, padx=10, pady=3)

root.mainloop()  # GUI wird upgedatet. Danach keine Elemente setzen

