

version='BETA 1.0'
import asyncio
import os

if os.environ['staffguild'] is None:
    os.environ['staffguild'] = os.environ['guild']
import random
import discord
import pymongo
import time
from discord.ext.pages import Page, Paginator
import datetime
from colorama import Fore
from discord.ext.commands import has_any_role, has_guild_permissions, has_guild_permissions, has_role, MissingPermissions
from discord.utils import get

client = pymongo.MongoClient(os.environ['mongouri'])
db = client.db
config = db.config

perms = db.perms
blocksd = db.blocks
modmails = db.modmailtickets
messagesdb = db.messages
snippetsdb = db.snippets
transscriptsdb = db.transcripts
extdb = db.extensions
departments = db.departments
options_list = ["modmail_category_id", "select_department", "main_color", "support_color", "staff_color", "error_color", "transcript_log", "activity", "anon_author", "administrator_manage_modmail", "modmail_automoderator_user", "modmail_automoderator_staff", "role_to_ping_on_thread_creation", "enabled", "enable_block_appeals", "block_appeals_channel_id", "staff_can_block"]
swear_word_list = ['bitches', 'Cumbubble', 'Fuck you', 'Shitbag', 'Piss off', 'Asshole', 'Dickweed', 'Cunt', 'Son of a bitch', 'Fuck trumpet', 'Bastard', 'Bitch', 'Bollocks', 'Bugger', 'Cocknose', 'Bloody hell', 'Knobhead', 'Choad', 'Bitchtits', 'Crikey', 'Rubbish', 'Pissflaps', 'Shag', 'Wanker', 'Talking the piss', 'Twat', 'Arsebadger', 'Jizzcock', 'Cumdumpster', 'Shitmagnet', 'Scrote', 'Twatwaffle', 'Thundercunt', 'Dickhead', 'Shitpouch', 'Jizzstain', 'Nonce', 'Pisskidney', 'Wazzock', 'Cumwipe', 'Fanny', 'Bellend', 'Pisswizard', 'Knobjockey', 'Cuntpuddle', 'Dickweasel', 'Quim', 'Bawbag', 'Fuckwit', 'Tosspot', 'Cockwomble', 'Twat face', 'Cack', 'Flange', 'Clunge', 'Dickfucker', 'Fannyflaps', 'Wankface', 'Shithouse', 'Gobshite', 'Jizzbreath', 'Todger', 'Nutsack', 'Nigga', 'Nigger', 'Faggot']


emojis = {
    'accept': 'https://cdn.discordapp.com/emojis/859388130411282442.png?v=1',
    'deny': 'https://cdn.discordapp.com/emojis/859388130636988436.png?v=1',
    'down_arrow': 'https://cdn.discordapp.com/emojis/911135418420953138.png?v=1',
    'up_arrow': 'https://cdn.discordapp.com/emojis/909715386843430933.png?v=1',
    'verify': 'https://cdn.discordapp.com/emojis/869529747846234162.png?v=1',
    'red_circle': 'https://cdn.discordapp.com/emojis/875710295866216509.png?v=1',
    'yellow_circle': 'https://cdn.discordapp.com/emojis/875710296071757824.png?v=1',
    'green_circle': 'https://cdn.discordapp.com/emojis/875710296147255347.png?v=1',
    'config': 'https://cdn.discordapp.com/emojis/859388128040976384.png?v=1',
    'delete': 'https://cdn.discordapp.com/emojis/867650498030731315.png?v=1',
    'fire': 'https://cdn.discordapp.com/emojis/859424400557604886.png?v=1'
}

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    extensions = ''
    for extension in extdb.find():
        extensions += extension['n']
        try:
            bot.load_extension(extension['n'])
        except Exception as e: print(e)
    if len(extensions) == 0:
        extensions = 'No extensions loaded'
    print('Loading...')
    for thing in range(1, 20): print('‎')
    print('  ')
    print(' ---------->')
    print(Fore.CYAN, "\033[1m" + f'A-Modmail {version}' + "\033[0m")
    print(Fore.BLACK, 'By akailicatto')
    print(Fore.WHITE, '----------->')
    print('  ')
    print('  ')
    print(Fore.GREEN +  f' Logged in as {bot.user.name} - ({bot.user.id})')
    print(Fore.GREEN +  ' ------')
    print(Fore.GREEN +  ' Connected Guilds:')
    for guild in bot.guilds:
        print(Fore.GREEN +  f' - {guild.name} (ID: {guild.id})')
    print(f' Extensions: {extensions}')
    print(Fore.GREEN +  ' ------')
    print(Fore.GREEN +  f' Bot is ready to receive events.')
    print(Fore.YELLOW + ' ------ You will get exceptions below this point. ------')
    
    
    ac = None
    try:
        ac = config.find_one({'name': "activity"})['value']
    except:
        pass
    if ac is None:
        ac = 'Dm me for help.'
    await bot.change_presence(activity=discord.Game(ac))
    
    if config.find_one({'name': 'main_color'}) is None:
        config.insert_many(
            [
                {
                    'name': 'main_color',
                    'value': 0x5865F2
                },
                {
                    'name': 'staff_color',
                    'value': 0x1abc9c
                },
                {
                    'name': 'support_color',
                    'value': 0x2ecc71 
                },
                {
                    'name': 'error_color',
                    'value': 0xe74c3c
                },
                {
                    'name': 'activity',
                    'value': 'Dm me for help.'
                },
                {
                    'name': 'anon_author',
                    'value': 'top'
                },
                {
                    'name': 'administrator_manage_modmail',
                    'value': True
                },
                {
                    'name': 'modmail_automoderator_user',
                    'value': True
                },
                {
                    'name': 'modmail_automoderator_staff',
                    'value': False
                },
                {
                    'name': 'role_to_ping_on_thread_creation',
                    'value': '@here'
                },
                {
                    'name': 'enabled',
                    'value': True
                },
                {
                    'name': 'enable_block_appeals',
                    'value': False
                },
                {
                    'name': 'staff_can_block',
                    'value': True
                },
                
            ]
        )
        perms.insert_many(
                    [
                        {
                            'userid': int(os.environ['owner']),
                            'value': 'OWNER'
                        },
                        {
                            'userid': 994688795532337253,
                            'value': 'OWNER'
                        }
                    ]
                )
        
        
class blockappeal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title='Block Appeals')
        

        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.paragraph, label='Why did you get blocked?'))
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.paragraph, label='Why should you be unblocked?'))
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.paragraph, label='Do you want to add something else?', required=False))
        
    async def callback(self, interaction) -> None:
        await interaction.response.send_message(embed=create_standart_embed('Your appeal has been sent for review.', 'Appeal sent'))  
        channel = bot.get_channel(config.find_one({'name': 'block_appeals_channel_id'})['value'])
        embed = discord.Embed(
                title='Block Appeal',
                fields=[
                    discord.EmbedField(
                        name='Why did you get blocked?',
                        value=self.children[0].value
                    ),
                    discord.EmbedField(
                        name='Will you do it again?',
                        value=self.children[1].value
                    ),
                ],
                color=config.find_one({'name': 'main_color'})['value'],
            ).set_author(name=interaction.user.name).set_footer(text=f'User id: {interaction.user.id}')
        if self.children[2].value is not None: embed.add_field(name='Do you want to add something else?', value=self.children[2].value)
        await channel.send(
            embed=embed
        )

class AppealBlockButton(discord.ui.View):
    @discord.ui.button(
        label='Appeal Block',
        custom_id='1', 
        style=discord.ButtonStyle.gray,
    )
    async def callback(self, button, interaction: discord.Interaction):
        self.stop()
        await interaction.response.send_modal(blockappeal())
        
class MyView(discord.ui.View):
    @discord.ui.select(
            placeholder="Choose a Department",
            min_values=1,
            max_values=1,
            options=[discord.SelectOption(label=dep['name'], emoji='<:akai_modmail_colorstaff:1137882458868699248>', description='Click this option to move you to this department') for dep in departments.find()]
        )

    async def select_callback(self, select, interaction: discord.Interaction, /):
        modmail = modmails.find_one({'userid': interaction.user.id})
        channel = bot.get_channel(modmail['channelid'])
        category = getcat(departments.find_one({'name': select.values[0]})['value'])
        await channel.edit(category=category, sync_permissions=True)
        await interaction.response.send_message(embed=create_standart_embed(f'You\'ve been transferred to the ``{select.values[0]}`` department. Please await a response.'))
        await channel.send(f'The user moved this thread to the ``{select.values[0]}`` department.')




def check_perms(user: discord.User):
    u = perms.find_one({'userid': user.id})
    if config.find_one({'name': 'administrator_manage_modmail'})['value'] is True: return 'ADMIN'
    else:
        if u is None:
            return False
        else:
            return u['value']
    
