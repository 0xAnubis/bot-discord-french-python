import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
from discord.utils import get
from discord.ext.commands import command, cooldown, BucketType, CommandOnCooldown
import sys
from discord import Embed, utils
import aiohttp
import os
import json
import datetime
import youtube_dl
import shutil
from os import system
import urllib.parse, urllib.request, re
import time
import asyncio
import traceback
import sqlite3

client = commands.Bot(command_prefix = '.')

def allowed(ctx):
    return ctx.author.id == Your discord ID

queues = {}

players = {}

@client.event
async def on_ready():
    print('Le bot est activé')
    change_status.start()

status = cycle(['.help', 'Backdoor'])

    
client.remove_command('help')
            

@tasks.loop(seconds=4)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
@cooldown(1, 2, commands.BucketType.guild)
async def ping(ctx):
    embed = discord.Embed(description=f'Pong! :ping_pong:  {round(client.latency * 1000)}ms', colour=discord.Color.green())
    await ctx.send(embed=embed)

@client.command(aliases=['8ball'])
@cooldown(1, 2, commands.BucketType.guild)
async def _8ball(ctx, *, question):
    responses = ['C\'est certain',
                 'Oui',
                 'Non',
                 'Il y a de fortes chances',
                 'Euh, attendez, je reviens',
                 'Mes sources disent que non',
                 'Inchallah',
                 'Plutot oui',
                 'Sûrement pas',
                 'Pas du tout',
                 'Certainement pas',
                 'Je ne pense pas',]
    embed = discord.Embed(description=f'Question: {question}\nRéponse: {random.choice(responses)}', colour=discord.Color.red())
    await ctx.send(embed=embed)



@client.command()
@cooldown(1, 3, commands.BucketType.guild)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@client.command()
@cooldown(1, 2, commands.BucketType.guild)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(description=f":o: ┃ {member} s'est fait emprisonner dans le nouveau monde car il a {reason}", colour=discord.Color.red())
        await ctx.send(embed=embed)

