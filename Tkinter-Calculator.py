# A simple non-scientific calculator programmed in python
# using the tkinter graphics library.
# Requirements: re, math, ctypes, tkinter, functools
# Programmed By: Stephen Adams

# Imports
import re
import math
import ctypes as ct
from tkinter import *
from functools import partial

# Global Variables
grey = '#3C3C3C'
ligh_grey = '#8D8D8D'
dark_grey = '#292929'

def evaluate(expression):
    for match in re.findall(r'√(\d+|\([^)]+\))', expression):
        if match.startswith('('):
            square_root = math.sqrt(eval(re.search(r'\(([^)]+)\)', match).group(1)))
        else:
            square_root = math.sqrt(float(match))
        expression = expression.replace('√' + match, str(square_root))
    try:
        return eval(expression.replace('×', '*').replace('÷', '/').replace('MOD', '%').replace('DIV', '//').replace('^', '**'))
    except:
        return 'Syntax Error'

# Button Press Function
def button_press(value):
    contains = str(display.cget('text')).replace('Syntax Error','')
    if value in ['=', '\r']:
        display.config(text=evaluate(contains))
    elif value in ['⌫', '\x08']:
        if contains.endswith('MOD') or contains.endswith('DIV'):
            display.config(text=contains[:-3])
        else:
            display.config(text=contains[:-1])
    elif value == 'AC':
        display.config(text='')
    elif value == 'Off':
        window.destroy()
    elif len(contains) <= 20 and re.fullmatch('[0-9,+,×,*,\\-,÷,/,(,),.,^,√,MOD,%,DIV,//]*',value):
        display.config(text=contains + value)

# Tkinter Window Configuration
window = Tk()
window.geometry('234x320')
window.title('Calculator')
window.resizable(False,False)
window.configure(bg=dark_grey)
window.bind('<Key>', lambda event:button_press(event.char))
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))
window.update()
ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(window.winfo_id()), 35, ct.byref(ct.c_int(0x00221F1E)),ct.sizeof(ct.c_int))

# User Interface Element Setup
Label(window,text='Standard Calculator',font=('Helvatical bold',15),bg=dark_grey,fg='white').pack(pady=8)

display = Label(window,text='',font=('Helvatical bold',10),bg=dark_grey,fg='white')
display.place(x=10,y=60)

buttons = [['^','√','(',')','Off'],['7','8','9','⌫','AC'],['4','5','6','+','×'],['3','2','1','-','÷'],['.','0','=','MOD','DIV']]
for row in range(5):
    for col in range(5):
        if row == 0:
            Button(window, text=buttons[row][col], command=partial(button_press,buttons[row][col]), height=1,width=4,bg=grey,fg='white',activebackground=ligh_grey,bd=0).place(x=45*col+10,y=50*row+90)
        else:
            Button(window, text=buttons[row][col], command=partial(button_press,buttons[row][col]), height=2,width=4,bg=grey,fg='white',activebackground=ligh_grey,bd=0).place(x=45*col+10,y=50*(row-1)+124)

# Tkinter Main Loop
window.mainloop()