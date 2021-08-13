from discord.ext import commands
import datetime
import discord
import os
start_time = datetime.datetime.utcnow()


# ------------------------ COGS ------------------------ #  
class extra(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


# ------------------------------------------------------ #  
  @commands.command()
  async def setup(self, ctx):
      embed = discord.Embed(description=f"**Anti-Nuke Information!**")
      embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
      embed.add_field(name=f"**Categories:**", value=f":heart: `— whitelist`\n:drop_of_blood: `— unwhitelist`\n:hearts: `— whitelisted`\n:diamonds: `— unbanall`\n:mending_heart: `— anti`\n", inline=False)
      embed.set_footer(text='Anti Nuke Setup')

      await ctx.send(embed=embed)

  @commands.command()
  async def fun(self, ctx):
    embed = discord.Embed(description=f"**Commands:**")
    embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
    embed.add_field(name=f"**Fun**", value=f"🐈 `— cat`\n🦆 `— duck`\n☕ `— coffee`\n🤣 `— meme`\n🎱 `— ball`\n🐕 `— dog`")
    embed.set_footer(text='SomeRandomApi')
    await ctx.send(embed=embed)

  @commands.command()
  async def emojis(self, ctx):
    embed = discord.Embed(description=f"**Commands:**")
    embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
    embed.add_field(name=f"**Emoji Utils**", value=f":heart: `— emojisteal` <emote>\n:drop_of_blood: `— emojiadd` <url>\n:diamonds: `— emojiremove` <emote>\n:mending_heart: `— emojiurl` <emote>\n:cupid: `— emojiurl` <list> \n:heart_on_fire: `— emoji` <name>")
    embed.set_footer(text='Emoji Utils')
    await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(extra(bot))
