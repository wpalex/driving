import operator
import numpy as np
import statistics
import matplotlib.pyplot as plt
from colour import Color
from bs4 import BeautifulSoup
import urllib3
from re import sub
from matplotlib.patches import Polygon

###############    ACCESS WEBPAGES       ####################
def makeSoup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soupdata = BeautifulSoup(response.data)
    return soupdata

siteURL = []
for i in range(10):
    siteURL.append(i)
siteURL[0] = ''
siteURL[1] = 'https://www.pgatour.com/stats/stat.02405.html'   #spin rate
siteURL[2] = 'https://www.pgatour.com/stats/stat.02404.html'   #launch angle
siteURL[3] = 'https://www.pgatour.com/stats/stat.02401.html'   #clubhead speed
siteURL[4] = 'https://www.pgatour.com/stats/stat.02402.html'   #ball speed
siteURL[5] = 'https://www.pgatour.com/stats/stat.101.html'   #driving distance
siteURL[6] = 'https://www.pgatour.com/stats/stat.460.html' #right rough tend
siteURL[7] = 'https://www.pgatour.com/stats/stat.459.html' #left rough tend
siteURL[8] = 'https://www.pgatour.com/stats/stat.02423.html' #right tend
siteURL[9] = 'https://www.pgatour.com/stats/stat.02422.html' #left tend

###############    ACCESS TABLE DATA      ###################
def row_number(soupdata):
    for row in table.findAll('tr'):
        tot_row = row
    return tot_row

def parse_table(soupdata):
    playerName = []
    aveg = []
    table = soupdata.find('tbody')
    tot_row = 0
    for row in table.findAll('tr'):
        #for col in row.findAll('td'):
        col = row.find_all('td')
        #column_1 = col[0]
        #currRank.append(column_1)
        #column_2 = col[1]
        #prevRank.append(column_2)
        column_3 = col[2].text
        column_3.strip()
        playerName.append(column_3)
        #column_4 = col[3]
        #rounds.append(column_4) 
        column_5 = col[4].text
        aveg.append(column_5)            
        #column_6 = col[5]
        #attempts.append(column_6)    
        #column_7 = col[6]
        #puttsMade.append(column_7)
        tot_row += 1
    #return currRank, prevRank, playerName, rounds, pctMake, attempts, puttsMade
    return playerName, aveg, tot_row

###############    CLASS DEFINITION      ###################
class Player(object):
    id_list={}
    def __init__(self,name, id, spin=0.0, launch=0.0, CHspeed=0.0, Bspeed=0.0, dis=0.0, RRtend=0.0,LRtend=0.0,Rtend=0.0,Ltend=0.0):
        self.name = name
        self.spin = spin
        self.launch = launch
        self.CHspeed = CHspeed
        self.Bspeed = Bspeed
        self.dis = dis
        self.RRtend = RRtend
        self.LRtend = LRtend
        self.Rtend = Rtend
        self.Ltend = Ltend
        self.id = id
        Player.id_list[self.name] = self # save the id as key and self as he value
    def __repr__(self):
        return '({},{},{})'.format(self.name, self.spin, self.launch)
    def addSpin(self,spin):
        self.spin = str(spin)
        self.spin = float((self.spin).replace(',',''))
    def addLaunch(self,launch):
        self.launch = float(launch)
    def addCHspeed(self,CHspeed):
        self.CHspeed = float(CHspeed)
    def addBspeed(self,Bspeed):
        self.Bspeed = float(Bspeed)
    def addDis(self,dis):
        self.dis = float(dis)
    def addRRtend(self,RRtend):
        self.RRtend = float(RRtend)
    def addLRtend(self,LRtend):
        self.LRtend = float(LRtend)
    def addRtend(self,Rtend):
        self.Rtend = float(Rtend) - self.RRtend
    def addLtend(self,Ltend):
        self.Ltend = float(Ltend) - self.LRtend
    def __cmp__(self, other):
        if hasattr(other, 'name'):
            return self.number.__cmp__(other.name)
        
    @classmethod
    def lookup_player_name_by_id(cls, name):
        try:
            return cls.id_list[name] # return the instance with the id 
        except KeyError: # error check for if id does not exist
            raise KeyError("No user with id %s" % str(id))

###############    DATA POPULATION      ###################
PlayerNumber=[]
soupdata = makeSoup(siteURL[1])
playerName, pctMake, tot_row = parse_table(soupdata)
for i in range(0,tot_row):
    PlayerNumber.append(i)
