import os
import random

import discord
from discord.ext import commands
from dislash import slash_commands, Option, OptionType, InteractionClient, ActionRow, Button, ButtonStyle, OptionChoice, SlashInteraction, SelectMenu, SelectOption

TOKEN = os.getenv('MIKUBOTMEGRO_TOKEN')
client = commands.Bot(command_prefix='/')
slash = slash_commands.SlashClient(client)

guild_ids = [651039531096735745, 782619921108303892]
valorant_map_list = ['FRACTURE', 'BREEZE', 'ICEBOX', 'BIND', 'HAVEN', 'SPLIT', 'ASCENT']
valorant_weapon_list = [
    'Classic',
    'Shorty',
    'Frenzy',
    'Ghost',
    'Sheriff',
    'Stinger',
    'Spectre',
    'Bucky',
    'Judge',
    'Bulldog',
    'Guardian',
    'Phantom',
    'Vandal',
    'Marshal',
    'Operator',
    'Ares',
    'Odin',
]


@client.event
async def on_ready():
    print('DONE LOGIN')
    await client.change_presence(activity=discord.Game('プロセカ'))


@slash.command(
    name = 'valorant',
    description = 'Valorantに関するものを自動生成するよ',
    options = [
        Option(
            'random_type',
            description = 'ランダム生成の内容',
            required = True,
            type = OptionType.INTEGER,
            choices = [
                OptionChoice('RandomMap', 1),
                OptionChoice('Oshibori', 2),
            ]
        )
    ],
    guild_ids = guild_ids
)
async def valorant(inters: SlashInteraction, random_type: int):
    if random_type == 1:
        map_name = random.choice(valorant_map_list)
        await inters.reply(map_name)
        await inters.channel.send(file=discord.File('/home/pi/HelloWorld/Development/MikuBotMegro/' + map_name + '.webp'))
    elif random_type == 2:
        await inters.reply(random.choice(valorant_weapon_list))


@client.command()
async def uouo(ctx):
    row = ActionRow(
        Button(
            style=ButtonStyle.danger,
            label='Danger',
            custom_id='a'
        )
    )
    await ctx.send('AAAA', components=[row])


client.run(TOKEN)
