import datetime
import discord
import requests
import asyncio 
import string
import itertools
import json
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
from discord import Colour, Embed, utils, Client, Intents
from discord.ext.commands import BadArgument, Cog, Context, command
from auth import token, mariadb_connection



# Locales 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="NWT", intents=intents)
client = commands.Bot(command_prefix = 'NWT')
slash = SlashCommand(bot, sync_commands=True)
addcommands = {}
db710 = mariadb_connection.cursor()
## Get guild bot is in

def get_guilds_bot_in():
    listofids = []
    for guild in bot.guilds:
        listofids.append(guild.id)
        print(listofids)
        return(listofids) 


guild_ids=get_guilds_bot_in


@bot.event 
async def on_ready():
    startmessage = f'I just started - My ping is {round(bot.latency * 1000)}ms!'
    await bot.change_presence(activity = discord.Activity (type = discord.ActivityType.watching, name = 'New World PvP'))
    inguilds = bot.guilds 
    embed=discord.Embed(title=f"I Have been started!",description=startmessage,color=0xadff2f)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.add_field(name='Servers', value=f'{len(inguilds)}',  inline=False)
    embed.set_footer(text="Created by Kmack710#0710")
    await bot.get_channel(907754450624585748).send(embed=embed)
    print("Online and Ready and in ", len(inguilds), "servers")
    #print(bot.fetch_guilds(limit=150).flatten())
  
#guild_ids=guilds
# Solo Register Event
@slash.slash(
    name='registersolo', 
    description= "Register as a solo player for event!",
    guild_ids=guild_ids,
    options=[
            create_option(
            name = "role",
            description= "Pick your role for the event!",
            required =True,
            option_type=3, 
            choices=[
                create_choice(
                    name="Healer!",
                    value="healer"
                ),
                create_choice(
                    name="DPS!",
                    value="dps"
                ),
                create_choice(
                    name="Tank!",
                    value="tank"
                )
            ]
        ),
        create_option( 
            name = "ign",
            description= "Name of your character ingame!",
            option_type=3, 
            required =True
        ),
        create_option( 
            name = "event_id",
            description= "Event ID for the event your registering to!",
            option_type=3, 
            required =True
        ) 
    ]
)
async def registersolo(ctx:SlashContext, role:str, event_id:str, ign:str):
    sql_statement = f"INSERT INTO `registration_solo` VALUES ('{event_id}', '{role}', '{ign}')"
    db710.execute(sql_statement)
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description="Registration Complete", color=0xadff2f)
    embed.add_field(name='Event ID', value=f'{event_id}',  inline=False)
    embed.add_field(name='Role', value=f'{role}',  inline=False)
    embed.add_field(name='Ingame Name', value=f'{ign}',  inline=False)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Powered By NWT.710gaming.xyz")
    await ctx.send(embed=embed)
    mariadb_connection.commit()
    


# Team Register Event
@slash.slash(
    name='registerteam', 
    description= "Register as team for the event! (Only register **Once per team**)",
    guild_ids=guild_ids,
    options=[
            create_option(
            name = "team",
            description= "Pick a team name for the event!",
            required =True,
            option_type=3, 
        ),
        create_option( 
            name = "ign",
            description= "Name of your team leaders character ingame!",
            option_type=3, 
            required =True
        ),
        create_option( 
            name = "event_id", 
            description= "Event ID for the event your registering to!",
            option_type=3, 
            required =True
        ) 
    ]
)
async def registerteam(ctx:SlashContext, team:str, event_id:str, ign:str):
    sql_statement = f"INSERT INTO `registration` VALUES ('{event_id}', '{team}', '{ign}')"
    db710.execute(sql_statement)
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description="Registration Complete", color=0xadff2f)
    embed.add_field(name='Event ID', value=f'{event_id}',  inline=False)
    embed.add_field(name='Team name', value=f'{team}',  inline=False)
    embed.add_field(name='Team Leader', value=f'{ign}',  inline=False)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Powered By NWT.710gaming.xyz")
    await ctx.send(embed=embed)
    mariadb_connection.commit()
    



## Create events 
@slash.slash(
    name='createevent', 
    description= "Create an Event!",
    guild_ids=guild_ids,
    options=[
            create_option(
            name = "event_name",
            description= "Give your event a name!",
            required =True,
            option_type=3, 
        ),
        create_option( 
            name = "time",
            description= "Time and Date of the event! (Be sure to put timezone)",
            option_type=3, 
            required =True
        ),
        create_option( 
            name = "server",
            description= "Server you are hosting this event on",
            option_type=3, 
            required =True
        ),
        create_option(
            name = "info",
            description= "A BREIF amount of info about your event (150 characters max)",
            option_type=3, 
            required =True
        ),
        create_option(
            name ="rules",
            description= "Basic rules for your event (100 characters max)",
            option_type=3, 
            required =True
        ) 
    ]
)
async def createevent(ctx:SlashContext, event_name:str, time:str, server:str, info:str, rules:str):
    sql_statement = f"INSERT INTO `events` VALUES (null, '{event_name}', '{time}', '{server}', '{info}', '{rules}', '{ctx.author}')"
    db710.execute(sql_statement)
    sql_statement2 = f"SELECT event_id FROM `events` WHERE event_name='{event_name}' AND event_time='{time}'"
    db710.execute(sql_statement2)
    neweid = db710.fetchone()[0]
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description="Event Created", color=0xadff2f)
    embed.add_field(name='Event Name', value=f'{event_name}',  inline=False)
    embed.add_field(name='Event Time', value=f'{time}',  inline=True)
    embed.add_field(name='Event Info', value=f'{info}',  inline=False)
    embed.add_field(name='Event Rules', value=f'{rules}',  inline=True)
    embed.add_field(name='Server', value=f'{server}',  inline=False)
    embed.add_field(name='Event ID', value=f'{neweid}',  inline=False)
    embed.add_field(name='Event Creator', value=f'{ctx.author.display_name}',  inline=True)
    embed.add_field(name='How to sign up', value=f'To sign up to this event use /registerteam (team name) (team leader name) {neweid} -- /registersolo is still in development!',  inline=False)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Powered By NWT.710gaming.xyz")
    await ctx.send(embed=embed)
    await bot.get_channel(899569395368607795).send(embed=embed)
    mariadb_connection.commit()
    

