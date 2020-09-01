import tkinter
import Steganography (Lean)

window = tkinter.Tk()
window.title("Stego")
window.geometry("300x300")
window.wm_iconbitmap('favicon.ico')
window.configure(background='white')

def Kill():
    window.destroy()
            
def Main():
    hide= tkinter.Button(window, text='Hide Data', command= hideCallBack)
    recover = tkinter.Button(window, text='Recover Data', command= recoverCallBack)
    Exit = tkinter.Button(window, text='Exit', fg='red',command=quit)
    Open_main.destroy()
    hide.configure(background='light blue')
    recover.configure(background='violet')
    #postions of buttons
    hide.place(x=10, y=30, width=280, height=30)
    recover.place(x=10, y=70, width=280, height=30)
    Exit.place(x=10, y=260, width=280, height=30)
            
def hideCallBack():
    window = tkinter.Tk()
    window.title("Hide")
    window.geometry("300x300")
    window.wm_iconbitmap('favicon.ico')

    window.configure(background='light blue')
    hide_1= tkinter.Button(window,text='Upload Image',command= uploadCallBack)
    hide_1.place(x=10,y= 50, width=280, height=30)
    hide_back = tkinter.Button(window,text='back', fg='red')
    hide_back.place(x=10,y=200, width=280, height=30)

def recoverCallBack():
    window = tkinter.Tk()
    window.title("Stego")   
    window.geometry("300x300")
    window.wm_iconbitmap('favicon.ico')
    window.configure(background='violet')
    recover_1= tkinter.Button(window,text='Retrive Image',command= retriveCallBack)
    recover_1.place(x=10,y= 50, width=280, height=30)
    recover_back = tkinter.Button(window,text='back', fg='red')
    recover_back.place(x=10,y=200, width=280, height=30)
    
def retriveCallBack():
    SteganographyClass.Retrive()
    
    
def uploadCallBack():
    SteganographyClass.Stego()

Open_main= tkinter.Button(window,text='Open', command=Main)
Open_main.configure(background='red')
Open_main.place(x=10, y=150, width=280, height=30)
window.mainloop()


