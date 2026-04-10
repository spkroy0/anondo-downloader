import os
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    # একটি সিম্পল HTML পেজ রিটার্ন করবে
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Anondo Downloader</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: sans-serif; text-align: center; padding: 20px; background: #f0f2f5; }
            .container { background: white; padding: 20px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            input, select { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
            button { background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
            #status { margin-top: 20px; color: #555; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🚀 Social Downloader</h2>
            <p>Design by Anondo</p>
            <form action="/download" method="POST">
                <input type="text" name="url" placeholder="Paste Link Here..." required>
                <select name="format">
                    <option value="mp4">MP4 Video (720p)</option>
                    <option value="mp3">MP3 Audio (256kbps)</option>
                </select>
                <button type="submit">Download Now</button>
            </form>
            <div id="status">Render-এ ফাইল বড় হলে প্রসেস হতে একটু সময় নিতে পারে।</div>
        </div>
    </body>
    </html>
    """

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    file_format = request.form.get('format')
    
    # সার্ভারের টেম্পোরারি ফোল্ডার ব্যবহার করা
    tmpdir = tempfile.gettempdir()
    
    ydl_opts = {
        'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'referer': 'https://www.google.com/',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    if file_format == 'mp4':
        ydl_opts['format'] = 'best[ext=mp4]/best'
    else:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            if file_format == 'mp3':
                file_path = file_path.rsplit('.', 1)[0] + '.mp3'

        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