## Remove losing teams from event list
@slash.slash(
    name = 'removeteam',
    description = 'Remove a team from the event! (Event creator only)',
    guild_ids=guild_ids,
    options=[
        create_option(
            name = "eventid",
            description= "Event ID for the event your removing a team from",
            required =True,
            option_type=3
        ),
        create_option(
            name = "teamname",
            description= "Team name for the team your want to remove (Must be exact with spaces and all!)",
            required =True,
            option_type=3
        )
    ]
)
async def removeteam(ctx:SlashContext, eventid:str, teamname:str):
    sql_statement = f"SELECT * FROM events WHERE event_id='{eventid}'"
    db710.execute(sql_statement)
    final_result = [i[6] for i in db710.fetchall()]
    final_name = final_result[0]
    ctxname = ctx.author
    if (str(final_name) == str(ctxname)):
        sql_statement2 = f"DELETE FROM registration WHERE event_id ='{eventid}' AND team_name ='{teamname}'"
        db710.execute(sql_statement2)
        mariadb_connection.commit()
        await ctx.send(f"{teamname} was removed from event {eventid}")
    else: 
        await ctx.send("You didnt make this event!")
        
        
## Make Bracket Command 
@slash.slash(
    name= 'makebracket',
    description= 'Make the matches for the event! After a team loses use /removeteam (Event Creator only)',
    guild_ids=guild_ids,
    options=[
        create_option(
            name = "eventid",
            description= "Event ID for your event!",
            required = True,
            option_type=3
        )
    ]
)

async def makebracket(ctx:SlashContext, eventid:str):
    sql_statement = f"SELECT * FROM events WHERE event_id='{eventid}'"
    db710.execute(sql_statement)
    final_result = [i[6] for i in db710.fetchall()]
    final_name = final_result[0]
    ctxname = ctx.author
    if (str(final_name) == str(ctxname)):
        sql_statement2 = f"SELECT * FROM registration WHERE event_id='{eventid}'"
        db710.execute(sql_statement2)
        final_result = [i[1] for i in db710.fetchall()]
        embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description=f'Bracket for event # {eventid}', color=0xadff2f)
        list_a = final_result[:len(final_result)//2]
        list_b = final_result[len(final_result)//2:]
        for j in range(len(list_a)):
            embed.add_field(name="Match", value=f"{list_a[j]} VS {list_b[j]}", inline=True)
        embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
        embed.set_footer(text="Sent by {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
        mariadb_connection.commit()
    else: 
        await ctx.send("You didnt make this event!")
      
## Check Registered teams command
@slash.slash(
    name= 'event',
    description= 'Check Registered teams for the event!',
    guild_ids=guild_ids,
    options=[
        create_option(
            name = "eventid",
            description= "Event ID for your event!",
            required = True,
            option_type=3
        )
    ]
)
async def event(ctx:SlashContext, eventid:str):
    sql_statement = f"SELECT * FROM registration WHERE event_id='{eventid}'"
    db710.execute(sql_statement)
    final_result = [i for i in db710.fetchall()]
    sql_statement2 = f"SELECT * FROM events WHERE event_id='{eventid}'"
    db710.execute(sql_statement2)
    final_result2 = [r for r in db710.fetchall()]
    final_result3 = list((final_result2[0]))
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description=f'Teams Registered for event # {eventid} - {final_result3[1]}', color=0xadff2f)
    for j in range(len(final_result)):
        embed.add_field(name=f"{final_result[j][1]}", value=f"{final_result[j][2]}", inline=True)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.add_field(name="Event Info", value=f"Time - {final_result3[2]}", inline=False)
    embed.add_field(name="Event Time", value=f"{final_result3[4]}", inline=False)
    embed.add_field(name="Event Rules", value=f"{final_result3[5]}", inline=False)
    embed.add_field(name="Event Creator", value=f"{final_result3[6]}", inline=False)
    embed.set_footer(text=f"This is the current Teams and their leaders signed up for event #{eventid}")
    await ctx.send(embed=embed)
    mariadb_connection.commit()
    

## Send embed message with manage message permissions
@bot.command(brief='Admin/Mod only')
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *,text):
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description=text, color=0xadff2f)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Sent by {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    await ctx.message.delete()


bot.run(token)

