# A simple non-scientific calculator programmed in python
# using the tkinter graphics library.
# Requirements: tkinter, functools
# Programmed By: Stephen Adams

# Imports
import re
from tkinter import *
from functools import partial

# Button Press Function
def button_press(value):
    contains = str(display.cget('text'))
    if contains == 'Syntax Error':
        contains = ''
    if value in ['=', '\r']:
        try:
            result = eval(contains.replace('×', '*').replace('÷', '/').replace('MOD', '%').replace('DIV', '//'))
            display.config(text=result)
        except:
            display.config(text='Syntax Error')
    elif value in ['⌫', '\x08']:
        if contains.endswith('MOD') or contains.endswith('DIV'):
            display.config(text=contains[:-3])
        else:
            display.config(text=contains[:-1])
    elif value == 'AC':
        display.config(text='')
    else:
        if len(contains) != 20 and re.fullmatch('[0-9,+,×,*,\\-,÷,/,(,),.,MOD,%,DIV,//]*',value):
            display.config(text=contains + value)

# Tkinter Window Configuration
window = Tk()
window.geometry('240x300')
window.title('Calculator')
window.resizable(False,False)
window.bind('<Key>', lambda event:button_press(event.char))
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