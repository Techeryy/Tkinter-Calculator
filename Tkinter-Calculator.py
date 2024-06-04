# A non-scientific calculator programmed in python
# using the tkinter graphics library.
# Requirements: re, os, math, time, threading, ctypes, tkinter, functools
# Programmed By: Stephen Adams

# Imports
import ctypes as ct
from tkinter import *
from functools import partial
import re, os, math, time, threading

# Colour Definitions
font, grey, light_grey, dark_grey = '#FFFFFF', '#3C3C3C', '#8D8D8D', '#252526'

# Global Variable Setup
pointer = 0

# Fetch Display Contents
def getDisplay():
    return str(display.cget('text')).replace('|','')

# Edit Pointer Location
def editPointerLocation(location):
    global pointer
    pointer = location

# Blinking Cursor
def cursor():
    while True:
        content = getDisplay()
        if content != 'Syntax Error':
            index = len(content) - pointer
            display.config(text=content[:index] + '|' + content[index:])
            time.sleep(0.6)
            display.config(text=getDisplay())
        time.sleep(0.6)

# Create Themed Button (Defaults: Height=2, Width=4, Position=(0,0))
def createButton(text=None,command=None,h=2,w=4,x=0, y=0):
    return Button(window, text=text, command=command, height=h,width=w,bg=grey,fg=font,bd=0,activebackground=light_grey).place(x=x,y=y)

# Expression Evaluation (Square Root Support)
def evaluate(expression):
    pattern = r'√([0-9,.]+)|√\((.+)\)'
    try:
        while re.findall(pattern, expression):
            expression = re.sub(pattern, lambda x: str(math.sqrt(eval(evaluate(x.group(1) if x.group(1) else x.group(2))))), expression)
        return str(eval(expression))
    except: return 'Syntax Error'

# Key & Button Handling
def triggerAction(value):
    content = getDisplay().replace('Syntax Error','')
    index = len(content) - pointer
    if value in ['=', '\r']:
        display.config(text=evaluate(content.replace('×', '*').replace('÷', '/').replace('MOD', '%').replace('DIV', '//').replace('^', '**')))
        editPointerLocation(0)
    elif value in ['⌫', '\x08']:
        display.config(text=(content[:index-(3 if content[index-3:index] in ['MOD','DIV'] else 1)] + content[index:]) if index != 0 else content)
    elif value == 'AC':
        display.config(text='')
    elif value == 'Off':
        window.destroy()
        os._exit(1)
    elif len(content) <= 20 and re.fullmatch('[0-9,+,\\-,×,*,÷,/,(,),^,√,.,MOD,%,DIV,//]*',value):
        display.config(text=content[:index] + value + content[index:])

def navigate(action):
    content = getDisplay().replace('Syntax Error','')
    index = len(content) - pointer
    if action == 'Left' and pointer < len(content):
        editPointerLocation(pointer+3 if content[index-3:index] in ['MOD','DIV'] else pointer+1)
    elif action == 'Right' and pointer > 0:
        editPointerLocation(pointer -3 if content[index:index+3] in ['MOD','DIV'] else pointer-1)

# Tkinter Window Configuration
window = Tk()
window.geometry('234x320')
window.title('Calculator')
window.resizable(False,False)
window.configure(bg=dark_grey)
window.bind('<Key>', lambda event:triggerAction(event.char))
window.bind('<Right>', lambda event:navigate(event.keysym))
window.bind('<Left>', lambda event:navigate(event.keysym))
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))
window.update()
ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(window.winfo_id()), 35, ct.byref(ct.c_int(0x00221F1E)),ct.sizeof(ct.c_int))

# User Interface Element Setup
Label(window,text='Standard Calculator',font=('Helvatical bold',15),bg=dark_grey,fg=font).pack(pady=8)

display = Label(window,text='',font=('Helvatical bold',10),bg=dark_grey,fg=font)
display.place(x=10,y=60)

buttons = [['^','√','(',')','Off'],['7','8','9','⌫','AC'],['4','5','6','+','×'],['3','2','1','-','÷'],['.','0','=','MOD','DIV']]
for row in range(len(buttons)):
    for col in range(5):
        createButton(text=buttons[row][col],command=partial(triggerAction, buttons[row][col]),x=45 * col + 10,y=(50*row+90 if row == 0 else 50*(row-1)+124),h=(1 if row == 0 else 2))

# Starting Processes
threading.Thread(target=cursor).start()
window.mainloop()
os._exit(1)