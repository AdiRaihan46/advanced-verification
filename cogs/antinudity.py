import discord
import json

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class AntiNudityCog(commands.Cog, name="change setting from anti nudity command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'antinudity', 
                        aliases= ["nudity", "porn"],
                        usage="<true/false>",
                        description="Enable or disable the nudity image protection.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def antinudity(self, ctx, antiNudity):

        antiNudity = antiNudity.lower()

        if antiNudity == "true":
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiNudity"] = True
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI NUDITY WAS ENABLED**", description = f"You are the brave one!.", color = 0x2fa737) # Green
            embed.set_image(url="https://comicvine1.cbsistatic.com/uploads/original/11134/111349002/6935609-4283522193-tumbl.gif")
        else:
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiNudity"] = False
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI NUDITY WAS DISABLED**", description = f"I see what you are...", color = 0xe00000) # Red
            embed.set_image(url="https://i.pinimg.com/originals/36/3a/80/363a8032da8414b27438955ea5e83dc6.gif")
        
        await ctx.channel.send(embed = embed)
        
        with open("configuration.json", "w") as config:
            config.write(newdata)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AntiNudityCog(bot))