@client.command()
@cooldown(1, 2, commands.BucketType.guild)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason):
    await member.ban(reason=reason)
    embed = discord.Embed(description=f":x: ┃ {member} s'est fait tué dans le nouveau monde car il a {reason}", colour=discord.Color.red())
    await ctx.send(embed=embed)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        embed = discord.Embed(description=f":no_entry: ┃ Veuillez réessayer dans {error.retry_after:,.2f} secondes ", colour=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(description=":no_entry: ┃ Vous n'êtes pas dans un salon NSFW", colour=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description=":no_entry: ┃ Vous n'avez pas la permission pour utiliser cette commande", colour=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingAnyRole):
        embed = discord.Embed(description=":no_entry: ┃ Vous n'êtes pas DJ", colour=discord.Color.red())
        await ctx.send(embed=embed)



@client.command()
@cooldown(1, 2, commands.BucketType.guild)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    await ctx.message.delete()
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(description=f":white_check_mark: ┃ {user.mention} s'est fait déban", colour=discord.Color.red())
            await ctx.send(embed=embed)
            return


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(title=":gear: Liste des commandes :",
    colour=discord.Color.green())
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/761610075852242954/9656a9cb7f1f763f3bdca481c8c6a140.webp?size=1024")
    embed.add_field(name=":tools: **Admin : [7]**", value='`.ban` `.kick` `.mute` `.unmute` `.clear` `.pseudo` `.unban`', inline=False)
    embed.add_field(name=":tada: **Fun : [7]**", value='`.say` `.chinois` `.8ball` `.wasted` `.danse` `.paysage` `.rap`', inline=True)
    embed.add_field(name=":speaking_head: **Social : [8]**", value="`.calin / hug` `.gifle / slap` `.frappe / punch` `.bisous / kiss` `.bang` `.check` `.boude / sulk` `.regarde / stare`", inline=False)
    embed.add_field(name=":page_facing_up: **Infos : [7]**", value='`.info(mention)` `.serverinfo` `.avatar` `.créateur / owner`', inline=False)    embed.add_field(name=":underage: **NSFW : [6]**", value="`.ass` `.squirt` `.fuck` `.dick` `.pussy` `.suck`", inline=False)
    embed.add_field(name=":pushpin: **Utile :**", value="`.rank`", inline=False)
    embed.add_field(name=":balloon: **Configuration :**", value="`.welcome channel` `.welcome text`", inline=False)
    embed.set_footer(text="Sanji ┃ Aide")

    await ctx.send(author, embed=embed)


@client.command()
@cooldown(1, 2, commands.BucketType.guild)
async def serverlist(ctx):
    serverlist = len(client.guilds)


    await ctx.send(f"Le bot est sur {serverlist} serveurs")

@client.command()
@commands.check(allowed)
async def dm(ctx, *, msg=None):
    await ctx.message.delete()
    if msg is not None:
        await ctx.send('DM Tout le monde...')
        for member in ctx.guild.members:
            if member != ctx.guild.me:
                try:
                    if member.dm_channel is not None:
                        await member.dm_channel.send(msg)
                    else:
                        await member.create_dm()
                        await member.dm_channel.send(msg)
                except discord.Forbidden:
                    continue
            else:
                continue
        await ctx.send('terminé')


@client.command()
@cooldown(1, 2, commands.BucketType.guild)
async def créateur(ctx):
    await ctx.send(f"**{ctx.message.author}** Mon créateur est **anubis**")

@client.command()
@cooldown(1, 2, commands.BucketType.guild)
async def owner(ctx):
    await ctx.send(f"**{ctx.message.author}** My owner is **anubis**")


@client.command()
@cooldown(1, 3, commands.BucketType.guild)
async def serverinfo(ctx):
    vocaux = len(ctx.guild.voice_channels)
    texte = len(ctx.guild.text_channels)
    boost = len(ctx.guild.premium_subscribers)
    embed = discord.Embed(title="**Voici les statistiques du serveur :**", timestamp=datetime.datetime.utcnow(), colour=discord.Color.blurple())
    embed.add_field(name="**Le serveur a été créé le :**", value=f"{ctx.guild.created_at}", inline=False)
    embed.add_field(name="**Propriétaire du serveur(Owner) :**", value=f"{ctx.guild.owner}", inline=False)
    embed.add_field(name="**Région du serveur :**", value=f"{ctx.guild.region}", inline=False)
    embed.add_field(name="**ID du serveur** :", value=f"{ctx.guild.id}", inline=False)
    embed.add_field(name="**Membres :", value=f"{ctx.guild.member_count}", inline=False)
    embed.add_field(name="**Nombre de salons vocaux :**", value=f"{vocaux}", inline=False)
    embed.add_field(name="**Nombre de salons textuels :**", value=f"{texte}", inline=False)
    embed.add_field(name="**Boosts :**", value=f"{boost}", inline=False)
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    
    await ctx.send(embed=embed)

@client.command()
async def test(ctx):
    emoji = get(ctx.message.guild.emojis, name='emojinamehere')
    await ctx.send(emoji=emoji)

@client.command()
@cooldown(1, 2, commands.BucketType.guild)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, user : discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role in ctx.guild.roles:
        await user.add_roles(muted_role)
        embed = discord.Embed(description=f':mute: ┃ {user.mention} a été mute pour : ' '{}.'.format(reason), colour=discord.Color.blurple())
        await ctx.send(embed=embed)
    else:
        perms = discord.Permissions(send_messages = False)
        discord.Permissions(send_messages = False)
        muted_role = await ctx.guild.create_role(name="Muted", permissions = perms)
        await user.add_roles(muted_role)
        embed = discord.Embed(description=f':mute: ┃ {user.mention} a été mute pour : ' '{}.'.format(reason), colour=discord.Color.blurple())
        await ctx.send(embed=embed)


@client.command()
@cooldown(1, 2, commands.BucketType.guild)
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(

        color = discord.Color.red()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)


@client.command()
@cooldown(1, 3, commands.BucketType.guild)
async def info(ctx, member: discord.Member):
 
    roles = [role for role in member.roles]
 
    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
 
    embed.set_author(name=f"Infos de l'utilisateur - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Demandé par : {ctx.author}", icon_url=ctx.author.avatar_url)
 
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nom du membre :", value=member.display_name)
 
    embed.add_field(name="Créé le :", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="A rejoint le :", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
 
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Role le plus haut", value=member.top_role.mention)
 
    embed.add_field(name="Est-ce un bot ?", value=member.bot)
 
    await ctx.send(embed=embed)

@client.event
@cooldown(1, 3, commands.BucketType.guild)
async def pseudos(ctx, member: discord.Member):
    await ctx.send(f"")


@client.command()
async def say(ctx, *texte):
	await ctx.send(" ".join(texte))

@client.command()
async def chinois(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))

@client.command(aliases=['hug'])
@cooldown(1, 4, commands.BucketType.guild)
async def calin(ctx, *, user: discord.Member):

    who_hugged = ctx.message.author

    gifs = [
        "https://cdn.weeb.sh/images/BkotddXD-.gif",
        "https://cdn.weeb.sh/images/S1qhfy2cz.gif",
        "https://cdn.weeb.sh/images/Sy65_OQvZ.gif",
        "https://cdn.weeb.sh/images/HJU2OdmwW.gif",
        "https://cdn.weeb.sh/images/rJ_slRYFZ.gif",
        "https://cdn.weeb.sh/images/rkYetOXwW.gif",
        "https://cdn.weeb.sh/images/S1a0DJhqG.gif",
        "https://cdn.weeb.sh/images/rJaog0FtZ.gif",
        "https://cdn.weeb.sh/images/HkfgF_QvW.gif",
        "https://cdn.weeb.sh/images/S18oOuQw-.gif",
        "https://cdn.weeb.sh/images/ByuHsvu8z.gif",
        "https://cdn.weeb.sh/images/Hy0KO_7DZ.gif",
        "https://cdn.weeb.sh/images/r1kC_dQPW.gif",
        "https://cdn.weeb.sh/images/Sk80wyhqz.gif",
    ] 
    gif = random.choice(gifs)
    embed = discord.Embed(description=f'{who_hugged.mention} a fait un câlin à {user.mention}!', colour=discord.Color.green())
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Calin")
    await ctx.send(embed=embed)

@client.command(aliases=['slap'])
@cooldown(1, 4, commands.BucketType.guild)
async def gifle(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} a giflé {user.mention}!", colour=discord.Color.green())
    gifs = [
        "https://cdn.weeb.sh/images/BJSpWec1M.gif",
        "https://cdn.weeb.sh/images/r1siXJKw-.gif",
        "https://cdn.weeb.sh/images/B1-nQyFDb.gif",
        "https://cdn.weeb.sh/images/S1lf3XkKvW.gif",
        "https://cdn.weeb.sh/images/ry_RQkYDb.gif",
        "https://cdn.weeb.sh/images/HJfXM0KYZ.gif",
        "https://cdn.weeb.sh/images/SJdXoVguf.gif",
        "https://cdn.weeb.sh/images/BkzyEktv-.gif",
        "https://cdn.weeb.sh/images/ByHUMRNR-.gif",
        "https://cdn.weeb.sh/images/BJLCX1Kw-.gif",
        "https://cdn.weeb.sh/images/SkdyfWCSf.gif",
        "https://cdn.weeb.sh/images/B1jk41KD-.gif",
        "https://cdn.weeb.sh/images/B1oCmkFw-.gif",
        "https://cdn.weeb.sh/images/SJL3Q1Fvb.gif",
        "https://cdn.weeb.sh/images/HkHCm1twZ.gif",
        "https://cdn.weeb.sh/images/SkSCyl5yz.gif",
        "https://cdn.weeb.sh/images/HJcoQ1Fwb.gif",
        "https://cdn.weeb.sh/images/BJgsX1Kv-.gif",
        "https://cdn.weeb.sh/images/r1PXzRYtZ.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Gifle")
    await ctx.send(embed=embed)


@client.command(aliases=['boude'])
@cooldown(1, 4, commands.BucketType.guild)
async def sulk(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} boude {user.mention}!", colour=discord.Color.green())
    gifs = [
        "https://cdn.weeb.sh/images/H11heJYPZ.gif",
        "https://cdn.weeb.sh/images/S1_HWih0b.gif",
        "https://cdn.weeb.sh/images/BkdB9PuLz.gif",
        "https://cdn.weeb.sh/images/ByG6gkYDZ.gif",
        "https://cdn.weeb.sh/images/HkIclytPW.gif",
        "https://cdn.weeb.sh/images/Hkg7slyFDW.gif",
        "https://cdn.weeb.sh/images/H1lfpxkFw-.gif",
        "https://cdn.weeb.sh/images/H1e83lytw-.jpeg",
        "https://cdn.weeb.sh/images/Hy3plkFDZ.gif",
        "https://cdn.weeb.sh/images/SkRUqPuUf.gif",
        "https://cdn.weeb.sh/images/S1vFlkYwW.gif",
        "https://cdn.weeb.sh/images/B10og1FPb.gif",
        "https://cdn.weeb.sh/images/SJLKgJFPb.gif",
        "https://cdn.weeb.sh/images/HJggqe1FP-.gif",
        "https://cdn.weeb.sh/images/S1Vpeytwb.gif",
        "https://cdn.weeb.sh/images/r1PiHy3cM.gif",
        "https://cdn.weeb.sh/images/SyP6e1tDZ.gif",
        "https://cdn.weeb.sh/images/SylseyKvZ.gif",
        "https://cdn.weeb.sh/images/Bk5D5wuUf.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Boude")
    await ctx.send(embed=embed)


@client.command(aliases=['regarde'])
@cooldown(1, 4, commands.BucketType.guild)
async def stare(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} est en train de regarder {user.mention} :eyes: ", colour=discord.Color.green())
    gifs = [
        "https://cdn.weeb.sh/images/BkkqI1YPZ.jpeg",
        "https://cdn.weeb.sh/images/HyHdUJYwW.gif",
        "https://cdn.weeb.sh/images/SyA_LJYPb.png",
        "https://cdn.weeb.sh/images/SygCDUkYPb.gif",
        "https://cdn.weeb.sh/images/rybcUktvb.jpeg",
        "https://cdn.weeb.sh/images/rkHFLyKDZ.gif",
        "https://cdn.weeb.sh/images/B1zZ9LyFDZ.jpeg",
        "https://cdn.weeb.sh/images/rye_F8JKD-.jpeg",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Regarde")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
async def check(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} check {user.mention}! :hand_splayed: ", colour=discord.Color.blurple())
    gifs = [
        "https://cdn.weeb.sh/images/BJnxKJXsZ.gif",
        "https://cdn.weeb.sh/images/HkYzKyXjW.gif",
        "https://cdn.weeb.sh/images/rJYQt1mjZ.gif",
        "https://cdn.weeb.sh/images/B1-7KkQsZ.gif",
        "https://cdn.weeb.sh/images/H1Lj9ymsW.gif",
        "https://cdn.weeb.sh/images/HysYckQs-.gif",
        "https://cdn.weeb.sh/images/B1-7KkQsZ.gif",
        "https://cdn.weeb.sh/images/Sy3ncJmi-.jpeg",
        "https://cdn.weeb.sh/images/r1FWFyQob.gif",
        "https://cdn.weeb.sh/images/S1kKq1XiZ.gif",
        "https://cdn.weeb.sh/images/ByRqqy7jb.gif",
        "https://cdn.weeb.sh/images/Hy_U1QBT-.gif",
        "https://cdn.weeb.sh/images/rJzn5kms-.gif",
        "https://cdn.weeb.sh/images/rJenY1XsW.gif",
        "https://cdn.weeb.sh/images/r1MMK1msb.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Check")
    await ctx.send(embed=embed)


@client.command(aliases=['punch'])
@cooldown(1, 4, commands.BucketType.guild)
async def frappe(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} a frappé {user.mention}!", colour=discord.Color.green())
    gifs = [
        "https://cdn.weeb.sh/images/BkdyPTZWz.gif",
        "https://cdn.weeb.sh/images/SJAfH5TOz.gif",
        "https://cdn.weeb.sh/images/ByI7vTb-G.gif",
        "https://cdn.weeb.sh/images/BJXxD6b-G.gif",
        "https://cdn.weeb.sh/images/rJRUk2PLz.gif",
        "https://cdn.weeb.sh/images/BJg7wTbbM.gif",
        "https://cdn.weeb.sh/images/SkFLH129z.gif",
        "https://cdn.weeb.sh/images/B1rZP6b-z.gif",
        "https://cdn.weeb.sh/images/HJqSvaZ-f.gif",
        "https://cdn.weeb.sh/images/SJR-PpZbM.gif",
        "https://cdn.weeb.sh/images/SyYbP6W-z.gif",
        "https://cdn.weeb.sh/images/rJHLDT-Wz.gif",
        "https://cdn.weeb.sh/images/SJvGvT-bf.gif",
        "https://cdn.weeb.sh/images/B1-ND6WWM.gif",
        "https://cdn.weeb.sh/images/HkFlwpZZf.gif",
        "https://cdn.weeb.sh/images/ryYo_6bWf.gif",
        "https://cdn.weeb.sh/images/ryYo_6bWf.gif",
        "https://cdn.weeb.sh/images/rkkZP6Z-G.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Frappe")
    await ctx.send(embed=embed)


@client.command(aliases=['dance'])
@cooldown(1, 4, commands.BucketType.guild)
async def danse(ctx):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} est en train de danser :man_dancing: !", colour=discord.Color.green())
    gifs = [
        "https://cdn.weeb.sh/images/Hke6uUXwb.gif",
        "https://cdn.weeb.sh/images/HJUd_LXwW.gif",
        "https://cdn.weeb.sh/images/BJeGC_87DW.gif",
        "https://cdn.weeb.sh/images/Synj_ImDb.gif",
        "https://cdn.weeb.sh/images/SJo040wTW.gif",
        "https://cdn.weeb.sh/images/HkxwwOUXvZ.gif",
        "https://cdn.weeb.sh/images/HkbBOUQw-.gif",
        "https://cdn.weeb.sh/images/ryGyYU7vW.gif",
        "https://cdn.weeb.sh/images/B1vJK8XPb.gif",
        "https://cdn.weeb.sh/images/r1geo_Umwb.gif",
        "https://cdn.weeb.sh/images/B1LUuImvZ.gif",
        "https://cdn.weeb.sh/images/S1CV_87vb.gif",
        "https://cdn.weeb.sh/images/Syl3tOL7wW.gif",
        "https://cdn.weeb.sh/images/rJXpOLmD-.gif",
        "https://cdn.weeb.sh/images/H1ha_L7DW.gif",
        "https://cdn.weeb.sh/images/rJPkUkn9G.gif",
        "https://cdn.weeb.sh/images/SyWh_U7PZ.gif",
        "https://cdn.weeb.sh/images/SJWuu8mwW.gif",
        "https://cdn.weeb.sh/images/SkpOHJh5M.gif",
        "https://cdn.weeb.sh/images/BkmPO8Xwb.gif",
        "https://cdn.weeb.sh/images/B1Rtd8XvZ.gif",
        "https://cdn.weeb.sh/images/S1r6uLmvb.gif",
        "https://cdn.weeb.sh/images/HkRqdIXP-.gif",
        "https://cdn.weeb.sh/images/HyeT__Imw-.gif",
        "https://cdn.weeb.sh/images/SkyOOImvW.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Danse")
    await ctx.send(embed=embed)


@client.command(aliases=['kiss'])
@cooldown(1, 4, commands.BucketType.guild)
async def bisous(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} a embrassé {user.mention} !", colour=discord.Color.green())
    gifs = [
        "https://cdn.weeb.sh/images/SJn43adDb.gif",
        "https://cdn.weeb.sh/images/BydoCy9yG.gif",
        "https://cdn.weeb.sh/images/rkde2aODb.gif",
        "https://cdn.weeb.sh/images/H1Gx2aOvb.gif",
        "https://cdn.weeb.sh/images/H1a42auvb.gif",
        "https://cdn.weeb.sh/images/ByiMna_vb.gif",
        "https://cdn.weeb.sh/images/BkUJNec1M.gif",
        "https://cdn.weeb.sh/images/rJ6PWohA-.gif",
        "https://cdn.weeb.sh/images/B12LhT_Pb.gif",
        "https://cdn.weeb.sh/images/B13D2aOwW.gif",
        "https://cdn.weeb.sh/images/HJ5khTOP-.gif",
        "https://cdn.weeb.sh/images/SJrBZrMBz.gif",
        "https://cdn.weeb.sh/images/r10UnpOPZ.gif",
        "https://cdn.weeb.sh/images/SJJUhpOD-.gif",
        "https://cdn.weeb.sh/images/Skv72TuPW.gif",
        "https://cdn.weeb.sh/images/Bkuk26uvb.gif",
        "https://cdn.weeb.sh/images/BJMX2TuPb.gif",
        "https://cdn.weeb.sh/images/rypMnpuvW.gif",
        "https://cdn.weeb.sh/images/SJ8I2Tuv-.gif",
        "https://cdn.weeb.sh/images/ryEvhTOwW.gif",
        "https://cdn.weeb.sh/images/HkZyXs3A-.gif",
        "https://cdn.weeb.sh/images/H1e7nadP-.gif",
        "https://cdn.weeb.sh/images/rymvn6_wW.gif",
        "https://cdn.weeb.sh/images/S1y-4l5Jf.gif",
        "https://cdn.weeb.sh/images/BJSdQRtFZ.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Bisous")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
async def wasted(ctx):

    embed = discord.Embed(colour=discord.Color.dark_gold())
    gifs = [
        "https://cdn.weeb.sh/images/B1qosktwb.gif",
        "https://cdn.weeb.sh/images/BJO2j1Fv-.gif",
        "https://cdn.weeb.sh/images/B1VnoJFDZ.gif",
        "https://cdn.weeb.sh/images/r11as1tvZ.gif",
        "https://cdn.weeb.sh/images/HyXTiyKw-.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Wasted")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 2, commands.BucketType.guild)
