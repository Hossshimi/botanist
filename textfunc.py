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

async def dl(msg,url,videoid,chid):
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
    finally: await msg.channel.send("ready to play:"+videoid)

async def yaudio(msg):
    global cue
    url = msg.content[9:]
    if url.startswith("http"):
        try:
            videoid = url[url.index("?v=")+3:url.index("&")]
        except:
            videoid = url[url.index("?v=")+3:]
        await dl(msg,url,videoid,msg.author.voice.channel.id)

async def naudio(msg):
    global cue
    url = msg.content[6:]
    if url.startswith("http"):
        videoid = url[url.index("sm"):]
        await dl(msg,url,videoid,msg.author.voice.channel.id)

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
        #cue[chid].pop(0)
        vc[chid].stop()
        musicbotter(msg)
    elif command == "cue":
        chid = msg.author.voice.channel.id
        reply = "```playing cue:\n- " + "\n- ".join(cue[chid]) + "```"
        msg.channel.send(reply)

def musicbotter(msg):
    def after(msg):
        #os.remove(old)
        musicbotter(msg)
    global vc,cue
    vc_id = msg.author.voice.channel.id
    try:
        if cue[vc_id]:
            audioname = cue[vc_id].pop(0) + ".mp3"
            #print("1")
            vc[vc_id].play(discord.FFmpegPCMAudio(audioname),after=lambda _: after(msg))
            #print("2")
    except:
        msg.channel.send("**CUE is empty!**")

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
        vc[vc_id].play(discord.FFmpegPCMAudio(audio_path,options="-af volume=-10dB"))
    #player = player[vc_id]
    #print(t().strftime("[ %H:%M:%S ] "),"finish audio function[",audioname,"]")

    #if message.content.startswith(">donotstop"): #止まるんじゃねえぞ
    #    vc_lock = False

async def join(client,message): #join vc
    global vc_id,airhorn_flag
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

async def leave(client,message): #leave vc
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

async def shutup(client,message): #shut up
    global vc
    vc_id = message.author.voice.channel.id
    #channel = client.get_channel(vc_id)
    #voice = client.voice_client_in(channel.server)
    #player = player[vc_id]
    vc[vc_id].stop()

def usr(client,message):
    return "<@" + message.content[5:] + ">"

async def hide(client,message):
    text = message.content[6:]
    hid = "||"+"||||".join(text)+"||"
    #hid = hid[:-3]
    return hid

async def honda(client,message):
    if "-win" in message.content:
        await vcfunc("honda-win",message)
    else:
        await vcfunc(f"honda{str(random.choice([1,2,3]))}",message)

def weather(client,message): #weather
    loc = message.content[9:]
    return getweather.get_weather(loc)

def rand(client,message): #random
    text = str(message.content)
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


def say(client,message): #say
    text = str(message.content)
    return text

async def nick(client,message): #change nick
    if message.author.id == 311147580715171842 :
        nick = str(message.content)
        nick = nick[6:]
        await message.guild.me.edit(nick=nick)
        reply = f"{message.author.mention} Changed nick"
        await message.channel.send(reply)
    else:
        reply = f"{message.author.mention} Err:you don't have permission"
        await message.channel.send(reply)

def help(client,message): #help--------------------------------
    fmt = "{0:<12}: {1}"
    commands_path = os.path.normpath(os.path.join(os.path.abspath(__file__),r"../data/helplist.json"))
    commands_open = open(commands_path,"r",encoding="utf-8-sig")
    commands = json.load(commands_open)
    commands_open.close()
    reply = (f"{message.author.mention}\n```=========== HELP ===========")
    for command,desc in sorted(commands.items()):
        reply = reply + f"\n{fmt.format(command,desc)}```"
    #reply = reply + "``` https://bot-anist.hatenablog.com/"
    return reply

def kabaorun(client,message): #精神を加速させろ
    user = str(message.content)
    user = user[10:]
    if user == "":
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　精神を加速させろ```"
    else:
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　"+user+"```"
    return reply

def chikuwa(client,message): #ちくわ
    user = str(message.content)
    user = user[9:]
    ckw = r".   \_\_ \_\_\_ \_\_" + "\n(0)  ≡ ≡≡ )\n   ￣￣￣ ￣"
    chikuwa_ext = [r" \_ \_\_\_\_\_","  ≡ ≡≡  "," ￣￣ ￣"]
    if user == "":
        reply = ckw
    elif int(user) <=0:
        reply = message.author.mention + "そんなちくわは無い"
    else:
        user = int(user) - 1
        reply = r".   \_\_ \_\_\_ \_\_" + chikuwa_ext[0]*user +"\n(0) ≡ ≡≡ " + chikuwa_ext[1]*user + ")\n   ￣￣￣" + chikuwa_ext[2]*user
    return reply

def anagosan(client,message): #ちくしょう
    user = str(message.content)
    user = user[10:]
    if user == "":
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　　ちくしょう・・・\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    else:
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　"+user+"\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    return reply

def HG(client,message): #大池沼
    userlist=[]
    for member in message.guild.members :
        if str(member.status) == "online":
            userlist.append(member.id)
    randuser = random.choice(userlist)
    reply = "どーもーハードゲイ( <@!"+str(randuser)+"> )で～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼） セイセイセイ・セイセイセイ・セイセイセイセイセイセイセイ（三三七拍子超池沼）ど～も～ハードゲイで～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼）"
    return reply

def walkingdrum(client,message): #歩くドラム缶の恐怖
    string = str(message.content)
    string = string[13:]
    if string == "":
        reply = "【歩くドラム缶の恐怖】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
    else:
        reply = "【"+string+"】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
    return reply

def kodakumi(client,message):
    easylist = ["difficult","easy","so easy","very easy","hyper easy","ultra easy"]
    easylevel = str(message.content)
    easylevel = easylevel[10:12]
    if easylevel == "":
        return "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは easy"
    elif 0 <= int(easylevel) <= 5:
        reply = "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは " + str(easylist[int(easylevel)])
        return reply
    else:
        return "easylevelが対応範囲外じゃないの?\nUsed to be help参照は easy"
