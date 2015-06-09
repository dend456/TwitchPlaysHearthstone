import string

playerY = 570
enemyY = 400

playerHeroY = 800
enemyHeroY = 200

heropowerX = 1093
heropowerY = 786

xs = [[930],
      [870,1000],
      [800,930,1060],
      [740,870,1000,1130],
      [670,800,930,1060,1190],
      [610,740,870,1000,1130,1260],
      [540,670,800,930,1060,1190,1320]]

cardXs = [[900],
          [830,975],
          [770,900,1025],
          [700,800,975,1100],
          [700,800,900,1000,1100],
          [670,765,850,935,1025,1100],
          [670,740,815,885,960,1030,1120],
          [640,725,780,835,915,960,1030,1130],
          [625,700,750,800,865,915,960,1025,1120],
          [620,690,730,785,825,885,940,985,1035,1110]]
cardY = 1000
middleX = 930
middleY = 500

with open("selectcommands.txt","w") as f:
    f.write("\t\t\"select a\": [{},{}],\r\n".format(middleX,playerHeroY))
    f.write("\t\t\"select e\": [{},{}],\r\n".format(middleX,enemyHeroY))
    for playerNumCards in range(0,7):
        for playerCard in range(0,playerNumCards+1):
            px = xs[playerNumCards][playerCard]
            py = playerY
            ey = enemyY
            f.write("\t\t\"select {},{} a\": [{},{}],\r\n".format(playerNumCards+1,playerCard+1,px,py))
            f.write("\t\t\"select {},{} e\": [{},{}],\r\n".format(playerNumCards+1,playerCard+1,px,ey))

with open("heroattacks.txt","w") as f:
    f.write("\t\t\"heroattack\": [{},{},{},{}],\r\n".format(middleX,playerHeroY,middleX,enemyHeroY))
    for playerNumCards in range(0,7):
        for playerCard in range(0,playerNumCards+1):
            x = xs[playerNumCards][playerCard]
            y = enemyY
            f.write("\t\t\"heroattack {},{}\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,middleX,playerHeroY,x,y))

with open("usecommands.txt","w") as f:
    for playerNumCards in range(0,10):
        for playerCard in range(0,playerNumCards+1):
            x1 = cardXs[playerNumCards][playerCard]
            y1 = cardY
            x2 = middleX
            y2 = enemyHeroY
            f.write("\t\t\"use {},{} e\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,x1,y1,x2,y2))
            y2 = playerHeroY
            f.write("\t\t\"use {},{} a\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,x1,y1,x2,y2))
    
    for playerNumCards in range(0,10):
        for playerCard in range(0,playerNumCards+1):
            x = cardXs[playerNumCards][playerCard]
            y = cardY
            f.write("\t\t\"use {},{}\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,x,y,middleX,middleY))

    
    for playerNumCards in range(0,10):
        for selectedCard in range(0,playerNumCards+1):
            for cardsOnBoard in range(0,7):
                for selectedCardOnBoard in range(0,cardsOnBoard+1):
                    x1 = cardXs[playerNumCards][selectedCard]
                    y1 = cardY
                    x2 = xs[cardsOnBoard][selectedCardOnBoard]
                    y2 = playerY
                    f.write("\t\t\"use {},{} {},{} a\": [{},{},{},{}],\r\n".format(playerNumCards+1,selectedCard+1,cardsOnBoard+1,selectedCardOnBoard+1,x1,y1,x2,y2))
                    y2 = enemyY
                    f.write("\t\t\"use {},{} {},{} e\": [{},{},{},{}],\r\n".format(playerNumCards+1,selectedCard+1,cardsOnBoard+1,selectedCardOnBoard+1,x1,y1,x2,y2))
            
    

with open("heropowercommands.txt","w") as f:
    for playerNumCards in range(0,7):
        for playerCard in range(0,playerNumCards+1):
            f.write("\t\t\"heropower {},{} a\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,heropowerX,heropowerY,xs[playerNumCards][playerCard],playerY))
            f.write("\t\t\"heropower {},{} e\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,heropowerX,heropowerY,xs[playerNumCards][playerCard],enemyY))
            

with open("attackcommands.txt","w") as f:
    for playerNumCards in range(0,7):
        for enemyNumCards in range(0,7):
            for enemyCard in range(0,enemyNumCards+1):
                for playerCard in range(0,playerNumCards+1):
                    px = xs[playerNumCards][playerCard]
                    py = playerY
                    ex = xs[enemyNumCards][enemyCard]
                    ey = enemyY
                    f.write("\t\t\"attack {},{} {},{}\": [{},{},{},{}],\r\n".format(playerNumCards+1,playerCard+1,enemyNumCards+1,enemyCard+1,px,py,ex,ey))
