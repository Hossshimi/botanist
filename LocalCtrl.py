import sys,os,json,random,subprocess
import datetime
t = datetime.datetime.now

async def p():
    global pflag
    if pflag: pass
    else:
        pflag = True
        print(t().strftime("[ %H:%M:%S ] "),"----- paused -----")

async def rsm():
    global pflag
    if (not pflag): pass
    else:
        pflag = False
        print(t().strftime("[ %H:%M:%S ] "),"----- resumed -----")

async def stop():
    global client,vc_id
    vc_connected = None
    try: #vc_id 存在確認
        channel = client.get_channel(vc_id)
        vc_connected = client.is_voice_connected(channel.server)
    finally: pass
    if vc_connected: # vc接続解除
        voice = client.voice_client_in(channel.server)
        await voice.disconnect()
        print(t().strftime("[ %H:%M:%S ] "),"----- vc disconnected -----")
    print(t().strftime("[ %H:%M:%S ] "),"+++++++++++++ BOTanist was stopped +++++++++++++")
    os._exit(0) #終了

async def restart():
    print(t().strftime("[ %H:%M:%S ] "),"restarting...")
    ap = os.path.abspath(sys.argv[0])
    res_path = os.path.join(ap,"..","restarter.bat")
    subprocess.run(f"{res_path} python \"{ap}\" rs l")
    sys.exit()