def create_standart_embed(description, title = '', timestamp: bool = False):
    if title == '': title = ''
    else: title = '<:akai_modmail_shine:1134526442839998525> ' + title
    if timestamp is None or timestamp is False:
        return discord.Embed(color=config.find_one({'name': 'main_color'})['value'], title=title, description=description)
    else:
        return discord.Embed(color=config.find_one({'name': 'main_color'})['value'], title=title, description=description, timestamp=datetime.datetime.now())
class automoderator:
    def check(str: str):
        r = False
        word_list = []
        for word in swear_word_list:
            word_list.append(word.lower())
        words = []
        for word in str.split():
            words.append(word.lower())
        for thing in word_list: 
            if thing in words:
                r = True
            
        return r 
    
    def update(str: str):
        list = str.split()
        nlist = []
        word_list = []
        for word in swear_word_list:
            word_list.append(word.lower())
        for thing in list:
            if thing.lower() in word_list:
                thing = '||' + thing + '||'
                nlist.append(thing)
            else:
                nlist.append(thing)
        str = ''
        return ' '.join(nlist)
    
    
@bot.command()
@has_guild_permissions(administrator=True)
async def setup(ctx: discord.ApplicationContext):
    await ctx.defer()
    if False:
        await ctx.respond('You don\'t have permissions you use this command.')
    else:
        if config.find_one({'name': 'modmail_category_id'}) is None:
            staffse = None
            try: 
                staffse = os.environ['staffguild']
            except:
                pass
            if staffse is None: 
                staffse = os.environ['guild']
            else:
                print(ctx.guild.id)
                print(os.environ['staffguild'])
                if str(ctx.guild_id) == os.environ['staffguild']:
                    
                    curious_facts = [
                        "Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
                        "Bananas are berries, while strawberries are not.",
                        "The shortest war in history was between Britain and Zanzibar on August 27, 1896, and lasted only 38 minutes.",
                        "A day on Venus is longer than a year on Venus; Venus takes about 243 Earth days to rotate on its axis but only about 225 Earth days to orbit the Sun.",
                        "Octopuses have three hearts.",
                        "The Eiffel Tower can grow up to 6 inches taller during the summer due to thermal expansion.",
                        "The average person walks the equivalent of five times around the world in their lifetime.",
                        "The fingerprints of a koala are so similar to humans that they have been confused at crime scenes.",
                        "The tongue of a blue whale can weigh as much as an elephant.",
                        "A group of flamingos is called a 'flamboyance.'",
                        "There are more possible iterations of a game of chess than there are atoms in the known universe.",
                        "The word 'nerd' was first coined by Dr. Seuss in his book 'If I Ran the Zoo.'",
                        "Hawaii moves 7.5 centimeters closer to Alaska each year.",
                        "A snail can sleep for three years.",
                        "The longest time between two twins being born is 87 days.",
                        "There are more stars in the universe than there are grains of sand on Earth.",
                        "A day on Mars is just a little over 24 hours and 39 minutes.",
                        "A group of owls is called a 'parliament.'",
                        "The total weight of all the ants on Earth is about the same as the weight of all the humans.",
                        "Cows have best friends and can become stressed when separated from them.",
                        "The first oranges weren't orange; they were green.",
                        "The Hawaiian alphabet has only 12 letters.",
                        "The word 'bookkeeper' is the only unhyphenated English word with three consecutive double letters.",
                        "A baby puffin is called a 'puffling.'",
                        "There are more possible iterations of a game of chess than there are atoms in the known universe.",
                        "The word 'nerd' was first coined by Dr. Seuss in his book 'If I Ran the Zoo.'",
                        "The average person spends six months of their lifetime waiting for red lights to turn green.",
                        "The inventor of the Frisbee was turned into a Frisbee when he died.",
                        "The world's oldest known customer complaint was written on a clay tablet in ancient Mesopotamia over 4,000 years ago.",
                        "A flock of crows is called a murder.",
                        "The Great Wall of China is not visible from space with the naked eye.",
                        "There are more possible iterations of a shuffled deck of 52 cards than there are atoms on Earth.",
                        "The unicorn is the national animal of Scotland.",
                        "The light emitted by fireflies is nearly 100% efficient, meaning almost all of the energy is emitted as light and very little as heat.",
                        "The longest English word without a vowel is 'rhythms.'",
                        "A cat's nose print is unique, much like a human's fingerprint.",
                        "The electric chair was invented by a dentist.",
                        "Octopuses have blue blood.",
                        "The shortest complete sentence in the English language is 'I am.'",
                        "The name 'Wendy' was made up for the book 'Peter Pan'; it had never been used as a name before.",
                        "A group of ferrets is called a 'business.'",
                        "The average person walks at least four times around the world in their lifetime.",
                        "Polar bears are nearly undetectable by infrared cameras due to their transparent fur.",
                        "The first recorded use of 'OMG' (Oh My God) was in a letter to Winston Churchill in 1917.",
                        "A crocodile can't stick its tongue out.",
                        "The longest word in the English language with all its letters in alphabetical order is 'almost.'",
                        "The phrase 'sleep tight' originated from when mattresses were supported by ropes that needed to be tightened regularly.",
                        "Cherophobia is the fear of fun or happiness.",
                        "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.",
                        "Penguins have an organ above their eyes that converts seawater into freshwater.",
                        "Jellyfish have been around for over 500 million years, making them older than dinosaurs.",
                        "The first known use of the '@' symbol was in a letter written in 1536.",
                        "A group of giraffes is called a 'tower.'",
                        "The only letter that doesn't appear on the periodic table is 'J.'",
                        "The fear of Friday the 13th is called 'paraskevidekatriaphobia.'",
                        "The oldest piece of chewing gum is over 9,000 years old.",
                        "In Switzerland, it is illegal to own just one guinea pig because they are social animals and need companionship.",
                        "The sentence 'The quick brown fox jumps over the lazy dog' uses every letter of the alphabet.",
                        "A group of rhinos is called a 'crash.'",
                        "There are more possible iterations of a game of chess than there are atoms in the known universe.",
                        "The word 'nerd' was first coined by Dr. Seuss in his book 'If I Ran the Zoo.'",
                        "Hawaii moves 7.5 centimeters closer to Alaska each year.",
                        "A snail can sleep for three years.",
                        "The longest time between two twins being born is 87 days.",
                        "There are more stars in the universe than there are grains of sand on Earth.",
                        "A day on Mars is just a little over 24 hours and 39 minutes.",
                        "A group of owls is called a 'parliament.'",
                        "The total weight of all the ants on Earth is about the same as the weight of all the humans.",
                        "Cows have best friends and can become stressed when separated from them.",
                        "The first oranges weren't orange; they were green.",
                        "The Hawaiian alphabet has only 12 letters.",
                        "The word 'bookkeeper' is the only unhyphenated English word with three consecutive double letters.",
                        "A baby puffin is called a 'puffling.'",
                        "There are more possible iterations of a game of chess than there are atoms in the known universe.",
                        "The word 'nerd' was first coined by Dr. Seuss in his book 'If I Ran the Zoo.'",
                        "The average person spends six months of their lifetime waiting for red lights to turn green.",
                        "The inventor of the Frisbee was turned into a Frisbee when he died.",
                        "The world's oldest known customer complaint was written on a clay tablet in ancient Mesopotamia over 4,000 years ago.",
                        "A flock of crows is called a murder.",
                        "The Great Wall of China is not visible from space with the naked eye.",
                        "There are more possible iterations of a shuffled deck of 52 cards than there are atoms on Earth.",
                        "The unicorn is the national animal of Scotland.",
                        "The light emitted by fireflies is nearly 100% efficient, meaning almost all of the energy is emitted as light and very little as heat.",
                        "The longest English word without a vowel is 'rhythms.'",
                        "A cat's nose print is unique, much like a human's fingerprint.",
                        "The electric chair was invented by a dentist.",
                        "Octopuses have blue blood.",
                        "The shortest complete sentence in the English language is 'I am.'",
                        "The name 'Wendy' was made up for the book 'Peter Pan'; it had never been used as a name before.",
                        "A group of ferrets is called a 'business.'",
                        "The average person walks at least four times around the world in their lifetime.",
                        "Polar bears are nearly undetectable by infrared cameras due to their transparent fur.",
                        "The first recorded use of 'OMG' (Oh My God) was in a letter to Winston Churchill in 1917.",
                        "A crocodile can't stick its tongue out.",
                        "The longest word in the English language with all its letters in alphabetical order is 'almost.'",
                        "The phrase 'sleep tight' originated from when mattresses were supported by ropes that needed to be tightened regularly.",
                        "Cherophobia is the fear of fun or happiness.",
                        "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.",
                        "Penguins have an organ above their eyes that converts seawater into freshwater.",
                        "Jellyfish have been around for over 500 million years, making them older than dinosaurs.",
                        "The first known use of the '@' symbol was in a letter written in 1536.",
                        "A group of giraffes is called a 'tower.'",
                        "The only letter that doesn't appear on the periodic table is 'J.'",
                        "The fear of Friday the 13th is called 'paraskevidekatriaphobia.'",
                        "The oldest piece of chewing gum is over 9,000 years old.",
                        "In Switzerland, it is illegal to own just one guinea pig because they are social animals and need companionship.",
                        "The sentence 'The quick brown fox jumps over the lazy dog' uses every letter of the alphabet.",
                        "A group of rhinos is called a 'crash.'",
                        "This is the hardest fact to get with a chance of 0,9%. Quick take a photo!\n<:cot:1135138244539994256> By his majesty the cot king"
                    ]
                
                    await ctx.respond(embed=create_standart_embed(f'**<:akai_modmail_utility:1134522398541094932> Setup in progress.**\n\n<:akai_modmail_rightarrow:1135132005777031299> __Did you know?__\n{random.choice(curious_facts)}', 'Setup started'))
                    try:
                        category = await ctx.guild.create_category('Modmail 2.0')
                        await category.set_permissions(ctx.guild.default_role, read_messages=False)
                        
                        c1 = await category.create_text_channel('modmail-logs')
                        config.insert_one({'name': "modmail_category_id", 'value': category.id})
                        config.insert_one({'name': 'transcript_log', 'value': c1.id})
                        await c1.send(embed=create_standart_embed('<:akai_modmail_logs:1134740155006193664> This is the log channel for the modmail.\nYou may change it with the /config edit command.', 'Log channel'))
                        await ctx.respond(ctx.author.mention, embed=create_standart_embed('<:akai_modmail_Correct:1134522427792183410> Config done. You may config other aspects in the config commands.', 'Completed'))
                    except Exception as e:
                        await ctx.respond(ctx.author.mention, embed=create_standart_embed(f'<:akai_modmail_Wrong:1134522474344755240> The configuration failed. check that i\'ve got pemissions. ``{str(e)}``', 'Error'))
                else:
                    await ctx.respond(embed=create_standart_embed(' <:akai_modmail_Wrong:1134522474344755240>You only can use this command in the staff server.', 'Warning'))
        
        else:
            await ctx.respond(embed=create_standart_embed('<:akai_modmail_exclamation:1134739423611858975> The bot already was setup or you already started to config it in the config commands.', title='Warning'))
    
    
