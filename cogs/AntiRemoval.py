import discord
import json
from discord.ext import commands
import datetime

# ------------------------ COGS ------------------------ #  
class AntiRemoval(commands.Cog):
    def __init__(self, client):
        self.client = client


# ------------------------------------------------------ #  
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):
      
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
    
          await guild.ban(i.user, reason="Anti-Nuke: Banning Members")
          await guild.kick(i.user, reason="Anti-Nuke: Banning Members")
          return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
      
          if str(i.user.id) in whitelisted[str(i.guild.id)]:
            return
          if i.target.id == member.id:
             await i.user.kick()
             return

    @commands.Cog.listener()
    async def on_member_join(self, member):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add):
      
          if str(i.user.id) in whitelisted[str(member.guild.id)]:
            return
          
          if member.bot:
             await member.ban(reason="Anti-Nuke: Unknown Bot")
             await i.user.kick(reason="Anti-Nuke: Added Unknown Bot")
             return
          
def setup(bot):
    bot.add_cog(AntiRemoval(bot))