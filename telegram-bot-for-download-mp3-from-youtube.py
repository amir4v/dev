import os

from pytube import YouTube
from telegram.ext import *

TOKEN = "TOKEN" # YOUR_TOKEN


def download(url):
    audio = YouTube(url)     
    # extracting and downloading the audio file 
    output = audio.streams.get_audio_only().download()
    # this splits the audio file, the base and the extension
    base, ext = os.path.splitext(output)
    # this converts the audio file to mp3 file
    new_file = base + '.mp3'
    # this renames the mp3 file
    os.rename(output, new_file)

    file = open(new_file, 'rb')

    try:
        os.remove(new_file)
    except:
        pass
    try:
        os.remove(output)
    except:
        pass

    return file, new_file


def route(update, cntx):
    try:
        text = update.message.text
        file, new_file = download(text)
        update.message.reply_document(
            document=file,
            filename=new_file,
            caption=""
        )
    except Exception as e:
        try:
            update.message.reply_text(str(e))
        except Exception as e:
            print(e)


updater = Updater(TOKEN)
updater.dispatcher.add_handler(RegexHandler(r'^.+$', route))
updater.start_polling()
print()
print("Your telegram bot is running!")
print()
updater.idle()

# nohup python3 bot.py &