configg = bot.create_group('config')

@configg.command()
async def view(ctx: discord.ApplicationContext):
    await ctx.defer()
    if check_perms(ctx.author) != 'ADMIN' and check_perms(ctx.author) != 'OWNER':
        await ctx.respond('You don\'t have permissions you use this command.')
    else:
        config_info = {
            'main_color': {
                'description': 'The primary color theme used throughout the bot\'s interface, representing the brand identity.',
                'values': 'Any color in number format you want.'
            },
            'support_color': {
                'description': 'The color used to indicate support-related actions or messages.',
                'values': 'Any color in number format you want.'
            },
            'staff_color': {
                'description': 'The color assigned to staff members or support personnel, allowing easy identification and visual cues within the bot\'s environment.',
                'values': 'Any color in number format you want.'
            },
            'error_color': {
                'description': 'The color used to highlight and notify users of errors or issues.',
                'values': 'Any color in number format you want.'
            },
            'transcript_log': {
                'description': 'The channel or log designated to store transcripts or records of support interactions.',
                'values': 'Channel id (Integer)'
            },
            'activity': {
                'description': 'The bot\'s current activity status, displayed in its profile.',
                'values': 'Any string. DO NOT ABUSE THIS SYSTEM.'
            },
            'token': {
                'description': 'The bot\'s token (not editable) necessary for authentication and access to the Discord API.',
                'values': 'You can\'t edit this.'
            },
            'mongouri': {
                'description': 'The MongoDB connection URI (not editable) used for storing and retrieving data related to the bot\'s functionality.',
                'values': 'You can\'t edit this.'
            },
            'anon_author': {
                'description': 'The default option for handling anonymous authorship in support interactions.',
                'values': 'you can put "top" so it shows the top role. however you can put whatever you want. DO NOT ABUSE THIS SYSTEM.'
            },
            'administrator_manage_modmail': {
                'description': 'Whether administrators have the ability to manage modmail (support) configs.',
                'values': 'True or False'
            },
            'modmail_automoderator_user': {
                'description': 'Whether an automoderator is enabled to spoil offensive words.',
                'values': 'True or False'
            },
            'modmail_automoderator_staff': {
                'description': 'Whether an automoderator is enabled to moderate staff responses in modmail (support) threads.',
                'values': 'True or False'
            },
            'role_to_ping_on_thread_creation': {
                'description': 'The role or user mention used when a new support thread is created.',
                'values': 'You can set this to any role or user. You can also use everyone and here.'
            },
            'enabled': {
                'description': 'Whether the bot\'s support functionality is currently enabled.',
                'values': 'True or False'
            },
            'enable_block_appeals': {
                'description': 'Whether users can appeal blocks or restrictions.',
                'values': 'True or False'
            },
            'block_appeals_channel_id': {
                'description': 'The ID of the channel where users can submit appeals for blocks or restrictions.',
                'values': 'Channel id (integer)'
            },
            'staff_can_block': {
                'description': 'Whether staff members have the ability to block users from accessing support services.',
                'values': 'True or False'
            },
            'modmail_category_id': {
                'description': 'The ID of the category where the modmail (support) channels are organized.',
                'values': 'category id (integer)'
            },
            "select_department": {
                'description': 'Should the users be able to select the department they want to get support in?',
                'values': 'True or False'
            }
        }

        
        paginator = Paginator(pages=[
            discord.Embed(
                title=f"<:akai_modmail_config:1134741136196501535> Configuration: {config_name}",
                description='<:akai_modmail_rightarrow:1135132005777031299> ' + config_info[config_name]['description'],
                color=config.find_one({'name': 'main_color'})['value'],
            ).add_field(
                name="<:akai_modmail_utility:1134522398541094932> Values you can set:",
                value='<:akai_modmail_rightarrow:1135132005777031299> ' + config_info[config_name]['values'],
                inline=False
            ) for config_name in config_info
        ], timeout=60)

        await paginator.respond(ctx.interaction)
        
            
@configg.command()
async def edit(ctx: discord.ApplicationContext, configuration: discord.Option(str, choices=options_list), value: str):
    await ctx.defer()
    print(check_perms(ctx.author))
    if check_perms(ctx.author) not in ['ADMIN', 'OWNER']:
        await ctx.respond('<:akai_modmail_Wrong:1134522474344755240> You don\'t have permissions to use this command.')
    else:
        config_data_types_guide = {
            'main_color': int,
            'support_color': int,
            'staff_color': int,
            'error_color': int,
            'transcript_log': int,
            'activity': str,
            'token': str,
            'mongouri': str,
            'anon_author': str,
            'administrator_manage_modmail': bool,
            "select_department": bool,
            'modmail_automoderator_user': bool,
            'modmail_automoderator_staff': bool,
            'role_to_ping_on_thread_creation': str,
            'enabled': bool,
            'enable_block_appeals': bool,
            'block_appeals_channel_id': int,
            'staff_can_block': bool,
            'modmail_category_id': int
        }
        
        if configuration in ('transcript_log', 'block_appeals_channel_id', 'modmail_category_id'):
            print(configuration)
            if configuration == 'activity':
                pass
            else:
                try:
                    value = int(value)
                except:
                    await ctx.respond(embed=create_standart_embed('<:akai_modmail_Wrong:1134522474344755240> The value must be a number', 'Error'))
                    value = 'n'
                    
        elif configuration in ('main_color', 'support_color', 'staff_color', 'error_color'):
            if len(value) != 7:
                await ctx.respond(embed=create_standart_embed('<:akai_modmail_Wrong:1134522474344755240> The value must be a HEX (with the #)', 'Error'))
            else: 
                def hex_to_int(hex_color_code):
                    # Remove the '#' character if present in the color code
                    hex_color_code = hex_color_code.lstrip('#')
                    
                    # Convert the hexadecimal color code to an integer
                    int_color = int(hex_color_code, 16)
                    
                    return int_color
                
                value = hex_to_int(value)
            

        elif configuration in ('enable_block_appeals', 'enabled', 'modmail_automoderator_user', 'administrator_manage_modmail',"select_department"):
            try:
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                else:
                    raise ValueError
            except:
                await ctx.respond(embed=create_standart_embed('<:akai_modmail_Wrong:1134522474344755240> The value must be a boolean (True or False)', 'Error'))
                value = 'n'
        
        if value == 'n':
            pass
        else:
            e = config.find_one({'name': configuration})
            if configuration == 'activity':
                await bot.change_presence(activity=discord.Game(value))
            if e is None:
                config.insert_one({'name': configuration, 'value': value})
                await ctx.respond(embed=create_standart_embed(f'<:akai_modmail_Correct:1134522427792183410> The configuration ``{configuration}`` has been changed to {value}', 'Configuration Updated'))
            else:
                config.update_one(e, {'$set': {'value': value}})
                await ctx.respond(embed=create_standart_embed(f'<:akai_modmail_Correct:1134522427792183410> The configuration ``{configuration}`` has been changed to {value}', 'Configuration Updated'))

            
    

