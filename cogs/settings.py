import discord
import json

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class SettingsCog(commands.Cog, name="settings command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'settings',
                        description="Display the settings.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def settings (self, ctx):

        with open("configuration.json", "r") as config:
            data = json.load(config) 
            captcha = data["captcha"] 
            captchaChannel = data["captchaChannel"]  
            logChannel = data["logChannel"]
            temporaryRole = data["temporaryRole"]
            roleGivenAfterCaptcha = data["roleGivenAfterCaptcha"]
            minAccountAge = data["minAccountDate"]
            antispam = data["antiSpam"]
            allowSpam = data["allowSpam"]
            antiNudity = data["antiNudity"]
            antiProfanity =  data["antiProfanity"]
            
            minAccountAge = int(minAccountAge/3600)

            allowSpam2= ""
            if len(allowSpam) == 0:
                allowSpam2 = "None"
            else:
                for x in allowSpam:
                    allowSpam2 = f"{allowSpam2}<#{x}>, "

            if roleGivenAfterCaptcha is not False:
                roleGivenAfterCaptcha = f"<@&{roleGivenAfterCaptcha}>"
            if captchaChannel is not False:
                captchaChannel = f"<#{captchaChannel}>"
            if logChannel is not False:
                logChannel = f"<#{logChannel}>"
            
        embed = discord.Embed(title=f"**SERVER SETTINGS**", description=f"[**Support Server**](https://discord.gg/RxB7AEvJ)", color=0xdeaa0c)
        embed.add_field(name= f"**MINIMUM ACCOUNT AGE** - ``({self.bot.command_prefix}minaccountage <number (hours)>)``", value= f"Minimum account age : **{minAccountAge} hours**", inline=False)
        embed.add_field(name= f"**ANTI SPAM** - ``({self.bot.command_prefix}antispam <true/false>)``", value= f"Anti spam enabled : **{antispam}**", inline=False)
        embed.add_field(name= f"**ALLOW SPAM** - ``({self.bot.command_prefix}allowspam <#channel> (remove))``", value= f"Channel where spam is allowed : **{allowSpam2[:-2]}**", inline=False)
        embed.add_field(name= f"**ANTI NUDITY** - ``({self.bot.command_prefix}antinudity <true/false>)``", value= f"Anti nudity image enabled : **{antiNudity}**", inline=False)
        embed.set_footer(text="Join the Support Server for help!")
        embed.set_image(url="https://img.cinemablend.com/filter:scale/quill/1/7/e/2/0/9/17e209db7c0e1ff6376bd157ad3514d273a8fd49.jpg?fw=1200")
        return await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SettingsCog(bot))