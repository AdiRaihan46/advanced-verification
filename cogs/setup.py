import discord
import asyncio
import json

from discord.ext import commands
from discord.utils import get

# ------------------------ COGS ------------------------ #  
def is_allowed(ctx):
    return ctx.message.author.id == 754453123971547266

class SetupCog(commands.Cog, name="setup command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'verify',
                        aliases=["captcha"],
                        usage="<on/off>",
                        description="Enable or disable the captcha system.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()

    async def verify(self, ctx, onOrOff):

        onOrOff = onOrOff.lower()

        if onOrOff == "on":
            embed = discord.Embed(title = f"**Nyssa Verification System**", description = f"**Set up the captcha protection includes the creation of :**\n\n- captcha verification channel\n- log channel\n- temporary role\n\n**Do you want to set up the captcha protection? \"__yes__\" or \"__no__\".**", color = 0xff0000)
            embed.set_image(url="https://miro.medium.com/max/2000/1*7YuxXLpRNzhvWSWnQGuMTg.png")
            await ctx.channel.send(embed = embed)
            # Ask if user are sure
            def check(message):
                if message.author == ctx.author and message.content in ["yes", "no",]:
                    return message.content

            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                if msg.content == "no":
                    await ctx.channel.send("The set up of the captcha protection was abandoned.")
                else:
                    try:
                        loading = await ctx.channel.send("Creation of captcha protection...")

                        # Data
                        with open("configuration.json", "r") as config:
                            data = json.load(config)

                        # Create role
                        temporaryRole = await ctx.guild.create_role(name="untested")
                        # Hide all channels
                        for channel in ctx.guild.channels:
                            if isinstance(channel, discord.TextChannel):
                                await channel.set_permissions(temporaryRole, read_messages=False)
                            elif isinstance(channel, discord.VoiceChannel):
                                await channel.set_permissions(temporaryRole, read_messages=False, connect=False)
                        # Create captcha channel
                        captchaChannel = await ctx.guild.create_text_channel('verification')
                        await captchaChannel.set_permissions(temporaryRole, read_messages=True, send_messages=True)
                        await captchaChannel.set_permissions(ctx.guild.default_role, read_messages=False)
                        await captchaChannel.edit(slowmode_delay= 5)
                        # Create log channel
                        if data["logChannel"] is False:
                            logChannel = await ctx.guild.create_text_channel(f"{self.bot.user.name}-logs")
                            await logChannel.set_permissions(ctx.guild.default_role, read_messages=False)
                            data["logChannel"] = logChannel.id
                        
                        # Edit configuration.json
                        # Add modifications
                        data["captcha"] = True
                        data["temporaryRole"] = temporaryRole.id
                        data["captchaChannel"] = captchaChannel.id
                        newdata = json.dumps(data, indent=4, ensure_ascii=False)

                        with open("configuration.json", "w") as config:
                            config.write(newdata)
                        
                        await loading.delete()
                        embed = discord.Embed(title = f"**CAPTCHA WAS SET UP WITH SUCCESS**", description = f"The captcha was set up with success.", color = 0x2fa737) # Green
                        await ctx.channel.send(embed = embed)
                    except Exception as error:
                        embed = discord.Embed(title=f"**ERROR**", description=f"An error was encountered during the set up of the captcha.\n\n**ERROR :** {error}", color=0xe00000) # Red
                        embed.set_footer(text="Join the Support Server for help!")
                        return await ctx.channel.send(embed=embed)

            
            except (asyncio.TimeoutError):
                embed = discord.Embed(title = f"**TIME IS OUT**", description = f"{ctx.author.mention} has exceeded the response time (30s).", color = 0xff0000)
                await ctx.channel.send(embed = embed)

        elif onOrOff == "off":
            loading = await ctx.channel.send("Deletion of captcha protection...")
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["captcha"] = False
            
            # Delete all
            noDeleted = []
            try:
                temporaryRole = get(ctx.guild.roles, id= data["temporaryRole"])
                await temporaryRole.delete()
            except:
                noDeleted.append("temporaryRole")
            try:  
                captchaChannel = self.bot.get_channel(data["captchaChannel"])
                await captchaChannel.delete()
            except:
                noDeleted.append("captchaChannel")

            # Add modifications
            data["captchaChannel"] = False
            newdata = json.dumps(data, indent=4, ensure_ascii=False)
            # Edit configuration.json
            with open("configuration.json", "w") as config:
                config.write(newdata)
            
            await loading.delete()
            embed = discord.Embed(title = f"**CAPTCHA WAS DELETED DISABLED**", description = f"Why would you do that...", color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
            if len(noDeleted) > 0:
                errors = ", ".join(noDeleted)
                embed = discord.Embed(title = f"**CAPTCHA DELETION ERROR**", description = f"**Error(s) detected during the deletion of the ** ``{errors}``.", color = 0xe00000) # Red
                await ctx.channel.send(embed = embed)


        else:
            embed = discord.Embed(title=f"**ERROR**", description=f"The setup argument must be on or off\nFollow the example : ``{self.bot.command_prefix}setup <on/off>``", color=0xe00000) # Red
            embed.set_footer(text="Join the Support Server for help!")
            return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SetupCog(bot))