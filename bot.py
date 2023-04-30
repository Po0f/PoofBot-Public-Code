import discord
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
import os

TOKEN = ''
allowed_channels = [1060182420059586580, 1086982623194255431, 1060183489510645911]
exempt_roles = ['1060169362088136744', '1086956623190311012', '1085622436021674096']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

import discord
from discord.ext import commands
import random

@bot.command()
async def cock(ctx):
    await ctx.send(f"https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.ebayimg.com%2Fimages%2Fg%2F8uUAAOSwnkldavW6%2Fs-l500.png&tbnid=OjUR7KuqIM2hvM&vet=12ahUKEwiA2OSO0_n9AhX5TKQEHXsHAa8QMygBegUIARCQAQ..i&imgrefurl=https%3A%2F%2Fwww.ebay.co.uk%2Fitm%2F113872577280&docid=QTgLAOwMimItVM&w=500&h=500&q=penis%20drawing&ved=2ahUKEwiA2OSO0_n9AhX5TKQEHXsHAa8QMygBegUIARCQAQ")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"Pong! Latency: {latency:.2f}ms")

@bot.command()
async def roll(ctx):
    random_number = random.randint(1, 100)
    await ctx.send(f"{ctx.author.mention} rolled {random_number}!")

@bot.command()
async def flip(ctx):
    coin = random.choice(["heads", "tails"])
    await ctx.send(f"{ctx.author.mention} flipped a coin and got {coin}!")

@bot.command()
async def joke(ctx):
    jokes = [
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why did the bicycle fall over? Because it was two tired!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fake noodle? An impasta!",
        "Why don't scientists trust atoms? Because they make up everything!",
    ]
    await ctx.send(random.choice(jokes))

# Responds with a random fun fact
@bot.command()
async def fact(ctx):
    facts = [
        "The shortest war in history was between Zanzibar and England in 1896. Zanzibar surrendered after just 38 minutes.",
        "The only letter that doesn't appear in any U.S. state name is 'Q'.",
        "A group of flamingos is called a flamboyance.",
        "The world's largest grand piano was built by a 15-year-old in New Zealand. It's nine feet long and has 85 keys.",
        "The longest word in the English language has 189,819 letters.",
        "There is a law in France that anyone can marry a dead person if they want.",
    ]
    await ctx.send(random.choice(facts))

@bot.command()
async def dog(ctx):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    if response.status_code == 200:
        data = response.json()
        image_url = data['message']
        embed = discord.Embed(title="Woof! 🐶", color=0x8E44AD)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, something went wrong while fetching the dog image. :(")

@bot.command()
async def cat(ctx):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    if response.status_code == 200:
        data = response.json()[0]
        image_url = data['url']
        embed = discord.Embed(title="Meow! 🐱", color=0x8E44AD)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, something went wrong while fetching the cat image. :(")

log_channel_id = 1060183489510645911

allowed_roles = [1060169362088136744, 1086956623190311012]

@bot.event
async def on_message(message):
    if message.channel.id == 1060183489510645911:
        log_channel = bot.get_channel(1060183489510645911)
        await log_channel.send(f"{message.author.name}#{message.author.discriminator} said: {message.content}")
    
    await bot.process_commands(message)

@bot.event
async def on_guild_role_delete(role):
    """Monitor for mass role deletions within a guild."""
    guild = role.guild
    log_channel = discord.utils.get(guild.text_channels, name='1060183489510645911')

    if len(guild.roles) < len(bot.cached_roles):
        await log_channel.send(f'Role {role.name} was deleted from {guild.name} without authorization.')
        await guild.create_role(name=role.name, permissions=discord.Permissions.none(), reason='Unauthorized role deletion')

@bot.event
async def on_member_join(member):
    """Automatically ban members who join with a certain name or profile picture."""
    guild = member.guild
    log_channel = discord.utils.get(guild.text_channels, name='1060183489510645911')

    if member.name.startswith('UnauthorizedName'):
        await member.ban(reason='Unauthorized member name')
        await log_channel.send(f'{member.display_name} was banned from {guild.name} for having an unauthorized name.')

    if member.avatar_url.startswith('https://example.com/unauthorized-avatar.png'):
        await member.ban(reason='Unauthorized profile picture')
        await log_channel.send(f'{member.display_name} was banned from {guild.name} for having an unauthorized profile picture.')

@bot.event
async def on_member_remove(member):
    """Monitor for mass member deletions within a guild."""
    guild = member.guild
    log_channel = discord.utils.get(guild.text_channels, name='1060183489510645911')
    
    if member.guild.me.guild_permissions.view_audit_log:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target == member:
                return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target == member:
                return

    if len(guild.members) < len(bot.cached_members):
        await log_channel.send(f'{member.display_name} was removed from {guild.name} without authorization.')
        await guild.ban(member, reason='Unauthorized member deletion')

@bot.event
@commands.has_role("1060945772293673041")
async def create_antinuke_channel(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name="private")
    if not existing_channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(name="antinuke-log", overwrites=overwrites)
        await channel.send("Anti-nuke logs will be displayed here.")
        await ctx.send("Anti-nuke channel created.")
    else:
        await ctx.send("The anti-nuke channel already exists.")
async def on_guild_channel_create(channel):
    """Delete any newly created channels within a guild."""
    guild = channel.guild
    log_channel = discord.utils.get(guild.text_channels, name='#1060183489510645911')

    await channel.delete()
    await log_channel.send(f'Channel {channel.name} was deleted because it was created without authorization.')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await ctx.send(f'Kicked {user.mention}. Reason: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)
    await ctx.send(f'Banned {user.mention}. Reason: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user):
    banned_users = await ctx.guild.bans()
    user_name, user_discriminator = user.split('#')

    for ban_entry in banned_users:
        banned_user = ban_entry.user

        if (banned_user.name, banned_user.discriminator) == (user_name, user_discriminator):
            await ctx.guild.unban(banned_user)
            await ctx.send(f'Unbanned {banned_user.mention}')
            return

    await ctx.send(f'Could not find user {user}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)

    await user.add_roles(muted_role, reason=reason)
    await ctx.send(f'Muted {user.mention}. Reason: {reason}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if muted_role in user.roles:
        await user.remove_roles(muted_role, reason=reason)
        await ctx.send(f'Unmuted {user.mention}. Reason: {reason}')
    else:
        await ctx.send(f'{user.mention} is not muted')

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: discord.Member, *, reason=None):
    await ctx.send(f'Issued a warning to {user.mention}. Reason: {reason}')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in allowed_channels:
        if '@625372456282095654' in message.content or '@673129333623357463' in message.content:
            exempt = False
            for role in message.author.roles:
                if role.name in exempt_roles:
                    exempt = True
                    break
            if not exempt:
                await message.channel.send(f"{message.author.mention}, Kindly Do not Ping Poof~  or Markyss for irrelivant reasons and please read Rule 8")
                role = discord.utils.get(message.guild.roles, name='Muted')
                await message.author.add_roles(1089197830293442560)
                await message.author.send("You've been muted for 1 day for mentioning @Poof~ or @Feeqz")
                await message.delete()
                await asyncio.sleep(86400)
                await message.author.remove_roles(role)
                return

    print(f"{message.author}: {message.content} in {message.channel}")
    await bot.process_commands(message)

bot.run(TOKEN)
