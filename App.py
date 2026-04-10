import os
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('format_type')

    if not url:
        return "URL কই ভাই? আগে লিঙ্ক দিন!"

    # Publer বা এই জাতীয় সাইটগুলো যে ধরণের API এন্ডপয়েন্ট ব্যবহার করে (Updated Cobalt)
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # অডিও নাকি ভিডিও চেক
    is_audio = "k" in quality
    
    payload = {
        "url": url,
        "videoQuality": quality.replace('k', '') if not is_audio else "720",
        "downloadMode": "audio" if is_audio else "video",
        "audioFormat": "mp3",
        "filenameStyle": "pretty",
        "youtubeVideoCodec": "h264" # এটি ভিডিও কোয়ালিটি স্টেবল রাখতে সাহায্য করে
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        # যদি এই API সার্ভারটি ব্যস্ত থাকে, তবে আমরা একটি প্রো-ব্যাকআপ মেথড ব্যবহার করব
        if response.status_code != 200:
            fallback_url = f"https://downloader.nocopyright.workers.dev/?url={url}"
            return redirect(fallback_url)
            
        result = response.json()

        if "url" in result:
            return redirect(result["url"])
        else:
            # ব্যাকআপ লিঙ্ক
            return redirect(f"https://downloader.nocopyright.workers.dev/?url={url}")

    except Exception as e:
        # সব ফেল করলে এই ইউনিভার্সাল গেটওয়ে কাজ করবেই
        return redirect(f"https://downloader.nocopyright.workers.dev/?url={url}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
