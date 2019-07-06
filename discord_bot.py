#=====VERSION:4.1.6=====

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
import datetime

VERSION = "4.1.6"
client = discord.Client()
t = datetime.datetime.now
rep_list = ("ごきげんよう","どちらさまでしょうか？","しらん","帰れ")
vc_list = ["neverdie", "sumanko", "airhorn", "goldrush1", "goldrush2",
            "scream","yarimasunee","kowareruwa","yurusite","soudayo",
            "haha","USSR","roboto","mankoja","jamayaro","oi","ike","dase",
            "keshigomu","marmelo","saikyou","TF","doko","hujino"]
func_list = {
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
    "hide" : func.hide
}
#vc_id = "317228479416500227" #chikwa
#vc_id = "392898035090456589" #test server
"""for c in client.get_all_channels():
    print(c.name)"""
vc_id = None
player = {}
vc = {}
airhorn_flag = False
vc_lock = False
pflag = False
LOG_CHANNEL = None


def getpath(rpath):
    base = os.path.dirname(os.path.abspath(__file__))
    apath = os.path.normpath(os.path.join(base,"..",rpath))
    return apath



@client.event
async def on_ready(): #-------起動時処理-------------
    global LOG_CHANNEL
    LOG_CHANNEL_ID = 577890877234741248
    LOG_CHANNEL = client.get_channel(LOG_CHANNEL_ID)
    print(LOG_CHANNEL)
    log = t().strftime("\n[ %H:%M:%S ] ")+"======= Logged in as : " + client.user.name +" "+ VERSION +"============"
    await LOG_CHANNEL.send(log)
    try:
        if (sys.argv[1] == "rs"):
            log = t().strftime("[ %H:%M:%S ] ")+"+++++++++++++ BOTanist was restarted +++++++++++++"
            await LOG_CHANNEL.send(log)
            channel = client.get_channel(int(sys.argv[2]))
            await channel.send("**RESTARTED!**")
    except: pass
    finally: pass

"""@client.event
async def on_voice_state_update(before, after): #VC参加時にairhorn
    global airhorn_flag,pflag
    if airhorn_flag and (not pflag) :
        if before.voice_channel is None:
            global vc_id
            channel = client.get_channel(vc_id)
            global player
            try:
                player.stop()
            except:
                pass
            finally:
                if client.is_voice_connected(channel.server):
                    voice = client.voice_client_in(channel.server)
                else:
                    voice = await client.join_voice_channel(channel)
                player = voice.create_ffmpeg_player(r'D:\Backup\work\discord_bot\sounds\airhorn.mp3')
                player.start()"""


@client.event
async def on_message(message):
    global pflag,vc_id,vc_list
    if message.author == client.user: #自分の発言は無視
            return
 #--------------重要な制御-------------------------------------
    if message.author.id==311147580715171842 : #管理者権限
        if message.content.startswith(">p"): #pause
            if pflag: pass
            else:
                pflag = True
                log = t().strftime("[ %H:%M:%S ] ")+"----- paused -----"
                await LOG_CHANNEL.send(log)
        if message.content.startswith(">rsm"): #resume
            if (not pflag): pass
            else:
                pflag = False
                log = t().strftime("[ %H:%M:%S ] ")+"----- resumed -----"
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
            log = t().strftime("[ %H:%M:%S ] ")+"+++++++++++++ BOTanist stopped +++++++++++++"
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
            reply = f"{message.author.mention} {random.choice(rep_list)}"
            await message.channel.send(reply)
        
        if ("used to be" in message.content) or ("Used to be" in message.content):
            reply = '諦めるのは easy'
            await message.channel.send(reply)

        ####### Voice Channel #######
        global player,airhorn_flag,vc_lock
        #vc_id = "317228479416500227" #chikwa
        #old_id = ""
        #channel = client.get_channel(vc_id)
        #voice = client.voice_client_in(channel.server)
        
        if message.content.startswith(">"):
            for f in func_list:
                if f in str(message.content[1:]):
                    await func_list[f](client,message,vc)
                    break
            
            vccom = message.content
            vccom = vccom[1:]
            if vccom in vc_list:
                await func.vcfunc(vccom, message, vc)


        #await f.textfunc_(client, message, vc_id)
    

#voice = client.join_voice_channel(client.get_channel("317228479416500227"))

client.run("NTAyNDYzMzUyNzMyMjU0MjA5.DqoUDA.HXPqz444qrvaA45MZvvnqJRW5EM")