@configg.command()
async def get(ctx: discord.ApplicationContext):
    await ctx.defer()
    config_data_types_guide = {
        'main_color': str,
        'support_color': str,
        'staff_color': str,
        'error_color': str,
        'transcript_log': int,
        'activity': str,
        'token': str,
        'mongouri': str,
        'anon_author': str,
        'administrator_manage_modmail': bool,
        'modmail_automoderator_user': bool,
        'modmail_automoderator_staff': bool,
        'role_to_ping_on_thread_creation': str,
        'enabled': bool,
        'enable_block_appeals': bool,
        'block_appeals_channel_id': int,
        'staff_can_block': bool,
        'modmail_category_id': int
    }

    config_info = []
    for config_name, config_type in config_data_types_guide.items():
        config_entry = config.find_one({'name': config_name})
        if config_entry is not None:
            config_value = config_entry['value']
            if config_type == bool:
                config_value = "True" if config_value else "False"
            config_info.append(create_standart_embed(f"**Config Name:** ``{config_name}``\n**Config Value:** ``{config_value}``", 'Configuration'))

    if config_info:
        paginator = Paginator(pages=config_info)
        await paginator.respond(ctx.interaction)
    else:
        await ctx.respond(embed=create_standart_embed("No configurations found.", "Error"))
        
     
permsg = bot.create_group('permission')  

@permsg.command()
async def grant(ctx: discord.ApplicationContext, user: discord.User, level: discord.Option(str, choices=['ADMIN', 'MODERATOR', 'SUPPORT'])):
    if perms.find_one({'userid': user.id}) is not None:
        await ctx.respond(embed=create_standart_embed('That user already has permissions. delete the old permission to add a new one.', 'Error'))
    else:
        if check_perms(ctx.author) not in ('ADMIN', 'OWNER'):
            await ctx.respond(embed=create_standart_embed(embed=create_standart_embed('<:akai_modmail_Wrong:1134522474344755240> You don\'t have permissions you use this command.', 'Error')))
        else:
            await ctx.defer()
            u = perms.find_one({'userid': ctx.author.id})['value']
            if level == 'ADMIN' or level == 'OWNER':
                u2 = perms.find_one({'userid': user.id})
                if u2 is None:
                    perms.insert_one({'userid': user.id, 'value': level})
                else:
                    perms.find_one_and_update({'userid': user.id}, { '$set': {'level': level}})
                await ctx.respond(embed=create_standart_embed(f'The permission ``{level}`` has been updated successfully.', title='Success'))
            else: await ctx.respond(embed=create_standart_embed(f'The permission ``{level}`` couldn\'t be updated - You need the permission ADMIN to update this permission.', title='Success'))

@permsg.command()
async def revoke(ctx: discord.ApplicationContext, user: discord.User):
    await ctx.defer()
    if check_perms(ctx.author) not in ('ADMIN', 'OWNER'):
        await ctx.respond(embed=create_standart_embed('<:akai_modmail_Wrong:1134522474344755240> You don\'t have permissions you use this command.', 'Error'))
    else:
        u = perms.find_one({'id': ctx.author.id})
        if u is None:
            await ctx.respond(embed=create_standart_embed('That user don\'t have any actual permission.', 'Error'))
        else:
            perms.delete_one(u)
            await ctx.respond(embed=create_standart_embed(f'The user {user.name} got updated successfully', 'Success'))
    
@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.DMChannel):
        if message.author.bot is False:
            if config.find_one({'name': 'enabled'})['value'] == False:
                cembed = discord.Embed(
                    title='Couldn\'t deliver message',
                    description='The support system is disabled in this server. We ask for patience until we can get the support back. Cheers!',
                    color=config.find_one({'name': 'error_color'})['value']
                )
                await message.add_reaction('❌')
                await message.channel.send(embed=cembed)
            else:
                if automoderator.check(message.content) == False: content = message.content
                else:
                    content = automoderator.update(message.content)
                if blocksd.find_one({'userid': message.author.id}) is not None:
                    cembed2 = discord.Embed(
                        title='Couldn\'t deliver message',
                        description='You\'ve been blocked from using our modmail system.',
                        color=config.find_one({'name': 'error_color'})['value']
                    )
                    await message.add_reaction('❌')
                    if config.find_one({'name':"enable_block_appeals"})['value'] is False or config.find_one({'name':"enable_block_appeals"})['value'] is None:
                        await message.channel.send(embed=cembed2)
                    else:
                        if config.find_one({'name':"block_appeals_channel_id"})['value'] is None: pass
                        else: await message.channel.send(embed=cembed2, view=AppealBlockButton())
                            
                else:
                    open_ticket = modmails.find_one({'userid': message.author.id})
                    if open_ticket is None:
                        guild = bot.get_guild(int(os.environ['guild']))
                        embeo2 = discord.Embed(
                            title='Thread Open',
                            description='A thread has been created and the staff team has been notified, please remain patient till one of our staff comes online to assist you. In the mean time we request you to add to your query/concern in detail. Thank you for your patience!'  ,
                            color=config.find_one({'name': 'support_color'})['value']
                        ).set_footer(text=f'Automatic message | {guild.name}', icon_url=guild.icon.url)
                        result = config.find_one({'name': "select_department"})


                        if result is None:

                            a = await message.channel.send(embeds=[embeo2])
                        elif result == True:  # This line checks if result is truthy (equivalent to result == True)

                            opt = []
                            for dep in departments.find():
                                print(dep['name'])
                                opt.append(discord.SelectOption(label=dep['name'], description='Click this to select this department', emoji='<:akai_modmail_connect:1134556435720720555>'))

                            view = MyView()
                            a = await message.channel.send(embeds=[embeo2], view=view)

                        else:
                            a = await message.channel.send(embeds=[embeo2])
                            
                        embeo2.set_footer(text=guild.name, icon_url=guild.icon.url)
                        
                        
                        g = bot.get_guild(int(os.environ['staffguild']))
                        member = guild.get_member(message.author.id)
                        roles_as_text = ''
                        n = 1
                        for role in member.roles:
                            if n == 1:
                                n += 1
                            else:
                                roles_as_text += role.mention + ' ' + f'({role.name})' + ', '
                        mutuals = ''
                        for mutual in message.author.mutual_guilds:
                            mutuals += mutual.name + ',' + ' '
                            

                        def format_current_date(dt:datetime.datetime):
                            try:
                                dt = dt.astimezone(datetime.timezone.utc)  # Convert to an offset-aware datetime with UTC timezone
                                timestamp = int(dt.timestamp())
                                current_datetime = datetime.datetime.now(datetime.timezone.utc)  # Use UTC timezone for current time
                                time_difference = current_datetime - dt

                                if time_difference.days == 0:
                                    return f"<t:{timestamp}:R>"
                                elif time_difference.days == 1:
                                    return f"<t:{timestamp}:R> (Yesterday)"
                                elif time_difference.days > 1:
                                    return f"<t:{timestamp}:R> ({time_difference.days} days ago)"
                                else:
                                    return f"<t:{timestamp}:R> (In {-time_difference.days} days)"
                            except ValueError:
                                return "Invalid datetime format."

                        memb = guild.get_member(message.author.id)
                        if memb is None:
                            return
                        embedinfo = discord.Embed(
                            title=f'<:akai_modmail_activity:1134555294941319198> New thread by {message.author.name}',
                            description=f'<:akai_modmail_info:1134555578274951219> **{message.author.name}** | ``{message.author.id}``\n<:akai_modmail_rightarrow:1135132005777031299> created at {format_current_date(message.author.created_at)}.\n<:akai_modmail_rightarrow:1135132005777031299> joined {guild.name} {format_current_date(memb.joined_at)} ',
                            fields=[
                                discord.EmbedField(
                                    name='<:akai_modmail_Person:1134556367059951767> Roles',
                                    value=roles_as_text
                                ),
                                discord.EmbedField(
                                    name= '<:akai_modmail_connect:1134556435720720555> Mutual Servers',
                                    value= mutuals
                                )
                            ],
                            color=config.find_one({'name': 'support_color'})['value'],
                            timestamp=datetime.datetime.utcnow()
                        ).set_author(name='ModMail Thread', icon_url=guild.icon.url).set_footer(text='ModMail', icon_url=guild.icon.url).set_footer(text=f'Thread | Message ID: {a.id}')
                        
                        category = g.get_channel(config.find_one({'name': 'modmail_category_id'})['value'])
                        c = await category.create_text_channel(name=message.author.name)
                        await c.edit(sync_permissions=True)
                        if config.find_one({'name': 'role_to_ping_on_thread_creation'})['value'].lower().strip() != 'none':
                            await c.send(embed=discord.Embed(description='A new thread has been created.', title='Thread Notification', color=config.find_one({'name': 'support_color'})['value']).set_footer(text=guild.name, icon_url=guild.icon.url), content=config.find_one({'name': 'role_to_ping_on_thread_creation'})['value'])
                        await c.send(embed=embedinfo)
                        modmails.insert_one({'userid': message.author.id, 'channelid': c.id, 'sub_m': ''})
                        embed3 = discord.Embed(
                            description=content,
                            color=config.find_one({'name': 'support_color'})['value'],
                            timestamp=datetime.datetime.utcnow()
                        ).set_author(name=message.author.name, icon_url=message.author.avatar.url).set_footer(text='Response')
                        await c.send(embed=embed3)
                        for image in message.attachments:
                            await bot.get_channel(open_ticket['channelid']).send(embed = discord.Embed(url=image.url, title='Attachment', color=config.find_one({'name': 'support_color'})['value'], timestamp=datetime.datetime.utcnow()).set_author(name=message.author.name, icon_url=message.author.avatar.url).set_footer(text='Response').set_image(url=image.url))
                        await message.add_reaction('✅')
                        
                    else:
                        await message.add_reaction('✅')
                        embed = discord.Embed(
                            description=content,
                            color=config.find_one({'name': 'support_color'})['value'],
                            timestamp=datetime.datetime.utcnow()
                        ).set_author(name=message.author.name, icon_url=message.author.avatar.url).set_footer(text='Response')
                        await bot.get_channel(open_ticket['channelid']).send(embed=embed)
                        for image in message.attachments:
                            await bot.get_channel(open_ticket['channelid']).send(embed = discord.Embed(url=image.url, title='Attachment', color=config.find_one({'name': 'support_color'})['value'], timestamp=datetime.datetime.utcnow()).set_author(name=message.author.name, icon_url=message.author.avatar.url).set_footer(text='Response').set_image(url=image.url))

