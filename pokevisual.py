import random, pygame as pg
import time
pg.init()
clock = pg.time.Clock() 
background = pg.display.set_mode((1100,700)) 
grd = pg.image.load("images/battlegrd.png")
grd = pg.transform.scale(grd, (1100,800))
startgrd = pg.image.load("images/startgrd.jpg")
startgrd = pg.transform.scale(startgrd, (1100,700))
gold = (255,215,0)
time_=0.5
pg.display.update()

class pokemon:
    moveset = []
    def __init__(self, pokename, basestats, moveset, poketype, level, img, needflip = False):
        self.pokename = pokename  #name of pokemon
        self.basestats = basestats #base stats of pokemon {it is list of 6 items and index of each item refers to:
        #               HP[0], Attack[1], Defense[2], Special-Attack[3], Special-Defense[4], Speed[5]
        self.moveset = moveset # list of 4 moves of pokemon
        self.level = level #level of pokemon
        self.poketype = list(poketype) # type of pokemon , eg: fire, water, grass
        self.ivs = [random.randint(0, 31) for i in range(0,6)] # individual values of pokemon
        self.actualHP = int(((basestats[0] + self.ivs[0])*2 )*self.level/100 + 10 + self.level) # HP of pokemon according to its level
        # for actual stats, index = base_index - 1
        self.actualstats = [int(((basestats[i] + self.ivs[i])*2 )*self.level/100 + 5) for i in range(1,6)] #stats of pokemon according to its level
        self.img = pg.image.load("images/" + img) #loading image of pokemon 
        self.img = pg.transform.scale(self.img, (200,200))
        self.imgaddress = img
        self.needflip = needflip
        if needflip == True:
            self.img = pg.transform.flip(self.img, True, False)
    def copy(pkmn):
        return pokemon(pkmn.pokename, pkmn.basestats, pkmn.moveset, pkmn.poketype, pkmn.level, pkmn.imgaddress, pkmn.needflip)

class move:
    def __init__(self, movetype, accuracy, power, makecontact, movename, pp):
        self.movetype = movetype
        self.accuracy = accuracy
        self.power = power
        self.makecontact = makecontact # only true or false
        self.movename = movename
        self.pp = pp

    def if_hit(self):
        i = random.randint(0, 100)
        if i > self.accuracy:
            return False
        return True

grassimg = pg.image.load("images/grassatk.png")
grassimg = pg.transform.scale(grassimg, (200,200))
waterimg = pg.image.load("images/wateratk.png")
waterimg = pg.transform.scale(waterimg, (200,200))
fireimg = pg.image.load("images/fireatk.png")
fireimg = pg.transform.scale(fireimg, (200,200))
normalimg = pg.image.load("images/normal.png")
normalimg = pg.transform.scale(normalimg, (200,200))

def battle(attacker, defender, move_used, pos = "C"):
    trainer = {'P':'bot', 'C':'player'}
    moveimg = {'grass':grassimg, 'water':waterimg, 'fire':fireimg, "normal":normalimg}
    effective = 1
    dialogue(f"{trainer[pos]} is using {move_used.movename}")
    if pos == "P":
        background.blit(moveimg[move_used.movetype], (200, 150))
    else:
        background.blit(moveimg[move_used.movetype], (700, 150))
    clock.tick(time_)
    pg.display.update()
    typechart = {   # 'water' : {'strong':[], 'weak':[], 'resistance':[]},
        'fire' : {'strong':['grass'], 'weak':['water', 'fire'], 'resistance':[None]}, 
        'water' : {'strong':['fire'], 'weak':['water', 'grass'], 'resistance':[None]}, 
        'normal' : {'strong':[], 'weak':[], 'resistance':[None]},
        'grass' : {'strong':['water'], 'weak':['fire', 'grass'], 'resistance':[None]}
    }

    for i in defender.poketype:
        if i in typechart[move_used.movetype]['strong']:
            effective*=2
            dialogue("its super effective!!")
            clock.tick(time_)
            pg.display.update()
            time.sleep(1)
        elif i in typechart[move_used.movetype]['weak']:
            effective /= 2
            dialogue("its not very effective!!")
            clock.tick(time_)
            time.sleep(1)
            pg.display.update()
        elif i in typechart[move_used.movetype]['resistance']:
            effective *= 0

    if move_used.makecontact:
        damage = ((((2*attacker.level/5)+2)*move_used.power*attacker.actualstats[0]/defender.actualstats[1]) + 100)/50 
    else:
        damage = ((((2*attacker.level/5)+2)*move_used.power*attacker.actualstats[2]/defender.actualstats[3]) + 100)/50 

    for i in attacker.poketype:
        if i == move_used.movetype:
            damage *= 6/5

    if move_used.if_hit() == False:
        dialogue(f"{trainer[pos]} missed")
        clock.tick(time_)
        pg.display.update()
        time.sleep(1)
        return 0
    return int(damage)

scratch = move('normal', 100, 40, True, 'scratch', 10)

ember = move('fire', 100, 40, False, 'ember',4)
fireblast = move('fire', 50,120, False, 'fire blast', 1)
firefang = move('fire', 85, 75, True, 'fire fang', 2)

