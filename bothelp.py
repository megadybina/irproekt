import asyncio
import discord
import random
import requests
import json
from tools import getlang,getpref

TOKEN = 'VerySecretCode'
client = discord.Client()

def helpmain(message,client,lang,pref):
        if lang=='en':
            embed = discord.Embed(title='Help | List of commands',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name='Command categories',value='<a:matchinfo:595952615599374337>Match information \n<:exp:593470312088338441>DOTA 2 information \n<a:Emoticon_bountyrune:594813355303239700>RPG \n'+u"\U0001F916"+'Bot information')
            embed.add_field(name='F.A.Q',value="Q: Where can I get my SteamID? \nA:Your SteamID is located in Your DOTA 2 profile: left of the profile picture, under profile name.\n\nQ: What's the server prefix \nA: You can get the server prefix by @mentioning yasha(send @yasha into any text channel)\n\n Q: Nothing is happening when I add reactions\nA: Possible reasons for this are:\n"+u"\u2022"+" You are adding reactions before bot changes ⏳ to ✅ on your command message\n"+u"\u2022"+"Someone else sent the command and only his reactions count\n"+u"\u2022"+" yasha lost connection to Discord / was restarted / is offline\n\n"+"Q: Why is the information about hero / item / mechanic / ability not relevant? \nA: Either Valve haven't uploaded latest patch notes to the Steam API or I have no opportunity to update the database\n*If there were no DOTA 2 updates recently then you should tell me about the mistake at the [Discord server](https://discord.gg/C9Qhg3B)*")
            return embed
        else:
            embed = discord.Embed(title='Помощь | Список команд',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
            embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
            embed.add_field(name='Категории комманд',value='<a:matchinfo:595952615599374337>Информация о матчах \n<:exp:593470312088338441>Информация о DOTA 2 \n<a:Emoticon_bountyrune:594813355303239700>RPG \n'+u"\U0001F916"+'Информация о боте')
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
                        embed.add_field(name='Output',value="**Иконка способности, название, владелец способности**\n\n**Описание способности**\nОписание\nПоказатели\n<:cooldown:595171442652479518>Длительность перезарядки\n<:manacost:595172991567134721>Затрачиваемая мана\n<:2_:591306566603636747>Улучшение с Aghanim's Scepter\nТип урона\nПроходит ли заклинание сквозь невосприимчивость магии \n\n**Дополнительная информация**\nПримечания\nЛор\n"+u"\u2800",inline=False)
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
                        embed.add_field(name='Результат',value=f'При использовании `{pref}patch <имя героя/предмета>` выводятся изменения <имя героя/предмета> в последнем досутпном патче \n\nПри использовании `{pref}patch <номер патча>` выводится список досутпных изменений в патче <patch> \n*Если досутпны общие изменения, то об этом указано в заголовке сообщения. Чтобы их просмотреть используйте `{pref}patch general <номер патча>`*\n\nПри использовании `{pref}patch` выводится список доступных патчей, которые можно использовать в <номер патча>\n*Новые изменения патча становятся досутпны в течение нескольких дней после выхода обновления*',inline=False)
                        await message.channel.send(embed=embed)
                elif com=='challenge':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Syntax',value=f'`{pref}chalenge`',inline=False)
                        embed.add_field(name='Output',value="You are given a random daily challenge, which you must complete within the next game",inline=False)
                        embed.add_field(name='Reactions',value="Use ❌ to cancel the daily challenge.\nUse ✅ to accept the daily challenge\n You can reroll the given challenge once using "+ u'\U0001F500'+".\n Using <a:Emoticon_obs:593495627342676040> initiates a check of the given challenge if you accepted it.",inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Синтаксис',value=f'`{pref}chalenge`',inline=False)
                        embed.add_field(name='Результат',value="Вам выдается случайное ежедневное испытание, которое нужно пройти в течение следующей игры. За выполнение дается вознаграждение, величина которого зависит от вашего результата",inline=False)
                        embed.add_field(name='Реакции',value="Используйте ❌, чтобы отказаться от испытания.\nИспользуйте ✅, чтобы принять испытание\n Вы можете один раз 'зарероллить' испытание, нажав на "+ u'\U0001F500'+"\nПри использовании <a:Emoticon_obs:593495627342676040> инициируется проверка данного испытания",inline=False)
                        await message.channel.send(embed=embed)

                #реакции       
                elif com=='<a:matchinfo:595952615599374337>':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:radiant:591631740435431465>**Match information**<:dire:561564058063732757>',value=f'`{pref}matchinfo <match ID>`  -  information about match with the given ID.\n *For more info use `{pref}help matchinfo`*\n\n`{pref}lastmatchinfo`  -  information about your latest parsed match\n*If you add x after the command only your reactions will take effect*\n',inline=True)
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:radiant:591631740435431465>**Информация о матче**<:dire:561564058063732757>',value=f'`{pref}matchinfo <match ID>`  -  информация о матче с заданным ID. *Для подробного описания используйте `{pref}help matchinfo`*\n\n`{pref}lastmatchinfo`  -  информация о вашем последнем обработанном матче\n*Если добавить х после команды обрабатываться будут только ваши реакции*\n',inline=True)
                        return embed
                elif com=='<:exp:593470312088338441>':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:exp:593470312088338441>DOTA 2 information<:exp:593470312088338441>',value=f'`{pref}info / {pref}tome`  -  Encyclopedia with descriptions of DOTA 2 mechanics, attributes, gameplay\n\n`{pref}patch <hero/item name> <patch>` - patch notes for given hero/item in given patch. *For more info use `{pref}help patch`*\n\n`{pref}hero <hero name>`  -  information about given hero\n*For more info use `{pref}help hero`*\n\n`{pref}item <item name>`  -  information about given item\n*For more info use `{pref}help item`*\n\n`{pref}ability <ability name>`  -  information about given ability\n*For more info use `{pref}help ability`*',inline=True)
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='<:exp:593470312088338441>Информация о DOTA 2<:exp:593470312088338441>',value=f'`{pref}info / {pref}tome`  -  Энциклопедия с описаниями механик, аттрибутов, геймплея DOTA 2\n\n`{pref}patch <имя героя/предмета> <номер патча>` - Список изменений данного героя / предмета в данном патче *Для подробного описания используйте `{pref}help patch`*\n\n`{pref}hero <hero name>`  - информация о заданном герое\n*Для подробного описания используйте `{pref}help hero`*\n\n`{pref}item <item name>`  -  информация о заданном предмете\n*Для подробного описания используйте `{pref}help item`*\n\n`{pref}ability <ability name>`  -  Информация о заданной способности\n*Для подробного описания используйте `{pref}help ability`*\n',inline=True)
                        return embed
                elif com=='<a:Emoticon_bountyrune:594813355303239700>':
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name="<a:Emoticon_bountyrune:594813355303239700>**Discord RPG**<a:Emoticon_bountyrune:594813355303239700>",value=f'`{pref}profile` - your profile where you can see your DOTA 2 profile with your rank, heroes with most matches and heroes with best winrate and your RPG profile with your <:gold:553976492779110410>gold and <:exp:593470312088338441>experience recieved by completing challenges\n *You can use `{pref} profile private` to get your profile as a private message*\n\n`{pref}games`  -  a list of available games\n\n`{pref}shop`  -  a shop where you can spend your <:gold:553976492779110410>gold\n\n`{pref}challenge` - get a random challenge to complete within the next match\n*For more info use `{pref}help challenge`*',inline=True)
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name="<a:Emoticon_bountyrune:594813355303239700>**Discord RPG**<a:Emoticon_bountyrune:594813355303239700>",value=f'`{pref}profile` - ваш DOTA 2 профиль в котором отображается ваш ранг, герои с наибольшим числом матчей и лучшим соотношением побед / поражений, и ваш RPG профиль в котором отображается ваше <:gold:553976492779110410>золото и <:exp:593470312088338441>опыт, полученный за выполнение испытаний\n *Вы можете использовать`{pref}profile private` чтобы получить ваш профиль в личные сообщения*\n\n`{pref}games`  -  список доступных игр\n\n`{pref}shop`  -  лавка, в которой вы можете потратить ваше <:gold:553976492779110410>золото\n\n`{pref}challenge` - получите случайное испытание, которое нужно пройти в следующем матче\n*Для подробного описания используйте `{pref}help challenge`*',inline=True)
                        return embed
                elif com==u"\U0001F916":
                    if lang=='en':
                        embed = discord.Embed(title='Help',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Bot information',value="Using this bot you can: \n"+u"\u2022"+" Get up-to-date information about DOTA 2 heroes, items, abilities, mechanics \n"+u"\u2022"+" Get information about a match \n"+u"\u2022"+" See patch notes for the latest DOTA 2 version \n"+u"\u2022"+" Show your personal DOTA 2 profile with your rank and information about your best heroes to other Discord users \n"+u"\u2022"+" Play an RPG game and get challenges to complete in-game")
                        embed.add_field(name='Links',value="If you encounter any bugs, errors, typos - feel free to join [Discord help server](https://discord.gg/C9Qhg3B) and let me know about it\n*Also some update news will be posted here*")
                        return embed
                    else:
                        embed = discord.Embed(title='Помощь',colour=discord.Colour(0x9d10bb),url="https://discordapp.com")
                        embed.set_footer(text=f"{client.user.name} | {pref}help", icon_url=client.user.avatar_url_as(format='png'))
                        embed.add_field(name='Информация о боте',value="С помощью этого бота вы можете: \n"+u"\u2022"+" Вы можете получить актулальную информацию о героях, предметах, способностях, механиках DOTA 2 \n"+u"\u2022"+" Получить информацию о матче \nПросмотреть изменения в последнем патче DOTA 2 \n"+u"\u2022"+" Показать свой DOTA 2 профиль с вашим рангом и информацией о лучших героях другим пользователям Discord \n"+u"\u2022"+" Играть в RPG игру и получать испытания, которые нужно пройти в DOTA 2")
                        embed.add_field(name='Ссылки',value="Если вы найдете какие-либо ошибки, баги, опечатки - можете присоединиться к [серверу Discord](https://discord.gg/C9Qhg3B) и сообщить об этом\n*Также новости об обновлениях будут размещаться на этом сервере*")
                        return embed
                else:
                    if lang=='en':
                        await message.channel.send(f'Command not found. Use {pref}help to see available commands')
                    else:
                        await message.channel.send(f'Команда не найдена. Используйте {pref}help чтобы получить список доступных команд')
