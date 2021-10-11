from asyncio.windows_events import NULL
from collections import namedtuple
from time import ctime
import discord
from discord.embeds import Embed
from discord.ext.commands import bot
from discord.flags import Intents
from pymongo import MongoClient
from discord import client
from discord.ext import commands
from discord.ext.commands.core import command

client = commands.Bot(command_prefix="+",intents=discord.Intents.all())


cluster = MongoClient("mongodb+srv://caxy:caxy@bump.uc060.mongodb.net/<dbname>?retryWrites=true&w=majority")
bumps = cluster["discord"]["bump"]


@client.command(aliases=['bc'])
async def bumpcount(ctx):
    stat = bumps.find_one({"id":ctx.author.id})
    if stat is None:
        await ctx.send("You havent bumped yet")
    else:
        rank = 0
        ranks = bumps.find().sort("count",-1)
        for i in ranks:
            rank = rank+1
            if i["id"]==ctx.author.id:
                em = discord.Embed(title="Bump Count",description=f"You have bumped {stat['count']} times")
                em.add_field(name="Rank",value=f"{rank}/{ctx.guild.member_count}")
                await ctx.send(embed=em)



@client.command(aliases=['blb'])
async def bumplb(ctx): 
    rankings = bumps.find().sort("count",-1)
    x = 1
    em = discord.Embed(title="Leaderboard")
    for i in rankings:  
        x = x+1
        try:
            name1 = ctx.guild.get_member(i["id"])
            bcount = i["count"]
            em.add_field(name=f"{name1}",value=f"Bump count:{bcount}",inline=False)
        except:
            pass
        if x==10:
            break
    await ctx.channel.send(embed=em)

@client.listen()
async def on_message(message):
    if message.author==client.user:
        return
    else:
        if message.content.startswith("!d invite"):
             await message.channel.send("Bump count is set")
        else:
            if message.author.id==302050872383242240:
                length = 0
                mid = 0
                em = message.embeds
                for i in em:
                    x = i.to_dict()
                    y = str(x["description"])
                    if y[2:20].isdigit():
                        mid = int(y[2:20])
                for j in em:
                    q = j.to_dict()
                    length = len(q["description"])
                if length>104:
                    if mid is not None:
                        stats = bumps.find_one({"id":mid})
                        if stats is None:
                            newuser = {"id":mid,"count":1}
                            bumps.insert_one(newuser)
                        else:
                            bcount = stats["count"] + 1
                            bumps.update_one({"id":mid},{"$set":{"count":bcount}})
                    
            
client.run("ODk2MzE4OTI1MzMwMDU1MTk4.YWFYDA.pvz9nWktNc3etOrwVwNWU4nzI7M")