watergun = move('water', 100, 40, False, 'water gun',4)
hydropump = move('water', 50,120, False, 'hydro pump', 1)
aquatail = move('water' , 85, 75, True,'aqua tail', 2)

razorleaf = move('grass', 100, 40, False, 'razor leaf', 4)
solarbeam = move('grass', 50,120, False, 'solar beam', 1)
winevip = move('grass', 85, 75, True, 'wine vip', 2)

squrtle  = pokemon('squrtle', [144,48,65,50,64,43], [scratch, watergun, aquatail,hydropump], ['water'], 10, "squrtle.png",True)
charmainder = pokemon('charmainder', [143,52,43,60,50,65], [scratch, ember, firefang, fireblast], ['fire'], 10, "charmainder.png")
bulbasaur = pokemon('bulbasaur', [145,49,49,65,65,45], [scratch, razorleaf, winevip, solarbeam], ['grass'], 10, "bulbasaur.png")
dragonair = pokemon('dragonair', [310, 100, 80, 100,80,10], [scratch, ember, watergun, razorleaf], ['normal'], 10, 'dragonair.png')
        # HP[0], Attack[1], Defense[2], Sp-Attack[3], Sp-Defense[4], Speed[5]

teamP = [charmainder, squrtle, bulbasaur]
teamC = [dragonair]

def Message(size, txt,xpos,ypos):
    font = pg.font.SysFont(None, size)
    render = font.render(txt, True, gold)
    background.blit(render, (xpos,ypos))

def hpbar(pokemon, xpos, ypos):
    maxhp = int(((pokemon.basestats[0] + pokemon.ivs[0])*2 )*pokemon.level/100 + 10 + pokemon.level)
    len = 350*pokemon.actualHP/maxhp
    pg.draw.rect(background, (0,0,0), [xpos, ypos, 390,100])
    Message(45,f"{pokemon.pokename},  HP = {pokemon.actualHP}/{maxhp}" ,xpos+10,25+ypos)
    pg.draw.rect(background, (255,255,255), [xpos+20, ypos+65, 350, 25])
    pg.draw.rect(background, (255,0,0), [xpos+20, ypos+65, len, 25])

def atkbutton(xbtn, ybtn, pokemon,i, size = 30):
    pg.draw.rect(background, (0,0,0), [xbtn, ybtn, 200, 100])
    Message(size, f"     {pokemon.moveset[i].movename}", xbtn, ybtn)
    Message(size, f" type: {pokemon.moveset[i].movetype}", xbtn, ybtn+25)
    Message(size, f" power: {pokemon.moveset[i].power}", xbtn, ybtn+50)
    Message(size, f" accuracy: {pokemon.moveset[i].accuracy}", xbtn, ybtn+75)
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if xbtn<mouse[0]<xbtn+200 and ybtn<mouse[1]<ybtn +100:
        pg.draw.rect(background, (40,40,40), [xbtn, ybtn, 200,100])
        Message(size, f"     {pokemon.moveset[i].movename}", xbtn, ybtn)
        Message(size, f" type: {pokemon.moveset[i].movetype}", xbtn, ybtn+25)
        Message(size, f" power: {pokemon.moveset[i].power}", xbtn, ybtn+50)
        Message(size, f" accuracy: {pokemon.moveset[i].accuracy}", xbtn, ybtn+75)
        if click == (1,0,0) and i == i:
            atk = pokemon.moveset[i]
            return atk
        return None

def pkmnbutton(xbtn, ybtn, pokemon,size = 40):
    pg.draw.rect(background, (0,0,0), [xbtn, ybtn, 200, 100])
    Message(size, f" {pokemon.pokename}", xbtn, ybtn)
    Message(size, f" type: {pokemon.poketype}", xbtn, ybtn+50)

    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if xbtn<mouse[0]<xbtn+200 and ybtn<mouse[1]<ybtn +100:
        pg.draw.rect(background, (40,40,40), [xbtn, ybtn, 200,100])
        Message(size, f" {pokemon.pokename}", xbtn, ybtn)
        Message(size, f" type: {pokemon.poketype}", xbtn, ybtn+50)
        if click == (1,0,0) and pokemon.pokename == pokemon.pokename:
            x = pokemon
            return x
        return None

def button(xbtn, ybtn, txt):
    pg.draw.rect(background, (0,0,0), [xbtn, ybtn, 200,100])
    Message(100, txt, xbtn, ybtn)
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if xbtn<mouse[0]<xbtn+200 and ybtn<mouse[1]<ybtn +100:
        pg.draw.rect(background, (40,40,40), [xbtn, ybtn,200,100])
        Message(100, txt, xbtn, ybtn)
        if click == (1,0,0) and txt == "QUIT":
            return False
    return True

def dialogue(dial = "try not to die"):
    pg.draw.rect(background, (0,0,0), [400/2, 355, 700,70])
    Message(50, dial, 230, 375)

def pcplay(teamC, C):
    return random.choice(C.moveset)

