import os
from osonbot import Bot
import requests
from environs import Env

env = Env()
env.read_env()

API_TOKEN = env.str("API_TOKEN")
BOT_TOKEN = env.str("BOT_TOKEN")

bot = Bot(BOT_TOKEN, admin_id=7077167971)

api_url = "https://full-media-downloader-pro-zfkrvjl323.vercel.app/"

def InstagramDownloader(url: str):
    return requests.get(api_url + "instagramdownloader", params={"url": url, "token": API_TOKEN}).json()

def YouTubeDownloader(url: str):
    response = requests.get(api_url + "youtubedownloader", params={'url': url, "token": API_TOKEN}).json()
    return {"title": response['title'], "thumbnail": response['thumbnail'], "url": response['video'][0]['url']}

def FacebookDownloader(url: str):
    return requests.get(api_url + "facebookdownloader", params={'url': url, 'token': API_TOKEN}).json()

def PinterestDownloader(url: str):
    return requests.get(api_url + "pinterestdownloader", params={'url': url, 'token': API_TOKEN}).json()

def TikTokDownloader(url: str):
    return requests.get(api_url + "tiktokdownloader", params={"url": url, "token": API_TOKEN}).json()['data']

def SnapchatDownloader(url: str):
    return requests.get(api_url + "snapchatdownloader", params={"url": url, "token": API_TOKEN}).json()

def videosaver(url: str):
    with requests.post(url, stream=True) as res:
        res.raise_for_status()
        with open("video.mp4", "wb") as file:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

def imagesaver(url: str):
    with requests.post(url, stream=True) as res:
        res.raise_for_status()
        with open("image.jpg", "wb") as f:
            for chunk in res.iter_content(8192):
                if chunk:
                    f.write(chunk)

def main(msg):
    text = msg['text']
    downloader = None
    if "https://" in text or "http://" in text:
        bot.send_message(msg['chat']['id'], "Yuklanmoqda...")
        if "www.instagram.com" in text:
            downloader = InstagramDownloader(text)
            if downloader['type'] == "video":
                videosaver(downloader['urls'][0])
                bot.send_video(msg['chat']['id'], "video.mp4", caption=downloader['title'])
                os.remove("video.mp4")
            elif downloader['type'] == "image":
                imagesaver(downloader['urls'][0])
                bot.send_photo(msg['chat']['id'], "image.jpg", caption=downloader['title'])
                os.remove("image.jpg")
        elif "youtube.com" in text or "youtu.be" in text:
            downloader = YouTubeDownloader(text)
            bot.send_video(msg['chat']['id'], downloader['url'], caption=downloader['title'])
        elif "facebook.com" in text or "fb.watch" in text:
            downloader = FacebookDownloader(text)
            if downloader['hd_url']:
                bot.send_video(msg['chat']['id'], str(downloader['hd_url']), caption=downloader['title'])
            elif downloader['sd_url']:
                bot.send_video(msg['chat']['id'], str(downloader['sd_url']), caption=downloader['title'])
            else:
                bot.send_photo(msg['chat']['id'], str(downloader['thumbnail']), caption=downloader['title'])
        elif "pinterest.com" in text or "pin.it" in text:
            downloader = PinterestDownloader(text)
            try:
                bot.send_photo(msg['chat']['id'], downloader['images'], caption=downloader['title'])
            except:
                bot.send_video(msg['chat']['id'], downloader['urls'], caption=downloader['title'])
        elif "tiktok" in text:
            downloader = TikTokDownloader(text)
            bot.send_video(msg['chat']['id'], downloader['play'], caption=downloader['title'])
        elif "snapchat.com" in text:
            downloader = SnapchatDownloader(text)
            print(downloader)
            bot.send_video(msg['chat']['id'], downloader['url'], caption=downloader['title'])
        

bot.when("/start", "Salom {first_name}")
bot.when("*", main)

bot.run()
