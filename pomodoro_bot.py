from pomodoro_func import *

# create the "user.json" file with an assigned dummy value.
open('user.json','w').write('{"dummy" : "dummy" }')

client = discord.Client()

#----------- @client.events -----------#

@client.event
async def on_message(message):      

    if (message.author == client.user): return

    if (re.match(r"^(\!timer start)$", message.content)):
        await userCheck(client, 15, message)    
        
    elif(re.match(r"^(\!timer start) [0-9]{1,2}$", message.content)):
        period = int(message.content.split(' ')[-1])
        await userCheck(client, period, message)
        
    elif(message.content == "!timer help"): await message.channel.send(help)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

while(True):
    try:    client.loop.run_until_complete(client.run('TOKEN'))
    except Exception:
        print("Reconnecting, please hold...")
        time.sleep(5)
