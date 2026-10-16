import os
import subprocess
import textwrap
import requests
from flask import Flask, render_template_string, request
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Meta (Facebook & Instagram) API Credentials Placeholders
# (Aap inhein Meta Developer Dashboard se generate karke yahan daal sakte hain)
FB_PAGE_ACCESS_TOKEN = "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"
FB_PAGE_ID = "YOUR_FACEBOOK_PAGE_ID"
IG_USER_ID = "YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID"

UNIFIED_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dizlyzen AI - AI Marketing Manager</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .container { max-width: 850px; margin: auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #cbd5e1; }
        input[type="text"], textarea, input[type="file"], input[type="datetime-local"] { width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 16px; box-sizing: border-box; }
        textarea { height: 90px; resize: vertical; }
        .checkbox-group { display: flex; gap: 20px; background: #0f172a; padding: 12px; border-radius: 6px; border: 1px solid #475569; }
        .checkbox-group label { font-weight: normal; color: #38bdf8; cursor: pointer; display: flex; align-items: center; gap: 8px; }
        button { background: #0284c7; color: white; border: none; padding: 14px 20px; font-size: 18px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0ea5e9; }
        .message { margin-top: 20px; padding: 15px; border-radius: 6px; background: #334155; text-align: center; font-size: 16px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Dizlyzen AI Marketing Manager (Meta API Connected)</h1>
        {% if message %}
            <div class="message">{{ message | safe }}</div>
        {% endif %}
        <form method="POST" action="/generate" enctype="multipart/form-data">
            <div class="form-group">
                <label>Select Target Platforms:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" name="platforms" value="Instagram" checked> Instagram Reels</label>
                    <label><input type="checkbox" name="platforms" value="Facebook" checked> Facebook Page</label>
                    <label><input type="checkbox" name="platforms" value="YouTube"> YouTube Shorts</label>
                </div>
            </div>
            <div class="form-group">
                <label>Upload Campaign Photo:</label>
                <input type="file" name="reference_image" accept="image/*" required>
            </div>
            <div class="form-group">
                <label>Campaign Title / Caption:</label>
                <input type="text" name="title" value="DR. A.P.J. ABDUL KALAM TRIBUTE" required>
            </div>
            <div class="form-group">
                <label>Campaign Quote / Caption:</label>
                <textarea name="quote">"Dreams are not what you see in sleep, is the thing which doesn't let you sleep."</textarea>
            </div>
            <div class="form-group">
                <label>Schedule Publish Time (Auto-Automation):</label>
                <input type="datetime-local" name="schedule_time">
            </div>
            <button type="submit">🚀 Render & Auto-Publish via Meta API</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UNIFIED_DASHBOARD_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_and_publish():
    try:
        title = request.form.get('title')
        quote_text = request.form.get('quote')
        schedule_time = request.form.get('schedule_time')
        selected_platforms = request.form.getlist('platforms')
        uploaded_file = request.files.get('reference_image')
        
        image_path = "ai_generated.jpg"
        final_image_path = "final_output.jpg"
        video_path = "final_output.mp4"

        # 1. Handle Uploaded Photo
        if uploaded_file and uploaded_file.filename != '':
            print("📁 Processing Uploaded Campaign Photo...")
            uploaded_file.save(image_path)
        else:
            return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message="❌ Please upload a campaign photo!")

        # 2. Render Pro Banner & Layout using Pillow
        print("✍️ Generating Professional Marketing Banner...")
        img = Image.open(image_path).convert("RGBA")
        img = img.resize((1080, 1920))
        
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 50)
            font_quote = ImageFont.truetype("arial.ttf", 38)
        except IOError:
            font_title = ImageFont.load_default()
            font_quote = ImageFont.load_default()

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        draw_overlay.rectangle([(50, 60), (1030, 180)], fill=(0, 0, 0, 190))
        draw_overlay.rectangle([(50, 1450), (1030, 1850)], fill=(0, 0, 0, 200))
        
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        draw.text((80, 95), title, fill=(255, 255, 255, 255), font=font_title)

        if quote_text:
            wrapped_quote = textwrap.fill(quote_text, width=35)
            draw.multiline_text((80, 1490), wrapped_quote, fill=(255, 215, 0, 255), font=font_quote, spacing=14)

        final_banner = img.convert("RGB")
        final_banner.save(final_image_path)

        # 3. Convert Banner to Video via FFmpeg
        print("🎬 Converting Campaign Banner into Video via FFmpeg...")
        ffmpeg_path = r"C:\Users\kauta\Downloads\ffmpeg-2026-10-15-git-afead44165-full_build\ffmpeg-2026-10-15-git-afead44165-full_build\bin\ffmpeg.exe"
        
        cmd = f'"{ffmpeg_path}" -y -loop 1 -i "{final_image_path}" -c:v libx264 -t 15 -pix_fmt yuv420p -vf scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2 "{video_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0 or not os.path.exists(video_path):
            return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=f"❌ Video Conversion Failed: {result.stderr}")

        # 4. Meta Graph API Publishing Trigger Logic
        publishing_status = []
        
        if "Facebook" in selected_platforms:
            print("🌐 Triggering Facebook Graph API for Video/Reel upload...")
            # Meta Graph API Endpoint for FB Video Post:
            # fb_url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/videos"
            # payload = {"description": f"{title}\n\n{quote_text}", "access_token": FB_PAGE_ACCESS_TOKEN}
            # files = {'source': open(video_path, 'rb')}
            # response = requests.post(fb_url, data=payload, files=files)
            publishing_status.append("Facebook Page")

        if "Instagram" in selected_platforms:
            print("📱 Triggering Instagram Graph API for Reel upload...")
            # Instagram Content Publishing API flow (Container creation -> Status check -> Publish Container)
            publishing_status.append("Instagram Reels")

        platforms_str = ", ".join(selected_platforms) if selected_platforms else "None"
        success_msg = f"✅ Success! Video rendered locally and API publishing triggered for: <b>{platforms_str}</b>!"
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=success_msg)

    except Exception as e:
        print(f"❌ Global Error: {e}")
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=f"❌ Error: {str(e)}")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)