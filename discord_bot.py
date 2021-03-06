VERSION = "5.2.4"

import discord
import random
import sys
from time import sleep
import json
import os
sys.path.append(os.path.abspath(__file__) + "..")
set(sys.path)

import textfunc as func
#import getweather

import subprocess

from datetime import datetime, timedelta

client = discord.Client()
t = datetime.now
REP_LIST = ("ごきげんよう","どちらさまでしょうか？","しらん","帰れ")

VC_LIST = ["neverdie", "sumanko", "airhorn", "goldrush1", "goldrush2",
            "scream","yarimasunee","kowareruwa","yurusite","soudayo",
            "haha","USSR","roboto","mankoja","jamayaro","oi","ike","dase",
            "keshigomu","marmelo","saikyou","TF","doko","hujino","h2",
            "yoneken","muscle","sidechest","ikerune","naniwo","oatumari",
            "ohayou","shakaijin","sizukani","subarasii","tanosikatta",
            "uttaemasu","edmfaq","faq","kobuside","mouowatta","osikko",
            "we","yuunou","daisuki","gomenna","kottikara","naraomae",
            "faqfaq","faaq","ruready","countdown","aim","ak","arigatoak",
            "dekee","dokosumi","hikeyo","lemon","pine","sugoi","tuee","zako",
            "zisin","heke","hamutarou","nikuniku"]
FUNC_LIST = {
    "join" : func.join,
    "leave" : func.leave,
    "shutup" : func.shutup,
    "weather" : func.weather,
    "rand" : func.rand,
    "say" : func.say,
    "nick" : func.nick,
    "help" : func.help,
    "kabaorun" : func.kabaorun,
    "chikuwa" : func.chikuwa,
    "anagosan" : func.anagosan,
    "HG" : func.HG,
    "walkingdrum" : func.walkingdrum,
    "kodakumi" : func.kodakumi,
    "honda" : func.honda,
    "hide" : func.hide,
    #"usr" : func.usr,
    #"MO" : func.MO
}

COR_LIST = ["join","leave","shutup","honda","nick","MO"]
#vc_id = "392898035090456589" #test server
"""for c in client.get_all_channels():
    print(c.name)"""
vc_id = None
player = {}
YM_flag = True
vc_lock = False
pflag = False
LOG_CHANNEL = None
VAR = [None for x in range(100)]
#FONTPATH = os.path.normcase((os.path.join(os.path.dirname(__file__), "/data/VL-Gothic-Regular.ttf")))
FONTPATH = "/app/data/VL-Gothic-Regular.ttf"
FONTSIZE = 20
COLOR = (255,255,255)
#print(os.environ.get("DISCORD_TOKEN"))



def getpath(rpath):
    base = os.path.dirname(os.path.abspath(__file__))
    apath = os.path.normpath(os.path.join(base,"..",rpath))
    return apath



@client.event
async def on_ready(): #-------起動時処理-------------
    global LOG_CHANNEL
    LOG_CHANNEL_ID = 577890877234741248
    LOG_CHANNEL = client.get_channel(LOG_CHANNEL_ID)
    if LOG_CHANNEL.guild.me.display_name != ("BOTanist "+VERSION):
        await LOG_CHANNEL.guild.me.edit(nick="BOTanist "+VERSION)
    #print(LOG_CHANNEL)
    log = (t()+timedelta(hours=9)).strftime("\n[ %H:%M:%S ] ")+\
        "======= Logged in as : " + client.user.name +" "+ VERSION +"============"
    await LOG_CHANNEL.send(log)
    try:
        if (sys.argv[1] == "rs"):
            log = (t()+timedelta(hours=9)).strftime("[ %H:%M:%S ] ")+\
                "+++++++++++++ BOTanist was restarted +++++++++++++"
            await LOG_CHANNEL.send(log)
            channel = client.get_channel(int(sys.argv[2]))
            await channel.send("**RESTARTED!**")
    except: pass
    finally: pass

#@client.event
#async def on_voice_state_update(member,before, after): #VC参加時にairhorn
#    global YM_flag,pflag
#    if YM_flag and (member.id == 482875226502332416) and (not pflag) :
#        #if before.channel == None:
#            #global vc_id
#            #channel = after.channel
#            vc_id = after.channel.id
#            #global player
#            try:
#                player[vc_id].stop()
#            except:
#                pass
#            finally:
#                #try:
#                #    if func.vc[vc_id]:
#                #        voice = client.voice_client_in(channel.server)
#                #except:
#                #    voice = await client.join_voice_channel(channel)
#                #finally:
#                    sleep(1)
#                    func.vc[vc_id].play(discord.FFmpegPCMAudio("./sounds/i_love.mp3"))
#                    #player.start()


