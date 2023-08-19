import discord
import os
import json
import urllib3
import traceback
from dotenv import load_dotenv
from uptime import keep_alive
from discord.ext import commands, tasks
from make_embed import MakeEmbed

load_dotenv('variables.env')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client(intents=intents)
http = urllib3.PoolManager()
allrepos = []

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # register repositories like below, microsoft/dotnet is the repo taken as example here
    # example = GithubWatcher("https://api.github.com/repos/microsoft/dotnet/events") 
  

    for i in allrepos:
      await i.SetEtagAndId()

    looprepos.start()

@tasks.loop(seconds=60)
async def looprepos():
    global allrepos

    try:
      for i in allrepos:
        await i.checkgithub()
    except Exception:
      traceback.print_exc()

class GithubWatcher:
  
  def __init__(self, events_url: str):
    global allrepos
    self.url = events_url
    self.Headers = {
      "if-none-match" : "", 
      "authorization" : f"token {os.getenv('git_token')}", 
      "Accept" : "application/vnd.github+json"
    }
    self.lastid = 0
    allrepos.append(self)
  
  async def SetEtagAndId(self):
    url = http.request('GET', url=self.url , headers=self.Headers)
    self.Headers["if-none-match"] = url.headers["ETag"]
    data = json.loads(url.data)
    self.lastid = data[0]['id']
    print(f'etag set for {self.url[29:].replace("/events", "")}: {url.headers["ETag"]}')
    print(f'last event id set for {self.url[29:].replace("/events", "")}: {self.lastid}')

  async def checkgithub(self):
    id = 0 # edit to your channel id here, it must be a integer
    channel = bot.get_channel(id)

    url = http.request('GET', 'https://api.github.com/rate_limit', headers=self.Headers)
    data = json.loads(url.data)
    if data["resources"]["core"]["remaining"] == 0:
      print('rate limited')
      return

    url = http.request('GET',url=self.url, headers=self.Headers)

    if url.status == 200:
      # only want the latest event from the list of events at a time
      data = json.loads(url.data)
      for i in data:
        if i['id'] != self.lastid:
          embed = MakeEmbed(i)
          if embed != None:
            await channel.send(embed=embed)
        elif i['id'] == self.lastid:
          break
      self.Headers["if-none-match"] = url.headers["ETag"]
      id = self.lastid
      self.lastid = data[0]['id']
      print(f'{self.url[29:].replace("/events", "")}: {id} to {self.lastid}')
      return

    print(f"http code {url.status} {self.url[29:].replace('/events', '')}")
    
keep_alive()
bot.run(os.getenv('TOKEN'))
