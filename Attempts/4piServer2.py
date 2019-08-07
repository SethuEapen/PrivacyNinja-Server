#Alexander Baran-Harper: https://www.youtube.com/watch?v=IZX7G77daG0

import socket
import os


host = ''
port = 5560


def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete")
    return s

def setupConnection():
    s.listen(1)#allow one person at a time
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def GET():
    reply = storedValue
    return reply

def REPEAT(dataMessage):
    reply = dataMessage[1]
    return reply

def closeFile():
    try:
        os.system('TASKKILL /F /IM firefox.exe')
    except Exception:
        print(Exception)

def dataTransfer(conn):
    #loop that sends recieves data until told not to
    while True:
        #receive the data
        data = conn.recv(1024)
        data = data.decode('utf-8')
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'GET':
            reply = GET()
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
        elif command == 'EXIT':
            print("Our client has left us :(")
            break
        elif command == 'KILL':
            print("Our server is shutting down")
            s.close()
            break
        elif command == 'DETECTED':
            print("Motion was detected at client")
            closeFile()
            reply = 'WORKED'
            
        else:
            reply = 'Unknown Command'
        #send the reply
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()


s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break
