import discord

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'help',
                        usage="(commandName)",
                        description = "Display the help message.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def help(self, ctx, commandName=None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break 
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                if stop:
                    break 

            if commandName2 is None:
                await ctx.channel.send("No command found!")   
            else:
                embed = discord.Embed(title=f"**{commandName2.name.upper()} COMMAND :**", description="[**Support Server**](https://discord.gg/RxB7AEvJ)", color=0xdeaa0c)
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(name=f"**NAME :**", value=f"{commandName2.name}", inline=False)
                aliases = ""
                if len(commandName2.aliases) > 0:
                    for aliase in commandName2.aliases:
                        aliases = aliase
                else:
                    commandName2.aliases = None
                    aliases = None
                embed.add_field(name=f"**ALIASES :**", value=f"{aliases}", inline=False)
                if commandName2.usage is None:
                    commandName2.usage = ""
                embed.add_field(name=f"**USAGE :**", value=f"{self.bot.command_prefix}{commandName2.name} {commandName2.usage}", inline=False)
                embed.add_field(name=f"**DESCRIPTION :**", value=f"{commandName2.description}", inline=False)
                embed.set_footer(text="Join the Support Server if you need help!")
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"__**Help page of {self.bot.user.name.upper()}**__", description="[**Support Server**](https://discord.gg/RxB7AEvJ)", color=0xdeaa0c)
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            embed.add_field(name=f"__COMMANDS :__", value=f"**{self.bot.command_prefix}help (command) :**\n`Display the help list`\n**{self.bot.command_prefix}setup (Anti Nuke)**\n `antirole` `antiremoval` `antichannel` `antiwebhook`\n**{self.bot.command_prefix}fun (Interactions)**\n `memes` `pictures`\n**{self.bot.command_prefix}emojis (Utils)**\n`emojisteal` `emojiadd` `emojiremove` `emojiurl`\n\n:tools: **settings**\n:bar_chart: **minaccountage <number>**\n:underage: **antinudity <true/false>**\n:drop_of_blood: **antispam <true/false>**\n:beginner: **allowspam <channel>**\n:closed_lock_with_key: **lock | unlock <channel/ID>**\n:pencil: **userinfos <user>**\n:warning: **kick <user/ID>**\n:warning: **ban <user/ID>**", inline=False)
            embed.set_footer(text="Join the Support Server if you need help!")
            embed.set_image(url="https://images.videociety.de/CoverWide/7B00F0ED5A6FBF8CA6D6D7431BD9B13A9166F42F_525x252.jpg")
            await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))