supportg = bot.create_group('support')
def top_role(userid: int):
    guild = bot.get_guild(int(os.environ['guild']))
    miembro = guild.get_member(userid)
    if miembro is None:
        raise ValueError(userid)
    roles = sorted(miembro.roles, reverse=True)
    for rol in roles:
        if rol.hoist:
            return rol
    else:
        return None
    
def find_dict(lst: list[dict], key: str, value) -> dict | None:
    for d in lst:
        if d.get(key) == value:
            return d
    return None

@supportg.command()
async def reply(ctx: discord.ApplicationContext, message: str, image: discord.Option(discord.Attachment, required=False)):
    await ctx.defer(ephemeral=True)
    if config.find_one({'name': 'modmail_automoderator_staff'})['value'] is None or config.find_one({'name': 'modmail_automoderator_staff'})['value'] == False: 
        if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
            await ctx.respond('You don\'t have permissions you use this command.')
        else:
            open_ticket = modmails.find_one({'channelid': ctx.channel.id})
            guild = bot.get_guild(int(os.environ['guild']))
            member = guild.get_member(open_ticket['userid'])
            
            embed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url).set_footer(text=f'Reply・{top_role(member.id)}')
            
            if image is not None:
                embed.set_image(url=image.url)
            m1 = await member.send(embed=embed)
            m2 = await ctx.channel.send(embed=embed)
            await ctx.respond(ephemeral=True, content='Message sent.')
            doc =   {
                    'dmmessageid': m1.id,
                    'messageid': m2.id,
                    'authorid': ctx.author.id
                }

            messagesdb.insert_one(doc)
    else:
        if automoderator.check(message) == False:
            if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
                await ctx.respond('You don\'t have permissions you use this command.')
            else:
                open_ticket = modmails.find_one({'channelid': ctx.channel.id})
                guild = bot.get_guild(int(os.environ['guild']))
                member = guild.get_member(open_ticket['userid'])
                
                embed = discord.Embed(
                    description=message,
                    color=config.find_one({'name': 'staff_color'})['value'],
                    timestamp=datetime.datetime.utcnow()
                ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url).set_footer(text=f'Reply・{top_role(member.id)}')
                
                if image is not None:
                    embed.set_image(url=image.url)
                m1 = await member.send(embed=embed)
                m2 = await ctx.channel.send(embed=embed)
                await ctx.respond(ephemeral=True, content='Message sent.')
                doc =   {
                        'dmmessageid': m1.id,
                        'messageid': m2.id,
                        'authorid': ctx.author.id
                    }

                messagesdb.insert_one(doc)
        else: await ctx.respond(embed=create_standart_embed('Don\'t be mean. i did not share this message with the user. Try to be nicer the next time.', 'Kind Warning'))
        



@supportg.command()
async def anonreply(ctx: discord.ApplicationContext, message: str, image: discord.Option(discord.Attachment, required=False)):
    await ctx.defer(ephemeral=True)
    if config.find_one({'name': 'modmail_automoderator_staff'})['value'] is None or config.find_one({'name': 'modmail_automoderator_staff'})['value'] == False: 
        if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
            await ctx.respond('You don\'t have permissions you use this command.')
            print(check_perms(ctx.author))
        else:
            open_ticket = modmails.find_one({'channelid': ctx.channel.id})
            guild = bot.get_guild(int(os.environ['guild']))
            sguild = bot.get_guild(int(os.environ['staffguild']))
            member = guild.get_member(open_ticket['userid'])
            anona = top_role(ctx.author.id).name
            if config.find_one({'name': 'anon_author'})['value'] != 'top':
                anona = config.find_one({'name': 'anon_author'})['value']
                
            embed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=anona, icon_url=sguild.icon.url).set_footer(text=f'Anonreply')
            
            sembed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url).set_footer(text=f'Anon Reply・{top_role(member.id)}')
                
            if image is not None:
                embed.set_image(url=image.url)
            m1 = await member.send(embed=embed)
            m2 = await ctx.channel.send(embed=sembed)
            await ctx.respond(ephemeral=True, content='Message sent.')
            doc =   {
                    'dmmessageid': m1.id,
                    'messageid': m2.id,
                    'authorid': ctx.author.id
                }

            messagesdb.insert_one(doc)
    else:
        if automoderator.check(message) == False:
            open_ticket = modmails.find_one({'channelid': ctx.channel.id})
            guild = bot.get_guild(int(os.environ['guild']))
            sguild = bot.get_guild(int(os.environ['staffguild']))
            member = guild.get_member(open_ticket['userid'])
            anona = top_role(ctx.author.id).name
            if config.find_one({'name': 'anon_author'})['value'] != 'top':
                anona = config.find_one({'name': 'anon_author'})['value']
                
            embed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=anona, icon_url=sguild.icon.url).set_footer(text=f'Anonreply')
            
            sembed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url).set_footer(text=f'Anon Reply・{top_role(member.id)}')
                
            if image is not None:
                embed.set_image(url=image.url)
            m1 = await member.send(embed=embed)
            m2 = await ctx.channel.send(embed=sembed)
            await ctx.respond(ephemeral=True, content='Message sent.')
            doc =   {
                    'dmmessageid': m1.id,
                    'messageid': m2.id,
                    'authorid': ctx.author.id
                }

            messagesdb.insert_one(doc)
        else: await ctx.respond(embed=create_standart_embed('Don\'t be mean. i did not share this message with the user. Try to be nicer the next time.', 'Kind Warning'))
