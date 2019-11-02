import asyncio
import discord
import random
import requests
import json
from tools import getlang,getpref

with open('token.txt','r') as f:
    TOKEN=f.read()
client = discord.Client()

def helpmain(message,client,lang,pref):
        if lang=='en':
            embed = discord.Embed(title='Help | List of commands',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name='Command categories',value='<a:matchinfo:595952615599374337>Match information \n<:exp:593470312088338441>DOTA 2 information \n<a:coinflip:594438507938709524>Random stuff \n'+u"\U0001F916"+'Bot information')
            embed.add_field(name='F.A.Q',value="Q: Where can I get my SteamID? \nA:Your SteamID is located in Your DOTA 2 profile: left of the profile picture, under profile name.\n\nQ: What's the server prefix \nA: You can get the server prefix by @mentioning yasha(send @yasha into any text channel)\n\n Q: Nothing is happening when I add reactions\nA: Possible reasons for this are:\n"+u"\u2022"+" You are adding reactions before bot changes ⏳ to ✅ on your command message\n"+u"\u2022"+"Someone else sent the command and only his reactions count\n"+u"\u2022"+" yasha lost connection to Discord / was restarted / is offline\n\n"+"Q: Why is the information about hero / item / mechanic / ability not relevant? \nA: Either Valve haven't uploaded latest patch notes to the Steam API or I have no opportunity to update the database\n*If there were no DOTA 2 updates recently then you should tell me about the mistake at the [Discord server](https://discord.gg/C9Qhg3B)*")
            return embed
        else:
            embed = discord.Embed(title='Помощь | Список команд',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name='Категории комманд',value='<a:matchinfo:595952615599374337>Информация о матчах \n<:exp:593470312088338441>Информация о DOTA 2 \n<a:coinflip:594438507938709524>Всякий рандом \n'+u"\U0001F916"+'Информация о боте')
            embed.add_field(name='Часто задаваемые вопросы',value="В: Где можно найти свой SteamID\nО:Ваш SteamID находится в Вашем профиле DOTA 2: слева от изображения профиля, под именем профиля.\n\nВ: Как узнать префикс сервера\nО: Чтобы получить префикс сервера, вы можете @mention бота(отправьте @yasha в любой текстовый канал)\n\nВ: После добавления реакции ничего не проиходит\nО: Возможные причины:\n"+u"\u2022"+" Вы добавляете реакции до того как бот сменит ⏳ на ✅ на сообщении-команде\n"+u"\u2022"+" Кто-то другой отправил команду и только его реакции имеют значение\n"+u"\u2022"+" yasha потерял соединение с Discord / был перезапущен / не в сети\n\n"+"Q: Почему информация о герое / предмете / способности / механике DOTA 2 не актуальна? \nA: Либо Valve еще не выгрузило изменения последнего обновления в Steam API, либо у меня нет возможности обновить базу данных\n*Если недавно не было обновлений, то вы можете сообщить об ошибке на [сервере Discord](https://discord.gg/C9Qhg3B)*")
            return embed
