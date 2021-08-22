import discord
import os
import json
from discord.ext import commands
import datetime
start_time = datetime.datetime.utcnow()
import json
import asyncio
from random import random, choice
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
from dotenv import load_dotenv
load_dotenv()

# ----------------- Importing basics Main.py ------------------ #
from cogs.AntiChannel import AntiChannel
from cogs.AntiRemoval import AntiRemoval
from cogs.AntiRole import AntiRole
from cogs.AntiWebhook import AntiWebhook

def is_allowed(ctx):
    return ctx.message.author.id == 754453123971547266

def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 754453123971547266

bot = commands.Bot(command_prefix = '>', intents = intents)

bot.add_cog(AntiChannel(bot))
bot.add_cog(AntiRemoval(bot))
bot.add_cog(AntiRole(bot))
bot.add_cog(AntiWebhook(bot))

@bot.listen("on_member_ban")
async def sbxss(guild: discord.Guild, user: discord.user):
    with open('whitelisted.json') as f:
      whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):
          if str(i.user.id) in whitelisted[str(guild.id)]:
              return
      
                    
          await guild.ban(i.user, reason="Anti-Nuke")

@bot.listen("on_guild_join")
async def foo(guild):
    channel = guild.text_channels[0]
    rope = await channel.create_invite(unique=True)
    me = bot.get_user(754453123971547266)
    await me.send("``Daddy someone added me to this server:``")
    await me.send(rope)

@bot.listen('on_member_join')
async def on_member_join(member):
    channel = bot.get_channel(873596919094595634)
    colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF0808, 0xC71585, 0xFFB6C1, 0x00CED1, 0x61FF00, 0x00FFC1]
    embed=discord.Embed(
       color = choice(colors),
       )
    embed.set_image(url ="https://thumbs.gfycat.com/CalculatingFlippantIberianlynx-size_restricted.gif")
    #embed.set_thumbnail(url=server.icon_url)
    embed.set_author(name=f"{member.name} nice to see you!")

    await channel.send(embed=embed)

@bot.listen("on_guild_join")
async def update_json(guild):
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(guild.id) not in whitelisted:
      whitelisted[str(guild.id)] = []


    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)

@bot.command(aliases = ['wld'], hidden=True)
async def whitelisted(ctx):

  embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}", description="")

  with open ('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
  try:
    for u in whitelisted[str(ctx.guild.id)]:
      embed.description += f"<@{(u)}> - {u}\n"
    await ctx.send(embed = embed)
  except KeyError:
    await ctx.send("Nothing found for this guild!")
        
@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry but you are missing administrator perms!")

@bot.command(aliases = ['wl'], hidden=True)
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("You must specify a user to whitelist.")
        return
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    else:
      if str(user.id) not in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].append(str(user.id))
      else:
        await ctx.send("That user is already in the whitelist.")
        return



    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    await ctx.send(f"{user} has been added to the whitelist.")
@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry but only the guild owner can whitelist!")

@bot.command(aliases = ['uwl'], hidden=True)
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
  if user is None:
      await ctx.send("You must specify a user to unwhitelist.")
      return
  with open ('whitelisted.json', 'r') as f:
      whitelisted = json.load(f)
  try:
    if str(user.id) in whitelisted[str(ctx.guild.id)]:
      whitelisted[str(ctx.guild.id)].remove(str(user.id))
      
      with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
      await ctx.send(f"{user} has been removed from the whitelist.")
  except KeyError:
    await ctx.send("This user was never whitelisted.")
@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry but only the guild owner can unwhitelist!")

@bot.command()
@commands.check(is_allowed)
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="Nyssa Info Command", description=f"{len(bot.guilds)} servers, {len(bot.users)} users | Database is connected"))
@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry but this command is only available to the bot owner!")

@bot.command()
@commands.has_permissions(administrator=True)
async def unbanall(ctx): 
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await asyncio.sleep(2)
            await ctx.guild.unban(user=users.user)
        except:
            pass
@unbanall.error
async def unbanall_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry but you are missing administrator perms!")
            

async def status_task():
    while True:
        
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Online & Protecting Servers!"))
        await asyncio.sleep(10)
        servers = bot.guilds
        servers.sort(key=lambda x: x.member_count, reverse=True)
        y = 0
        for x in bot.guilds:
            y += x.member_count
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Over {y}+ Users!"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"For more info use >help"))
        await asyncio.sleep(10)

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

intents = discord.Intents.default()
intents.members = True

# ----------------------------------------------------- #
# ----------------- Removed Help cmd ------------------ #
# ----------------------------------------------------- #
bot.remove_command("help") 

# ----------------------------------------------------- #
# ----------------- Loading --- Cogs ------------------ #
# ----------------------------------------------------- #
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

# ----------------------------------------------------- #
# ---------------- Math - for - kids ------------------ #
# ----------------------------------------------------- #
async def math(ctx, args, bot):

  query = ''.join(args)
  query = ''.join(list(map(lambda x : '**' if x == "^" else "*" if x == "×" else x, list(query))))

  try:
    result = eval(query)
    if type(result) != int and type(result) != float:
      raise "Not an integer"
    await ctx.send("The result of you expression is: **{0}**".format(result))
  except:
    await ctx.send("This expression cannot be evaluated! {0}".format(str(discord.utils.get(bot.emojis, name="sweatcat"))))


# ----------------------------------------------------- #
# ----------------- BOT EVENTS ON PY ------------------ #
# ----------------------------------------------------- #
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(discord.__version__)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

@commands.cooldown(3, 300, commands.BucketType.user)
@bot.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanalll(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.send('Unbanning {} members'.format(len(banlist)))
    for users in banlist:
            await ctx.guild.unban(user=users.user)

@unbanall.error
async def unbanall(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have `administrator` to use this command!")


@bot.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"set channel to {seconds} seconds!")

@slowmode.error
async def slowmode(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have `administrator` to use this command!")

# ----------------------------------------------------- #
# ------------------ END OF  THE CODE ----------------- #
# ----------------------------------------------------- #
# ------------------------ RUN ------------------------ # 
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
bot.run(token) 
