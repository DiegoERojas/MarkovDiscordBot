import discord
from discord.ext import commands
import creds
import MarkovTextComposer as mtc

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='.', intents=intents)

class MainBotClass:
    def __init__(self, forceChain):
        self.forceChain = forceChain
        self.forceChainFrequencyCONST = forceChain
        self.autoRunMarkov = False
        self.canForceMarkov = False
        self.numberOfMessages = 0
        self.minMessagesToForceMarkov = forceChain // 2
        self.creatorID = "<@251087613325344768>"


def run_Discord_Bot():
    messageList = []
    listOfWords = []

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready.")

    def resettingMarkov():
        messageList.clear()
        listOfWords.clear()
        user.numberOfMessages = 0

    @bot.event
    async def on_message(message):
        # Bot will ignore any messages sent by itself
        if message.author == bot.user:
            return
        if user.numberOfMessages >= user.minMessagesToForceMarkov:
            user.canForceMarkov = True

        if user.numberOfMessages >= user.forceChainFrequencyCONST:
            user.autoRunMarkov = True

        if not user.autoRunMarkov:
            # If a user's message is a command for Markov or a link, then ignore it
            if not message.content.startswith(".") and not message.content.startswith("http"):
                user.numberOfMessages += 1
                messageList.insert(0, message.content.split())
                # Obtaining each individual work within the user message and storing in a list
                for word in messageList[0]:
                    listOfWords.append(word)
        # Automatically creating a markov chain
        elif user.autoRunMarkov:
            if not message.content.startswith("."):
                listOfWords.append(message.content)
            # Force calling the markov command
            ctx = await bot.get_context(message)
            await markov(ctx)
        await bot.process_commands(message)

    @bot.command()
    async def markov(ctx):
        if user.canForceMarkov:
            userMarkov = mtc.MarkovComposer(listOfWords, user.forceChainFrequencyCONST)
            userMarkov.totalNumberOfWords()
            userMarkov.settingKeyValues()
            userMarkov.markovOutput()
            await ctx.send(f"`{userMarkov.unpackingResult()}`")
            user.autoRunMarkov = False
            user.canForceMarkov = False
            resettingMarkov()
        else:
            await ctx.send("`Please give me time to reference additional messages to the markov chain`")

    bot.remove_command("help")

    @bot.command()
    async def help(ctx):
        await ctx.send("```Here is the list of things I can do: \n"
                       "1) .markov        (Forces a markov chain based on current data)\n"
                       "2) .help          (Displays a menu of all available commands)\n"
                       "3) .description   (What this bot does)\n"
                       "4) .credits       (Creator of this bot)\n"
                       "5) .source        (Link to the GitHub repo)\n"
                       "6) .bug           (Nicely pings the creator if there is a problem)```")

    @bot.command()
    async def description(ctx):
        await ctx.send(f"```Hello, I am a bot that relies on text from users and composes a markov chain."
                       f"This process will occur every {user.forceChainFrequencyCONST} messages or can be forced using the"
                       f"\'.markov\' command when at least {user.minMessagesToForceMarkov} messages have been sent.```")

    @bot.command()
    async def credits(ctx):
        await ctx.send(f" {user.creatorID} `made me`:clown:")

    @bot.command()
    async def source(ctx):
        await ctx.send(f"`Repo: https://github.com/DiegoERojas/MarkovDiscordBot`")

    @bot.command()
    async def bug(ctx):
        await ctx.send(f"`HEY` {user.creatorID} `FIX THIS RIGHT NOW! or else...` :point_down: :rage:")
    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    """
    The argument is the number of messages the bot will reference before
    automatically running the markov text chain.
    """
    user = MainBotClass(5)
    run_Discord_Bot()