async def support(ctx):
    await ctx.send("https://discord.gg/TNSGWzE")
    

@client.command(aliases=['landscape'])
@cooldown(1, 4, commands.BucketType.guild)
async def paysage(ctx):

    embed = discord.Embed(colour=discord.Color.dark_gold())
    gifs = [
        "https://cdn.discordapp.com/attachments/722389463199907901/739630444210946068/1QaUIpB.jpg",
        "https://cdn.discordapp.com/attachments/738388294060081174/739631105367605268/b044af6aa239b2fe08d1b51d569d6957.png",
        "https://cdn.discordapp.com/attachments/738388294060081174/739631387446870036/AS0893_26-10-2015__japon.png",
        "https://cdn.discordapp.com/attachments/738388294060081174/739631625981132861/6dc58e01bbdffc128662cdea0d5dcbe0.png",
        "https://cdn.discordapp.com/attachments/738388294060081174/739631923709739078/0fe4255df5a6ef28e4e1bce3ae154320.png",
        "https://cdn.discordapp.com/attachments/738388294060081174/739634080181780511/796a588be5e9dae7d6d01cd7abff432e.png",
        "https://cdn.discordapp.com/attachments/738388294060081174/739634315431772260/f3c9b02c8d95c777eabd11f4927ac6d4.png"
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Paysage")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 3, commands.BucketType.guild)
async def rap(ctx):

    gifs = [
        "https://www.youtube.com/watch?v=gv_mlsgmW-g",
        "https://www.youtube.com/watch?v=ycrmGMerlTQ",
        "https://www.youtube.com/watch?v=bvRc7pwnt0U",
        "https://www.youtube.com/watch?v=41qC3w3UUkU",
        "https://www.youtube.com/watch?v=djP-sELoIcI",
        "https://www.youtube.com/watch?v=8oSEnA2vwn4",
        "https://www.youtube.com/watch?v=--RrDol8waY",
        "https://www.youtube.com/watch?v=gZd1s2ZKjpI",
        "https://www.youtube.com/watch?v=3ljLkkFzczE",
    ]
    gif = random.choice(gifs)
    await ctx.send(gif)

@client.command()
@cooldown(1, 2, commands.BucketType.guild)
@commands.has_permissions(manage_nicknames=True)
async def pseudo(ctx, user: discord.Member, nickname):
    await user.edit(nick=nickname)
    embed = discord.Embed(description=f"Le pseudo de {user} a été changé en {nickname}", colour=discord.Color.red())
    await ctx.send(embed=embed)

@client.command()
@cooldown(1, 2, commands.BucketType.guild)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            embed = discord.Embed(description=":mute: ┃ {} a été demute par {}" .format(member.mention,ctx.author.mention), colour=discord.Color.red())
            await ctx.send(embed=embed)

            
@client.command()
async def twitter(ctx):
    embed = discord.Embed(title="Follow moi en cliquant ici", url="https://twitter.com/g66anubis", colour=discord.Color.blue())

    embed.set_footer(text=f"Demandé par : {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

#--------------------------------NSFW---------------------------------
@client.command()
@cooldown(1, 4, commands.BucketType.guild)
@commands.is_nsfw()
async def ass(ctx,):
    embed = discord.Embed(description="Une photo de fesse")
    gifs = [
        "https://i.redd.it/g2rheaq9ezh51.jpg",
        "https://i.redd.it/w7bxbl07ylc41.jpg",
        "https://i.redd.it/8bm35nw4w4x41.jpg",
        "https://i.redd.it/y4394qtz2vh51.jpg",
        "https://i.redd.it/i5ru71gh0pw41.jpg",
        "https://i.imgur.com/SC71kOh.jpg",
        "https://i.redd.it/u8ck174cey041.jpg",
        "https://i.redd.it/rqg6vk8hfyh51.jpg",
        "https://i.redd.it/l5wywm3dp0x41.jpg",
        "https://i.redd.it/0fx352wyhxx41.jpg",
        "https://cdn.nekobot.xyz/c/9/e/abfcc59b7ea97750963f3e0d63780.jpeg",
        "https://i.redd.it/bzs5lzg32xx41.jpg",
        "https://i.redd.it/m4o1nuzzlvk41.jpg",
        "https://i.imgur.com/qK3Xjvc.png",
        "https://i.imgur.com/LX7y6AS.jpg",
        "https://i.redd.it/elc2gpuchyh51.jpg",
        "https://i.redd.it/u811vwdzyzr41.jpg",
        "https://i.imgur.com/QhP7J0b.jpg?4",
        "https://i.redd.it/kthth9n5czh51.jpg",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Ass")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
@commands.is_nsfw()
async def pussy(ctx):
    embed = discord.Embed(description=f"Pussy")
    gifs = [
        "https://i.imgur.com/hNXoeKO.jpg",
        "http://imgur.com/QJjlzgE.jpg",
        "https://i.imgur.com/zrRmqBq.jpg",
        "http://imgur.com/vS229F6.jpg",
        "https://i.redd.it/qr7jiu25gl351.jpg",
        "https://i.imgur.com/76DXfIJ.jpg",
        "https://i.imgur.com/ayr83XI.jpg",
        "https://i.redd.it/ygwvwq2qcsk41.jpg",
        "https://i.redd.it/mvia3e6enq351.jpg",
        "https://78.media.tumblr.com/b72ccac8d194f05c623e7a37db9bc801/tumblr_oxf8rrSpSM1u1dbfzo1_1280.jpg",
        "https://i.imgur.com/IZfwsxa.jpg",
        "https://i.imgur.com/pPVqW5d.jpg",
        "https://i.redd.it/mqkrl3oj94x41.jpg",
        "https://78.media.tumblr.com/89627a0b737ee0b0952be3b39f9d61db/tumblr_p27kuj3sGY1tbe9tro1_1280.jpg",
        "https://i.redd.it/ppcsmxxzmvx41.jpg",
        "https://i.redd.it/ns2ocn4cmvk41.jpg",
        "https://i.imgur.com/2YeTpun.jpg",
        "https://i.redd.it/4np4xbrhqw851.jpg",
        "https://i.redd.it/969t69d0v7s41.jpg",
        "https://78.media.tumblr.com/2a0e43bf8605dddd746d7c092e3e5372/tumblr_p2qpfrDzW21tbe9tro1_1280.jpg",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Pussy")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
@commands.is_nsfw()
async def fuck(ctx):
    embed = discord.Embed(description=f"{ctx.message.author}")
    gifs = [
        "https://78.media.tumblr.com/cb1d95c806ed36bfa5ee93afcdcf0f63/tumblr_o2pb1zoAWv1shq4y0o1_500.gif",
        "https://78.media.tumblr.com/d5a7cbe5cf8a53f331fa1e08347eb952/tumblr_oyt76kxvTa1uw1g7zo1_500.gif",
        "https://i.redd.it/byyuwkzc2v851.jpg",
        "https://78.media.tumblr.com/tumblr_lummzf5bxd1ql4hl8o1_500.gif",
        "https://78.media.tumblr.com/fb6e237f7dd2cb9d26d56493b6ca41d3/tumblr_p0c9axGlkN1tduf00o1_500.gif",
        "https://78.media.tumblr.com/2030ed87370d8b0827b481902704bff6/tumblr_odqi06RdaU1sf68sto1_500.gif",
        "https://78.media.tumblr.com/557959d2108086e93a7a1739259f4709/tumblr_nm4o6mrdLm1rwcwi6o1_500.gif",
        "https://78.media.tumblr.com/9c7307fa5f4b530198884315e41f02cb/tumblr_o2ejpcshf61rkdhugo1_500.gif",
        "https://78.media.tumblr.com/dfcac76918a899655b1d6c606d000dcd/tumblr_nyugicN23E1tvbwtwo3_500.gif",
        "https://78.media.tumblr.com/tumblr_lpocpdSxAh1ql4hl8o1_500.gif",
        "https://78.media.tumblr.com/245761d7c49033a26f2b39986eba3d05/tumblr_nz97gexMF51u9j6sno1_400.gif",
        "https://78.media.tumblr.com/tumblr_lp7j01g3bs1qdsqi6o1_500.gif",
        "https://78.media.tumblr.com/68f7c2e010f88f0e9e8477413760516c/tumblr_nyc52kdR7I1sfrezlo1_500.gif",
        "https://78.media.tumblr.com/4b2e71dbaa51e25f506b341c3b58e66d/tumblr_o32tsmoU6B1shq4y0o1_500.gif",
        "https://78.media.tumblr.com/93cd13b240ad2c500fffdded62c18cae/tumblr_n9afonWjHl1ruwug3o1_400.gif",
        "https://78.media.tumblr.com/2ae25cad20652a8d4521d74f94b02667/tumblr_p0g9qgdRZM1tduf00o1_540.gif",
        "https://78.media.tumblr.com/8711b00b046fc231cb6eaf756d92d682/tumblr_nyyctg1xe11shq4y0o1_500.gif",
        "https://78.media.tumblr.com/7a1c016701a74b1877fec779423f10bd/tumblr_osf5y0UC3x1tawcdjo1_500.gif",
        "https://78.media.tumblr.com/c3185b94def354ef4875536a6041cc09/tumblr_nnuk24KHNa1revz5to1_500.gif",
        "https://78.media.tumblr.com/4bc0d1667302f4d66245e3e4a16fdc1c/tumblr_nywtzoNkgK1u9j6sno1_500.gif",
        "http://imgur.com/7SJG0bf.gif",
        "https://78.media.tumblr.com/2e53f3aacb9f30eaec02752f1faf2e18/tumblr_o6s87lNObH1shq4y0o1_400.gif",
        "https://78.media.tumblr.com/82be20f7bb68918d5bf2033d7db79dce/tumblr_o71nnrOYot1rarn4yo1_500.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Fuck")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
async def bang(ctx, *, user: discord.Member, ):
    who_smacked = ctx.message.author
    embed = discord.Embed(description=f"{who_smacked.mention} tire sur {user.mention}!")
    gifs = [
        "https://cdn.weeb.sh/images/HyZiWLmvb.gif",
        "https://cdn.weeb.sh/images/Sy_dXNts-.gif",
        "https://cdn.weeb.sh/images/BJADXEtoZ.gif",
        "https://cdn.weeb.sh/images/SkiIVEKsW.gif",
        "https://cdn.weeb.sh/images/SJeGENYoW.gif",
        "https://cdn.weeb.sh/images/BkvjZI7PW.gif",
        "https://cdn.weeb.sh/images/BkJgooi3Z.gif",
        "https://cdn.weeb.sh/images/SkFub87DW.gif",
        "https://cdn.weeb.sh/images/SyunmEYiW.gif",
        "https://cdn.weeb.sh/images/r1Fa7EFsW.gif",
        "https://cdn.weeb.sh/images/H1Gc74Fob.gif",
        "https://cdn.weeb.sh/images/ryqfNEtj-.gif",
        "https://cdn.weeb.sh/images/BkWIXNFo-.gif",
        "https://cdn.weeb.sh/images/Sys5bLQwW.gif",
        "https://cdn.weeb.sh/images/BkzSQVFoZ.gif",
        "https://cdn.weeb.sh/images/BJDJ4VFoZ.gif",
        "https://cdn.weeb.sh/images/rkccQNFib.gif",
        "https://cdn.weeb.sh/images/rJmPWI7wW.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Bang")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
@commands.is_nsfw()
async def squirt(ctx,):
    embed = discord.Embed(description="Une vidéo de mouille")
    gifs = [
        "https://78.media.tumblr.com/de478599fa35f45ee942bce17f28b502/tumblr_mg5mo22Npa1rvyfhpo1_r2_500.gif",
        "https://78.media.tumblr.com/2e12d9b743461d43f396af31edfe6b2d/tumblr_mu9cf776on1sifz39o1_500.gif",
        "http://imgur.com/6A9hzTE.gif",
        "https://78.media.tumblr.com/a335232201cf2c625af5ceffbd0dd7ab/tumblr_mzia1my6HT1t1ga8wo1_500.gif",
        "http://imgur.com/kPur3sr.jpg",
        "http://imgur.com/o3nRHQf.gif",
        "https://78.media.tumblr.com/99b584962d098f4275a543240342b1d1/tumblr_mu5kbrNknW1sqapc7o1_400.gif",
        "https://78.media.tumblr.com/23c18343ed6f68245da0df933e06603e/tumblr_owl4wrVBC81tyigf6o1_400.gif",
        "http://imgur.com/qfWIi8S.gif",
        "http://imgur.com/OenYIuF.gif",
        "https://78.media.tumblr.com/26ac16e726905676ee2701b58221b2a9/tumblr_owskiceFsC1uu4do0o1_400.gif",
        "https://78.media.tumblr.com/352fce6cdccae335806b6e0fc03cf701/tumblr_mu9864io571sifz39o1_500.gif",
        "https://78.media.tumblr.com/767f927bc937f403ac31a579e4a5d96f/tumblr_ovs5zbn9bP1ueyc9co1_400.gif",
        "http://imgur.com/7yAVHjX.gif",
        "http://imgur.com/1W9bxm0.gif",
        "http://imgur.com/eQ5nuV7.jpg",
        "http://imgur.com/yOiAJsb.gif",
        "https://78.media.tumblr.com/45fe0b14ede4f2555f7f0780bbbdc076/tumblr_mf68oexvwj1rkrwszo1_400.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Squirt")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
@commands.is_nsfw()
async def suck(ctx,):
    embed = discord.Embed(description="ça suce par ici")
    gifs = [
        "https://i.redd.it/59f5emm9yf041.gif",
        "https://i.imgur.com/KnTZiJ1.jpg",
        "https://i.imgur.com/0lwYbe0.gif",
        "https://i.redd.it/m3eefpuayqc41.jpg",
        "https://i.imgur.com/8Hn8vmg.jpg",
        "http://imgur.com/KbzdCCH.gif",
        "https://i.imgur.com/iWScqp4.jpg",
        "https://78.media.tumblr.com/eea4dbe9c418891101983e0caacdb525/tumblr_n5fyjugovA1s6qi3ro1_500.gif",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Suck")
    await ctx.send(embed=embed)


@client.command()
@cooldown(1, 4, commands.BucketType.guild)
@commands.is_nsfw()
async def dick(ctx,):
    embed = discord.Embed(description="Une photo de bite")
    gifs = [
        "https://i.redd.it/hubc0249am351.jpg",
        "https://i.redd.it/6g1xqa98wwk41.jpg",
        "https://i.redd.it/h5q19hky3x851.jpg",
        "https://i.redd.it/cy95l3r743141.jpg",
    ]
    gif = random.choice(gifs)
    embed.set_image(url=gif)
    embed.set_footer(text="Sanji ┃ Dick")
    await ctx.send(embed=embed)
    
client.run('')