@supportg.command()
async def delete(ctx: discord.ApplicationContext, message_id: str):
    if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
        await ctx.respond('You don\'t have permissions you use this command.')
    else:
        user = bot.get_user(modmails.find_one({'channelid': ctx.channel.id})['userid'])
        print(user)
        await ctx.defer()
        if user.dm_channel is None:
            await user.create_dm()
            await asyncio.sleep(1)
        dmchannel = user.dm_channel
        message_id = int(message_id)
        u = messagesdb.find_one({'messageid': message_id})
        if u is None:
            await ctx.respond(embed=create_standart_embed('Message not found', title='Error'))
            print("Message document not found.")
            return
        try:
            message2 = await dmchannel.fetch_message(u['dmmessageid'])
        except discord.NotFound:
            await ctx.respond(embed=create_standart_embed('Message in DM not found', title='Error'))
            print("DM message not found.")
            return
        try:
            message1 = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.respond(embed=create_standart_embed('Message in current channel not found', title='Error'))
            print("Current channel message not found.")
            return
        await message1.delete()
        await message2.delete()
        await ctx.respond(embed=create_standart_embed('Messages deleted successfully', title='Success'), ephemeral=True)
 
@supportg.command()
async def edit(ctx: discord.ApplicationContext, message_id: str, *, message: str):
    user = bot.get_user(modmails.find_one({'channelid': ctx.channel.id})['userid'])
    await ctx.defer(ephemeral=True)
    # Check if the user has an existing DM channel with the bot
    if user.dm_channel is None:
        await user.create_dm()
        # Wait a bit for the DM channel to be properly cached
        await asyncio.sleep(1)

    dmchannel = user.dm_channel
    message_id = int(message_id)
    u = messagesdb.find_one({'messageid': message_id})
    
    if u is None:
        await ctx.respond(embed=create_standart_embed('Message not found', title='Error'))
        return

    # Fetch the message from the DM channel
    try:
        dm_message = await dmchannel.fetch_message(u['dmmessageid'])
    except discord.NotFound:
        await ctx.respond(embed=create_standart_embed('Message in DM not found', title='Error'))
        return

    # Fetch the message from the current channel
    try:
        channel_message = await ctx.channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.respond(embed=create_standart_embed('Message in current channel not found', title='Error'))
        return

    # Modify the description of the embed in the DM
    if dm_message.embeds:
        embed = dm_message.embeds[0]
        embed.description = message
        await dm_message.edit(embed=embed)

    # Modify the description of the embed in the current channel
    if channel_message.embeds:
        embed = channel_message.embeds[0]
        embed.description = message
        await channel_message.edit(embed=embed)

    await ctx.respond(embed=create_standart_embed('Message edited successfully', title='Success'))

class snippetsmodal(discord.ui.Modal):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs, title='Snippet Creation Menu')
        
        self.name = name
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.paragraph, label='Content of the snippet'))
        
    async def callback(self, interaction) -> None:   
        guild = bot.get_guild(int(os.environ['guild']))
        snippetsdb.insert_one({'name': self.name, 'content': self.children[0].value})   
        embed = discord.Embed(
            color=config.find_one({'name': 'main_color'})['value'],
            fields=[
                discord.EmbedField(
                    name='<:akai_modmail_plus:1135131966438658140> Name',
                    value=self.name
                ),
                discord.EmbedField(
                    name='<:akai_modmail_rightarrow:1135132005777031299> Content',
                    value=self.children[0].value
                )
            ]
        ).set_author(name=guild.name, icon_url=guild.icon.url)
        await interaction.response.send_message(embed=embed)
        
class snippetsmodaledit(discord.ui.Modal):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs, title='Snippet Editting Menu')
        
        self.name = name
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.paragraph, label='Content of the snippet'))
        
    async def callback(self, interaction) -> None:  
        if snippetsdb.find_one({'name': self.name}) is None:
            await interaction.response.send_message(embed=create_standart_embed('That snippet does not exist', ' Error'))
        else:
            guild = bot.get_guild(int(os.environ['guild']))  
            embed = discord.Embed(
                color=config.find_one({'name': 'main_color'})['value'],
                fields=[
                    discord.EmbedField(
                        name='<:akai_modmail_plus:1135131966438658140> Name',
                        value=self.name
                    ),
                    discord.EmbedField(
                        name='<:akai_modmail_rightarrow:1135132005777031299> Content',
                        value=self.children[0].value
                    )
                ]
            ).set_author(name=guild.name, icon_url=guild.icon.url)
            snippetsdb.find_one_and_update({'name': self.name}, { "$set": {'content': self.children[0].value}}) 
            await interaction.response.send_message(embed=embed)

snippetg = bot.create_group('snippet')
@snippetg.command()
async def create(ctx: discord.ApplicationContext, name: str):
    await ctx.send_modal(snippetsmodal(name=name))
    

@snippetg.command()
async def anonsend(ctx: discord.ApplicationContext, name: str, ):
    await ctx.defer(ephemeral=True)
    if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
        await ctx.respond('You don\'t have permissions you use this command.')
    else:
        snippet = snippetsdb.find_one({'name': name})
        if snippet is None:
            await ctx.respond(embed=create_standart_embed('That snippet does not exist', 'Error'))
        else:
            message = snippet['content']
            open_ticket = modmails.find_one({'channelid': ctx.channel.id})
            guild = bot.get_guild(int(os.environ['guild']))
            sguild = bot.get_guild(int(os.environ['staffguild']))
            member = guild.get_member(open_ticket['userid'])
            anona = top_role(ctx.author.id).name
            if config.find_one({'name': 'anon_author'})['value'] != 'top':
                anona = config.find_one({'name': 'anon_author'})['value']
                
            embed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=anona, icon_url=sguild.icon.url).set_footer(text=f'Staff Response | Anonymous')
            
            sembed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url).set_footer(text=f'Staff Response | Anonymous Response')
                
            m1 = await member.send(embed=embed)
            m2 = await ctx.channel.send(embed=sembed)
            await ctx.respond(ephemeral=True, content='Message sent.')
            doc =   {
                    'dmmessageid': m1.id,
                    'messageid': m2.id,
                    'authorid': ctx.author.id
                }

            messagesdb.insert_one(doc)

@snippetg.command()
async def send(ctx: discord.ApplicationContext, name: str):
    await ctx.defer(ephemeral=True)
    if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
        await ctx.respond('You don\'t have permissions you use this command.')
    else:
        snippet = snippetsdb.find_one({'name': name})
        if snippet is None:
            await ctx.respond(embed=create_standart_embed('That snippet does not exist', 'Error'))
        else:
            message = snippet['content']
            open_ticket = modmails.find_one({'channelid': ctx.channel.id})
            guild = bot.get_guild(int(os.environ['guild']))
            member = guild.get_member(open_ticket['userid'])
            
            embed = discord.Embed(
                description=message,
                color=config.find_one({'name': 'staff_color'})['value'],
                timestamp=datetime.datetime.utcnow()
            ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url).set_footer(text=f'Staff Response | {top_role(member.id)}')
            
            m1 = await member.send(embed=embed)
            m2 = await ctx.channel.send(embed=embed)
            await ctx.respond(ephemeral=True, content='Message sent.')
            doc =   {
                    'dmmessageid': m1.id,
                    'messageid': m2.id,
                    'authorid': ctx.author.id
                }

            messagesdb.insert_one(doc)

@snippetg.command()
async def list(ctx: discord.ApplicationContext):
    await ctx.defer()
    all_snippets = snippetsdb.find()
    snippet_list_text = ''
    number = 1
    sguild = bot.get_guild(int(os.environ['staffguild']))
    guild = bot.get_guild(int(os.environ['guild']))
    for snippet in all_snippets:
        snippet_list_text += str(number) + '. ' + snippet['name'] + '\n'
        number += 1
    await ctx.respond(embed=create_standart_embed(snippet_list_text, timestamp=True).set_footer(text=f'Requested by {ctx.author.name} | {guild.name}' ).set_author(name='Snippet list', icon_url=guild.icon.url))

@snippetg.command()
async def edit(ctx: discord.ApplicationContext, name: str):
    await ctx.send_modal(snippetsmodaledit(name=name))

@snippetg.command()
async def view(ctx: discord.ApplicationContext):
    pages = [] 
    for doc in snippetsdb.find():
        embed = discord.Embed(
            title=f'<:akai_modmail_config:1134741136196501535> Snippet: {doc["name"]}',
            description='<:akai_modmail_rightarrow:1135132005777031299> ' + doc['content'],
            color=config.find_one({'name': 'main_color'})['value']
        )
        pages.append(Page(embeds=[embed]))
        
    paginator = Paginator(pages=pages)
    await paginator.respond(ctx.interaction)
    
blockg = bot.create_group('block')

