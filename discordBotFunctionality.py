import discord
from discord.ext import commands
import creds


intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='.', intents=intents)


def run_Discord_Bot():
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready.")

    @bot.command()
    async def markov(ctx):
        await ctx.send("`Forcing a markov chain...`")

    @bot.command()
    async def elp(ctx):
        await ctx.send("```Here is the list of things I can do: \n1) .markov\n2) .elp\n3) .credits```")

    @bot.command()
    async def credits(ctx):
        await ctx.send(f"`D E G O#5308 made me :)`")

    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    run_Discord_Bot()
