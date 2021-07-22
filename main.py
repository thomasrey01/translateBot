from googletrans import Translator
import discord
import psycopg2
import db
import ast
import requests

translator = Translator()
client = discord.Client()
messageStack = []
conn = db.initialise()
# conn.cursor().execute('''DELETE * FROM languages''')
file = open("languages.txt", "r")
languages = ast.literal_eval(file.read())

async def translate(message):
    comm = message.content.split(" ")
    sentence = ' '.join(comm[2:])
    await message.channel.send("Translating to " + languages[comm[1]].capitalize() + ".")
    translated = translator.translate(sentence, dest=comm[1]).text
    await message.channel.send(translated)
    url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=' + comm[1] + '-TR&client=tw-ob&q=' + '+'.join(translated.split(' '))
    r = requests.get(url, allow_redirects=True)
    f = open('pronunciation.mp3', 'wb').write(r.content)
    await message.channel.send("Pronunciation: ", file=discord.File(r'pronunciation.mp3'))

async def display_help(message):
    await message.channel.send("Here is a list of commands:\n"
                               "**!translateHelp**: displays help\n"
                               "**!ping**: pings bot\n"
                               "**!translate LANGUAGE_PREFIX MESSAGE**: translates message into chosen language\n"
                               "**!getTranslation**: translates most recent message which wasn't in the server's default language\n"
                               "**!update LANGUAGE_PREFIX**: changes server's prefered language"
                               "For a list of language prefixes go to: https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    db.check_table(message.guild.id, conn)
    if message.author == client.user:
        return
    if message.author.bot:
        return
    if message.content.startswith("!ping"):
        await message.channel.send("pong!")
        print("pinged")
    elif message.content.startswith("!getTranslation"):
        if len(messageStack) != 0:
            translation = translator.translate(messageStack.pop(), dest='en')
            await message.channel.send("Original message: " + translation.origin)
            await message.channel.send("Translating from " + languages[translator.detect(translation.origin).lang].capitalize() + ".")
            await message.channel.send("Translated message: " + translation.text)
        else:
            await message.channel.send("Nothing to translate")
    elif message.content.startswith("!translateHelp"):
        await display_help(message)
    elif message.content.startswith("!translate"):
        await translate(message)
    elif message.content.startswith("!update"):
        arguments = message.content.split(' ')
        db.update_language(message.guild.id, arguments[1], conn)
    else:
        lang = translator.detect(message.content)
        default_language = db.get_language(message.guild.id, conn)
        if lang.lang != default_language and lang.confidence > 0.6:
            await message.channel.send("The previous message was not in " + languages[default_language[0]].capitalize() + " added to the stack). Type **!getTranslation** to translate.\n"
                                        "Confidence: " + str((lang.confidence * 100).__round__(2)) + "%.")
            messageStack.append(message.content)


client.run('BOT_TOKEN')
