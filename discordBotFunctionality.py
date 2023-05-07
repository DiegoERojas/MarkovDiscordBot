import discord
from discord.ext import commands
import creds
import MarkovTextComposer as mtc
import json

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
        self.serverDict = {}

    def run_Discord_Bot(self):
        messageList = []
        listOfWords = []

        @bot.event
        async def on_ready():
            print(f"{bot.user} is ready.")
            # Setting the status for the bot
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,
                                                                name="IDK"))

        def loadingJSONFile():
            with open("ServerChannels.json", 'r') as f:
                user.serverDict = json.load(f)

        def dumpingJSONFile():
            with open("ServerChannels.json", 'w') as f:
                json.dump(user.serverDict, f)

        def resettingMarkov():
            messageList.clear()
            listOfWords.clear()
            user.numberOfMessages = 0

        @bot.event
        async def on_message(message):
            ctx = await bot.get_context(message)
            loadingJSONFile()
            # If the current guild's text-channels have not been stored
            if str(ctx.message.guild) not in user.serverDict['serverSettings']:
                user.serverDict['serverSettings'] = {str(ctx.message.guild): []}
                user.serverDict['allServerChannels'] = {str(ctx.message.guild): []}
                user.serverDict['allNonprivateServerChannels'] = {str(ctx.message.guild): []}
                '''
                ServerChannels.serverSettings[str(ctx.message.guild)] = []
                ServerChannels.allServerChannels[str(ctx.message.guild)] = []
                ServerChannels.allNonprivateServerChannels[str(ctx.message.guild)] = []
                '''

                # Grabbing each text channel from the server this message was invoked in
                for textChannel in ctx.message.guild.text_channels:
                    # ServerChannels.allServerChannels[str(ctx.message.guild)] += [textChannel.name]
                    user.serverDict['allServerChannels'][str(ctx.message.guild)] += [textChannel.name]
                    for members in textChannel.members:
                        # If the bot is one of the members of the text channel, add to the list of channels that markov is active in
                        if bot.user.id == members.id:
                            # ServerChannels.serverSettings[str(ctx.message.guild)] += [textChannel.name]
                            # ServerChannels.allNonprivateServerChannels[str(ctx.message.guild)] += [textChannel.name]
                            user.serverDict['serverSettings'][str(ctx.message.guild)] += [textChannel.name]
                            user.serverDict['allNonprivateServerChannels'][str(ctx.message.guild)] += [textChannel.name]
                dumpingJSONFile()
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
            loadingJSONFile()
            if str(ctx.message.channel) in user.serverDict['serverSettings'][str(ctx.message.guild)]:
                if user.canForceMarkov:
                    userMarkov = mtc.MarkovComposer(listOfWords, user.forceChainFrequencyCONST)
                    userMarkov.totalNumberOfWords()
                    userMarkov.settingKeyValues()
                    userMarkov.markovOutput()
                    await ctx.send(userMarkov.unpackingResult())
                    user.autoRunMarkov = False
                    user.canForceMarkov = False
                    resettingMarkov()
                else:
                    rejectedMarkov = EmbedMessage()
                    rejectedMarkov.embed.add_field(name="Please give me time to reference additional messages to the markov chain",
                                                   value="")
                    await ctx.send(embed=rejectedMarkov.embed)
            dumpingJSONFile()

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
            helpEmbed.embed.add_field(name=".outputonly",
                                      value="Allows the user (if they are admin) to only output markov chains in the specified"
                                            ", non-private channel. \nFormat: .outputonly <textchannel>",
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
            loadingJSONFile()
            formattedEmbedOutput = ', '.join(user.serverDict['serverSettings'][str(ctx.message.guild)])
            channelsEmbed = EmbedMessage()
            channelsEmbed.embed.add_field(
                name=f"Markov is active in the following channels: ",
                value=f"{formattedEmbedOutput}")
            dumpingJSONFile()
            await ctx.send(embed=channelsEmbed.embed)


        @bot.command()
        @commands.has_permissions(administrator=True)
        async def togglechannel(ctx, message):
            loadingJSONFile()
            toggleBotChannel = EmbedMessage()
            toggleBotChannel.embed.add_field(name="",
                                             value="")

            userMessage = message.replace(".togglechannel", "").lower()

            # If the message contains a valid channel name
            if userMessage in user.serverDict['allServerChannels'][str(ctx.message.guild)]:
                # If the bot can already talk in the channel, then remove it from outputting messages in that channel
                if userMessage in user.serverDict['serverSettings'][str(ctx.message.guild)]:
                    user.serverDict['serverSettings'][str(ctx.message.guild)].remove(userMessage)
                    toggleBotChannel.embed.set_field_at(0,
                                                        name="",
                                                        value=f"{bot.user} can no longer output messages in the \'{userMessage}\' channel.")
                # Otherwise, add that channel to the list of channels the bot can talk in
                elif userMessage in user.serverDict['allNonprivateServerChannels'][str(ctx.message.guild)]:
                    user.serverDict['serverSettings'][str(ctx.message.guild)] += [userMessage]
                    toggleBotChannel.embed.set_field_at(0,
                                                        name="",
                                                        value=f"{bot.user} can now output messages in the \'{userMessage}\' channel.")
                else:
                    # User requested that the bot be allowed to output in a private channel which is not possible
                    # Unless the bot has been given the required roles to access the private channel
                    toggleBotChannel.embed.set_field_at(0,
                                                        name="",
                                                        value=f"{bot.user} cannot access the \'{userMessage}\' channel due to restrictions. Please select a non-private text channel.")
            else:
                toggleBotChannel.embed.set_field_at(0,
                                                    name="",
                                                    value=f"There is no non-private text channel with the name \'{userMessage}\'. Format: \'.TBC <TextChannel>\'.")
            dumpingJSONFile()
            await ctx.send(embed=toggleBotChannel.embed)

        @bot.command()
        @commands.has_permissions(administrator=True)
        async def outputonly(ctx, message):
            loadingJSONFile()
            outputonlyembed = EmbedMessage()
            outputonlyembed.embed.add_field(name="",
                                            value="")
            userMessage = message.replace(".outputonly", "").lower()
            if userMessage in user.serverDict['allNonprivateServerChannels'][str(ctx.message.guild)]:
                user.serverDict['serverSettings'][str(ctx.message.guild)] = [userMessage]
                outputonlyembed.embed.set_field_at(0,
                                                   name="",
                                                   value=f"{bot.user} can now only output messages in the \'{userMessage}\' channel.")
            elif userMessage in user.serverDict['allServerChannels'][str(ctx.message.guild)]:
                outputonlyembed.embed.set_field_at(0,
                                                   name="",
                                                   value=f"{bot.user} cannot access the \'{userMessage}\' channel due to restrictions."
                                                         f" Please select a non-private text channel.")
            else:
                outputonlyembed.embed.set_field_at(0,
                                                   name="",
                                                   value=f"The channel, \'{userMessage}\' does not exist.")
            dumpingJSONFile()
            await ctx.send(embed=outputonlyembed.embed)

        bot.run(creds.botTOKEN)


if __name__ == "__main__":
    """
    The argument is the number of messages the bot will reference before
    automatically running the markov text chain.
    """
    user = MainBotClass(10)
    user.run_Discord_Bot()
