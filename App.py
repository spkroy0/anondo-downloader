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
    choice = request.form.get('format_type')
    
    if not url:
        return "Link kothay? Age link din dost!"

    api_url = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # অডিও কোয়ালিটি চেক করা হচ্ছে (যদি অপশনে 'k' থাকে)
    is_audio = True if 'k' in choice else False
    bitrate = choice.replace('k', '') if is_audio else "128"
    
    payload = {
        "url": url,
        "vQuality": choice if not is_audio else "720",
        "isAudioOnly": is_audio,
        "aFormat": "mp3",
        "aBitrate": bitrate, # অডিও বিটরেট সেট করা হলো
        "filenamePattern": "pretty"
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()

        if result.get("status") in ["stream", "redirect"]:
            return redirect(result["url"])
        elif result.get("status") == "picker":
            return redirect(result["picker"][0]["url"])
        else:
            return f"Error: {result.get('text', 'Kisu ekta vul hoyeche, abar try koro.')}"

    except Exception as e:
        return f"Server Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
