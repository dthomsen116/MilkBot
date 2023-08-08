# MilkBot
A Music (among other things) Bot for Discord

## Previous Iterations

### CHATGPT
I used API keys in order to query chatgpt using Discord as an interface. This was an interesting project and was fun to see behind the scenes of an AI query. The issue with this bot was the tokens, as I ran out and did not fund more in order to keep this bot up and running. 

```
@bot.command()
async def chat(message, *, arg):
        
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt= arg,
                temperature=0.75,
                max_tokens=100,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0
                )
            
    await message.send(response['choices'][0]['text'])

@bot.command()
async def art(message, *, arg):
            
    #Image Creation through openai:
    response = openai.Image.create(prompt=arg[4:],
                                    n=1,
                                    size="1024x1024"
                                    )

    image_url = response['data'][0]['url']
            
    #Send the Image as a URl. 
    await message.channel.send(image_url)

```

### The 1.0...
This Bot does pretty much nothing except connect to the server and let you know it joined. It has a few basic commands but was more for the experience of working on a discord bot, rather than making this the final working bot.

```
class Client(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        #print(message.content)
        
        if message.content == '$Alive' or message.content.startswith('$alive'):
            await message.channel.send('I am Alive!')
        
        if message.content == '$sing' or message.content.startswith('$sing'):
            await message.channel.send("Never gonna give you up")
            await message.channel.send("Never gonna let you down")
            await message.channel.send("Never gonna run around and desert you")
            await message.channel.send("Never gonna make you cry")
            await message.channel.send("Never gonna say goodbye")
            await message.channel.send("Never gonna tell a lie and hurt you")
            await message.channel.send("https://tenor.com/view/rickroll-gif-26319886")
```
