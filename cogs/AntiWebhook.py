import discord
import json
from discord.ext import commands
import datetime

# ------------------------ COGS ------------------------ #  
class AntiWebhook(commands.Cog):
    def __init__(self, client):
        self.client = client


# ------------------------------------------------------ #  
    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in webhook.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_create):
          if str(i.user.id) in whitelisted[str(webhook.guild.id)]:
            return
          

          await webhook.guild.kick(i.user, reason="Anti-Nuke: Creating Webhooks")
          await i.target.delete()
          return

def setup(bot):
    bot.add_cog(AntiWebhook(bot))