import discord
import json

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class LogsCog(commands.Cog, name="change setting from logs command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'logs', 
                        aliases= ["log", "setlog", "setlogs", "logchannel"],
                        usage="<true/false>",
                        description="Enable or disable the log system.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def logs(self, ctx, logChannel):

        logChannel = logChannel.lower()

        if logChannel == "true":
            # Create channel
            logChannel = await ctx.guild.create_text_channel(f"{self.bot.user.name}-logs")
            await logChannel.set_permissions(ctx.guild.default_role, read_messages=False)

            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["logChannel"] = logChannel.id
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**LOG CHANNEL WAS ENABLED**", description = f"The log channel was enabled.", color = 0x2fa737) # Green
            embed.set_image(url="https://64.media.tumblr.com/5bb6c4b5e4776179615cfcb5b5a11569/tumblr_pqrf5v8IKO1y1kim6o4_500.gifv")
        else:
            # Read configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)

            # Delete
            logChannel = self.bot.get_channel(data["logChannel"])
            await logChannel.delete()

            # Add modifications
            data["logChannel"] = False
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**LOG CHANNEL WAS DISABLED**", description = f"The log channel was disabled.", color = 0xe00000) # Red
            embed.set_image(url="https://64.media.tumblr.com/5bb6c4b5e4776179615cfcb5b5a11569/tumblr_pqrf5v8IKO1y1kim6o4_500.gif")
        
        await ctx.channel.send(embed = embed)
        
        with open("configuration.json", "w") as config:
            config.write(newdata)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(LogsCog(bot))