def battle_():
    run = True
    for i in teamP:
        i.img = pg.transform.flip(i.img, True, False)
    P, C = random.choice(teamP), random.choice(teamC)

    while run == True:
        go = "no"
        background.blit(grd, (0,-100))
        background.blit(C.img, (700, 150))
        dialogue()
       
        y = atkbutton(60,450, P, 0)
        if y != None:
            atk = y
            go = "yes"
        y = atkbutton(320, 450,P,1)
        if y != None:
            atk = y
            go = "yes"
        y = atkbutton(60, 575,P,2)
        if y != None:
            atk = y
            go = "yes"
        y = atkbutton(320, 575,P,3)
        if y != None:
            atk = y
            go = "yes"

        x = pkmnbutton(580,450,teamP[0])
        if x != None:
            P = x
            go = "mon"
        x = pkmnbutton(840,450, teamP[1])
        if x != None:
            P = x
            go = "mon"
        x = pkmnbutton(580, 575, teamP[2])
        if x != None:
            P = x
            go = "mon"
        run = button(840,575, "QUIT")

        hpbar(P,60,20)
        hpbar(C,650,25)
        background.blit(P.img, (200, 150))        
        if go != "no":
            if go == "mon":

                done = pcplay(teamC, C)
                damage = battle(C,P,done, "P")
                for i in range(damage):
                    P.actualHP -= 1
                    hpbar(P, 60,20)
                    pg.display.update()
                    if P.actualHP == 0:
                            dialogue(f"{P.pokename} is dead")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(1)
                            dialogue("U lost")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(1)
                            pg.quit()
                            quit()
                    


            if go == "yes":
                done = pcplay(teamC, C)
               
                if P.actualstats[4] >= C.actualstats[4]:
                    faster, slower = P, C
                    damage = battle(faster, slower, atk)
                    for i in range(damage):
                        slower.actualHP -= 1
                        hpbar(C,650,25)
                        pg.display.update()
                        if slower.actualHP== 0:
                            dialogue(f"{slower.pokename} is dead")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            dialogue("U won")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            pg.quit()
                            quit()
                    
                    damage = battle(slower, faster, done, "P")
                    for i in range(damage):
                        faster.actualHP -= 1
                        hpbar(P, 60,20)
                        pg.display.update()
                        if faster.actualHP==0:
                            dialogue(f"{faster.pokename} is dead")
                            pg.display.update()
                            clock.tick(0.5)
                            time.sleep(3)
                            dialogue("U lost")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            pg.quit()
                            quit()
                else:
                    faster,slower = C, P
                    damage = battle(faster, slower,done, "P")
                    for i in range(damage):
                        faster.actualHP -= 1
                        hpbar(P, 60,20)
                        pg.display.update()
                        if faster.actualHP== 0:
                            dialogue(f"{faster.pokename} is dead")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            dialogue("U lost")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            pg.quit()
                            quit()
                    
                    damage = battle(slower, faster, atk)
                    for i in range(damage):
                        slower.actualHP -= 1
                        hpbar(C,650,25)
                        pg.display.update()
                        if slower.actualHP == 0:
                            dialogue(f"{slower.pokename} is dead")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            dialogue("U won")
                            clock.tick(0.5)
                            pg.display.update()
                            time.sleep(3)
                            pg.quit()
                            quit()

        for event in pg.event.get():
            if event.type==pg.QUIT:
                run = False

        pg.display.update()

def start_screeninfo(pkmn, x):
    ivs = pkmn.ivs
    background.blit(pkmn.img, (x,100))
    pg.draw.rect(background, (217,0,0), [x,325, 200, 350])
    Message(45, pkmn.pokename, x, 350)
    Message(35, f"  Type: {pkmn.poketype}", x,400)
    Message(35, f"  HP: {pkmn.actualHP} [{ivs[0]}]", x,450)
    Message(35, f"  Atk: {pkmn.actualstats[0]} [{ivs[1]}]", x,475)
    Message(35, f"  Def: {pkmn.actualstats[1]} [{ivs[2]}]", x,500)
    Message(35, f"  Satk: {pkmn.actualstats[2]} [{ivs[3]}]", x,525)
    Message(35, f"  Sdef: {pkmn.actualstats[3]} [{ivs[4]}]", x,550)
    Message(35, f"  spd: {pkmn.actualstats[4]} [{ivs[5]}]", x,575)

def stat_screen():
    while True:
        background.blit(startgrd, (0,0))
        pg.draw.rect(background, (217,0,0), [37.5,20, 750, 60])
        Message(80, "YOUR TEAM", 250,20)
        pg.draw.rect(background, (217,0,0), [862.5,20, 200, 60])
        Message(80, "START", 862.5,20)
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if 862.5<mouse[0]<862.5+200 and 20<mouse[1]<80:
            pg.draw.rect(background, (200,0,0), [862.5,20, 200, 60])
            Message(80, "START", 862.5,20)
            if click == (1,0,0) and "START" == "START":
                battle_()
        start_screeninfo(teamC[0], 862.5)
        start_screeninfo(teamP[0], 37.5)
        start_screeninfo(teamP[1], 312.5)
        start_screeninfo(teamP[2], 587.5)

        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                quit()
        pg.display.update()

stat_screen()