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
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready.")

    @bot.command()
    async def markov(ctx):
        await ctx.send("`I have awoken from my slumber.`")

    @bot.command()
    async def elp(ctx):
        await ctx.send("```Here is the list of things I can do: \n1) .markov\n2) .elp\n3) .WAKEUP\n4) .credits```")

    @bot.command()
    async def WAKEUP(ctx):
        await ctx.send(f"`Hey {ctx.author}, FRICK YOU. Now I'm just going to stop running out of spite.`")

    @bot.command()
    async def credits(ctx):
        await ctx.send(f"`D E G O#5308 made me :) (Don't ask how long it took his dumbass)`")

    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    run_Discord_Bot()
