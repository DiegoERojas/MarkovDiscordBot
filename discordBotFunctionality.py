import discord
from discord.ext import commands
import creds
import MarkovTextComposer as mtc
import ServerChannels

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
        self.devID = 0
        self.allChannels = []
        self.getChannels = False
        self.allNonPrivateChannels = []  # List of all Non-private text channels, immutable


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
        ctx = await bot.get_context(message)
        # Run the block of code first
        if not user.getChannels:
            # Adding the current server as a key with an empty list as its value
            ServerChannels.serverSettings[str(ctx.message.guild)] = []
            # Grabbing each text channel from the server this message was invoked in
            for textChannel in ctx.message.guild.text_channels:
                user.allChannels.append(textChannel.name)
                for members in textChannel.members:
                    # If the bot is one of the members of the text channel, add to the list of channels that markov is active in
                    if bot.user.id == members.id:
                        ServerChannels.serverSettings[str(ctx.message.guild)] += [textChannel.name]
                        user.allNonPrivateChannels.append(textChannel.name)
            user.getChannels = True

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
            await markov(ctx)
        await bot.process_commands(message)

    @bot.command()
    async def markov(ctx):
        # If the bot can talk in the current channel
        if str(ctx.message.channel) in ServerChannels.serverSettings[str(ctx.message.guild)]:
            if user.canForceMarkov:
                userMarkov = mtc.MarkovComposer(listOfWords, user.forceChainFrequencyCONST)
                userMarkov.totalNumberOfWords()
                userMarkov.settingKeyValues()
                userMarkov.markovOutput()
                '''
                markovMessage = EmbedMessage()
                markovMessage.embed.add_field(name="Result: ",
                                              value=f"{userMarkov.unpackingResult()}")
                await ctx.send(embed=markovMessage.embed)
                '''
                await ctx.send(userMarkov.unpackingResult())
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
        helpEmbed.embed.add_field(name=".botchannels",
                                  value="Displays the channels in which markov is active in.",
                                  inline=False)
        helpEmbed.embed.add_field(name=".togglechannel",
                                  value="Allows the user (if they are an admin) to allow or deny "
                                        "the bot access to certain text channels within the server. \nFormat: .togglechannel "
                                        "<textchannel>",
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
        creditsEmbed.set_footer(text=f"type \'.help\' for a menu of commands.")
        print(f"dictionary: {ServerChannels.serverSettings}")
        print(f"all channels: {user.allChannels}")
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
    async def botchannels(ctx):
        formattedEmbedOutput = ', '.join(ServerChannels.serverSettings[str(ctx.message.guild)])

        channelsEmbed = EmbedMessage()
        channelsEmbed.embed.add_field(
            name=f"Markov is active in the following channels: ",
            value=f"{formattedEmbedOutput}")
        for i in ServerChannels.serverSettings:
            print(f"Key: {i}\n Value: {ServerChannels.serverSettings[i]}")
        await ctx.send(embed=channelsEmbed.embed)


    @bot.command()
    @commands.has_permissions(administrator=True)
    async def togglechannel(ctx, message):

        toggleBotChannel = EmbedMessage()
        toggleBotChannel.embed.add_field(name="",
                                         value="")

        userMessage = message
        userMessage = userMessage.replace(".TBC", "").lower()

        # If the message contains a valid channel name
        if userMessage in user.allChannels:
            # If the bot can already talk in the channel, then remove it from outputting messages in that channel
            if userMessage in ServerChannels.serverSettings[str(ctx.message.guild)]:
                ServerChannels.serverSettings[str(ctx.message.guild)].remove(userMessage)
                toggleBotChannel.embed.set_field_at(0,
                                                    name="",
                                                    value=f"{bot.user} can no longer output messages in the \'{userMessage}\' channel.")
                await ctx.send(embed=toggleBotChannel.embed)

            # Otherwise, add that channel to the list of channels the bot can talk in
            else:

                if userMessage in user.allNonPrivateChannels:
                    ServerChannels.serverSettings[str(ctx.message.guild)] += [userMessage]
                    toggleBotChannel.embed.set_field_at(0,
                                                        name="",
                                                        value=f"{bot.user} can now output messages in the \'{userMessage}\' channel.")
                    await ctx.send(embed=toggleBotChannel.embed)
                # User requested that the bot be allowed to output in a private channel which is not possible
                # Unless the bot has been given the required roles to access the private channel
                else:
                    toggleBotChannel.embed.set_field_at(0,
                                                        name="",
                                                        value=f"{bot.user} cannot access the \'{userMessage}\' channel due to restrictions. Please select a non-private text channel.")
                    await ctx.send(embed=toggleBotChannel.embed)

        else:
            toggleBotChannel.embed.set_field_at(0,
                                                name="",
                                                value=f"There is no non-private text channel with the name \'{userMessage}\'. Format: \'.TBC <TextChannel>\'.")
            await ctx.send(embed=toggleBotChannel.embed)
        for i in ServerChannels.serverSettings:
            print(f"Key: {i}\nValue: {ServerChannels.serverSettings[i]}")

    bot.run(creds.botTOKEN)


if __name__ == "__main__":
    """
    The argument is the number of messages the bot will reference before
    automatically running the markov text chain.
    """
    user = MainBotClass(10)
    run_Discord_Bot()
