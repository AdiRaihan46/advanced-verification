import discord
import json

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class AntiSpamCog(commands.Cog, name="change setting from anti spam command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'antispam', 
                        usage="<true/false>",
                        description="Enable or disable the spam protection.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def antispam(self, ctx, antiSpam):

        antiSpam = antiSpam.lower()

        if antiSpam == "true":
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiSpam"] = True
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI SPAM WAS ENABLED**", description = f"The anti spam was enabled.", color = 0x2fa737) # Green
            embed.set_image(url="https://i.pinimg.com/originals/37/ba/c1/37bac196993a5d12551354f60c59a8bb.gif")
        else:
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiSpam"] = False
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI SPAM WAS DISABLED**", description = f"The anti spam was disabled.", color = 0xe00000) # Red
            embed.set_image(url="https://i.pinimg.com/originals/37/ba/c1/37bac196993a5d12551354f60c59a8bb.gif")
        
        await ctx.channel.send(embed = embed)
        
        with open("configuration.json", "w") as config:
            config.write(newdata)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AntiSpamCog(bot))