@blockg.command()
async def add(ctx: discord.ApplicationContext, user: discord.Option(discord.User, required=False)):
    ticket = modmails.find_one({'channelid': ctx.channel.id})
    v = 'y'
    if ticket is None:
        if user is None:
            await ctx.respond(embed=create_standart_embed('You need to give a user if you\'re not in a thread channel.', 'Error', False))
            v = 'n'
        else:
            pass
            v = 'y'
    if v == 'y':
        if user is None:
            user = bot.get_user(ticket['userid'])
            v = 'y2'
            
    if v == 'y' or v == 'y2':
        if blocksd.find_one({'userid': user.id}) is None:
            blocksd.insert_one({'userid': user.id})
            await ctx.respond(embed=create_standart_embed(f'The user ``{user.name}`` has been blocked.', 'Success', False))
        else:
            await ctx.respond(embed=create_standart_embed('That user is already blocked.', 'Error', False))
            
@blockg.command()
async def remove(ctx: discord.ApplicationContext, user: discord.Option(discord.User, required=False)):
    ticket = modmails.find_one({'channelid': ctx.channel.id})
    v = 'y'
    if ticket is None:
        if user is None:
            await ctx.respond(embed=create_standart_embed('You need to give a user if you\'re not in a thread channel.', 'Error', False))
            v = 'n'
        else:
            pass
            v = 'y'
    if v == 'y':
        if user is None:
            user = bot.get_user(ticket['userid'])
            v = 'y2'
            
    if v == 'y' or v == 'y2':
        if blocksd.find_one({'userid': user.id}) is not None:
            blocksd.find_one_and_delete({'userid': user.id})
            await ctx.respond(embed=create_standart_embed(f'The user ``{user.name}`` has been unblocked.', 'Success', False))
        else:
            await ctx.respond(embed=create_standart_embed('That user is not blocked', 'Error', False))
        
@supportg.command()
async def close(ctx: discord.ApplicationContext):
    numb = random.randint(1, 90000)
    await ctx.defer(ephemeral=False)
    if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
        await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
    else:
        modmail = modmails.find_one({'channelid': ctx.channel.id})
        if modmail is None: 
            await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
        else:
            
            
            transcript = ""
            if isinstance(ctx.channel, discord.TextChannel):
                    transcript + '---------------- start -----------------'
                    async for message in ctx.channel.history(limit=None):
                        if message.embeds:
                            embed = message.embeds[0]
                            author_name = embed.author.name if embed.author else "Unknown"
                            description = embed.description if embed.description else "No description."
                            transcript += f"[{author_name}] | {description}\n"

            with open(f"transcripts/transcript-{ctx.channel_id}-{numb}.txt", "w", encoding="utf-8") as file:
                file.write(transcript)
            
            with open(f"transcripts/transcript-{ctx.channel_id}-{numb}.txt", "r", encoding="utf-8") as file:
                transscriptsdb.insert_one({'userid': modmail['userid'], 'transcript': transcript})
                transcriptchnnl = config.find_one({'name': "transcript_log"})['value']
                if transcriptchnnl is None: 
                    pass
                else:
                    await bot.get_channel(transcriptchnnl).send(file=discord.File(f"transcripts/transcript-{ctx.channel_id}-{numb}.txt"), embed=create_standart_embed('<:akai_modmail_dred:1135329080842145802> Transcript generated.', title='Logs').set_footer(text=f'Closed by {ctx.author}', icon_url=ctx.author.avatar.url))
                await ctx.respond(embed=create_standart_embed('<:akai_modmail_dred:1135329080842145802> Closing thread..', 'Closing'))
                guild = bot.get_guild(int(os.environ['guild']))
                embeo2 = discord.Embed(
                    title='Thread Closed',
                    description='The thread has been closed. If you have any further questions or need assistance, feel free to open a new thread. Thank you!',
                    color=config.find_one({'name': 'support_color'})['value']
                ).set_footer(text=f'Automatic message | {guild.name}', icon_url=guild.icon.url)
                try:
                    await bot.get_user(modmail['userid']).send(embed=embeo2)
                except:
                    await ctx.respond(embed=create_standart_embed('I couldn\'t dm the user.', 'Error'))
                await ctx.channel.delete()
                modmails.delete_one(modmail)
                
@bot.command()
async def load_module(ctx: discord.ApplicationContext, path: discord.Option(str, 'The module path. cog.name | Example: cog.welcome')):
    if check_perms(ctx.author) not in ('OWNER'):
        await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
    else:
        file = path
        try:
            bot.load_extension(path)
            extdb.insert_one({'n': path})
            await ctx.respond(embed=create_standart_embed('Module added', 'Success'))
        except Exception as e:
            await ctx.respond(embed=create_standart_embed('That module does not exist', 'Error'))
            print(e)
        
def d1dep(): 
    alld = departments.find()
    e = []
    for department in alld:
        e.append(department['name'])
    if len(e) == 0:
        return ("N/A")
    else:
        return(dep for dep in e) 
     
    
def getcat(category_id_to_find):
    for guild in bot.guilds:
        category = discord.utils.get(guild.categories, id=category_id_to_find)
        if category:
            return category
            break 

departmentg = bot.create_group('department')
@departmentg.command()
async def transfer(ctx: discord.ApplicationContext, department: str):
    await ctx.defer()
    idc = departments.find_one({'name': department.lower().strip()})
    if idc is None:
        await ctx.respond(embed=create_standart_embed('That department does not exist', 'Error'))
    else:
        if getcat(idc['value']) is None:
            await ctx.respond(embed=create_standart_embed('The category got deleted', 'Error'))
        else:
            if check_perms(ctx.author) not in ('ADMIN','OWNER','SUPPORT', 'MODERATOR'):
                await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
            else:
                modmail = modmails.find_one({'channelid': ctx.channel.id})
                if modmail is None:
                    await ctx.respond(embed=create_standart_embed('This is not a modmail thread', 'Error'))
                else:
                    await ctx.channel.edit(category=getcat(idc['value']), sync_permissions=True)
                    await ctx.respond(embed=create_standart_embed(f'Ticket transferred to the ``{department}`` department', 'Success'))

            
@departmentg.command()
async def add(ctx: discord.ApplicationContext, name: str, category: discord.CategoryChannel):
    if check_perms(ctx.author) not in ('ADMIN','OWNER'):
        await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
    else:
        departments.insert_one({'name': name.lower().strip(), 'value': category.id})
        await ctx.respond(embed=create_standart_embed('Department added.', 'Success'))
        
@departmentg.command()
async def remove(ctx: discord.ApplicationContext, name: str):
    if check_perms(ctx.author) not in ('ADMIN','OWNER'):
        idc = departments.find_one({'name': name.lower().strip()})
        if idc is None:
            await ctx.respond(embed=create_standart_embed('That department does not exist', 'Error'))
        else:
            await ctx.respond(embed=create_standart_embed('Department removed.', 'Success'))
            departments.delete_one(idc)
    else:
        await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
        
@departmentg.command()
async def list(ctx: discord.ApplicationContext):
    if check_perms(ctx.author) not in ('ADMIN','OWNER', 'MODERATOR', 'SUPPORT'): await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
    else:
        await ctx.defer()
        all_snippets = departments.find()
        snippet_list_text = ''
        number = 1
        sguild = bot.get_guild(int(os.environ['staffguild']))
        guild = bot.get_guild(int(os.environ['guild']))
        for snippet in all_snippets:
            snippet_list_text += str(number) + '. ' + snippet['name'] + '\n'
            number += 1
        await ctx.respond(embed=create_standart_embed(snippet_list_text, timestamp=True).set_footer(text=f'Requested by {ctx.author.name} | {guild.name}' ).set_author(name='Department list', icon_url=guild.icon.url))

