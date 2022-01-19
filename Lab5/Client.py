'''
Tom Ekshtein, Client side file of Lab 5.
'''

import threading
import socket
import os
import pickle


HOST = '127.0.0.1'
PORT = 5551

def Menu(choice,s):
    '''Main menu selection'''
    menuDict={
        1:lambda:sendToServer(choice,s),
        2:lambda:sendToServer(choice,s),
        3:lambda:sendToServer(choice,s),
        4:lambda:sendToServer(choice,s),
        5:lambda:quit(choice,s)
        }        
    switcher=menuDict.get(choice,lambda:"")
    switcher()
    
def sendToServer(choice,s):
    '''Sends user choice to the server'''
    choice=str(choice)
    data=[]
    data.append(choice)
    if choice=='2':
        newDir=input("Please input a new Directory to change to:\n")
        data.append(newDir)
    pickledData=pickle.dumps(data)
    s.send(pickledData) 
    fromServer = pickle.loads(s.recv(1024)) 
    print("\nFrom the Server:\n")
    if type(fromServer)==list:
        for i in fromServer:
            print(i)
    else:
        print(fromServer)

def quit(choice,s):
    '''Sends user choice to the server only when quit is selected.'''
    data=pickle.dumps([str(choice)])
    s.send(data)    
    raise SystemExit()

if __name__=="__main__":
    '''Main'''
    menuText=("\nMAIN MENU\n1) Get the current directory\n2) Change the current directory\n3) List all files in the current directory\n4) List all sub-directories\n5) Exit")
    s=socket.socket()
    s.connect((HOST, PORT))                 
    Menu(1,s)
    while True:
        try:
            print(f"Client connected to: {HOST} , Port: {PORT}")            
            print(menuText)
            choice=int(input("Select an option from the menu: "))
            Menu(choice,s)
        except ValueError:
            print("Please try a valid input 1-5")
    s.close()