@client.event
async def on_message(message):
    global pflag,vc_id,VC_LIST,VAR
    if message.author == client.user: #自分の発言は無視
            return
 #--------------重要な制御-------------------------------------
    if message.author.id==311147580715171842 : #管理者権限
        if message.content == ">p": #pause
            if pflag: pass
            else:
                pflag = True
                log = (t()+timedelta(hours=9)).strftime("[ %H:%M:%S ] ")+"----- paused -----"
                await LOG_CHANNEL.send(log)
        if message.content == ">rsm": #resume
            if (not pflag): pass
            else:
                pflag = False
                log = (t()+timedelta(hours=9)).strftime("[ %H:%M:%S ] ")+"----- resumed -----"
                await LOG_CHANNEL.send(log)

        if ">stop" in message.content: #stop
            """try: #vc_id 存在確認
                channel = client.get_channel(vc_id)
                is_vc_connected = client.is_voice_connected(channel.server)
            finally: pass
            if "is_vc_connected" in locals(): # vc接続解除
                voice = client.voice_client_in(channel.server)
                await voice.disconnect()
                log = t().strftime("[ %H:%M:%S ] ")+"----- vc disconnected -----"
                await LOG_CHANNEL.send(log)
            log = t().strftime("[ %H:%M:%S ] ")+"----- vc off -----"
            await LOG_CHANNEL.send(log)"""
            reply = f"{message.author.mention} Stop bot..."
            await message.channel.send(reply)
            log = (t()+timedelta(hours=9)).strftime("[ %H:%M:%S ] ")+\
                "+++++++++++++ BOTanist stopped +++++++++++++"
            await LOG_CHANNEL.send(log)
            os._exit(0) #終了
            #except: print(t().strftime("[ %H:%M:%S ] "),"stop failed")

    #-------常時利用可能-------------
    """if message.content.startswith(">restart"): #restart bot
        log = t().strftime("[ %H:%M:%S ] ")+"starting restart..."
        await client.send_message(LOG_CHANNEL,log)
        ap = os.path.abspath(__file__)
        res_path = os.path.join(ap,"..","restarter.bat")
        subprocess.run(f"{res_path} python -W default \"{ap}\" rs {message.channel.id}")
        sys.exit()"""

 #-----------------------------------------------------------------
    if pflag==False:
        """if message.content.startswith(">test"):
            reply = message.author.id
            await client.send_message(message.channel,reply)
       """
        if str(client.user.id) in message.content: #メンション受けたら
            reply = f"{message.author.mention} {random.choice(REP_LIST)}"
            await message.channel.send(reply)
        
        if ("used to be" in message.content) or ("Used to be" in message.content):
            reply = '諦めるのは easy'
            await message.channel.send(reply)
        
        if message.content == ">vars":
            reply = "```"
            for i,v in enumerate(VAR):
                if v != None:
                    reply += (f"{str(i)} : "+str(v)+"\n")
                else:
                    break
            reply += "```"
            await message.channel.send(reply)

        global player,vc_lock,FONTPATH,FUNC_LIST
        #vc_id = "317228479416500227" #chikwa
        #old_id = ""
        #channel = client.get_channel(vc_id)
        #voice = client.voice_client_in(channel.server)
        
        if message.content.startswith(">"):
            if message.content.startswith(">youtube"):
                await func.yaudio(message)
            elif message.content.startswith(">nico"):
                await func.naudio(message)
            elif message.content.startswith(">music"):
                func.musicctrl(message)
            for f in FUNC_LIST:
                if str(message.content[1:]).startswith(f):
                    flag = True
                    result = "e"
                    if f in COR_LIST:
                        await FUNC_LIST[f](client,message)
                        flag = False
                        result = ""
                    
                    if (result == "e") and message.content.startswith(">deltmp"):
                        now = t()
                        since = message.content.split()[1]
                        if since == "help":
                            text = [
                                message.author.mention,
                                "[deltmp] usage:",
                                "this command will delete your posts,",
                                "which starts with `>del`.",
                                "Examples:",
                                "    >del text1\n    >deltext2\n    deltext3",
                                "text1, text2 will be deleted. text3 won't be deleted.",
                                "`>deltmp {since}` : delete your posts since `since` **hours**."
                            ]
                            await message.channel.send(f"{message.author.mention} \n{text}")
                        elif since.isnumeric():
                            await message.channel.send(f"{message.author.mention} [deltmp] start deleting(since: {since} hour(s))")
                            del_count = 0
                            async for msg in message.channel.history(limit=1000):
                                posted_time = message.created_at
                                if (msg.author == message.author) and \
                                    (msg.content.startswith(">del")) and \
                                    ((now - posted_time) <= timedelta(hours=int(since))):
                                    await msg.delete()
                                    del_count += 1
                            await message.channel.send(f"{message.author.mention} [deltmp] finished: your {int(del_count)} post(s) has been deleted")
                        else:
                            await message.channel.send(f"{message.author.mention} err:deltmp:invalid option")

                    elif result == "e":
                        result = FUNC_LIST[f](client,message)
                        await message.channel.send(result)
            
            vccom = message.content
            if len(vccom) > 20:
                vccom = vccom[1:-23]
            else:
                vccom = vccom[1:]
            if vccom in VC_LIST:
                await func.vcfunc(vccom, message)


        #await f.textfunc_(client, message, vc_id)
    

#voice = client.join_voice_channel(client.get_channel("317228479416500227"))

client.run(os.environ.get("DISCORD_TOKEN"))