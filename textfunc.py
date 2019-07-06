import discord
client = discord.Client()

import sys,os,json,random
import datetime
import getweather
t = datetime.datetime.now

from discord.ext import commands

bot = commands.Bot(command_prefix=">")

async def vcfunc(audioname, msg, vc): #音声流すだけ
    #print(t().strftime("[ %H:%M:%S ] "),"start audio function[",audioname,"]...")
    global client
    audiofname = r"../sounds//" + audioname + ".mp3"
    audio_path = os.path.normpath(os.path.join(os.path.abspath(__file__),audiofname))
    vc_id = msg.author.voice.channel.id
    if vc[vc_id].is_playing():
        vc[vc_id].stop()
    channel = msg.author.voice.channel
    try:
        vc[vc_id] =  await channel.connect()
    except:
        pass
    finally:
        vc[vc_id].play(discord.FFmpegPCMAudio(audio_path))
    #player = player[vc_id]
    #print(t().strftime("[ %H:%M:%S ] "),"finish audio function[",audioname,"]")


#async def textfunc_(client, message, vc_id):
#    global rep_list
    #======== Text Channel ==============================================================
"""if message.content.startswith(">channel"): #change voice channel
    user = message.content
    user = user[:10]
    if user == "chikuwa":
        vc_id = "317228479416500227"
        old_id = "392898035090456589"
    elif user == "test":
        vc_id = "392898035090456589"
        old_id = "317228479416500227"
    channel = client.get_channel(vc_id)
    channel_old = client.get_channel(old_id)
    voice = client.voice_client_in(channel_old.server)
    await voice.disconnect()
    await client.join_voice_channel(channel)"""

    #if message.content.startswith(">donotstop"): #止まるんじゃねえぞ
    #    vc_lock = False

async def join(client,message,vc): #join vc
    global vc_id,airhorn_flag
    LOG_CHANNEL_ID = 577890877234741248
    LOG_CHANNEL = client.get_channel(LOG_CHANNEL_ID)
    if message.author.voice.channel == None:
        message.channel.send("_err:please join vc_")
    else:
        vc_id = message.author.voice.channel.id
        channel = client.get_channel(vc_id)
        airhorn_flag = False
        vc[vc_id] = await channel.connect()
        log = t().strftime("[ %H:%M:%S ] ")+"join vc["+str(channel)+"]"
        await LOG_CHANNEL.send(log)
        #airhorn_flag = True

async def leave(client,message,vc): #leave vc
    LOG_CHANNEL_ID = 577890877234741248
    LOG_CHANNEL = client.get_channel(LOG_CHANNEL_ID)
    try:
        vc_id = message.author.voice.channel.id
    except: pass
    try:
        #if f"vc{vc_id}" in locals():
            await vc[vc_id].disconnect()
    except:
        """log = t().strftime("[ %H:%M:%S ] ")+"leave failed"
        await LOG_CHANNEL.send(log)"""
        pass
    finally:
        log = t().strftime("[ %H:%M:%S ] ")+"leave vc["+str(vc[vc_id].name)+"]"
        await LOG_CHANNEL.send(log)

async def shutup(client,message,vc): #shut up
    vc_id = message.author.voice.channel.id
    #channel = client.get_channel(vc_id)
    #voice = client.voice_client_in(channel.server)
    #player = player[vc_id]
    vc[vc_id].stop()


async def hide(client,message,vc):
    text = message.content[6:]
    hid = "||"+"||||".join(text)+"||"
    #hid = hid[:-3]
    await message.channel.send(hid)

async def honda(client,message,vc):
    await vcfunc(f"honda{str(random.choice([1,2,3]))}",message,vc)

async def weather(client,message,vc): #weather
    await message.channel.send(getweather.get_weather(message.content[9:]))

async def rand(client,message,vc): #random
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
    await message.channel.send(result)


async def say(client,message,vc): #say
    text = str(message.content)
    text = text[5:]
    #if text[:7] == "command":
    #    text = "/" + text[8:]
    #    await client.send_message(message.channel,text)
    #else:
    await message.channel.send(text)

