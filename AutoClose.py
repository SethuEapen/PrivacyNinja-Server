#Sockets code by Alexander Baran-Harper: https://www.youtube.com/watch?v=IZX7G77daG0
#Hotkey, Keyboard Simulation, and email by PyTutorials: https://www.youtube.com/watch?v=n_dfv5DLCGI, https://www.youtube.com/watch?v=DTnz8wA6wpw, https://www.youtube.com/watch?v=YPiHBtddefI
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from tkinter import *
from time import sleep
from functools import partial
import threading
import smtplib
import socket
import os

#Email variables
email = ''#PUT YOUR EMAIL DEFAULTS HERE
password = ''
send_to_email = ''
subject = 'ALERT'
message = 'Motion Detected At Pi'
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

#socket variables
host = ''
port = 5560

#GUI variables
closeVar = True
closeTabVar = False
sendMail = False

#Other global variables
t1 = 'firefox.exe'
COMBINATIONS = [
    {keyboard.Key.ctrl_l, keyboard.Key.alt_l,keyboard.KeyCode(char='w')},
    {keyboard.Key.ctrl_l, keyboard.Key.alt_l,keyboard.KeyCode(char='W')}
]
current = set()
k = keyboard.Controller()

#GUI thread
class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def hide(self, event):
        self.root.withdraw()

    def see(self):
        self.root.deiconify()

    def kill(self, *args):
        kill()
        self.root.quit()

    def program(self, event, arg):#Sets program to close
        global t1
        t1 = arg.get()
        arg.config(bg = 'light green')
        self.root.update()
        sleep(.1)
        arg.config(bg = 'light gray')
    
    def email(self, event, arg):#should program send email
        if arg['text'] == 'OFF':
            arg['text'] = 'ON'
        else:
            arg['text'] = 'OFF'
        global sendMail
        sendMail = not sendMail
        
    def close(self, event, arg):#should program close program
        if arg['text'] == 'OFF':
            arg['text'] = 'ON'
        else:
            arg['text'] = 'OFF'
        global closeVar
        closeVar = not closeVar

    def closeT(self, event, arg):#should program close tab
        if arg['text'] == 'OFF':
            arg['text'] = 'ON'
        else:
            arg['text'] = 'OFF'
        global closeTabVar
        closeTabVar = not closeTabVar

    def setEmail(self, event, arg, arg2, arg3):#set email credentials 
        global email
        email = arg.get()
        global password
        password = arg2.get()
        global send_to_email
        send_to_email = arg3.get()
        arg.config(bg = 'light green')
        arg2.config(bg = 'light green')
        arg3.config(bg = 'light green')
        self.root.update()
        sleep(.1)
        arg.config(bg = 'light gray')
        arg2.config(bg = 'light gray')
        arg3.config(bg = 'light gray')


    def setInfoBox(self,text,):#set the user output text
        self.infoBox['text'] = text
        
    
    def run(self):
        #setup all the components
        self.root = Tk()
        self.root.title('Auto Close')
        self.root.protocol('WM_DELETE_WINDOW', self.kill)

        serverKill = Label(self.root, text='Server Kill')
        serverKill.grid(row=0, column=0)
        serverKill.bind('<Button-1>', self.kill)

        hideB = Label(self.root, text='Hide')
        hideB.grid(row=0, column=1)
        hideB.bind('<Button-1>', self.hide)

        entryText = StringVar()
        entry = Entry(self.root, textvariable=entryText, bg='light gray')
        entryText.set('firefox.exe')
        entry.grid(row=1, column=1)

        programB = Label(self.root, text='Program Name')
        programB.grid(row=1, column=0, sticky=E)
        programB.bind('<Button-1>', lambda event, arg=entry: self.program(event, arg))

        emailStatus = Label(self.root, text='OFF')
        emailStatus.grid(row=2, column=1)

        sendEmail = Label(self.root, text='Send Email?')
        sendEmail.grid(row=2, column=0, sticky=E)
        sendEmail.bind('<Button-1>', lambda event, arg=emailStatus: self.email(event, arg))

        programStatus = Label(self.root, text='ON')
        programStatus.grid(row=3, column=1)
        
        closeProgram = Label(self.root, text='Close Program?')
        closeProgram.grid(row=3, column=0, sticky=E)
        closeProgram.bind('<Button-1>', lambda event, arg=programStatus: self.close(event, arg))

        tabStatus = Label(self.root, text='OFF')
        tabStatus.grid(row=4, column=1)
        
        closeTab = Label(self.root, text='Close Tab?')
        closeTab.grid(row=4, column=0, sticky=E)
        closeTab.bind('<Button-1>', lambda event, arg=tabStatus: self.closeT(event, arg))

        logintxt = StringVar()
        login = Entry(self.root, textvariable=logintxt, bg='light gray')
        logintxt.set('SENDING EMAIL')#PUT YOUR DEFAULT EMAIL HERE
        login.grid(row=5, column=0)

        passtxt = StringVar()
        password = Entry(self.root, textvariable=passtxt, bg='light gray', show='*')
        passtxt.set('SENDING PASSWORD')#PUT DEFAULT EMAIL'S PASSWORD HERE
        password.grid(row=5, column=1)

        sendtotxt = StringVar()
        sendto = Entry(self.root, textvariable=sendtotxt, bg='light gray')
        sendtotxt.set('RECEIVING EMAIL')#PUT DEFAULT RECEIVING EMAIL HERE
        sendto.grid(row=6, column=0)

        setCredentials = Label(self.root, text='Set Credentials')
        setCredentials.grid(row=6, column=1)
        setCredentials.bind('<Button-1>', lambda event, arg=login, arg2=password, arg3=sendto: self.setEmail(event, arg, arg2, arg3))

        self.infoBox = Label(self.root, text='Server Started')
        self.infoBox.grid(columnspan=2)
        
        self.root.mainloop()



#Hotkey funcions

def execute():
    gui.see()

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

class mythread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

thread1 = mythread()
thread1.start()


#Gui functions
def kill():
    s.close()

#socket functions

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except socket.error as msg:
        success = msg
    return s

def setupConnection():
    s.listen(1)#allow one person at a time
    conn, address = s.accept()
    gui.setInfoBox('Connected to: ' + address[0] + ':' + str(address[1]))
    return conn

def closeFile():
    try:
        os.system('TASKKILL /F /IM ' + t1)
    except Exception:
        gui.setInfoBox(Exception)

def pressCommand():#this command closes one tab using CTRL + W you can use this if you prefer it
    k.press(keyboard.Key.ctrl_l)
    #k.press(keyboard.Key.shift_l) #uncomment this if you want to close the whole window on motion
    k.press('w')
    k.release(keyboard.Key.ctrl_l)
    #k.release(keyboard.Key.shift_l)
    k.release('w')

def sendEmail():
    if email != '' and password != '' and send_to_email != '':
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()

def dataTransfer(conn):
    #loop that sends recieves data until told not to
    while True:
        #receive the data
        data = conn.recv(1024)
        data = data.decode('utf-8')
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'EXIT':
            break
        elif command == 'KILL':
            gui.setInfoBox('Our server is shutting down')
            s.close()
            break
        elif command == 'DETECTED':
            gui.setInfoBox('Motion was detected at client')
            if closeVar:
                closeFile()
            if closeTabVar:
                pressCommand()
            if sendMail:
                sendEmail()
            reply = 'WORKED'
        else:
            reply = 'Unknown Command'
        #send the reply
        conn.sendall(str.encode(reply))
        gui.setInfoBox('Data has been sent!')
    conn.close()

gui = GUI()#start up the GUI

s = setupServer()
    
while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break