for i in range(1,10):
    soupdata = makeSoup(siteURL[i])
    playerName, aveg, tot_row = parse_table(soupdata)
    for x in range(0,tot_row):
        #PlayerNumber.append(x)
        name = playerName[x]
        name = name.replace("\xa0", " ")
        name = name.replace("\n", "")
        if i == 1:
            PlayerNumber[x] = Player(name, x)
            Player.addSpin(PlayerNumber[x],aveg[x])
        if i == 2:
            val = Player.lookup_player_name_by_id(name)
            Player.addLaunch(PlayerNumber[val.id],aveg[x])
        if i == 3:
            val = Player.lookup_player_name_by_id(name)
            Player.addCHspeed(PlayerNumber[val.id],aveg[x])
        if i == 4:
            val = Player.lookup_player_name_by_id(name)
            Player.addBspeed(PlayerNumber[val.id],aveg[x])
        if i == 5:
            val = Player.lookup_player_name_by_id(name)
            Player.addDis(PlayerNumber[val.id],aveg[x])
        if i == 6:
            val = Player.lookup_player_name_by_id(name)
            Player.addRRtend(PlayerNumber[val.id],aveg[x])
        if i == 7:
            val = Player.lookup_player_name_by_id(name)
            Player.addLRtend(PlayerNumber[val.id],aveg[x])
        if i == 8:
            val = Player.lookup_player_name_by_id(name)
            Player.addRtend(PlayerNumber[val.id],aveg[x])
        if i == 9:
            val = Player.lookup_player_name_by_id(name)
            Player.addLtend(PlayerNumber[val.id],aveg[x])

PlayerNumber.sort(key = operator.attrgetter('name'))

#####################     AVERAGES     #################################
def avg(distance):
    average = sum(distance)/float(len(PlayerNumber))
    return average

avgD1 = avg(float(name.spin) for name in PlayerNumber)
avgD2 = avg(float(name.launch) for name in PlayerNumber)
avgD3 = avg(float(name.CHspeed) for name in PlayerNumber)
avgD4 = avg(float(name.Bspeed) for name in PlayerNumber)
avgD5 = avg(float(name.dis) for name in PlayerNumber)
avgD6 = avg(float(name.RRtend) for name in PlayerNumber)
avgD7 = avg(float(name.LRtend) for name in PlayerNumber)
avgD8 = avg(float(name.Rtend) for name in PlayerNumber)
avgD9 = avg(float(name.Ltend) for name in PlayerNumber)

#####################     STD DEVS     #################################
stdD1=statistics.stdev(float(name.spin) for name in PlayerNumber)
stdD2=statistics.stdev(float(name.launch) for name in PlayerNumber)
stdD3=statistics.stdev(float(name.CHspeed) for name in PlayerNumber)
stdD4=statistics.stdev(float(name.Bspeed) for name in PlayerNumber)
stdD5=statistics.stdev(float(name.dis) for name in PlayerNumber)
stdD6=statistics.stdev(float(name.RRtend) for name in PlayerNumber)
stdD7=statistics.stdev(float(name.LRtend) for name in PlayerNumber) 
stdD8=statistics.stdev(float(name.Rtend) for name in PlayerNumber) 
stdD9=statistics.stdev(float(name.Ltend) for name in PlayerNumber) 

##################   COLOR INITIALIZATION     #########################
blue = Color("blue")
colors = list(blue.range_to(Color("red"),40))

###############     PLAYER SELECTION INPUT    ########################
try:
    playerName_input=str(input('Player Name: '))
except ValueError:
    print("Not a string")
for pos in range(0,tot_row):
    if playerName_input == PlayerNumber[pos].name:
        player_input = pos
        golfer = PlayerNumber[pos].name
        
#################     COLOR GRADIENT CALC     #############################
def color_grad(distance, avg, std):
    color_loc = 0
    Dcolor = 0
    dtD = 0
    for grad in range(-20,20):
        if distance < (avg + (grad/10.0)*std) and Dcolor == 0:
            Dcolor = colors[color_loc]
            dtD = distance - avg
        if grad == 19 and Dcolor == 0:
            Dcolor = colors[color_loc]
            dtD = distance - avg
        color_loc += 1
    return Dcolor, dtD

Dcolor, dtD = color_grad(PlayerNumber[player_input].dis, avgD5, stdD5)
#################     COLOR TRANSPARENCY CALC     ###########################
def color_transp(percent):
    Alphacolor = percent/100.0
    return Alphacolor

AlphaRRtend = color_transp(PlayerNumber[player_input].RRtend)
AlphaLRtend = color_transp(PlayerNumber[player_input].LRtend)
AlphaRtend = color_transp(PlayerNumber[player_input].Rtend)
AlphaLtend = color_transp(PlayerNumber[player_input].Ltend)

#################     SET AXES     #############################
bottom_limit = 220
top_limit = 330
fairway_width = 40

ax = plt.subplot(111)
ax.set_aspect('equal')
ax.set_xlim((-40, 40))
ax.set_ylim((bottom_limit, top_limit))

