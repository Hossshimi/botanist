import sys,os,json,random
import datetime
import getweather
t = datetime.datetime.now


async def vcfunc(audioname, msg=None): #音声流すだけ
    #print(t().strftime("[ %H:%M:%S ] "),"start audio function[",audioname,"]...")
    global player,vc_lock,voice,client
    audiofname = r"..\sounds\\" + audioname + ".mp3"
    audio_path = os.path.normpath(os.path.join(os.path.abspath(__file__),audiofname))
    vc_id = msg.author.voice_channel.id
    try:
        player[vc_id].stop()
        pass
    except:
        #print(t().strftime("[ %H:%M:%S ] "),"---VC error---")
        #reply = f"{msg.author.mention} {sys.exc_info()}"
        #await client.send_message(msg.channel, reply)
        pass
    finally:
        channel = client.get_channel(vc_id)
        if client.is_voice_connected(channel.server):
            voice[vc_id] = client.voice_client_in(channel.server)
        else:
            voice[vc_id] = await client.join_voice_channel(channel)
        player[vc_id] = voice[vc_id].create_ffmpeg_player(audio_path)
        #player = player[vc_id]
        player[vc_id].start()
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

async def join(client,message): #join vc
    if message.author.voice_channel == None:
        client.send_message(message.channel,"_err:please join vc_")
    else:
        vc_id = message.author.voice_channel.id
        channel = client.get_channel(vc_id)
        airhorn_flag = False
        await client.join_voice_channel(channel)
        log = t().strftime("[ %H:%M:%S ] ")+"join vc["+str(channel)+"]"
        await client.send_message(LOG_CHANNEL,log)
        #airhorn_flag = True

async def leave(client,message): #leave vc
    try:
        vc_id = message.author.voice_channel.id
    except: pass
    if "vc_id" in locals():
        channel = client.get_channel(vc_id)
        voice = client.voice_client_in(channel.server)
        await voice.disconnect()
        log = t().strftime("[ %H:%M:%S ] ")+"leave vc["+str(channel)+"]"
        await client.send_message(LOG_CHANNEL,log)
    else:
        log = t().strftime("[ %H:%M:%S ] ")+"leave failed"
        await client.send_message(LOG_CHANNEL,log)

async def shutup(client,message): #shut up
    global player
    vc_id = message.author.voice_channel.id
    #channel = client.get_channel(vc_id)
    #voice = client.voice_client_in(channel.server)
    #player = player[vc_id]
    player[vc_id].stop()


async def weather(client,message): #weather
    getweather.get_weather(message.content[9:])

async def rand(client,message): #random
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
    await client.send_message(message.channel,result)


async def say(client,message): #say
    text = str(message.content)
    text = text[5:]
    #if text[:7] == "command":
    #    text = "/" + text[8:]
    #    await client.send_message(message.channel,text)
    #else:
    await client.send_message(message.channel,text)

async def nick(client,message): #change nick
    if str(message.author.id) == "311147580715171842":
        nick = str(message.content)
        nick = nick[6:]
        await client.change_nickname(message.server.me, nick)
        reply = f"{message.author.mention} Changed nick"
        await client.send_message(message.channel,reply)
    else:
        reply = f"{message.author.mention} Err:権限がありません"
        await client.send_message(message.channel,reply)

async def help(client,message): #help--------------------------------
    fmt = "{0:<12}: {1}"
    commands_path = os.path.normpath(os.path.join(os.path.abspath(__file__),r"../data/helplist.json"))
    commands_open = open(commands_path,"r",encoding="utf-8-sig")
    commands = json.load(commands_open)
    commands_open.close()
    reply = (f"{message.author.mention}\n```=========== HELP ===========")
    for command,desc in sorted(commands.items()):
        reply = reply + f"\n{fmt.format(command,desc)}"
    reply = reply + "``` https://bot-anist.hatenablog.com/"
    await client.send_message(message.channel,reply)

async def kabaorun(client,message): #精神を加速させろ
    user = str(message.content)
    user = user[10:]
    if user == "":
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　精神を加速させろ```"
    else:
        reply = "```  　　　　　　　　　　∩＿∩\n　　　　　　　　　 ／ ＼ ／ ＼\n　　　　　　　　　|  (°)=(°) |\n　　　　　　　　　|　  ●_● 　|\n　　　　　　　　 / 　　   　 ヽ\n　　　　   r⌒  |〃 ------ ヾ |\n　　　　　/　 i／  | _＿二＿＿ノ\n　　　　./　 ／　　/　　　　   ) 　\n　　　 ./ ／　　／　　　　 　/／\n　　　/　　　.／　　　　　/￣\n　　 .ヽ､__.／　　　 ／ ⌒ヽ\n　 　　　　 r　　  ／      |\n　　　　　/　　 　　  　   ﾉ\n　　　　/　　　　 / 　　  /\n　　　./　　　　／/　   ／\n　　 /.　 　.／ ./   ／\n　　i　　　／  ./  ／\n　　i　　./  .ノ.^/\n　　i　 ./  　|_／\n　　i   /\n　／  /\n (_／　"+user+"```"
    await client.send_message(message.channel, reply)

async def chikuwa(client,message): #ちくわ
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
    await client.send_message(message.channel,reply)

async def anagosan(client,message): #ちくしょう
    user = str(message.content)
    user = user[10:]
    if user == "":
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　　ちくしょう・・・\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    else:
        reply = ".　   ／￣⌒⌒ヽ\n  　 |   ／￣￣￣ヽ\n  　 |   | 　  ／ 　＼|\n　 .|    |   　 ´　｀  |\n 　(6       　つ  　/　"+user+"\n  　.| 　     / ／⌒⌒ヽ\n  　 |　         ＼   ￣ ノ\n  　  |　　       /￣"
    await client.send_message(message.channel, reply)

async def HG(client,message): #大池沼
    userlist=[]
    for member in message.server.members :
        userlist.append(member.id)
    randuser = random.choice(userlist)
    reply = "どーもーハードゲイ( <@!"+randuser+"> )で～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼） セイセイセイ・セイセイセイ・セイセイセイセイセイセイセイ（三三七拍子超池沼）ど～も～ハードゲイで～～～す（池沼） フォォォォォォォォォォォォォ！！！（大池沼）"
    await client.send_message(message.channel,reply)

async def walkingdrum(client,message): #歩くドラム缶の恐怖
    string = str(message.content)
    string = string[13:]
    if string == "":
        reply = "【歩くドラム缶の恐怖】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
        await client.send_message(message.channel,reply)
    else:
        reply = "【"+string+"】\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"
        await client.send_message(message.channel, reply)

async def kodakumi(client,message):
    easylist = ["difficult","easy","so easy","very easy","hyper easy","ultra easy"]
    easylevel = str(message.content)
    easylevel = easylevel[10:12]
    if easylevel == "":
        await client.send_message(message.channel, "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは easy")
    elif 0 <= int(easylevel) <= 5:
        reply = "全て投げ出してもいいじゃないの?\nUsed to be 諦めるのは " + str(easylist[int(easylevel)])
        await client.send_message(message.channel, reply)
    else:
        await client.send_message(message.channel,"easylevelが対応範囲外じゃないの?\nUsed to be help参照は easy")

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