async def nick(client,message,vc): #change nick
    if message.author.id == 311147580715171842 :
        nick = str(message.content)
        nick = nick[6:]
        await message.guild.me.edit(nick=nick)
        reply = f"{message.author.mention} Changed nick"
        await message.channel.send(reply)
    else:
        reply = f"{message.author.mention} Err:you don't have permission"
        await message.channel.send(reply)

async def help(client,message,vc): #help--------------------------------
    fmt = "{0:<12}: {1}"
    commands_path = os.path.normpath(os.path.join(os.path.abspath(__file__),r"../data/helplist.json"))
    commands_open = open(commands_path,"r",encoding="utf-8-sig")
    commands = json.load(commands_open)
    commands_open.close()
    reply = (f"{message.author.mention}\n```=========== HELP ===========")
    for command,desc in sorted(commands.items()):
        reply = reply + f"\n{fmt.format(command,desc)}"
    reply = reply + "``` https://bot-anist.hatenablog.com/"
    await message.channel.send(reply)

async def kabaorun(client,message,vc): #精神を加速させろ
    user = str(message.content)
    user = user[10:]
    if user == "":
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　精神を加速させろ```"
    else:
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　"+user+"```"
    await message.channel.send(reply)

async def chikuwa(client,message,vc): #ちくわ
    user = str(message.content)
    user = user[9:]
    if user == "":
        reply = ".   \_\_ \_\_\_ \_\_\n(0)  ≡ ≡≡ )\n   ￣￣￣ ￣"
    elif int(user) <=0:
        reply = message.author.mention + "そんなちくわは無い"
    else:
        user = int(user) - 1
        chikuwa_ext = [" \_ \_\_\_\_\_","  ≡ ≡≡  "," ￣￣ ￣"]
        reply = ".   \_\_ \_\_\_ \_\_" + chikuwa_ext[0]*user +"\n(0) ≡ ≡≡ " + chikuwa_ext[1]*user + ")\n   ￣￣￣" + chikuwa_ext[2]*user
    await message.channel.send(reply)

async def anagosan(client,message,vc): #ちくしょう
    user = str(message.content)
    user = user[10:]
    if user == "":
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　　ちくしょう・・・\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    else:
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　"+user+"\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    await message.channel.send(reply)

async def HG(client,message,vc): #大池沼
    userlist=[]
    for member in message.guild.members :
        if str(member.status) == "online":
            userlist.append(member.id)
    randuser = random.choice(userlist)
    reply = "どーもーハードゲイ( <@!"+str(randuser)+"> )で～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼） セイセイセイ・セイセイセイ・セイセイセイセイセイセイセイ（三三七拍子超池沼）ど～も～ハードゲイで～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼）"
    await message.channel.send(reply)

async def walkingdrum(client,message,vc): #歩くドラム缶の恐怖
    string = str(message.content)
    string = string[13:]
    if string == "":
        reply = "【歩くドラム缶の恐怖】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
        await message.channel.send(reply)
    else:
        reply = "【"+string+"】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
        await message.channel.send(reply)

async def kodakumi(client,message,vc):
    easylist = ["difficult","easy","so easy","very easy","hyper easy","ultra easy"]
    easylevel = str(message.content)
    easylevel = easylevel[10:12]
    if easylevel == "":
        await message.channel.send("全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは easy")
    elif 0 <= int(easylevel) <= 5:
        reply = "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは " + str(easylist[int(easylevel)])
        await message.channel.send(reply)
    else:
        await message.channel.send("easylevelが対応範囲外じゃないの?\nUsed to be help参照は easy")

#    if message.content.startswith(">lovelyradio"):
#        await client.send_message(message.channel, "えいニャ！えいニャ！渚の小悪魔☆えいニャ！えいニャ！ラヴリィ～レイディオ！")


    """if 'フェリス' in message.content:
        reply = 'フェリス女学院大学 〒245-8650 横浜市泉区緑園4-5-3\nhttp://www.ferris.ac.jp/'
        await client.send_message(message.channel, reply)"""

    
    """if message.content.startswith('>allclean'): #全発言を削除        
        clean_flag = True
        while (clean_flag):
            msgs = [msg async for msg in client.logs_from(message.channel)]
            if len(msgs) > 1: # 1発言以下でdelete_messagesするとエラーになる
                await client.delete_messages(msgs)
            else:
                clean_flag = False
                await client.send_message(message.channel, '-----Deleted all log-----')
        """