#FAIRWAY
ax.add_patch(Polygon([((-fairway_width/2), bottom_limit), ((fairway_width/2),bottom_limit), ((fairway_width/2), top_limit), ((-fairway_width/2),top_limit)],
                       closed=True, facecolor='forestgreen', alpha=0.25))
#LEFT ROUGH
ax.add_patch(Polygon([(-40, bottom_limit), ((-fairway_width/2),bottom_limit), ((-fairway_width/2), top_limit), ((-40),top_limit)],
                       closed=True, facecolor='forestgreen', alpha=0.25))
#RIGHT ROUGH
ax.add_patch(Polygon([(40, bottom_limit), ((fairway_width/2),bottom_limit), ((fairway_width/2), top_limit), (40,top_limit)],
                       closed=True, facecolor='forestgreen', alpha=0.25))

centre_fairway = np.linspace(0, 0, 1000, endpoint=False)
right_fairway = np.linspace(fairway_width/2,fairway_width/2,1000,endpoint=False)
left_fairway = np.linspace(-fairway_width/2,-fairway_width/2,1000,endpoint=False)
fairway_edge = np.linspace(bottom_limit, top_limit, 1000, endpoint=False)
ax.plot(left_fairway,fairway_edge,color = 'forestgreen')
ax.plot(right_fairway,fairway_edge,color='forestgreen')

max_dis = PlayerNumber[player_input].dis

#RIGHT FAIRWAY TEND
ax.add_patch(Polygon([(0, bottom_limit), ((fairway_width/2),max_dis), (0,max_dis)],
                       closed=True, facecolor=str(Dcolor), alpha=AlphaRtend))
#LEFT FAIRWAY TEND
ax.add_patch(Polygon([(0, bottom_limit), ((-fairway_width/2),max_dis), (0, max_dis)],
                       closed=True, facecolor=str(Dcolor), alpha=AlphaLtend))
#RIGHT ROUGH TEND
ax.add_patch(Polygon([(0, bottom_limit), ((fairway_width/2+20),max_dis), (0, max_dis)],
                       closed=True, facecolor=str(Dcolor), alpha=AlphaRRtend))
#LEFT ROUGH TEND
ax.add_patch(Polygon([(0, bottom_limit), ((-fairway_width/2-20),max_dis), (0,max_dis)],
                       closed=True, facecolor=str(Dcolor), alpha=AlphaLRtend))

cross_image = np.linspace(-40,40,1000,endpoint=False)
average_dis = np.linspace(avgD5,avgD5,1000,endpoint=False)
stdevPlus1_dis = np.linspace(avgD5+stdD5,avgD5+stdD5,1000,endpoint=False)
stdevMinus1_dis = np.linspace(avgD5-stdD5,avgD5-stdD5,1000,endpoint=False)
ax.plot(cross_image, average_dis, color='black')
ax.plot(cross_image, stdevPlus1_dis, color='black')
ax.plot(cross_image, stdevMinus1_dis, color='black')

fig = plt.gcf()
fig.set_size_inches(20, 20)
plt.rcParams.update({'font.size': 24})

plt.title("Driving Data for " + golfer)
ax.text(-38,int(round(avgD5))+2, u"\u03BC" + ": " + "{0:.1f}".format(avgD5) + ' YDS', color='black',fontsize=16)
ax.text(-38,int(round(avgD5-stdD5))+2, u"\u03BC" + "-" + u"\u03C3" + ": " + "{0:.1f}".format(avgD5-stdD5) + ' YDS', color='black',fontsize=16)
ax.text(-38,int(round(avgD5+stdD5))+2, u"\u03BC" + "+" + u"\u03C3" + ": " + "{0:.1f}".format(avgD5+stdD5) + ' YDS', color='black',fontsize=16)

ax.text(15,bottom_limit+5, 'Player Value vs PGA Tour Avg\n' + 
        'Spin: ' + "{0:.1f}".format(PlayerNumber[player_input].spin) + ' rpm' +'\n'
        'Avg: ' + "{0:.1f}".format(avgD1) + ' rpm' +'\n'
        'Launch Angle: ' + "{0:.1f}".format(PlayerNumber[player_input].launch) + ' deg' +'\n'
        'Avg: ' + "{0:.1f}".format(avgD2) + ' deg' +'\n'
        'Clubhead Speed: ' + "{0:.1f}".format(PlayerNumber[player_input].CHspeed) + ' mph' + '\n'
        'Avg: ' + "{0:.1f}".format(avgD3) + ' mph' +'\n'
        'Ball Speed: ' + "{0:.1f}".format(PlayerNumber[player_input].Bspeed) + ' mph' + '\n'
        'Avg: ' + "{0:.1f}".format(avgD4) + ' mph',
        bbox={'facecolor':'white'},fontsize=16)

plt.savefig('/Users/Will/Desktop/Driving Data for ' + golfer + '.png')
plt.show()