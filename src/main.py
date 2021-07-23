from googletrans import Translator
import discord
import os
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
    lang = db.get_language(message.guild.id, conn)[0]
    sentence = ' '.join(comm[2:])
    await message.channel.send(translator.translate("Translating to " + languages[comm[1]].capitalize() + ".", dest=lang).text)
    translated = translator.translate(sentence, dest=comm[1]).text
    await message.channel.send(translated)
    url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=' + comm[1] + '-TR&client=tw-ob&q=' + '+'.join(translated.split(' '))
    r = requests.get(url, allow_redirects=True)
    filename = translator.translate("Pronunciation", dest=db.get_language(message.guild.id, conn)[0]).text + '.mp3'
    f = open(filename, 'wb').write(r.content)
    await message.channel.send(translator.translate("Pronunciation: ", dest=db.get_language(message.guild.id, conn)[0]).text, file=discord.File(filename))
    os.remove(filename)

async def display_help(message):
    language = db.get_language(message.guild.id, conn)[0]
    if language == 'en':
        await message.channel.send("Here is a list of commands:\n"
                                   "**!translateHelp**: displays help\n"
                                   "**!ping**: pings bot\n"
                                   "**!translate LANGUAGE_PREFIX MESSAGE**: translates message into chosen language\n"
                                   "**!getTranslation**: translates most recent message which wasn't in the server's default language\n"
                                   "**!update LANGUAGE_PREFIX**: changes server's preferred language"
                                   "For a list of language prefixes go to: https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages")
    else:
        f = open('help.txt', 'r')
        text = f.readlines()
        await message.channel.send(translator.translate(text[0], dest=language).text + "."
            + "\n**!translateHelp**: " + translator.translate(text[1], dest=language).text + "."
            + "\n**!ping**: " + translator.translate(text[2], dest=language).text + "."
            + "\n**!translate LANGUAGE_PREFIX MESSAGE**: " + translator.translate(text[3], dest=language).text + "."
            + "\n**!getTranslation**: " + translator.translate(text[4], dest=language).text + "."
            + "\n**!update LANGUAGE_PREFIX**: " + translator.translate(text[5], dest=language).text
            + "\n**!getLanguage**: " + translator.translate(text[6], dest=language).text + ".\n"
            + translator.translate(text[7], dest=language).text + " https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    db.check_table(message.guild.id, conn)
    lang = db.get_language(message.guild.id, conn)[0]
    if message.author == client.user:
        return
    if message.author.bot:
        return
    if message.content.startswith("!ping"):
        await message.channel.send("pong!")
        print("pinged")
    elif message.content.startswith("!getTranslation"):
        if len(messageStack) != 0:
            translation = translator.translate(messageStack.pop(), dest=lang)
            await message.channel.send(translator.translate("Original message: ", dest=lang).text + " " + translation.origin)
            await message.channel.send(translator.translate("Translating from " + languages[translator.detect(translation.origin).lang].capitalize(), dest=lang).text + ".")
            await message.channel.send(translator.translate("Translated message: ", dest=lang).text + " " + translation.text)

        else:
            await message.channel.send(translator.translate("Nothing to translate.", lang).text)
            await message.channel.send(translator.translate("The server's language has been updated.", dest=lang).text)

    elif message.content.startswith("!translateHelp"):
        await display_help(message)
    elif message.content.startswith("!translate"):
        await translate(message)
    elif message.content.startswith("!update"):
        arguments = message.content.split(' ')
        db.update_language(message.guild.id, arguments[1], conn)
        await message.channel.send(translator.translate("The server's language has been updated.", dest=db.get_language(message.guild.id, conn)[0]).text)
    else:
        language = translator.detect(message.content)
        default_language = db.get_language(message.guild.id, conn)[0]
        if language.lang != default_language and language.confidence > 0.6:
            old_str = translator.translate("The previous message was not in " + languages[default_language].capitalize() + " (added to the stack). Type $$ to translate.", dest=lang).text + "\n" + translator.translate("Confidence:", dest=lang).text + " " + str((language.confidence * 100).__round__(2)) + "%."
            new_str = old_str.replace("$$", "**!getTranslation**")
            await message.channel.send(new_str)
            # await message.channel.send("The previous message was not in " + languages[default_language].capitalize() + " (added to the stack). Type **!getTranslation** to translate.\n"
            #                             "Confidence: " + str((language.confidence * 100).__round__(2)) + "%.")

            messageStack.append(message.content)


client.run('ODY3NTYxMDE0NTA0OTgwNTIx.YPi5KA.V6sdM_eEQHUP8Niqcwy4qvMsDR0')
