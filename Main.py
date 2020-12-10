from tkinter import *


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


def callback2():
    print(1 + 1)


buttonFrame = Frame(rightFrame)
buttonFrame.grid(row=1, column=0, padx=10, pady=3)

B1 = Button(buttonFrame, text="Button 1", bg="#FF0000", width=15, command=callback1)
B1.grid(row=0, column=0, padx=10, pady=3)

B2 = Button(buttonFrame, text="Button 2", bg="#FFFF00", width=15, command=callback2)
B2.grid(row=0, column=1, padx=10, pady=3)

Slider = Scale(rightFrame, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=400)
Slider.grid(row=2, column=0, padx=10, pady=3)

root.mainloop()  # GUI wird upgedatet. Danach keine Elemente setzen

if __name__ == "__main__":
    # execute only if run as a script
    main()