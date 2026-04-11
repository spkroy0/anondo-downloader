import os
from flask import Flask, render_template

app = Flask(__name__)

# র‍্যান্ডম এআই ছবি এবং সেগুলোর প্রম্পট ডেটা
gallery_images = [
    {
        "id": "p1",
        "title": "Neon Samurai Knight",
        "prompt": "Hyper-realistic samurai in neon armor, futuristic Tokyo background, cinematic lighting, 8k, Unreal Engine 5 render, sharp details.",
        "image_url": "https://images.unsplash.com/photo-1614728263952-84ea206f9c45?q=80&w=1000&auto=format&fit=crop" 
    },
    {
        "id": "p2",
        "title": "Mystical Forest Spirit",
        "prompt": "Glowing ethereal spirit in a deep dark forest, magical fireflies, soft volumetric lighting, fantasy art style, photorealistic, 8k.",
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"
    },
    {
        "id": "p3",
        "title": "Cyberpunk Street Girl",
        "prompt": "Cinematic portrait of a girl in cyberpunk techwear, rainy night, neon signs reflection, bokeh background, DSLR quality, highly detailed.",
        "image_url": "https://images.unsplash.com/photo-1635322966219-b75ed372eb3c?q=80&w=1000&auto=format&fit=crop"
    }
]

@app.route('/')
def index():
    return render_template('index.html', images=gallery_images)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
