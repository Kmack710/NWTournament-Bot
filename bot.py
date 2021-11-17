import datetime
import discord
import requests
import asyncio 
import string
import itertools
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
guild_ids=[898721255572766721]

@bot.event 
async def on_ready():
    startmessage = f'I just started - My ping is {round(bot.latency * 1000)}ms!'
    await bot.change_presence(activity = discord.Activity (type = discord.ActivityType.watching, name = 'New World PvP'))
    embed=discord.Embed(title=f"I Have been started!",description=startmessage,color=0xadff2f)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Created by Kmack710#0710")
    await bot.get_channel(907754450624585748).send(embed=embed)
    print("Online and Ready")
  

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
        ) 
    ]
)
async def createevent(ctx:SlashContext, event_name:str, time:str, server:str):
    sql_statement = f"INSERT INTO `events` VALUES (null, '{event_name}', '{time}', '{server}')"
    db710.execute(sql_statement)
    sql_statement2 = f"SELECT event_id FROM `events` WHERE event_name='{event_name}' AND event_time='{time}'"
    db710.execute(sql_statement2)
    neweid = db710.fetchone()[0]
    #neweidc = neweid['event_id']
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description="Event Created", color=0xadff2f)
    embed.add_field(name='Event Name', value=f'{event_name}',  inline=False)
    embed.add_field(name='Event Time', value=f'{time}',  inline=False)
    embed.add_field(name='Server', value=f'{server}',  inline=False)
    embed.add_field(name='Event ID', value=f'{neweid}',  inline=False)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Powered By NWT.710gaming.xyz")
    await ctx.send(embed=embed)
    mariadb_connection.commit()

## Make Bracket from teams FUNCTION
def makebracketf(eventid):
    sql_statement = f"SELECT * FROM registration WHERE event_id='{eventid}'"
    db710.execute(sql_statement)
    final_result = [i[1] for i in db710.fetchall()]
    print(final_result)
    



## Make Bracket Command 
@slash.slash(
    name= 'makebracket',
    description= 'Make the bracket for event! WARNING once this is done you can no longer create the bracket!',
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
    sql_statement = f"SELECT * FROM registration WHERE event_id='{eventid}'"
    db710.execute(sql_statement)
    final_result = [i[1] for i in db710.fetchall()]
    print(final_result)
    embed = discord.Embed(title="NW Tournaments", url="https://710gaming.xyz/nwtournaments", description=f'Bracket for event # {eventid}', color=0xadff2f)
    list_a = final_result[:len(final_result)//2]
    list_b = final_result[len(final_result)//2:]
    print(list_a)
    print(list_b, "LIST B")
    for x, j in itertools.product(range(len(list_a)), range(len(list_b))):
        ##embed.add_field(name='Team Name', value=final_result[i], inline=False)
        embed.add_field(name="Match", value=f"{list_a[x]} VS {list_b[j]}", inline=True)
    embed.set_thumbnail(url="https://imgur.com/xhasHXb.png")
    embed.set_footer(text="Sent by {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)



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


 
"""    for x in range(len(list_a)):
        print(list_a[x])
    j = 0
    for j in range(len(list_b)):
        print(list_b[j])
        #j = j + 1"""