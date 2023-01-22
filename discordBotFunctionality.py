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
        self.forceChainFrequency = forceChain
        self.fourthMessage = ""

    def setFourthMessage(self, message):
        self.fourthMessage = message

    def getFourthMessage(self):
        return self.fourthMessage

    def getForceChain(self):
        return self.forceChain

    def setForceChain(self, value):
        self.forceChain = value

def run_Discord_Bot():
    chainMessages, cooldown = user.forceChain, user.forceChain
    messageList = []
    listOfWords = []

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready.")

    def resettingMarkov():
        messageList.clear()
        listOfWords.clear()
        user.setForceChain(user.forceChainFrequency)

    @bot.event
    async def on_message(message):

        # Bot will ignore any messages sent by itself
        if message.author == bot.user:
            return
        # If a user's message is a command for Markov or a link, then ignore it
        if user.getForceChain() != -1:
            if not message.content.startswith(".") and not message.content.startswith("http"):
                messageList.insert(0, message.content.split())
                # Obtaining each individual work within the user message and storing in a list
                for word in messageList[0]:
                    listOfWords.append(word)
                user.setForceChain(user.getForceChain() - 1)
        elif user.getForceChain() == -1:
            print("Automatically Forcing a markov chain...")
            ctx = await bot.get_context(message)
            await markov(ctx)
            user.setFourthMessage(message.content)
            resettingMarkov()
            listOfWords.append(user.fourthMessage)
        await bot.process_commands(message)

    @bot.command()
    async def markov(ctx):
        if len(messageList) < user.forceChainFrequency - 1:
            await ctx.send("`Please give me time to reference additional messages to the markov chain`")
        else:
            userMarkov = mtc.MarkovComposer(listOfWords, user.forceChainFrequency)
            userMarkov.settingKeyValues()
            userMarkov.markovOutput()
            await ctx.send(f"`{userMarkov.unpackingResult()}`")
            resettingMarkov()

    bot.remove_command("help")

    @bot.command()
    async def help(ctx):
        await ctx.send("```Here is the list of things I can do: \n"
                       "1) .markov        (Forces a markov chain based on current data)\n"
                       "2) .help          (Displays a menu of all available commands)\n"
                       "3) .description   (What this bot does)\n"
                       "4) .credits       (Creator of this bot)\n"
                       "5) .source        (Link to the GitHub repo)```")

    @bot.command()
    async def description(ctx):
        await ctx.send(f"```Hello, I am a bot that relies on text from users and composes a markov chain."
                       f"This process will occur every {chainMessages} messages or can be forced using the"
                       f"\'.markov\' command```")

    @bot.command()
    async def credits(ctx):
        await ctx.send(f"`D E G O#5308 made me :)`")

    @bot.command()
    async def source(ctx):
        await ctx.send(f"`Repo: https://github.com/DiegoERojas/MarkovDiscordBot`")

    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    user = MainBotClass(3)
    run_Discord_Bot()
