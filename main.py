from tkinter import *
import io
import serial
import time

base = None

window = Tk()
window.title("Power Supply Control - TWINTEX TPM-3005")
window.geometry('380x170')
window.resizable(height=0, width=0)
window.configure(bg='gray')

state2 = Label(window, text="Made by Adrian Sabau", bg='gray', font=("Arial Bold", 10))
state2.grid(column=1, row=1)

try:
    ser = serial.Serial('COM238', baudrate=9600,
                        bytesize=8,
                        timeout=1,
                        stopbits=serial.STOPBITS_ONE,
                        parity=serial.PARITY_NONE,
                        xonxoff=False)
    if ser.isOpen():
        ser.close()
    ser.open()
    eol_char = '\r\n'
    sio = io.TextIOWrapper(io.BufferedReader(ser), newline=eol_char)
except Exception as e:
    state2.configure(text="Error: " + str(e))
    pass


def unlock():
    sending = 'SYST:LOC'
    ser.write((sending + eol_char).encode('utf-8'))
    time.sleep(0.3)
    ans = sio.read()
    state2.configure(text="Error: " + str(ans))


def startup():
    unlock()
    sending = 'APPL 13,5'
    ser.write((sending + eol_char).encode('utf-8'))
    time.sleep(0.3)
    ans = sio.read()
    state2.configure(text="Error: " + str(ans))
    unlock()


def clicked_start():
    state.configure(text="Started", bg='green')
    sending = 'OUTP:STAT ON'
    ser.write((sending + eol_char).encode('utf-8'))
    time.sleep(0.3)
    ans = sio.read()
    state2.configure(text="Error: " + str(ans))
    unlock()


def clicked_stop():
    state.configure(text="Stopped", bg="red")
    sending = 'OUTP:STAT OFF'
    ser.write((sending + eol_char).encode('utf-8'))
    time.sleep(0.3)
    ans = sio.read()
    state2.configure(text="Error: " + str(ans))
    unlock()


btnStart = Button(window, text="Start", font=("Arial Bold", 45), bg='gray', command=(lambda: clicked_start))
btnStart.grid(column=0, row=0)

btnStop = Button(window, text="Stop", font=("Arial Bold", 45), bg='gray', command=(lambda: clicked_stop))
btnStop.grid(column=1, row=0)

state = Label(window, text="State", bg='gray', font=("Arial Bold", 30))
state.grid(column=0, row=1)

startup()
startup()
window.mainloop()
