from googletrans import Translator
import discord

translator = Translator()
client = discord.Client()
messageStack = []

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

async def translate(message):
    comm = message.content.split(" ")
    sentence = ' '.join(comm[2:])
    await message.channel.send("Translating from " + LANGUAGES[translator.detect(sentence).lang] + ".")
    await message.channel.send(translator.translate(sentence, dest=comm[1]).text)

async def display_help(message):
    await message.channel.send("Here is a list of commands:\n"
                               "**!translateHelp**: displays help\n"
                               "**!ping**: pings bot\n"
                               "**!translate LANGUAGE_PREFIX MESSAGE**: translates message into chosen language\n"
                               "**!getTranslation**: translates most recent message which wasn't in english\n"
                               "For a list of language prefixes go to: https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!ping"):
        await message.channel.send("pong!")
    elif message.content.startswith("!getTranslation"):
        if len(messageStack) != 0:
            translation = translator.translate(messageStack.pop(), dest='en')
            await message.channel.send("Original message: " + translation.origin)
            await message.channel.send("Translating from " + LANGUAGES[translator.detect(translation.origin).lang] + ".")
            await message.channel.send("Translated message: " + translation.text)
        else:
            await message.channel.send("Nothing to translate")
    elif message.content.startswith("!translateHelp"):
        await display_help(message)
    elif message.content.startswith("!translate"):
        await translate(message)
    else:
        lang = translator.detect(message.content)
        if lang.lang != 'en':
            await message.channel.send("The previous message is not in English (added to the stack). Type **!getTranslation** to translate")
            messageStack.append(message.content)


client.run('ODY1MDg5MTQ5MDk0ODU0Njc3.YO-7DQ.o2kjnhNb6644IWsPEpioY8bxf2o')
