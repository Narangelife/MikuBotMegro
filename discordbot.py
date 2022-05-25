import json
import os
import random
import uuid

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
megro_role_ids = {
    16: 782622394217005066,
    17: 782622369151713301,
    18: 782622338050949160,
    19: 782622297788907520,
    20: 782622435496296488,
    21: 832626956302155796,
    22: 905297269492944926,
}


@client.event
async def on_ready():
    print('[SERVER] DONE LOGIN')
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
        print('[SERVER] Valorant random map generated')
    elif random_type == 2:
        await inters.reply(random.choice(valorant_weapon_list))
        print('[SERVER] Valorant random weapon generated')


@slash.command(
    name = 'year_uec',
    description = '年度タグを付与するよ',
    options = [
        Option(
            'year',
            description = '入学年度',
            required = True,
            type = OptionType.INTEGER,
        ),
        Option(
            'operation',
            description='付与操作',
            required = True,
            type=OptionType.INTEGER,
            choices=[
                OptionChoice('ADD', 1),
                OptionChoice('REMOVE', 2)
            ]
        )
    ],
    guild_ids = [782619921108303892] #目黒会のみ
)
async def year_uec(inters: SlashInteraction, year: int, operation: int):
    if 16 <= year <= 22:
        role = inters.guild.get_role(megro_role_ids[year])
        if operation == 1:
            await inters.author.add_roles(role)
            embed_text = discord.Embed(title='DONE', description=str(year) + '生ロールを付与しました', color=0x98f5ff)
            print('[SERVER] Add ' + str(year) + '生 role from ' + inters.author.name)
        elif operation == 2:
            await inters.author.remove_roles(role)
            embed_text = discord.Embed(title='DONE', description=str(year) + '生ロールを削除しました', color=0x98f5ff)
            print('[SERVER] Remove ' + str(year) + '生 role from ' + inters.author.name)
    else:
        embed_text = discord.Embed(title='INPUT ERROR', description='入力は16以上22以下です', color=0xff0000)

    await inters.reply(embed=embed_text)


@slash.command(
    name = 'paper',
    description = 'VOC-A PROJECT SECRET RESEARCH PAPER',
    options = [
        Option(
            'index',
            description='INDEX',
            required=True,
            type=OptionType.INTEGER
        )
    ],
    guild_ids = guild_ids
)
async def paper(inters: SlashInteraction, index: int):
    if 1 <= index <= 1:
        with open('/home/pi/HelloWorld/Development/MikuBotMegro/PAPER/PAPER_' + str(index) + '.json', 'r') as fi:
            json_load = json.load(fi)
            embed_text = discord.Embed.from_dict(json_load)
        #embed_text = discord.Embed(title='VOC-A P.S.E.P. #' + str(index), description=f.read(), color=0x81ffb1)
        embed_text.set_footer(text='DOCTOR ID: ' + str(uuid.uuid4())[-6:], icon_url="https://cdn.discordapp.com/embed/avatars/2.png")
        print('[SERVER] P.S.E.P. #' + str(index) + ' displayed')
    else:
        embed_text = discord.Embed(title='VOC-A P.S.E.P. ---ERROR', description='INPUT INDEX IS NOT FOUND\n ERROR CODE: [0x2de837]', color=0xff0000)
        print('[SERVER] P.S.E.P. Input index is not found ERROR')

    await inters.reply(embed=embed_text)


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


@client.command()
async def test(ctx):
    msg = await ctx.send(
        "This message has a select menu!",
        components=[
            SelectMenu(
                custom_id="test",
                placeholder="Choose up to 2 options",
                max_values=2,
                options=[
                    SelectOption("Option 1", "value 1"),
                    SelectOption("Option 2", "value 2"),
                    SelectOption("Option 3", "value 3")
                ]
            )
        ]
    )
    # def check(inter):
    #     # inter is instance of MessageInteraction
    #     # read more about it in "Objects and methods" section
    #     if inter.author == ctx.author
    # Wait for a menu click under the message you've just sent
    inter = await msg.wait_for_dropdown()
    # Tell which options you received
    labels = [option.label for option in inter.select_menu.selected_options]
    await inter.reply(f"Your choices: {', '.join(labels)}")


client.run(TOKEN)