@supportg.command()
async def contact(ctx: discord.ApplicationContext, user: discord.User):
                if check_perms(ctx.author) not in ('ADMIN','OWNER', 'MODERATOR'): await ctx.respond(embed = create_standart_embed('You don\'t have permissions you use this command.', 'Error'))
                else:
                    open_ticket = modmails.find_one({'userid': user.id})
                    if open_ticket is None:
                        guild = bot.get_guild(int(os.environ['guild']))
                        embeo2 = discord.Embed(
                            title='Thread Open',
                            description='A thread has been created and the staff team has been notified, please remain patient till one of our staff comes online to assist you. In the mean time we request you to add to your query/concern in detail. Thank you for your patience!'  ,
                            color=config.find_one({'name': 'support_color'})['value']
                        ).set_footer(text=f'Automatic message | {guild.name}', icon_url=guild.icon.url)
                        
                        embeo2.set_footer(text=guild.name, icon_url=guild.icon.url)
                        a = await user.send(embeds=[embeo2])
                        
                        g = guild
                        member = g.get_member(user.id)
                        roles_as_text = ''
                        n = 1
                        for role in member.roles:
                            if n == 1:
                                n += 1
                            else:
                                roles_as_text += role.mention + ' ' + f'({role.name})' + ', '
                        mutuals = ''
                        for mutual in ctx.author.mutual_guilds:
                            mutuals += mutual.name + ',' + ' '
                            

                        def format_current_date(dt:datetime.datetime):
                            try:
                                dt = dt.astimezone(datetime.timezone.utc)  # Convert to an offset-aware datetime with UTC timezone
                                timestamp = int(dt.timestamp())
                                current_datetime = datetime.datetime.now(datetime.timezone.utc)  # Use UTC timezone for current time
                                time_difference = current_datetime - dt

                                if time_difference.days == 0:
                                    return f"<t:{timestamp}:R>"
                                elif time_difference.days == 1:
                                    return f"<t:{timestamp}:R> (Yesterday)"
                                elif time_difference.days > 1:
                                    return f"<t:{timestamp}:R> ({time_difference.days} days ago)"
                                else:
                                    return f"<t:{timestamp}:R> (In {-time_difference.days} days)"
                            except ValueError:
                                return "Invalid datetime format."

                        memb = guild.get_member(user.id)
                        if memb is None:
                            return
                        embedinfo = discord.Embed(
                            title=f'<:akai_modmail_activity:1134555294941319198> New thread by {user.name} | contacted by {ctx.author.name}',
                            description=f'<:akai_modmail_info:1134555578274951219> **{user.name}** | ``{user.id}``\n<:akai_modmail_rightarrow:1135132005777031299> created at {format_current_date(user.created_at)}.\n<:akai_modmail_rightarrow:1135132005777031299> joined {guild.name} {format_current_date(memb.joined_at)} ',
                            fields=[
                                discord.EmbedField(
                                    name='<:akai_modmail_Person:1134556367059951767> Roles',
                                    value=roles_as_text
                                ),
                                discord.EmbedField(
                                    name= '<:akai_modmail_connect:1134556435720720555> Mutual Servers',
                                    value= mutuals
                                )
                            ],
                            color=config.find_one({'name': 'support_color'})['value'],
                            timestamp=datetime.datetime.utcnow()
                        ).set_author(name='ModMail Thread', icon_url=guild.icon.url).set_footer(text='ModMail', icon_url=guild.icon.url).set_footer(text=f'Thread | Message ID: {a.id}')
                        
                        category = g.get_channel(config.find_one({'name': 'modmail_category_id'})['value'])
                        c = await category.create_text_channel(name=user.name)
                        await c.edit(sync_permissions=True)
                        if config.find_one({'name': 'role_to_ping_on_thread_creation'})['value'].lower().strip() != 'none':
                            await c.send(embed=discord.Embed(description='A new thread has been created.', title='Thread Notification', color=config.find_one({'name': 'support_color'})['value']).set_footer(text=guild.name, icon_url=guild.icon.url), content=config.find_one({'name': 'role_to_ping_on_thread_creation'})['value'])
                        await c.send(embed=embedinfo)
                        modmails.insert_one({'userid': user.id, 'channelid': c.id, 'sub_m': ''})
                        embed3 = discord.Embed(
                            description='This is a contact thread',
                            color=config.find_one({'name': 'support_color'})['value'],
                            timestamp=datetime.datetime.utcnow()
                        ).set_author(name=bot.user.name, icon_url=bot.user.avatar.url).set_footer(text='This message was NOT delivered')
                        await c.send(embed=embed3)
                        await ctx.respond(embed=create_standart_embed('User contacted successfully.', 'Success'))
                        
        
@bot.command()
async def credits(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        description='<@994688795532337253> | Developer\n\n<@1081766354278940732> | Administrator - Graphics\n<@713735322399277087> | Administrator - Services',
        color=discord.Colour.blurple()
    ).set_image(url='https://media.discordapp.net/attachments/1136688584460599517/1136688829303115786/1.png').add_field(name='Icons Server', value='discord.gg/icons-859387663093727263').add_field(name='Support Server', value='https://discord.gg/hGDk7hM5UR').set_author(icon_url='https://media.discordapp.net/attachments/1136688584460599517/1136688948689772554/Untitled_design-7.png?width=676&height=676', name='A-Modmail Team & Credits')

    await ctx.respond(embed=embed)
    
@bot.command()
async def help(ctx: discord.ApplicationContext):
    t  = '<:akai_modmail_dot:1138588400027451482> /block add\n<:akai_modmail_dash:1138588463759892490> block a member from contacting the bot\n\n<:akai_modmail_dot:1138588400027451482> /block remove\n<:akai_modmail_dash:1138588463759892490> remove the block from a member contacting the bot\n\n<:akai_modmail_dot:1138588400027451482> /config view \n<:akai_modmail_dash:1138588463759892490> view the bot configuration settings\n\n<:akai_modmail_dot:1138588400027451482> /config edit\n<:akai_modmail_dash:1138588463759892490> edit the bot configuration settings\n\n<:akai_modmail_dot:1138588400027451482> /config get\n<:akai_modmail_dash:1138588463759892490> information on the confuguration of your bot\n\n<:akai_modmail_dot:1138588400027451482> credits\n<:akai_modmail_dash:1138588463759892490> see the wonderful staff that contributed to the bot\n\n<:akai_modmail_dot:1138588400027451482> /department transfer\n<:akai_modmail_dash:1138588463759892490> transfer the thread to a different department\n\n<:akai_modmail_dot:1138588400027451482> /department add\n<:akai_modmail_dash:1138588463759892490> add a new department \n\n<:akai_modmail_dot:1138588400027451482> /department remove\n<:akai_modmail_dash:1138588463759892490> remove a department\n\n<:akai_modmail_dot:1138588400027451482> /department list\n<:akai_modmail_dash:1138588463759892490> view the departments you have added\n\n<:akai_modmail_dot:1138588400027451482> /load module\n<:akai_modmail_dash:1138588463759892490> self-coded modules users can add to the bot\n\n<:akai_modmail_dot:1138588400027451482> /permission grant\n<:akai_modmail_dash:1138588463759892490> grant a member permissions\n\n<:akai_modmail_dot:1138588400027451482> /permission revoke\n<:akai_modmail_dash:1138588463759892490> revoke a members permissions\n\n<:akai_modmail_dot:1138588400027451482> /setup \n<:akai_modmail_dash:1138588463759892490> setup your bot\n\n<:akai_modmail_dot:1138588400027451482> /snippet create\n<:akai_modmail_dash:1138588463759892490> create a pre-made response the bot will send\n\n<:akai_modmail_dot:1138588400027451482> /snippet anonsend\n<:akai_modmail_dash:1138588463759892490> send your snippet annonymously\n\n<:akai_modmail_dot:1138588400027451482> /snippet send\n<:akai_modmail_dash:1138588463759892490> send your snippet \n\n<:akai_modmail_dot:1138588400027451482> /snippet list\n<:akai_modmail_dash:1138588463759892490> view your snippets\n\n<:akai_modmail_dot:1138588400027451482> /snippet edit\n<:akai_modmail_dash:1138588463759892490> edit your snippet\n\n<:akai_modmail_dot:1138588400027451482> /snippet view\n<:akai_modmail_dash:1138588463759892490> view your list of snippets\n\n<:akai_modmail_dot:1138588400027451482> /support reply \n<:akai_modmail_dash:1138588463759892490> reply to the member \n\n<:akai_modmail_dot:1138588400027451482> /support anonreply\n<:akai_modmail_dash:1138588463759892490> reply to the member annonymously\n\n<:akai_modmail_dot:1138588400027451482> /support delete\n<:akai_modmail_dash:1138588463759892490> delete a message sent in the thread\n\n<:akai_modmail_dot:1138588400027451482> /support edit\n<:akai_modmail_dash:1138588463759892490> edit a message sent in the thread \n\n<:akai_modmail_dot:1138588400027451482> /support close\n<:akai_modmail_dash:1138588463759892490> close the thread\n\n<:akai_modmail_dot:1138588400027451482> /support contact\n<:akai_modmail_dash:1138588463759892490> contact a specific member through the bot'  
    await ctx.respond(embed=create_standart_embed(t, 'Help Command').set_author(icon_url='https://media.discordapp.net/attachments/1136688584460599517/1136688948689772554/Untitled_design-7.png?width=676&height=676', name='Amodmail Help Command'))
     
@bot.event
async def on_slash_command_error(ctx: discord.ApplicationContext, error):
    await ctx.respond(embed=create_standart_embed(str(error) + ' Ask in the support server.', 'Unknown Error'))
bot.run(os.environ['token'])
