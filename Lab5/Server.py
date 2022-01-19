'''
Tom Ekshtein, Server side file of lab 5
'''
import threading
import socket
import os
import pickle
import sys


HOST = "localhost"      
PORT = 5551
START_DIR=os.getcwd()
CLIENTS={}

def createThreads(timer,N):
    '''Creates and handles the socket for the server, as well as the threads for each client.'''
    oldN=N
    threadsAlive=[2 for i in range(0,N)]
    threadCount=0
    with socket.socket() as s:
        threads=[]        
        s.bind((HOST,PORT))      
        s.listen()
        
        while True:
            counter=0
            for t in threads:
                if t.is_alive()==False:
                    threadsAlive[counter]=0
                    counter+=1
            if threadsAlive==[0 for i in range(0,oldN)]:
                print("No more connections to the server, closing server.")
                raise SystemExit()
            try:
                if threadCount<N:
                    s.settimeout(timer)
                else:
                    s.settimeout(None)
                if threadCount<N:
                    (conn,addr)=s.accept()
                    s.settimeout(timer)
                    if conn:
                        try:
                            threadsAlive[threadCount]=1
                        except IndexError:
                            print("Maximum number of clients have already been made.\nClosing server...")
                            raise SystemExit()
                        threadCount+=1                    
                        t=threading.Thread(target=serverFunctions,args=(s,conn,START_DIR,threadCount,threadsAlive))
                        threads.append(t)
                        CLIENTS[threadCount]=START_DIR
                        t.setDaemon(True)
                        t.start()
                        counter=0
                        for t in threads:
                            if t.is_alive()==False:
                                threadsAlive[counter]=0
                            counter+=1
                            
                          
            except socket.timeout:
                print(f"Total active connections: {threadCount}\nNot accepting new connections")
                for i in range(len(threadsAlive)):
                    if threadsAlive[i]==2:
                        threadsAlive[i]=0
                N=threadCount
                if threadCount==0:
                    print("No connections made, closing server.")
                    raise SystemExit()
            
def serverFunctions(s,conn,cwd,threadCount,threadsAlive):
    '''Handles the actual processes of the lab. Takes the user choice and figures out what to do with it along with sending back the appropriate response to the client.'''
    looper=True
    
    while looper:
        fromClient = pickle.loads(conn.recv(1024))  
        
        if fromClient[0]=='1':
            one=CLIENTS[threadCount]
            pickledData=pickle.dumps(one)
            conn.send(pickledData)
            print(f"\nCWD of client #{threadCount} is {one}\n")
            
        elif fromClient[0]=='2':
            success="Success"
            notSuccess="New directory is not valid"
            try:
                os.chdir(fromClient[1])
                CLIENTS[threadCount]=fromClient[1]
                print(f"\nNew current directory for client #{threadCount} is: {CLIENTS[threadCount]}\n")
                pickledData=pickle.dumps(success)
                conn.send(pickledData)
            except:
                print("\nInvalid directory\n")
                pickledData=pickle.dumps(notSuccess)
                conn.send(pickledData)
        
        elif fromClient[0]=='3':
            data=(os.listdir(CLIENTS[threadCount]))
            print(f"\n{data}\n")
            pickledData=pickle.dumps(data)
            conn.send(pickledData)
        
        elif fromClient[0]=='4':
            data=[]
            for i in os.walk(CLIENTS[threadCount]):
                data.append(i)
            print()
            print(data)
            print()
            pickledData=pickle.dumps(data)
            conn.send(pickledData)
        
        elif fromClient[0]=='5':
            print(f"Client number {threadCount} has disconnected")       
            looper=False
        
            
if __name__=="__main__":
    '''Main'''
    invalid="Command Line Arguments invalid. Please use the format of max number of clients (1-5), timer time (3-120)"
    if len(sys.argv)!=3:
        print(invalid)
        raise SystemExit()
    if int(sys.argv[1])<1 or int(sys.argv[1])>5 or int(sys.argv[2])<3 or int(sys.argv[2])>120:
        print(invalid)
        raise SystemExit()
    print(f"Server is up. Hostname: {HOST} , Port {PORT}")    
    try:
        createThreads(int(sys.argv[2]),int(sys.argv[1]))
    except TypeError:
        print(invalid)
        raise SystemExit()