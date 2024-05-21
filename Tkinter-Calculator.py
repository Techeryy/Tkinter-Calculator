# A simple non-scientific calculator programmed in python
# using the tkinter graphics library.
# Requirements: tkinter, functools
# Programmed By: Stephen Adams

# Imports
from tkinter import *
from functools import partial

# Button Press Function
def button_press(value):
    contains = str(display.cget('text'))
    if contains == 'Syntax Error':
        contains = ''
    if value == '=':
        try:
            display.config(text=eval(contains.replace('×','*').replace('÷','/').replace('MOD','%').replace('DIV','//')))
        except:
            display.config(text='Syntax Error')
    elif value == '⌫' or value == '':
        sub = contains[len(contains)-3:len(contains)]
        if sub != 'MOD' and sub != 'DIV':
            display.config(text=contains[0:len(contains)-1])
        else:
            display.config(text=contains[0:len(contains)-3])
    elif value == 'AC':
        display.config(text='')
    else:
        if len(contains) != 21:
            display.config(text=contains + value)

# Detect Key Presses & Pass To Function
def key_press(event):
    button_press(event.char)

# Tkinter Window Configuration
window = Tk()
window.geometry('240x300')
window.title('Calculator')
window.resizable(False,False)
window.bind('<Key>', key_press)
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))

# User Interface Element Setup
Label(window,text='Standard Calculator',font=('Helvatical bold',15)).pack(pady=8)

display = Label(window,text='',font=('Helvatical bold',10))
display.place(x=10,y=60)

buttons = [['7','8','9','⌫','AC'],['4','5','6','+','×'],['3','2','1','-','÷'],['.','0','=','MOD','DIV']]
for row in range(4):
    for col in range(5):
        Button(window, text=buttons[row][col], command=partial(button_press,buttons[row][col]), height=2,width=4).place(x=45*col+10,y=50*row+100)

# Tkinter Main Loop
window.mainloop()