import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Updated Unified Dashboard Template with New Professional Marketing Features
UNIFIED_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dizlyzen AI Marketing Manager - Pro</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h1 { text-align: center; color: #38bdf8; margin-bottom: 25px; }
        .section-box { background: #334155; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #475569; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #cbd5e1; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; margin-bottom: 15px; background: #0f172a; border: 1px solid #64748b; color: #fff; border-radius: 6px; box-sizing: border-box; }
        input[type="file"], input[type="datetime-local"] { width: 100%; padding: 8px; margin-bottom: 15px; background: #0f172a; border: 1px solid #64748b; color: #fff; border-radius: 6px; box-sizing: border-box; }
        .checkbox-group { display: flex; gap: 20px; margin-bottom: 15px; }
        .checkbox-group label { font-weight: normal; color: #e2e8f0; cursor: pointer; }
        button { background: #0284c7; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0369a1; }
        .message { background: #065f46; color: #a7f3d0; padding: 12px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Dizlyzen AI Marketing Manager (Pro)</h1>
        
        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}

        <form action="/generate" method="POST" enctype="multipart/form-data">
            
            <!-- Target Platforms -->
            <div class="section-box">
                <label>Select Target Platforms:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" name="platforms" value="Instagram" checked> Instagram Reels</label>
                    <label><input type="checkbox" name="platforms" value="Facebook" checked> Facebook Page</label>
                    <label><input type="checkbox" name="platforms" value="YouTube" checked> YouTube Shorts</label>
                </div>
            </div>

            <!-- Post Type & Format -->
            <div class="section-box">
                <label for="post_format">Post Format / Type:</label>
                <select name="post_format" id="post_format">
                    <option value="Reel">Reel / Video</option>
                    <option value="Single Image">Single Image Post</option>
                    <option value="Carousel">Carousel (Multiple Images)</option>
                </select>

                <label for="campaign_file">Upload Campaign Media (Photo/Video):</label>
                <input type="file" name="campaign_file" id="campaign_file">
            </div>

            <!-- AI Caption & Hashtag Generator -->
            <div class="section-box">
                <label for="ai_prompt">AI Caption Quick Prompt (e.g., Summer Sale, Tech Startup):</label>
                <input type="text" name="ai_prompt" id="ai_prompt" placeholder="Enter topic for auto-generation...">
                
                <label for="title">Campaign Title / Caption:</label>
                <input type="text" name="title" id="title" value="DR. A.P.J. ABDUL KALAM TRIBUTE" required>

                <label for="quote">Campaign Quote / Description:</label>
                <textarea name="quote" id="quote" rows="3">"Dreams are not what you see in sleep, is the thing which doesn't let you sleep."</textarea>

                <label for="hashtags">Automatic Hashtags:</label>
                <input type="text" name="hashtags" id="hashtags" value="#InstaReel #Marketing #DizlyzenAI #Trending">
            </div>

            <!-- CTA and Destination Link -->
            <div class="section-box">
                <label for="cta">Call to Action (CTA):</label>
                <select name="cta" id="cta">
                    <option value="Shop Now">Shop Now</option>
                    <option value="Learn More">Learn More</option>
                    <option value="Sign Up">Sign Up</option>
                    <option value="Message Us">Message Us</option>
                </select>

                <label for="destination_link">Destination Link (URL):</label>
                <input type="text" name="destination_link" id="destination_link" placeholder="https://yourwebsite.com or WhatsApp link">
            </div>

            <!-- Advanced Scheduling -->
            <div class="section-box">
                <label for="schedule_time">Schedule Publish Time (Auto-Automation):</label>
                <input type="datetime-local" name="schedule_time" id="schedule_time">

                <label for="approval_status">Workflow Status:</label>
                <select name="approval_status" id="approval_status">
                    <option value="Publish Now">Publish Instantly</option>
                    <option value="Save Draft">Save as Draft / Send for Approval</option>
                </select>
            </div>

            <button type="submit">✨ Generate & Publish Campaign</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(UNIFIED_DASHBOARD_TEMPLATE)

@app.route("/generate", methods=["POST"])
def generate_and_publish():
    try:
        platforms = request.form.getlist("platforms")
        post_format = request.form.get("post_format")
        title = request.form.get("title")
        quote = request.form.get("quote")
        hashtags = request.form.get("hashtags")
        cta = request.form.get("cta")
        link = request.form.get("destination_link")
        schedule_time = request.form.get("schedule_time")
        status = request.form.get("approval_status")
        
        file = request.files.get("campaign_file")
        
        if not file or file.filename == "":
            return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message="⚠️ Kripya ek campaign media file select karein!")

        # Success message with pro options
        success_msg = f"✅ Campaign '{title}' ({post_format}) successfully processed for {', '.join(platforms)}! Status: {status}."
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=success_msg)

    except Exception as e:
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=f"❌ Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)