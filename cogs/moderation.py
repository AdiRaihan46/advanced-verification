import discord
from discord.ext import commands
import asyncio
import data

blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
yellow = 0xfff900
gray = 0x6d6868

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Ban a specified member")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        channel_message = discord.Embed(title=f"{member.name} has been banned by {ctx.author.name}.", description=f"Reason: {reason}", color=red)
        user = discord.Embed(title=f"You have been banned by {ctx.author.name} in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)

        if member == ctx.author:
          await ctx.send("You cannot ban yourself.")
        else:
          try:
              await member.send(embed=user)
          except:
              await ctx.send("I could not DM the User. I will still ban.")
          await member.ban(reason = reason, delete_message_days=0) 
          await ctx.message.add_reaction("✅")
          await ctx.send(embed=channel_message)
        


    @commands.command(name='unban')
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.message.add_reaction("✅")
        await ctx.guild.unban(user)
        embed1 = discord.Embed(description=f"Member has been unbanned successfully", color=yellow)
        await ctx.send(embed=embed1)
        


    @commands.command(description="Kick a specified member")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):   
        channel_message = discord.Embed(title=f"{member.name} has been kicked by {ctx.author.name}.", description=f"Reason: {reason}", color=red)
        user = discord.Embed(title=f"You have been kicked by {ctx.author.name} in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)

        if member == ctx.author:
          await ctx.send("You cannot kick yourself.")
        else:
          try:
              await member.send(embed=user)
          except:
              await ctx.send("I could not DM the User. I will yeet him/her anyways.")
          await member.kick(reason = reason) 
          await ctx.message.add_reaction("✅")
          await ctx.send(embed=channel_message) 
        
        


    @commands.command(description="Mute a specified user.")
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name=data.MUTE_ROLE)
        
        channel_message = discord.Embed(title=f"{member.name} has been muted.", description=f"Reason: {reason}", colour=red) 
        user = discord.Embed(title=f"You have been muted by {ctx.author.name} in {ctx.guild.name}.", description=f"Reason: {reason}", color=red) 
        try:
            await member.send(embed=user)
        except:
            await ctx.send("I could not DM the User. I will still mute")
        try:
            await member.add_roles(mutedRole, reason=reason)
            await ctx.message.add_reaction("✅")
            await ctx.send(embed=channel_message)
        except: 
            await ctx.send("There is no mute role, so I could not mute the user")
            await ctx.message.add_reaction("❌") 


      
    @commands.command(description="Unmute a specified user.")
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name=data.MUTE_ROLE) 
        try:
            await member.remove_roles(mutedRole)
            await ctx.message.add_reaction("✅")
            await ctx.send(f"{member.name} is unmuted.")
        except:
            await ctx.send("The user is not muted")
            await ctx.message.add_reaction("❌") 

   
def setup(bot):
  bot.add_cog(Moderation(bot))