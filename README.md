# Mr.Kitty

```
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

        
        What's new in v1.0.1?
        + Solved sending and receiving issues with the buffer
        + Changed the way the payload uses 
        - The obfuscation and creating process doesn't work yet, will solve this issue in the next versions (need to research on PyInstaller and pyArmor)
```

# How do you use it?

```python
#for launching the server and listening to the incoming connections
python mainKitty.py --run

#for launching the client side
python kittyPayload.py
```

# Requirements

A future requirement is pyarmor.
For now, I only used built-in Python modules.
Python version is Python 3.9.6.

