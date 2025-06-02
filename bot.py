import os
import re
import instaloader
import subprocess
import telebot
from pytube import YouTube
from yt_dlp import YoutubeDL

# Bot Token
BOT_TOKEN = '7804973923:AAF7czyqJyFKNzhsrsmFVGdo6wOE00FuQZ0'
bot = telebot.TeleBot(BOT_TOKEN)

# Stylish Font (simple demo)
def style_text(text):
    return ''.join([chr(ord(c) + 0x1D5A0 - ord('A')) if 'A' <= c <= 'Z' else 
                    chr(ord(c) + 0x1D5BA - ord('a')) if 'a' <= c <= 'z' else c for c in text])

# Start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, style_text("Welcome to the Ultimate Downloader Bot!"))

# YouTube Video Download
@bot.message_handler(commands=['ytvideo'])
def yt_video(message):
    try:
        url = message.text.split()[1]
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download()
        with open(filename, 'rb') as f:
            bot.send_video(message.chat.id, f, caption=yt.title)
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# YouTube Audio Download
@bot.message_handler(commands=['ytaudio'])
def yt_audio(message):
    try:
        url = message.text.split()[1]
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        filename = audio.download(filename_prefix='audio_') + '.mp3'
        os.rename(audio.default_filename, filename)
        with open(filename, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=yt.title)
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# Instagram Reel + Caption
@bot.message_handler(commands=['insta'])
def insta_reel(message):
    try:
        url = message.text.split()[1]
        shortcode = re.findall(r'/p/([a-zA-Z0-9_-]+)|/reel/([a-zA-Z0-9_-]+)', url)
        shortcode = next(filter(None, shortcode[0]))
        loader = instaloader.Instaloader(save_metadata=False, download_video_thumbnails=False)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        caption = post.caption or "No caption"
        loader.download_post(post, target='insta_download')
        for file in os.listdir('insta_download'):
            if file.endswith('.mp4'):
                with open(f"insta_download/{file}", 'rb') as f:
                    bot.send_video(message.chat.id, f, caption=caption[:1024])
        for file in os.listdir('insta_download'):
            os.remove(f"insta_download/{file}")
        os.rmdir('insta_download')
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# Snapchat Download (Placeholder)
@bot.message_handler(commands=['snap'])
def snap_download(message):
    bot.send_message(message.chat.id, "🚧 Snapchat reel download coming soon...")

# Help command
@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = """
🎵 /ytaudio <link> – Download YouTube audio  
📹 /ytvideo <link> – Download YouTube video  
📸 /insta <link> – Download Instagram Reel with caption  
👻 /snap <link> – Snapchat download (soon)  
🆘 /help – Show this help
    """
    bot.send_message(message.chat.id, help_text)

# Polling
bot.infinity_polling()