async def helpcom(message,client,command,lang,pref):
                com=command
                #без реакций   
                if com=='hero':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}hero <hero name>`',inline=False)
                        embed.add_field(name='Output',value="**Hero portarit, name, icon and aliases** \n\n**Short description**\n\n**Attributes**\n*hovering over an attribute icon reveals the name of the attribute*\nMessage color represents the color of hero's main attribite \nFirst three attributes<:str:591659961092669462><:agi:591659959905812500><:int:591659960551604234> show base value and value gained per level \nArmor<:armor:591659959960469524> shows base armor + armor gained from agility and base armor\n\n**Hero abilities**\n\n**Hero talents**\n"+u"\u2800",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}hero <Имя героя>`',inline=False)
                        embed.add_field(name='Результат',value=f"**Портрет героя, имя, иконка и псевдонимы** \n\n**Краткое описание**\n\n**Показатели героя**\n*При наведении курсора на иконку атрибута отображается его название*\nЦвет сообщения обозначает основной атрибут героя\nПервые три показателя<:str:591659961092669462><:agi:591659959905812500><:int:591659960551604234> отображают базовое значение и значение получаемое героем за повышение уровня \nБроня<:armor:591659959960469524> показывает сумму базовой брони и брони, полученной от атрибута ловкость, и базовую броню\n\n**Способности героя**\n\n**Таланты героя**\n"+u"\u2800",inline=False)
                        await message.channel.send(embed=embed)
                elif com=='item':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}item <item name>`',inline=False)
                        embed.add_field(name='Output',value=f"**Item icon, name and aliases** \n\n**Item abilities**\n\n**Description**\nAttributes and cost\nNotes \nLore \n\n**Additional info**\nIf the item can be bought in side or secret shop, then corresponding icons will appear here\n*Stackable* means you can have more than one of this item in a single inventory slot(e.g. Tango)",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}item <Имя героя>`',inline=False)
                        embed.add_field(name='Output',value="**Изображение предмета, название и альтернативные названия** \n\n**Способности предмета**\n\n**Описание**\nПоказатели и цена\nПримечания \nЛор \n\n**Дополнительная информация**\nЕсли предмет можно купить в боковой или потайной лавке, то в этом разделе появятся соответствующие иконки\n*Стакается* означает, что в одной ячейке инвентаря вы можете хранить несколько этих предметов(Пример: Танго)",inline=False)
                        await message.channel.send(embed=embed)
                elif com=='matches':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}matches <criteria 1> ... <criteria n>`\nYou can use\n'+u"\u2022"+' **<Hero name/alias>** to get matches where you played as <Hero>\n'+u"\u2022"+' **+<Hero name/alias>** to get matches where you played with <Hero> in your team\n'+u"\u2022"+' **-<Hero name/alias>** to get matches where you played against <Hero>\n'+u"\u2022"+' **win/won/victory** to get matches where you won\n'+u"\u2022"+' **lose/lost** to get matches where you lost\n'+u"\u2022"+f' **all** to get all matches available (Turbo, Events etc.)\n\n**Example**\n`{pref}matches grimstroke +brewmaster +ns -chen win all` will return all matches won by player <your SteamID> as <:grim:553950961161207809>Grimstroke with <:nightstalker:553951284454227969>Night Stalker and <:brew:553950617576669205>Brewmaster against <:chen:553950671280406528>Chen',inline=False)
                        embed.add_field(name='Output',value=f"List matches meeting given criterias (no more than 100 matches)",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}matches <критерий 1> ... <критерий n>`\nДопустимые критерии:\n'+u"\u2022"+' **<Имя/прозвище героя>** отберёт матчи, в которых вы играли за <Героя>\n'+u"\u2022"+' **+<Имя/прозвище героя>** отберёт матчи, в которых вы играли c <Героем> в команде\n'+u"\u2022"+' **-<Имя/прозвище героя>** отберёт матчи, в которых вы играли против <Героя>\n'+u"\u2022"+' **win/won/victory** отберёт матчи, в которых вы выиграли\n'+u"\u2022"+' **lose/lost** отберёт матчи, в которых вы проиграли\n'+u"\u2022"+f' **all**, чтобы рассматривать матчи всех игровых режимов (Turbo, События и т.д.)\n\n**Example**\n`{pref}matches grimstroke +brewmaster +ns -chen win all` вернет все выигранные матчи игрока <Ваш SteamID> за <:grim:553950961161207809>Grimstroke с <:nightstalker:553951284454227969>Night Stalker и <:brew:553950617576669205>Brewmaster против <:chen:553950671280406528>Chen',inline=False)
                        embed.add_field(name='Output',value="Список матчей, подходящих под заданные критерии(не более ста матчей)",inline=False)
                        await message.channel.send(embed=embed)
                elif com=='ability':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}ability <item name>`',inline=False)
                        embed.add_field(name='Output',value="**Ability icon, name and the hero it belongs to**\n\n**Ability description**\nDescription\nAttributes\n<:cooldown:595171442652479518>Cooldown\n<:manacost:595172991567134721>Mana cost\n<:2_:591306566603636747>Aghanim's upgrade\nDamage type\nWhether the ability pierces spell immunity  \n\n**Additional info**\nNotes\nLore\n"+u"\u2800",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}ability <Имя героя>`',inline=False)
                        embed.add_field(name='Output',value="**Иконка способности, название, владелец способности**\n\n**Описание способности**\nОписание\nПоказатели\n<:cooldown:595171442652479518>Длительность перезарядки\n<:manacost:595172991567134721>Затрачиваемая мана\n<:2_:591306566603636747>Улучшение с Aghanim's Scepter\nТип урона\nПроходит ли заклинание сквозь невосприимчивость к магии \n\n**Дополнительная информация**\nПримечания\nЛор\n"+u"\u2800",inline=False)
                        await message.channel.send(embed=embed)
                elif com=='abs':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}abs <criteria 1> .. <criteria n>`\nYou can use keywords\n'+u"\u2022"+' **cd**(Cooldown duration)\n'+u"\u2022"+' **mc**(Mana cost)\n'+u"\u2022"+' **damage**(Damage)\n'+u"\u2022"+' **atk_dmg**(Bonus attack damage)\n'+u"\u2022"+' **dur**(Duration)\n'+u"\u2022"+' **range**(Range)\n'+u"\u2022"+' **radius**(Area of effect)\n'+u"\u2022"+' **dps**(Damage per second)\n'+u"\u2022"+' **stun**(Stun)\n'+u"\u2022"+' **silence**(Silence)\n with operators `>=` и `<=`, for example, `!abs damage>=600 cd<=400` \n\nKeywords\n'+u"\u2022"+' **dmg_red**(Incoming damage reduction)\n'+u"\u2022"+' **slow**(Movement and/or attack slow)\n'+u"\u2022"+' **atk_spd**(Bonus attack speed)\n'+u"\u2022"+' **armor_red**(Armor reduction)\n'+u"\u2022"+' **crit**(Critical damage)\n'+u"\u2022"+' **lifesteal**(Lifesteal)\n'+u"\u2022"+' **hpregen**(Health regeneration)\n should be used without any operators or values, for example, `!abs crit cd<=3`',inline=False)
                        embed.add_field(name='Output',value=f"List of abilities meeting given criterias",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}abs <критерий 1> .. <критерий n>`\nВы можете использовать ключевые слова\n'+u"\u2022"+' **cd**(Длительность перезарядки)\n'+u"\u2022"+' **mc**(Затрачиваемая мана)\n'+u"\u2022"+' **damage**(Урон)\n'+u"\u2022"+' **atk_dmg**(Бонусный урон к атаке)\n'+u"\u2022"+' **dur**(Длительность)\n'+u"\u2022"+' **range**(Дальность применения)\n'+u"\u2022"+' **radius**(Радиус зоны эффекта)\n'+u"\u2022"+' **dps**(Урона в секунду)\n'+u"\u2022"+' **stun**(Оглушение)\n'+u"\u2022"+' **silence**(Заглушение)\n с операторами `>=` и `<=`, например, `!abs damage>=600 cd<=400` \n\nКлючевые слова\n'+u"\u2022"+' **dmg_red**(Снижение получаемого урона)\n'+u"\u2022"+' **slow**(Замедление атаки и/или передвижения)\n'+u"\u2022"+' **atk_spd**(Бонусная скорость атаки)\n'+u"\u2022"+' **armor_red**(Снижение брони)\n'+u"\u2022"+' **crit**(Критический урон)\n'+u"\u2022"+' **lifesteal**(Вампиризм)\n'+u"\u2022"+' **hpregen**(Регенерация здоровья)\n должны использоваться без операторов и значений, например, `!abs crit cd<=3`',inline=False)
                        embed.add_field(name='Output',value="Список способностей, подходящих под заданные критерии",inline=False)
                        await message.channel.send(embed=embed)
                elif com=='matchinfo' or com=='lastmatchinfo':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}matchinfo <match ID>`\nUsing **{pref}lastmatchinfo** automatically gets your latest parsed match',inline=False)
                        embed.add_field(name='Output',value="**League name**\n\n**Teams**\n*Color of the message represents the winner<:radiant:591631740435431465><:dire:561564058063732757>*\nTwo columns with player and basic info about them\n(K/D/A stands for Kills/Deaths/Assists, LH/D stands for Last Hits/Denies and NW stands for Net Worth)\nIf player's account is public his profile name is shown instead of hero's name\n\n**Draft**\nShows heroes banned and picked(in certain game modes)by teams\n\n**Teams' total gold and experience advantage graph**\nShows advantage of one team over another\nThick horizontal axis of the graph can sometimes match with one of the teams max advantage over the other team\nMax gold advantage is shown at the top(<:radiant:591631740435431465>Radiant) and bottom(<:dire:561564058063732757>Dire) right corners of the graph",inline=False)
                        embed.add_field(name='Reactions',value="**Heroes**\nPressing one of these returns more information about selected player, including his inventory at the end of the game and seasonal rank(if rank is available in player's profile, otherwise it defaults to <:Emoticon_Uncalibrated:591205373835476994>Uncalibrated)\n**Map**\nSelecting <:mapemoji:561636043204329556> returns the building map at the end of the game\n\nSelecting ❌ clears reactions",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}matchinfo <ID матча>`\nПри использовании `{pref}lastmatchinfo` выводится информация о вашем последнем обработанном матче',inline=False)
                        embed.add_field(name='Результат',value="**Название события**\n\n**Команды**\n*Цвет сообщения обозначает победителя<:radiant:591631740435431465><:dire:561564058063732757>*\nДве колонны с игроками и краткой информацией о них\n(K/D/A обозначает убийства/смерти/помощи, LH/D обозначает ластхиты/денаи и NW обозначает общую ценность игрока)\nЕсли профиль игрока публичный имя героя заменятся именем игрока\n\n**Драфт**\nПоказывает героев запрещенных и выбранных(в некоторых игровых режимах) командами\n\n**График преимущества сторон по общему количеству золота и опыта**\nПоказывает превосходство одной команды над другой по двум параметрам\nВыделенная горизонтальная ось графика может совпадать с максимальным преимуществом одной из команд\nМаксимальное премиущество команд по золоту показывается в верхнем\n(<:radiant:591631740435431465>Силы Света) и нижнем(<:dire:561564058063732757>Силы тьмы) углу графика",inline=False)
                        embed.add_field(name='Реакции',value="**Герои**\nВыбор одной из этих реакций выведет подробную информацию о игроке, в том числе его инвентарь в конце матча и медаль сезонного рейтинга(если ранг доступен в профиле игрока, иначе ранг отображается как <:Emoticon_Uncalibrated:591205373835476994>Без Ранга)\n**Карта**\nПри выборе <:mapemoji:561636043204329556> выводится карта построек в конце матча\n\nПри выборе ❌ удаляются все реакции",inline=False)
                        await message.channel.send(embed=embed)
                elif com=='patch':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}patch <hero/item name> <patch number>`')
                        embed.add_field(name='Output',value=f'Using `{pref}patch <hero/item name>` returns patch notes for <hero/item name> from the latest patch\n\nUsing `{pref}patch <patch>` returns the list of available patch notes in <patch> \n*If general notes are available it is stated in the title of the embed. To see them use `{pref}patch general <patch>`*\n\nUsing `{pref}patch` returns a list of patches available to use in <patch>\n*It can take up to a couple of days for new patches to become available*',inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}patch <имя героя/предмета> <номер патча>`')
                        embed.add_field(name='Результат',value=f'При использовании `{pref}patch <имя героя/предмета>` выводятся изменения <имя героя/предмета> в последнем досутпном патче \n\nПри использовании `{pref}patch <номер патча>` выводится список досутпных изменений в патче <номер патча> \n*Если доступны общие изменения, то об этом указано в заголовке сообщения. Чтобы их просмотреть используйте `{pref}patch general <номер патча>`*\n\nПри использовании `{pref}patch` выводится список доступных патчей, которые можно использовать в <номер патча>\n*Новые изменения патча становятся досутпны в течение нескольких дней после выхода обновления*',inline=False)
                        await message.channel.send(embed=embed)


                #реакции       
                elif com=='<a:matchinfo:595952615599374337>':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:radiant:591631740435431465>**Match information**<:dire:561564058063732757>',value=f'`{pref}matchinfo <match ID>`  -  information about match with the given ID.\n *For more info use `{pref}help matchinfo`*\n\n`{pref}lastmatchinfo`  -  information about your latest parsed match\n*If you add x after the command only your reactions will take effect*\n\n`{pref}profile <SteamID>` - player\'s DOTA 2 profile where you can see your personal statistics(including Battle Cup info), most picked heroes, heroes with highest winrate(heroes with more than 20 games only) and 10 latest matches\n*Use `{pref}profile private` to recieve profile via Direct Messages\n<a:note:595915864231116801>__The profile is only available for public accounts. You can make it public via DOTA 2 client settings__*\n\n`{pref}matches <keywords>` - your matches meeting given criterias\n*For more info use `{pref}help matches`*',inline=True)
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:radiant:591631740435431465>**Информация о матче**<:dire:561564058063732757>',value=f'`{pref}matchinfo <match ID>`  -  информация о матче с заданным ID. *Для подробного описания используйте `{pref}help matchinfo`*\n\n`{pref}lastmatchinfo`  -  информация о вашем последнем обработанном матче\n*Если добавить х после команды обрабатываться будут только ваши реакции*\n\n`{pref}profile <SteamID>` - DOTA 2 профиль пользователя с персональной статистикой, например, информация о Боевом Кубке, самые выбираемые герои, герои с наибольшим процентом побед(учитываются только герои, на которых пользователь сыграл более 20 раз) и 10 последних матчей\n*Используйте `{pref}profile private` если хотите получить профиль в личные сообщения\n<a:note:595915864231116801>__Доступны только профили пользователей с публичным профилем DOTA 2. Сделать профиль публичным можно в клиенте DOTA 2__*\n\n`{pref}matches <keywords>` - Ваши матчи, подходящие под заданные критерии\n*Для подробного описания используйте {pref}help matches*',inline=True)
                        return embed
                elif com=='<:exp:593470312088338441>':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:exp:593470312088338441>DOTA 2 information<:exp:593470312088338441>',value=f'`{pref}info / {pref}tome`  -  Encyclopedia with descriptions of DOTA 2 mechanics, attributes, gameplay\n\n`{pref}patch <hero/item name> <patch>` - patch notes for given hero/item in given patch. *For more info use `{pref}help patch`*\n\n`{pref}hero <hero name>`  -  information about given hero\n*For more info use `{pref}help hero`*\n\n`{pref}item <item name>`  -  information about given item\n*For more info use `{pref}help item`*\n\n`{pref}ability <ability name>`  -  information about given ability\n*For more info use `{pref}help ability`*\n\n`{pref}abs <criteria 1> .. <criteria n>`  -  return all hero abilities meeting given criterias\n*For more info and the list of criterias use `{pref}help abs`*',inline=True)
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:exp:593470312088338441>Информация о DOTA 2<:exp:593470312088338441>',value=f'`{pref}info / {pref}tome`  -  Энциклопедия с описаниями механик, аттрибутов, геймплея DOTA 2\n\n`{pref}patch <имя героя/предмета> <номер патча>` - Список изменений данного героя / предмета в данном патче *Для подробного описания используйте `{pref}help patch`*\n\n`{pref}hero <hero name>`  - информация о заданном герое\n*Для подробного описания используйте `{pref}help hero`*\n\n`{pref}item <item name>`  -  информация о заданном предмете\n*Для подробного описания используйте `{pref}help item`*\n\n`{pref}ability <ability name>`  -  Информация о заданной способности\n*Для подробного описания используйте `{pref}help ability`*\n\n`{pref}abs <критерий 1> .. <критерий n>`  -  все способности, чьи характеристики попадают под заданные критерии\n*Для подробного описания и списка критериев используйте `{pref}help abs`*',inline=True)
                        return embed
                elif com=='<a:coinflip:594438507938709524>':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<a:coinflip:594438507938709524>Random stuff<a:coinflip:594438507938709524>',value=f'`{pref}random <command>`  - returns a random value. Available commands:\n'+u"\u2022"+'**hero** - If you have a hard time picking a hero\n'+u"\u2022"+'**tip** - Random in-game pause tip\n'+u"\u2022"+f'**mode** - If you don\'t know which game mode to choose\n\n`{pref}flip` - coinflip\n\n`{pref}roll <right border> / <left border> <right border>` - get a random number in the given range. If no numbers are given the range is 1-100',inline=True)
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<a:coinflip:594438507938709524>Всякий рандом<a:coinflip:594438507938709524>',value=f'`{pref}random <command>`  - возвращает случайное значение. Допустимые команды:\n'+u"\u2022"+'**hero** - если сложно выбрать героя\n'+u"\u2022"+'**tip** - случайный совет с экрана паузы\n'+u"\u2022"+f'**mode** - если не получается выбрать режим игры\n\n`{pref}flip` - подбрасывание монетки\n\n`{pref}roll <правая граница> / <левая граница> <правая граница>` - возвращает случайное число в заданном диапазоне. Если числа не введены, то диапазон допустимых значений: 1-100',inline=True)
                        return embed
                elif com==u"\U0001F916":
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Bot information',value="Using this bot you can: \n"+u"\u2022"+" Get up-to-date information about DOTA 2 heroes, items, abilities, mechanics \n"+u"\u2022"+" Get information about a match \n"+u"\u2022"+" See patch notes for the latest DOTA 2 version \n"+u"\u2022"+" Show your personal DOTA 2 profile with your rank and information about your best heroes to other Discord users")
                        embed.add_field(name='Links',value="If you encounter any bugs, errors, typos - feel free to join [Discord help server](https://discord.gg/C9Qhg3B) and let me know about it\n*Also some update news will be posted here*")
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Информация о боте',value="С помощью этого бота вы можете: \n"+u"\u2022"+" Вы можете получить актулальную информацию о героях, предметах, способностях, механиках DOTA 2 \n"+u"\u2022"+" Получить информацию о матче \nПросмотреть изменения в последнем патче DOTA 2 \n"+u"\u2022"+" Показать свой DOTA 2 профиль с вашим рангом и информацией о лучших героях другим пользователям Discord")
                        embed.add_field(name='Ссылки',value="Если вы найдете какие-либо ошибки, баги, опечатки - можете присоединиться к [серверу Discord](https://discord.gg/C9Qhg3B) и сообщить об этом\n*Также новости об обновлениях будут размещаться на этом сервере*")
                        return embed
                else:
                    if lang=='en':
                        await message.channel.send(f'Command not found. Use {pref}help to see available commands')
                    else:
                        await message.channel.send(f'Команда не найдена. Используйте {pref}help чтобы получить список доступных команд')
