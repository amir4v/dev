import os
import urllib.parse

from pytube import YouTube
from telegram.ext import *

TOKEN = "TOKEN" # YOUR_TELEGRAM_BOT_TOKEN
HOST_PATH = "IP-OR-DOMAIN" # in /var/www/HOST_PATH/ needed for NginX
#
HOST = f"http://{HOST_PATH}:8000" # for making a download link URL
VIDEOS_PATH = f'/var/www/{HOST_PATH}/' # where we want to save videos


def download_audio(url):
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


def download_video(url, res='720p'):
    mp4s = YouTube(url).streams
    video = mp4s.filter(res=res).filter(mime_type="video/mp4")[0]
    file_path = video.download(VIDEOS_PATH)
    filename = file_path.lstrip(VIDEOS_PATH)
    file = open(file_path, 'rb')
    return file, filename


def route(update, cntx):
    try:
        text = update.message.text.strip(' ')
        # Video
        if text.startswith('v'): # v URL 720 (Means: Video URL Resolution)
                                 # v URL
                                 # vURL 
            parts = text.split(' ')
            if len(parts) == 3:
                v, url, res = parts
            elif len(parts) == 2:
                v, url = parts
                res = '720'
            else:
                url = parts[0].lstrip('v')
                res = '720'
            res += 'p'
            
            file, filename = download_video(url, res)
            url_encoded_filename = urllib.parse.quote(filename)
            update.message.reply_text(filename + ':')
            update.message.reply_text(f"{HOST}/{url_encoded_filename}")
        else: # Audio
            file, filename = download_audio(text)
        update.message.reply_document(
            document=file,
            filename=filename,
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

"""
nohup python3 bot.py &

systemctl reload nginx.service
systemctl restart nginx.service

# NginX
server {
	listen 8000;
	listen [::]:8000;

	server_name HOST;

	root /var/www/HOST; # This directory must not have any index(.html) files.
	# index index.html;

	location / {
		autoindex on;
		# try_files $uri $uri/ =404;
	}
}
