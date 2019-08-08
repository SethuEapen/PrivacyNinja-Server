<h1 align="center">AutoClose</h1>

<p align="center">
  <img src="https://user-images.githubusercontent.com/31808277/62737974-fa547880-b9e5-11e9-9794-0d9b6940ab62.JPG">
</p>

AutoClose is a program that provides safety and privacy from your parents, boss, or anyone else who you do not want walking in on you. AutoClose uses network sockets to communicate with a raspberry pi wirelessly. When motion is detected by the RPi you can chose whether to close a program (i.e. browser, game), close a tab or window via the commands ctrl + w and ctrl + shift + w respectively, or send an alert email to your phone. the program can be completely hidden and exposed using the command ctrl + alt + w.

Please watch the [video]() before using AutoClose


## Getting Started

### Server Setup

You can download the exe and AutoClose will work properly, however using the email function will be quite difficult since the email credentials will need to be entered every time the program is run. To avoid this, you need to edit the AutoClose.py file

First you need to enter your email credentials inside the email, password, and send_to_email strings in the 'Email variables' section:
```
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

```
You should also put the same credentials as defaults for the entry boxes in the GUI:
```
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

```

Another way you can modify the script is to close a whole browser window instead of closing one tab when motion is detected by uncommenting the two lines in the pressCommand function:
```
def pressCommand():#this command closes one tab using CTRL + W you can use this if you prefer it
    k.press(keyboard.Key.ctrl_l)
    #k.press(keyboard.Key.shift_l) #uncomment this if you want to close the whole window on motion
    k.press('w')
    k.release(keyboard.Key.ctrl_l)
    #k.release(keyboard.Key.shift_l)
    k.release('w')
```

If you want to run AutoClose without a console you need to convert it to an exe file. Running as a .pyw file interferes with some of the email functions. To convert the .py file to .exe I recommend PyTutorial's tutorial [here](https://www.youtube.com/watch?v=lOIJIk_maO4) or a GUI version [here](https://www.youtube.com/watch?v=OZSZHmWSOeM). If you want to add the icon in my GitHub repository, I would recommend using the GUI version since I have had more success with that version. When you run the exe for the first time you may get a popup from your firewall saying that some features were blocked but this is just because the program uses sockets.

Finally, you need a way to SSH into your RPi. A Linux terminal emulator such as [Cygwin](https://www.cygwin.com/) can be used for this or an SSH program such as [putty](https://www.putty.org/). 

### Client Setup

The client setup is much easier. First, attach a PIR motion sensor to the GPIO pins 5v, GND, and 11. Next, open up the terminal and navigate to the directory you want to store the program. Next, enter the command:
```
git clone https://github.com/SethuEapen/AutoClose-Client.git
```

Next, open AutoClose-Client.py in your preferred text editor (i.e. NANO, IDLE, Mu_Code, Thonney). On your server computer open up CMD and run the command ipconfig to find your IPv4 address. Set the host string equal to the hosts IPv4 address:
```
import RPi.GPIO as GPIO

host = '#ENTER SERVER IP ADDRESS HERE'
port = 5560 #YOU CAN CHANGE PORT IF THIS ONE IS USED UP
```
After this you need to set up SSH on your RPi explained [here](https://www.raspberrypi.org/documentation/remote-access/ssh/)


## Program Startup

To startup the program, first start the server, enable the functions you want to do on motion, and set the program to close and the email credentials. Next, SSH into the RPi. If you don't know the IP address of your RPi you can use the command `ifconfig` or `hostname -I`. Once connected, navigate to the directory with AutoClose.py. Then enter the command `sudo python3 AutoClose-Client.py`. AutoClose should work now!
