import discord
import asyncio

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.monitor_stratz())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    async def m(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(593474878519377970) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60) # task runs every 60 seconds
   
    async def monitor_stratz(client):
        await self.wait_until_ready()
        channel = self.get_channel(593474878519377970) 
        while not self.is_closed():
            print(1)
            r=requests.get("https://api.stratz.com/api/v1/Player/143597200")
            print(r.status_code)
            if int(r.status_code)==200:
                note=channel.mention
                await channel.send(str(r.status_code)+note)
            else:
                await channel.send(r.status_code)
            await asyncio.sleep(60) 
   

client = MyClient()
client.run('codecode')
