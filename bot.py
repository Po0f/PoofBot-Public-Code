import discord
from discord.ext import commands
import datetime
import os


TOKEN = ''
allowed_channels = [1060182420059586580, 1086982623194255431, 1060183489510645911] #Change Channel ID
exempt_roles = ['1060169362088136744', '1086956623190311012', '1085622436021674096'] #Change role ID

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


@bot.command()
async def link(ctx, *, ingame_name):
    user = ctx.author
    now = datetime.datetime.utcnow()
    player_stats_url = f'https://stats.pika-network.net/player/{ingame_name}'
    embed = discord.Embed(title='Account Information', color=0x00ff00)
    embed.add_field(name='Username', value=user.mention, inline=False)
    embed.add_field(name='Ingame Name', value=f'[Link]({player_stats_url})', inline=False)
    embed.add_field(name='Date Linked', value=now.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    private_channel = bot.get_channel(1097601360217772052, 1102128412954464307) #change channel ID
    await private_channel.send(embed=embed)
    role = discord.utils.get(ctx.guild.roles, name='Linked user')
    await ctx.author.add_roles(role)
    await ctx.send(f'{user.mention} thanks for linking, you will receive your role within 24 hours!')

@bot.command()
async def info(ctx):
    user = ctx.author
    member = ctx.guild.get_member(user.id)
    linked_role = discord.utils.get(ctx.guild.roles, id=1097608912229908580) #change role ID
    if linked_role in member.roles:
        # user is linked
        # get linked info and send in the same channel as command was invoked
        # you can reuse the same code from link command
        ingame_name = "Some ingame name" # replace with actual ingame name
        now = datetime.datetime.utcnow()
        embed = discord.Embed(title='Account Information', color=0x00ff00)
        embed.add_field(name='Username', value=user.mention, inline=False)
        embed.add_field(name='Account Link', value=f"Account Is Linked", inline=False)
        embed.add_field(name='Date Linked', value=now.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Account Information', color=0x00ff00)
        embed.add_field(name='Username', value=user.mention, inline=False)
        embed.add_field(name='Account Linked', value=f"Account Is Not Linked", inline=False)
        embed.add_field(name='Date Linked', value=now.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
      

bot.run(TOKEN)
