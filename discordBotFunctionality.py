import discord
from discord.ext import commands
import creds


intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='.', intents=intents)

# Idea (ish): Grab user input on what command they want to execute, then set each command as a key in a dictionary. If
# the lowercase input is equal to one of the keys, execute that key value pair. Otherwise, say that command doesn't exist

def run_Discord_Bot():
    chainMessages = 10
    messageList = [""]
    listOfWords = []

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready.")

    @bot.event
    async def on_message(message):
        # Bot will ignore any messages sent by itself
        if message.author == bot.user:
            return
        # If a user's message is a command for Markov or a link, then ignore it
        if not message.content.startswith(".") and not message.content.startswith("http"):
            print(f"Message contents: {message.content}")
            messageList.insert(0, message.content.split())
            print(f"messageList: {messageList}")
        # Obtaining each individual work within the user message and storing in a list
        for word in messageList[0]:
            listOfWords.append(word)
        print(f"listOfWords: {listOfWords}")
        await bot.process_commands(message)

    @bot.command()
    async def markov(ctx):
        await ctx.send("`Forcing a markov chain...`")

    bot.remove_command("help")

    @bot.command()
    async def help(ctx):
        await ctx.send("```Here is the list of things I can do: \n1) .markov\n2) .help\n3) .description\n4) .credits\n5) .source```")

    @bot.command()
    async def description(ctx):
        await ctx.send(f"```Hello, I am a bot that relies on text from users and composes a markov chain.\n"
                       f"This process will occur every {chainMessages} messages or can be forced using the\n"
                       f"\'.markov\' command```")

    @bot.command()
    async def credits(ctx):
        await ctx.send(f"`D E G O#5308 made me :)`")

    @bot.command()
    async def source(ctx):
        await ctx.send(f"`Repo: https://github.com/DiegoERojas/MarkovDiscordBot`")

    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    run_Discord_Bot()
