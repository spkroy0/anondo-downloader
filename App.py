import os
from flask import Flask, render_template

app = Flask(__name__)

# গ্যালারিতে ছবি এবং প্রম্পট ডেটা (পরবর্তীতে আপনি এটি ডাটাবেস থেকে আনতে পারেন)
gallery_images = [
    {
        "id": "p1",
        "title": "Cinematic Cyberpunk Portrait",
        "prompt": "Hyper-realistic portrait of a cyberpunk hacker, neon city reflection in sunglasses, cinematic lighting, 8k, Unreal Engine 5 render.",
        "image_file": "cyberpunk_hacker.jpg" # static/images ಫೋಲ್ಡರ್ ಎ ತಾಕಬೆ
    },
    {
        "id": "p2",
        "title": "Fantasy Landscape at Sunset",
        "prompt": "Epic fantasy landscape with floating islands and waterfall at sunset, golden hour lighting, photorealistic, matte painting style.",
        "image_file": "fantasy_landscape.jpg"
    },
    # নতুন ছবি যোগ করতে এখানে একটি নতুন ডিকশনারি কপি করে বসিয়ে দিন
]

@app.route('/')
def index():
    # gallery.html পেজে ডেটা পাঠানো হচ্ছে
    return render_template('index.html', images=gallery_images)

if __name__ == "__main__":
    # Render বা Local এ রান করার জন্য
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
