
import discord
from discord.ext import commands
from cogs.utils.checks import embed_perms
'''Module for the info command.'''

class Userinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avi(self, ctx, txt: str = None):
        """View bigger version of user's avatar.[prefix]avi @user"""
        if txt:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(txt)
            if not user:
                user = ctx.guild.get_member(int(txt))
            if not user:
                user = self.bot.get_user(int(txt))
            if not user:
                await ctx.send(self.bot.bot_prefix + 'Could not find user.')
                return
        else:
            user = ctx.message.author

        if str(user.avatar_url_as(format='png'))[54:].startswith('a_'):
            avi = user.avatar_url.rsplit("?", 1)[0]
        else:
            avi = user.avatar_url_as(static_format='png')
        if embed_perms(ctx.message):
            em = discord.Embed(colour=0x708DD0)
            em.set_image(url=avi)
            em.set_author(name=user, icon_url='https://images-ext-1.discordapp.net/external/WBQDLWKS8uWe1hQijonvrOsr-gE5QBfESYK2ZD_3L14/https/media.discordapp.net/attachments/608711485849337856/778231733250162703/20200401_155736.gif')
            em.set_footer(text="pretty isn't it?")
            await ctx.send(embed=em)
        else:
            await ctx.send(self.bot.bot_prefix + avi)
        await ctx.message.delete()


def setup(bot):
  bot.add_cog(Userinfo(bot))
