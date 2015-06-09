from IRCBot import IRCBot
import time, re, win32api, win32con, win32gui, win32ui, ctypes, threading, json

class TwitchBot(IRCBot):
    def __init__(self,channel,user,password,keyFile,bannedWordFile):
        IRCBot.__init__(self,"irc.twitch.tv",6667,channel,user,password)
        self.totalInput = 0
        self.lastSave = time.clock()
        self.paused = False
        self.positionPattern = re.compile(r'[0-9]{1,3},[0-9]{1,3}')
        self.basePos = (0,0)
        self.bannedWords = []
        self.bannedWordFile = bannedWordFile
        self.keyFile = keyFile
        self.keyMap = dict()
        self.currentSaveSlot = 1
        self.allowTouching = False
        self.allowDragging = False
        self.inputDelay = 0.05
        self.onCommandCallback = None
        self.mods = []
        self.votes = dict()
        self.echoCommands = True
        self.defaultDemoTime = 10
        self.demoTime = self.defaultDemoTime
        self.currentScene = -1
        self.votesLock = threading.RLock()
        self.commands = dict()
        
        self.loadKeyMap(keyFile)
        
        
        if bannedWordFile:
            self.loadBannedWords(bannedWordFile)

    def _onRun(self):
        t = threading.Timer(self.defaultDemoTime,self._processCommand)
        t.daemon = True
        t.start()

        t = threading.Timer(1,self._getCurrentScene)
        t.daemon = True
        t.start()

    def _getCurrentScene(self):
        try:
            with open("currentscene.txt","r") as f:
                s = int(f.readline().strip())
                if s != self.currentScene:
                    dt = self.commands.get(str(s))
                    if dt:
                        dt = dt.get("demoTime")
                        if dt:
                            self.demoTime = dt
                        else:
                            self.demoTime = self.defaultDemoTime
                    self.currentScene = s
                    self.votesLock.acquire()
                    self.votes = dict()
                    self.votesLock.release()
        except:
            raise
            self.currentScene = -1

        t = threading.Timer(1,self._getCurrentScene)
        t.daemon = True
        t.start()

    def __getWinningCommand(self):
        winning = ""
        numVotes = -1
        self.votesLock.acquire()
        for key,value in self.votes.iteritems():
            if value > numVotes:
                numVotes = value
                winning = key
        self.votesLock.release()
        return winning
        
    def _processCommand(self):
        winningCommand = self.__getWinningCommand()
        self.votesLock.acquire()
        self.votes = dict()
        self.votesLock.release()

        if not self.paused:
            if winningCommand == "":
                print("No Command")
            else:
                print(winningCommand)
                x = self.commands.get(str(self.currentScene))
                if x:
                    x = x.get(winningCommand)
                    if x:
                        if self.echoCommands:
                            self.sendMessage("PRIVMSG {0} :=={1}==\r\n".format(self.channel,winningCommand))
                        if len(x) == 2:
                            self.sendMouseClick(0,x[0],x[1])
                        elif len(x) == 4:
                            self.sendMouseDrag(0,x[0],x[1],x[2],x[3])

                        self.moveMouse(50,100)

        
        t = threading.Timer(self.demoTime,self._processCommand)
        t.daemon = True
        t.start()

    def __isCommandValid(self,command):
        commands = self.commands.get(str(self.currentScene))
        if commands:
            if commands.get(command):
                return True
        return False

    def _onMessage(self,name,message):
        currentTime = time.clock()
        
        msg = message.lower()
        name = name.lower()

        if name == 'trakof':
            if msg == '!pause':
                self.paused = True
            elif msg == '!unpause':
                self.paused = False
            elif msg == '!pong':
                print("\t\t\t\t\t\tping")
            elif msg == '!reload':
                print("\t\t\t\t\t\treloading")
                self.votesLock.acquire()
                self.votes = dict()
                self.votesLock.release()
                self.loadKeyMap(self.keyFile)
                
                if self.bannedWordFile:
                    self.loadBannedWords(self.bannedWordFile)
            elif msg == '!echoon':
                self.echoCommands = True
            elif msg == '!echooff':
                self.echoCommands = False

        if name in self.mods:
            if msg[0] == '!':
                if msg.startswith("!"):
                    if self.onCommandCallback:
                        self.onCommandCallback(msg)

        
        
        for word in self.bannedWords:
            if word in msg:
                #print("\t\t\t\t\t\tban {0}".format(name))
                self.sendMessage("PRIVMSG {0} :.ban {1}\r\n".format(self.channel,name))
                return

        if self.__isCommandValid(msg):
            self.votesLock.acquire()
            numVotes = self.votes.get(msg)
            if numVotes:
                numVotes += 1
                self.votes[msg] = numVotes
            else:
                self.votes[msg] = 1
            self.votesLock.release()

    def loadKeyMap(self,filename):
        try:
            self.keyMap = dict()
            with open(filename,"r") as f:
                self.commands = json.load(f)
            x = self.commands.get(self.currentScene)
            if x:
                x = x.get("demoTime")
                if x:
                    self.demoTime = x
                else:
                    self.demoTime = self.defaultDemoTime
        except:
            print("Error loading key map.")
            
    def loadBannedWords(self, filename):
        try:
            with open(filename,"r") as words:
                banned = words.readlines()
                banned = [word.strip("\r\n") for word in banned]
                self.bannedWords = banned
        except:
            print("Error loading banned words.")

    def sendKeyboardInput(self,keys):
        #sendKeys(keys,pause=self.inputDelay)
        pass

    def moveMouse(self,x,y):
        ctypes.windll.user32.SetCursorPos(x,y)
        time.sleep(0.05)
        
    def sendMouseClick(self, button, x, y):
        x += self.basePos[0]
        y += self.basePos[1]
        
        LEFT_DOWN = 0x2
        LEFT_UP = 0x4
        RIGHT_DOWN = 0x8
        RIGHT_UP = 0x10
        MIDDLE_DOWN = 0x20
        MIDDLE_UP = 0x40

        pos = win32gui.GetCursorPos()

        ctypes.windll.user32.SetCursorPos(x,y)

        time.sleep(.1)
        
        if button == 0:
            ctypes.windll.user32.mouse_event(LEFT_DOWN,0,0,0,0)
            time.sleep(0.1)
            ctypes.windll.user32.mouse_event(LEFT_UP,0,0,0,0)
        if button == 1:
            ctypes.windll.user32.mouse_event(RIGHT_DOWN,0,0,0,0)
            time.sleep(0.1)
            ctypes.windll.user32.mouse_event(RIGHT_UP,0,0,0,0)
        if button == 2:
            ctypes.windll.user32.mouse_event(MIDDLE_DOWN,0,0,0,0)
            time.sleep(0.1)
            ctypes.windll.user32.mouse_event(MIDDLE_UP,0,0,0,0)

        time.sleep(.1)

    def sendMouseDrag(self, button, x1, y1, x2, y2):
        x1 += self.basePos[0]
        y1 += self.basePos[1]
        x2 += self.basePos[0]
        y2 += self.basePos[1]
        
        LEFT_DOWN = 0x2
        LEFT_UP = 0x4
        RIGHT_DOWN = 0x8
        RIGHT_UP = 0x10
        MIDDLE_DOWN = 0x20
        MIDDLE_UP = 0x40

        pos = win32gui.GetCursorPos()

        ctypes.windll.user32.SetCursorPos(x1,y1)

        time.sleep(.1)
        
        if button == 0:
            ctypes.windll.user32.mouse_event(LEFT_DOWN,0,0,0,0)
        if button == 1:
            ctypes.windll.user32.mouse_event(RIGHT_DOWN,0,0,0,0)
        if button == 2:
            ctypes.windll.user32.mouse_event(MIDDLE_DOWN,0,0,0,0)

        time.sleep(0.1)
        ctypes.windll.user32.SetCursorPos(x2,y2)
        time.sleep(0.1)

        if button == 0:
            ctypes.windll.user32.mouse_event(LEFT_UP,0,0,0,0)
        if button == 1:
            ctypes.windll.user32.mouse_event(RIGHT_UP,0,0,0,0)
        if button == 2:
            ctypes.windll.user32.mouse_event(MIDDLE_UP,0,0,0,0)

        time.sleep(.1)

        
if __name__ == "__main__":
    channel = "xxxx"
    username = "xxxx"
    password = "xxxx"
    keyFile = "commands.txt"
    bannedWordFile = "bannedwords.txt"

    x = TwitchBot(channel,username,password,keyFile,bannedWordFile)
    x.run()
