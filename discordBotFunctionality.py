import discord
from discord.ext import commands
import creds
import MarkovTextComposer as mtc

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='.', intents=intents)

class EmbedMessage:
    def __init__(self):
        self.embed = discord.Embed(title="Markov chain",
                                   url="https://en.wikipedia.org/wiki/Markov_chain",
                                   description="",
                                   color=0x4db8ff)
        self.embed.set_footer(text=f"type \'.help\' for a menu of commands.")


class MainBotClass:
    def __init__(self, forceChain):
        self.forceChain = forceChain
        self.forceChainFrequencyCONST = forceChain
        self.autoRunMarkov = False
        self.canForceMarkov = False
        self.numberOfMessages = 0
        self.minMessagesToForceMarkov = forceChain // 2
        self.markovChannels = []
        self.devID = 0


def run_Discord_Bot():
    messageList = []
    listOfWords = []

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready.")
        # Setting the status for the bot
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name="you feed me words"))
        devID = await bot.fetch_user(251087613325344768)
        user.devID = devID

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
            # Takes the current word and appends it to the list before calling markov
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
            markovMessage = EmbedMessage()
            markovMessage.embed.add_field(name="Result: ",
                                          value=f"{userMarkov.unpackingResult()}")
            await ctx.send(embed=markovMessage.embed)
            user.autoRunMarkov = False
            user.canForceMarkov = False
            resettingMarkov()
        else:
            rejectedMarkov = EmbedMessage()
            rejectedMarkov.embed.add_field(name="Please give me time to reference additional messages to the markov chain",
                                           value="")
            await ctx.send(embed=rejectedMarkov.embed)

    bot.remove_command("help")

    @bot.command()
    async def help(ctx):
        helpEmbed = EmbedMessage()
        helpEmbed.embed.add_field(name=".markov",
                                  value="Forces a markov chain based on current data.",
                                  inline=False)
        helpEmbed.embed.add_field(name=".help",
                                  value="Displays a menu of all available commands.",
                                  inline=False)
        helpEmbed.embed.add_field(name=".dev",
                                  value="Who the developer of this bot is (with link to the repo).",
                                  inline=False)
        helpEmbed.embed.add_field(name=".description",
                                  value="Describes what this bot does.",
                                  inline=False)
        helpEmbed.embed.add_field(name=".bug",
                                  value="DMs the developer of the bot to let them know there is an issue occurring.",
                                  inline=False)
        helpEmbed.embed.add_field(name=".mchannels",
                                  value="Displays the channels in which markov is active in.",
                                  inline=False)
        await ctx.send(embed=helpEmbed.embed)

    @bot.command()
    async def description(ctx):
        descriptionEmbed = EmbedMessage()
        descriptionEmbed.embed.add_field(name="Hello, I am a text bot that relies on text from users and composes a markov chain. "
                                              f"This process will occur every {user.forceChainFrequencyCONST} messages or can be forced using the "
                                              f"\'.markov\' command when at least {user.minMessagesToForceMarkov} messages have been sent.",
                                              value="")
        await ctx.send(embed=descriptionEmbed.embed)

    @bot.command()
    async def dev(ctx):
        devID = await bot.fetch_user(251087613325344768)

        creditsEmbed = discord.Embed(title="",
                                     url="",
                                     description=devID.mention,
                                     color=0x4db8ff)
        creditsEmbed.set_author(name="GitHub",
                                url="https://github.com/DiegoERojas/MarkovDiscordBot",
                                icon_url="https://cdn.discordapp.com/avatars/251087613325344768/2e63086e1d0571575001cd60fd4dd02c.webp?size=100")
        creditsEmbed.set_thumbnail(url=f"{devID.avatar}")
        creditsEmbed.set_footer(text=f"type \'.help\' for a menu of commands.")
        await ctx.send(embed=creditsEmbed)

    @bot.command()
    async def bug(ctx):
        devID = await bot.fetch_user(251087613325344768)
        # An embed to notify the channel that their response was acknowledged
        bugEmbed = EmbedMessage()
        bugEmbed.embed.add_field(name=f"A message has been sent to {devID} regarding the issue you are currently facing.",
                                 value="")

        # An embed to send to the dev with the specific server and channel
        dmEmbed = discord.Embed(title="",
                                url="",
                                description=f"Your assistance is needed in {ctx.message.guild.name} "
                                            f"in the {ctx.message.channel.mention} channel.",
                                color=0x4db8ff)
        await devID.send(embed=dmEmbed)
        await ctx.send(embed=bugEmbed.embed)

    @bot.command()
    async def mchannels(ctx):
        # Grabbing each text channel from the server this message was invoked in
        for textChannel in ctx.message.guild.text_channels:
            #
            for members in textChannel.members:
                # If the bot is one of the members of the text channel, add to the list of channels that markov is active in
                if bot.user.id == members.id:
                    user.markovChannels.append(textChannel.name)
        formattedEmbedOutput = ', '.join(user.markovChannels)

        channelsEmbed = EmbedMessage()
        channelsEmbed.embed.add_field(
            name=f"Markov is active in the following channels: ",
            value=f"{formattedEmbedOutput}")
        await ctx.send(embed=channelsEmbed.embed)

    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    """
    The argument is the number of messages the bot will reference before
    automatically running the markov text chain.
    """
    user = MainBotClass(10)
    run_Discord_Bot()
