import discord, time, asyncio, re

help = """
Welcome to my timer bot!!
Use this `!timer start` command to start your countdown! By default, `!timer start` will only give you 30 minutes.\n
However, you can make your own timer from 0 to 99 mintues using command like this:
`!timer start 40` for 40 minutes timer.\n
When the timer is up, it will nudge you every 5 seconds. To stop that, just reply `!done` and it will stop.
Furthermore, you can use `!stop` command to stop the timer in the middle of countdown, and timer will be reset.\n
I hope you find this useful. Have fun! 
Xopher
"""
client = discord.Client()

def stop(m): return m.content == '!stop'

def done(m): return m.content == '!done'

def sender(message, string):
    return message.author.send(string)

def waiter(timeout, check):
    return client.wait_for('message', timeout=timeout, check=check)

@client.event
async def on_message(message):      
    if (message.author == client.user): 
        return

    if (re.match(r"^(!timer start)$", message.content)):
        await sender(message, "No time set, you have 30 minutes! Now go get them tiger!") 
        await timer(5, message)       

    elif(re.match(r"^(!timer start) [0-9]{1,2}$", message.content)):
        period = int(message.content.split(' ')[-1])
        await sender(message, f"You have set a timer for {period} minutes! Now go get them tiger!") 
        await timer(period * 60, message)            
    
    elif(message.content == "!help"): await message.channel.send(help)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def timer(period, message):
    try:
        await waiter(period, stop)
        await sender(message, "Timer is stopped and reset.") 
    except asyncio.TimeoutError:
        while(True):
            try: 
                await sender(message, 'Times Up!!!')
                await waiter(5, done)
                await sender(message, 'Hooray you made it! Take a break.')
                break
            except asyncio.TimeoutError:
                pass

client.run("YOUR_TOKEN")

