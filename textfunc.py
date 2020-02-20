import discord
#client = discord.Client()

import sys,os,json,random,re
from datetime import datetime, timedelta
import getweather
t = datetime.now

import youtube_dl

vc = {}
cue = {}

import numpy

async def dl(url,videoid,chid):
    global cue
    opts = {
        "format":"bestaudio/best",
        "outtmpl":videoid + ".mp4",
        'postprocessors':[
            {'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'},
        ],
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    try: cue[chid].append(videoid)
    except: cue[chid] = [videoid]

async def yaudio(msg):
    global cue
    url = msg.content[9:]
    if url.startswith("http"):
        videoid = url[url.index("?v=")+3:]
        await dl(url,videoid,msg.author.voice.channel.id)

async def naudio(msg):
    global cue
    url = msg.content[6:]
    if url.startswith("http"):
        videoid = url[url.index("sm"):]
        await dl(url,videoid,msg.author.voice.channel.id)

def musicctrl(msg):
    global vc,cue
    command = msg.content[7:]
    if command == "start":
        #print("start")
        musicbotter(msg)
    elif command == "clear":
        chid = msg.author.voice.channel.id
        cue[chid].clear()
    elif command == "skip":
        chid = msg.author.voice.channel.id
        cue[chid].pop(0)
        vc[chid].stop()

def musicbotter(msg):
    def after(old):
        os.remove(old)
        musicbotter(msg)
    global vc,cue
    vc_id = msg.author.voice.channel.id
    if cue[vc_id]:
        audioname = cue[vc_id].pop(0) + ".mp3"
        #print("1")
        vc[vc_id].play(discord.FFmpegPCMAudio(audioname),after=lambda _: after(audioname))
        #print("2")

async def vcfunc(audioname, msg): #音声流すだけ
    #print(t().strftime("[ %H:%M:%S ] "),"start audio function[",audioname,"]...")
    global client,vc
    audiofname = r"../sounds//" + audioname + ".mp3"
    audio_path = os.path.normpath(os.path.join(os.path.abspath(__file__),audiofname))
    if msg.content[-20:-2].isdecimal():
        vc_id = int(msg.content[-20:-2])
    else:
        vc_id = msg.author.voice.channel.id
    try:
        if vc[vc_id].is_playing():
            vc[vc_id].stop()
        channel = msg.author.voice.channel
        vc[vc_id] =  await channel.connect()
    except:
        pass
    finally:
        vc[vc_id].play(discord.FFmpegPCMAudio(audio_path))

async def join(client,message,inopt=None,outopt=None): #join vc
    global vc_id,vc
    LOG_CHANNEL_ID = 577890877234741248
    LOG_CHANNEL = client.get_channel(LOG_CHANNEL_ID)
    if message.author.voice.channel == None:
        message.channel.send("_err:please join vc_")
    else:
        vc_id = message.author.voice.channel.id
        channel = client.get_channel(vc_id)
        #airhorn_flag = False
        vc[vc_id] = await channel.connect()
        log = (t()+timedelta(hours=9)).strftime("[ %H:%M:%S ] ")+"join vc["+str(channel)+"]"
        await LOG_CHANNEL.send(log)
        #airhorn_flag = True

async def leave(client,message,inopt=None,outopt=None): #leave vc
    global vc
    LOG_CHANNEL_ID = 577890877234741248
    LOG_CHANNEL = client.get_channel(LOG_CHANNEL_ID)
    vc_id = message.author.voice.channel.id
    try:
        await vc[vc_id].disconnect()
        log = (t()+timedelta(hours=9)).strftime("[ %H:%M:%S ] ")+"leave vc["+str(vc[vc_id].channel.name)+"]"
        await LOG_CHANNEL.send(log)
    except Exception as e:
        log = t().strftime("[ %H:%M:%S ] ")+"leave failed"
        await LOG_CHANNEL.send(log)
        print(e)

async def shutup(client,message,inopt=None,outopt=None): #shut up
    global vc
    vc_id = message.author.voice.channel.id
    #channel = client.get_channel(vc_id)
    #voice = client.voice_client_in(channel.server)
    #player = player[vc_id]
    vc[vc_id].stop()

def usr(client,message,inopt=None,outopt=None):
    return "<@" + message.content[5:] + ">"

async def hide(client,message,inopt=None,outopt=None):
    if (outopt == "v") or (outopt == "i"):
        text = message.content[14:]
    elif outopt == None:
        text = message.content[6:]
    hid = "||"+"||||".join(text)+"||"
    #hid = hid[:-3]
    return hid

async def honda(client,message,inopt=None,outopt=None):
    if "-win" in message.content:
        await vcfunc("honda-win",message)
    else:
        await vcfunc(f"honda{str(random.choice([1,2,3]))}",message)

def weather(client,message,inopt=None,outopt=None): #weather
    if (outopt == "v") or (outopt == "i"):
        loc = message.content[17:]
    elif outopt == None:
        loc = message.content[9:]
    return getweather.get_weather(loc)

def rand(client,message,inopt=None,outopt=None): #random
    text = str(message.content)
    if inopt:
        text = inopt
    elif outopt:
        text = text[14:]
    elif outopt == None:
        text = text[6:]
    
    ulist = text.split()
    if ulist[0].startswith("m-"):
        mode = ulist[0]
        mode = mode[2:]
        ulist = ulist[1:]
        if mode=="choice":
            if ulist==None: pass
            else:
                result = random.choice(ulist)
        elif mode=="sample":
            modeopt = ulist[0]
            ulist = ulist[1:]
            if ulist==None: pass
            else:
                result = random.sample(ulist,int(modeopt))
                result = " ".join(result)
        elif mode=="choices":
            modeopt = ulist[0]
            ulist = ulist[1:]
            if ulist==None: pass
            else: 
                result = random.choices(ulist,k=int(modeopt))
                result = " ".join(result)
        else: result = "Err:無効なmode"
    elif ulist==None: result = "Err:選択肢の指定がありません"
    else:
        result = random.choice(ulist)
    return result


def say(client,message,inopt=None,outopt=None): #say
    text = str(message.content)
    if inopt:
        text = inopt.replace("-imgout ","",1)
    elif outopt == None:
        text = text[5:]
    elif outopt:
        text = text[5:].replace("-imgout ","",1).replace("-varout ","",1)
    return text

async def nick(client,message,inopt=None,outopt=None): #change nick
    if message.author.id == 311147580715171842 :
        nick = str(message.content)
        nick = nick[6:]
        await message.guild.me.edit(nick=nick)
        reply = f"{message.author.mention} Changed nick"
        await message.channel.send(reply)
    else:
        reply = f"{message.author.mention} Err:you don't have permission"
        await message.channel.send(reply)

def help(client,message,inopt=None,outopt=None): #help--------------------------------
    fmt = "{0:<12}: {1}"
    commands_path = os.path.normpath(os.path.join(os.path.abspath(__file__),r"../data/helplist.json"))
    commands_open = open(commands_path,"r",encoding="utf-8-sig")
    commands = json.load(commands_open)
    commands_open.close()
    reply = (f"{message.author.mention}\n```=========== HELP ===========")
    for command,desc in sorted(commands.items()):
        reply = reply + f"\n{fmt.format(command,desc)}"
    reply = reply + "``` https://bot-anist.hatenablog.com/"
    return reply

def kabaorun(client,message,inopt=None,outopt=None): #精神を加速させろ
    user = str(message.content)
    if inopt:
        user = inopt.replace("-imgout ","",1)
    elif outopt:
        user = user[18:]
    elif outopt == None:
        user = user[10:]
    if user == "":
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　精神を加速させろ```"
    else:
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　"+user+"```"
    if outopt == "i":
        return reply[3:-3]
    else:
        return reply

def chikuwa(client,message,inopt=None,outopt=None): #ちくわ
    user = str(message.content)
    if inopt:
        user = inopt.replace("-imgout ","",1)
    elif outopt:
        user = user[17:]
        ckw = ".   __ ___ __\n(0)  ≡ ≡≡ )\n   ￣￣￣ ￣"
        chikuwa_ext = [" _ __ __ _","  ≡ ≡≡ "," ￣￣ ￣ ￣"]
    elif outopt == None:
        user = user[9:]
        ckw = ".   \_\_ \_\_\_ \_\_\n(0)  ≡ ≡≡ )\n   ￣￣￣ ￣"
        chikuwa_ext = [" \_ \_\_\_\_\_","  ≡ ≡≡  "," ￣￣ ￣"]
    if user == "":
        reply = ckw
    elif int(user) <=0:
        reply = message.author.mention + "そんなちくわは無い"
    else:
        user = int(user) - 1
        if outopt == "i":
            reply = ".   __ ___ __" + chikuwa_ext[0]*user +"\n(0) ≡ ≡≡ " + chikuwa_ext[1]*user + ")\n   ￣￣￣" + chikuwa_ext[2]*user
        else:
            reply = ".   \_\_ \_\_\_ \_\_" + chikuwa_ext[0]*user +"\n(0) ≡ ≡≡ " + chikuwa_ext[1]*user + ")\n   ￣￣￣" + chikuwa_ext[2]*user
    return reply

def anagosan(client,message,inopt=None,outopt=None): #ちくしょう
    user = str(message.content)
    if "vi" in outopt:
        user = inopt.replace("-imgout ","",1)
    elif outopt:
        user = user[18:]
    elif outopt == None:
        user = user[10:]
    if user == "":
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　　ちくしょう・・・\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    else:
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　"+user+"\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    return reply

def HG(client,message,inopt=None,outopt=None): #大池沼
    userlist=[]
    for member in message.guild.members :
        if str(member.status) == "online":
            userlist.append(member.id)
    randuser = random.choice(userlist)
    reply = "どーもーハードゲイ( <@!"+str(randuser)+"> )で～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼） セイセイセイ・セイセイセイ・セイセイセイセイセイセイセイ（三三七拍子超池沼）ど～も～ハードゲイで～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼）"
    return reply

def walkingdrum(client,message,inopt=None,outopt=None): #歩くドラム缶の恐怖
    string = str(message.content)
    if inopt:
        string = inopt.replace("-imgout ","",1)
    elif outopt:
        string = string[21:]
    elif outopt == None:
        string = string[13:]
    if string == "":
        reply = "【歩くドラム缶の恐怖】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
        if outopt == "i":
            return reply[:54]+reply[56:]
        else:
            return reply
    else:
        reply = "【"+string+"】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
        if outopt == "i":
            return reply[:54-9+len(string)]+reply[56-9+len(string):]
        else:
            return reply

def kodakumi(client,message,inopt=None,outopt=None):
    easylist = ["difficult","easy","so easy","very easy","hyper easy","ultra easy"]
    easylevel = str(message.content)
    if inopt:
        easylevel = int(inopt.replace("-imgout ","",1))
    elif outopt:
        easylevel = easylevel[18:20]
    elif outopt == None:
        easylevel = easylevel[10:12]
    if easylevel == "":
        return "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは easy"
    elif 0 <= int(easylevel) <= 5:
        reply = "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは " + str(easylist[int(easylevel)])
        return reply
    else:
        return "easylevelが対応範囲外じゃないの?\nUsed to be help参照は easy"

white = 1
black = -1
blank = 0

class MOB():
    def __init__(self):
        self.cell = numpy.zeros((8,8))
        self.cell = self.cell.astype(int)
        self.cell[3][3] = self.cell[4][4] = 1
        self.cell[3][4] = self.cell[4][3] = -1
        self.current = black
        self.turn = 1
        self.dspl = ["",""]
    
    def turnchange(self):
        MOBoard.current *= -1
    
    def rangecheck(self,x,y):  # ①　盤内かどうか　
        if x == None: x = -1
        if y == None: y = -1
        if x < 0 or 8 <= x  or y < 0 or 8 <= y:
            return False
        return True

    def check_can_reverse(self,x,y):  # 置けるかどうか
        #if not MOBoard.rangecheck(x,y):   # →　①へ
        #    return False
        if not MOBoard.cell[x][y] == blank:   #  ②
            return False
        elif not MOBoard.can_reverse_stone(x,y):   # →　③へ
            return False
        else: return True

    def can_reverse_one(self,x,y,dx,dy):  # ⑶、⑷　　(dx,dy)方向に敵石があり、その先に自石があるかどうか

        #if not MOBoard.rangecheck(x+dx,y+dy):
        #    return False
        length = 0
        if not MOBoard.cell[x+dx][y+dy] == -MOBoard.current: #  ⑶
            return False # (dx,dy)方向が敵石じゃない時False
        else:    
            while MOBoard.cell[x+dx][y+dy] == -MOBoard.current: 
                x +=dx
                y +=dy
                length += 1
                if MOBoard.cell[x+dx][y+dy] == MOBoard.current:  # ⑷-True
                    return length
                elif not MOBoard.cell[x+dx][y+dy] == -MOBoard.current:
                    continue
                else: return False
            else: return False  # ⑷-False

    def can_reverse_stone(self,x,y):  # 　③入力座標ではひっくり返せる石はあるか
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == dy == 0: continue   # ⑴
                elif (not MOBoard.rangecheck(x+dx,y+dy)): continue  # ①（調べた範囲が番外だったらエラーが起こるため）
                elif not MOBoard.can_reverse_one(x,y,dx,dy):  # →　⑶、⑷の処理へ
                    continue
                else: return True

    def reverse_stone(self,x,y): #  ④ 座標に石を置いて石をひっくり返す
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    length = MOBoard.can_reverse_one(x,y,dx,dy)
                    if length == None: length = 0
                    if length > 0:
                        for l in range(length):
                            k = l+1
                            self.cell[x + dx*k][y + dy*k] *= -1

    def display(self):  # 盤面の状況を表示
        #print('==='*10)
        b = ["","","","","","","",""]
        for y in range(8):
            if y == 0: b[y] += "\n:one:"
            elif y == 1: b[y] += ":two:"
            elif y == 2: b[y] += ":three:"
            elif y == 3: b[y] += ":four:"
            elif y == 4: b[y] += ":five:"
            elif y == 5: b[y] += ":six:"
            elif y == 6: b[y] += ":seven:"
            elif y == 7: b[y] += ":eight:"
            for x in range(8):
                if MOBoard.cell[x][y] == blank:
                    b[y] += "<:b:650704687280160784>"
                elif MOBoard.cell[x][y] == white:
                    b[y] += "<:W:650692140422266892>"
                    #print('W', end = '  ')
                elif MOBoard.cell[x][y] == black:
                    b[y] += "<:B:650692249746669568>"
                    #print('B', end = '  ')
            #print('\n', end = '')
        MOBoard.dspl[0] = "<:b:650704687280160784>:regional_indicator_a::regional_indicator_b:"+\
            ":regional_indicator_c::regional_indicator_d::regional_indicator_e:"+\
            ":regional_indicator_f::regional_indicator_g::regional_indicator_h:."
        MOBoard.dspl[1] = "\n".join(b)

    def put_stone(self,x,y):  # 一回のターン内の行動 
        if MOBoard.check_can_reverse(x,y):   # 入力座標に石を置ける
            #self.pass_count = 0
            MOBoard.cell[x][y] = MOBoard.current
            MOBoard.reverse_stone(x,y)
            MOBoard.turnchange()
            return True
        else:  # 入力座標に石を置けない
            return False

    def check_put_place(self):  # ❶盤面上に石が置ける場所があるか　次のクラスの時に使用
        for i in range(8):
            for j in range(8):
                if MOBoard.check_can_reverse(i,j): # (i,j)座標に置いて石が置けたら成立
                    return True
                else:continue
        return False

class MOG(MOB):
    def __init__(self):
        self.white_count = 2
        self.black_scount = 2
        self.blank_count = 60
        self.place_point = [None,None]
        self.Player_Black_Member = None
        self.Player_White_Member = None
        self.status = None
        self.channel = None

    def Entry(self,pB,pW):
        self.Player_Black_Member = pB
        self.Player_White_Member = pW

    # パスをする関数
    def pass_system(self):  #  ②
        #board.pass_count += 1
        MOBoard.turnchange()
        #if board.pass_count ==2:  # 連続二回パスしたので③のゲームを終わらせる関数へ移動
        #    self.gameset()
        return True

    async def gameset(self): #  ③ ゲーム終了、石の数をカウントし勝敗を表示
        self.count_system()
        desc = "《ホワイト》 : "+str(self.white_count)+\
            " / 《二グロ》 : "+str(self.black_count)+"\n\n"
        
        if self.white_count > self.black_count:
            desc += "白人 WIN!!"
        if self.white_count < self.black_count:
            desc += "黒人 WIN!!"
        if self.white_count == self.black_count:
            desc += "!!平和!!"
        embed = discord.Embed(title="-=≡ GAME SET ≡=-",\
            description=desc,color=0xffa000)
        await self.channel.send(embed=embed)
        self.status = "set"


    def count_system(self):  #  ⑤ 石のカウントシステム
        self.white_count = numpy.sum(MOBoard.cell == white)
        self.black_count = numpy.sum(MOBoard.cell == black)
        self.blank_count = numpy.sum(MOBoard.cell == blank)

    #def input_point(self):    #  ① 座標を入力
        #print('石を置く座標を(1~8で)入力してください。(x,y)=(9,9)でpass、(0,0)で終了します。')
        #x = input('x>>')
        #y = input('y>>')
        #try:
        #    x = int(x)-1
        #    y = int(y)-1
        #except:
        #    self.input_point()
        #return x, y

    def one_turn_play(self):  # ①〜⑤と❶をまとめる（❶に関しては上に記述）　
        if MOGame.place_point != [None,None] and MOBoard.check_put_place():  #  ❶ 盤面に石が置ける場所があるかどうか
            x = MOGame.place_point[0]   #  ① 座標を入力
            y = MOGame.place_point[1]
            MOBoard.put_stone(x,y)  # Boardクラスで作ったやつ。石をおいてひっ繰り返してTrueを返すか、何もせずFalseを返す
            if not MOBoard.put_stone(x,y):
                    if (x,y) == (8,8):       #  ② パスするとき
                        self.pass_system()
                    elif (x,y) == (-1,-1):   #  ③ ゲームをやめる時
                        self.gameset()
                    #石をおけない時は もう一度同じことをする
                    while False:
                        self.one_turn_play()     
        else:self.pass_system()

    def a2n(self,a):
        if a == "a": MOGame.place_point[0] = 0
        elif a == "b": MOGame.place_point[0] = 1
        elif a == "c": MOGame.place_point[0] = 2
        elif a == "d": MOGame.place_point[0] = 3
        elif a == "e": MOGame.place_point[0] = 4
        elif a == "f": MOGame.place_point[0] = 5
        elif a == "g": MOGame.place_point[0] = 6
        elif a == "h": MOGame.place_point[0] = 7
        elif a == "i": MOGame.place_point[0] = 8

    # 最後まで続くようにしてみる   
    async def gameplay(self,client):
        while self.blank_count >0:
            MOBoard.display()
            await self.channel.send(MOBoard.dspl[0])
            await self.channel.send(MOBoard.dspl[1])
            MOBoard.turn += 1
            self.status = "-" + str(MOBoard.turn) + "年目-\n"
            if MOBoard.current == -1:
                self.status += f"{self.Player_Black_Member.mention} 《ニグロ》のターン\n"+\
                    ""
            elif MOBoard.current == 1:
                self.status += f"{self.Player_White_Member.mention} 《ホワイト》のターン\n"
            await self.channel.send(self.status)
            self.place_point = [None,None]
            await self.channel.send("位置を入力してください:")
            def check(m):
                return bool(re.match(r">([A-Za-z]\d)|\d[A-Za-z]",m.content))
            msg = await client.wait_for("message",check=check)
            if re.match(r"[A-Ia-i]",msg.content[1]) and re.match(r"[1-9]",msg.content[2]):
                MOGame.a2n(msg.content[1])
                self.place_point[1] = int(msg.content[2])-1
            elif re.match(r"[A-Ia-i]",msg.content[2]) and re.match(r"[1-9]",msg.content[1]):
                MOGame.a2n(msg.content[2])
                self.place_point[1] = int(msg.content[1])-1

            #print('-----'*10)
            self.one_turn_play()   # ターンでの行動
            self.count_system()   # 石とblankの数を出す
            await self.channel.send('<:W:650692140422266892> : '+str(self.white_count)+' / <:B:650692249746669568> : '+str(self.black_count))
            #print('pass_count : ',MOBoard.pass_count)
        self.gameset()

MOBoard = None
MOGame = None

async def MO(client,message):
    global MOBoard,MOGame
    if (not MOGame): # 何も無い
        MOBoard = MOB()
        MOGame = MOG()
        MOGame.channel = message.channel

        desc = "Matsuoka Othelloのマッチが開始されました.\n"+\
            "《二グロ》にエントリーするプレイヤーは先に,\n"+\
            ">MO entry B\n"+\
            "《ホワイト》にエントリーするプレイヤーはその後,\n"+\
            ">MO entry W\n"+\
            "を送信してください.\n\n"+\
            "最終的な勢力が大きかった人種の勝利です."
        embed = discord.Embed(title="-=≡ Matsuoka Othelloへようこそ ≡=-",\
            description=desc,color=0xffa000)
        embed.set_thumbnail(url="https://gyazo.com/3426e16d4dfe1765ae95afbe5b87363f")
        await message.channel.send(message.author.mention,embed=embed)

        def check_b(m):
            return m.content.startswith(">MO entry B")
        def check_w(m):
            return m.content.startswith(">MO entry W")
        try:
            msg = await client.wait_for("message",check=check_b,timeout=30)
            await message.channel.send(f"{msg.author.mention} 《二グロ》にエントリーしました.\n"+\
                "続いて《ホワイト》のエントリーを行います.")
            pb = msg.author
            msg = await client.wait_for("message",check=check_w,timeout=30)
            await message.channel.send(f"{msg.author.mention} 《ホワイト》にエントリーしました.")
            MOGame.Entry(pB=pb,pW=msg.author)
        except:
            await message.channel.send("エントリーがタイムアウトしたため,マッチは解散しました.")
            MOBoard = None
            MOGame = None
        
        await MOGame.gameplay(client)

    
