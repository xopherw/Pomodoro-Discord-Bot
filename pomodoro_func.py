import discord, time, asyncio, re, json, datetime as dt, os

#----------- constants -----------#

help = """
Welcome to my timer bot!!
Use this `!timer start` command to start your countdown! By default, `!timer start` will only give you 15 minutes.\n
However, you can make your own timer from 0 to 99 mintues using command like this:
`!timer start 40` for 40 minutes timer.\n
When the timer is up, it will nudge you every 5 seconds. To stop that, just reply `!done` and it will stop.
Furthermore, you can use `!stop` command to stop the timer in the middle of countdown, and timer will be reset.\n
I hope you find this useful. Have fun! 
"""

#----------- async defs -----------#

# Perform a user check to prevent double timer set. If no existing user, continue to "async def timer"
async def userCheck(client, period, message):
    if(json.loads(open('user.json' , 'r').read()).get(str(message.author.id)) != None): 
        await sender(message, "Only one timer is allowed. Stop & reset if necessary.")  
    else:
        await sender(message, f"You have set a timer for {period} minutes! Now go get them tiger!" if(period != 15) else "No time set, default timer is 15 minutes! Now go get them tiger!") 
        await timer(client, period, message) 

# Does the countdown work as well as remove user once "stop" command is used, or "done" command when time is up.
async def timer(client, period, message):
    try:
        temp_data = json.loads(open('user.json' , 'r').read())
        temp_data.update(json.loads(assigner(message.author.id)))
        open('user.json', 'w').write(json.dumps(temp_data))
        def stop(m): return m.content == '!stop' and m.author.id == message.author.id
        await waiter(client, period * 60, stop)
        await sender(message, "Timer is stopped and reset.")
        removeID(message.author.id) 

    except asyncio.TimeoutError:
        while(True):
            try: 
                await sender(message, 'Times Up!!!')
                def done(m): return m.content == '!done' and m.author.id == message.author.id
                await waiter(client, 2.5, done)
                await sender(message, 'Hooray you made it! Take a break.')
                removeID(message.author.id)
                break
            except asyncio.TimeoutError:
                pass

#----------- normal defs -----------#

def assigner(id):
    return json.dumps( { id : str(dt.datetime.now())} )

def sender(message, string):
    return message.author.send(string)

def waiter(client, timeout, check):
    return client.wait_for('message', timeout=timeout, check=check)

def removeID(id):
    try:
        temp_data = json.loads(open('user.json' , 'r').read())
        temp_data.pop(str(id))
        open('user.json', 'w').write(json.dumps(temp_data))
    except:
        pass
