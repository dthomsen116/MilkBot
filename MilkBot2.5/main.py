# Imports
import asyncio, discord, os, sys
import yt_dlp as youtube_dl
from discord.ext import commands, tasks
from dotenv import load_dotenv

# environment
load_dotenv()

# Keys
f = open('DISCTOKEN.txt', 'r')
DISCORD_KEY = f.read()
os.getenv(DISCORD_KEY)  
    
# intents and command delimeter
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

# youtube DL
youtube_dl.utils.bug_reports_message = lambda: ''

# format options
yt_dl_opts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_opts = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

#downloading/streaming

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data=data
        self.title=data.get('title')
        self.url=''
    
    @classmethod
    async def from_url(cls,url,*,loop=None,stream=False):
        loop=loop or asyncio.get_event_loop()
        data=await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data=data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

# Commands

@bot.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} not connected to a vc".format(ctx.message.author.name))
        return
    else:
        channel=ctx.message.author.voice.channel
        await channel.connect()
        
@bot.command(name='play')
async def join(ctx, url):
        server=ctx.message.guild
        voice_channel=server.voice_client
        async with ctx.typing():
            filename=await YTDLSource.from_url(url,loop=bot.loop)
            voice_channel.play(discord.FFmpegAudio(executable="C:\\Users\\dthom\\Desktop\\Milky2.0\\ffmpeg-2023-05-04-git-4006c71d19-full_build\\bin",source=filename, args='-vn'))
        await ctx.send('**NOW PLAYING** {}'.format(filename))
    

@bot.command(name='pause')
async def pause(ctx):
    voice_client= ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("Bro Im already Paused.")

@bot.command(name='resume')
async def resume(ctx):
    voice_client= ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("Bro Im not playin.")

@bot.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()    
    else: 
        await ctx.send("Milky hasnt joined silly")
        
@bot.command(name='stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()    
    else: 
        await ctx.send("Milky isnt playing")
        
if __name__ == "__main__":
    bot.run(DISCORD_KEY)