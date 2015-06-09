import socket,time,string

class IRCBot:
    def __init__(self,server,port,channel,user,password):
        self.server = server
        self.port = port
        self.channel = channel
        self.user = user
        self.password = password
        self.connectedUsers = []
        self.irc = None
        self.lastPing = 0

    def __reconnect(self):
        attempt = 0
        self.irc = None
        while not self.irc:
            if attempt > 0:
                time.sleep(10)
                print("{}: Connection failed...trying again in 10 seconds.".format(attempt))
            self.__connect()
            attempt += 1
            
    def __connect(self):
        self.connectedUsers = []
        self.irc = None
        irc = None
        
        try:
            irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            irc.connect((self.server,self.port))
            print("Connected to {}".format(self.server))
        except:
            irc = None

        self.irc = irc
        if self.irc:
            self.lastPing = time.clock()
            self.sendMessage('pass {}\r\n'.format(self.password))
            self.sendMessage('nick {}\r\n'.format(self.user))
            self.sendMessage('user {}\r\n'.format(self.user))
            self.sendMessage('join {}\r\n'.format(self.channel))

            print("Joined channel {}".format(self.channel))

    def __onRun(self):
        pass

    def run(self):
        self.__onRun()
        self.__reconnect()
        while True:
            data = ''
            try:
                data = self.irc.recv(2048)
            except:
                self.__reconnect()
                continue

            if data == '':
                continue
            
            messages = data.split("\n")

            for message in messages[:-1]:
                self._parseMessage(message)

            currentTime = time.clock()
                
            if self.lastPing < currentTime - 120:
                self.sendMessage("PING\r\n")
                self.lastPing = currentTime
            

    def _onCommand(self,command):
        command = command.lower()
        if command == "ping":
            self.sendMessage("PONG tmi.twitch.tv\r\n")

    def _parseMessage(self,data):
        if data.startswith("PING"):
            self._onCommand("PING")
            
        if data.startswith(":") and not data.startswith(":jtv") and not data.startswith(":tmi.twitch.tv"):
            try:
                data = data.strip()
                strings = data.split(':')
            
                msg = ":".join(strings[2:])
                name = strings[1][0:strings[1].index('!')]

                strings = data.split(' ')
                command = strings[1].lower()
                
                if command == "privmsg":
                    self._onMessage(name, msg)
                elif command == "join":
                    self._onJoin(name)
                elif command == "part":
                    self._onPart(name)
            except:
                pass

    def _onJoin(self,name):
        pass
        #self.connectedUsers.append(name)
        
    def _onPart(self,name):
        #self.connectedUsers.remove(name)
        pass
    
    def _onMessage(self,name,message):
        print(message)

    def sendMessage(self,message):
        while True:
            try:
                self.irc.send(message)
                break
            except:
                self.__reconnect()

if __name__ == "__main__":
    x = IRCBot("irc.twitch.tv",6667,"xxxx","xxxx","xxxx")
    x.run()

    

