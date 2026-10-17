import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

UNIFIED_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dizlyzen AI Marketing Manager - Pro Phase 1</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .main-wrapper { display: flex; gap: 30px; max-width: 1200px; margin: 0 auto; }
        .form-container { flex: 2; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .preview-container { flex: 1; background: #1e293b; padding: 20px; border-radius: 12px; height: fit-content; position: sticky; top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #475569; }
        h1 { text-align: center; color: #38bdf8; margin-bottom: 25px; font-size: 24px; }
        .section-box { background: #334155; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #475569; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #cbd5e1; }
        input[type="text"], textarea, select, input[type="date"], input[type="time"] { width: 100%; padding: 10px; margin-bottom: 15px; background: #0f172a; border: 1px solid #64748b; color: #fff; border-radius: 6px; box-sizing: border-box; }
        input[type="file"] { width: 100%; padding: 8px; margin-bottom: 15px; background: #0f172a; border: 1px solid #64748b; color: #fff; border-radius: 6px; box-sizing: border-box; }
        .checkbox-group { display: flex; gap: 20px; margin-bottom: 15px; flex-wrap: wrap; }
        .checkbox-group label { font-weight: normal; color: #e2e8f0; cursor: pointer; }
        .counter { font-size: 12px; color: #94a3b8; text-align: right; margin-top: -10px; margin-bottom: 15px; display: block; }
        .tabs { display: flex; gap: 10px; margin-bottom: 15px; }
        .tab-btn { background: #475569; border: none; padding: 8px 12px; color: white; border-radius: 4px; cursor: pointer; font-size: 14px; }
        .tab-btn.active { background: #0284c7; font-weight: bold; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        /* Mobile Mockup Preview */
        .mobile-mockup { background: #000; border: 4px solid #475569; border-radius: 24px; padding: 15px; width: 260px; margin: 0 auto; color: #fff; font-family: sans-serif; }
        .mockup-screen { background: #111; border-radius: 12px; padding: 10px; min-height: 380px; font-size: 13px; }
        .mockup-header { font-weight: bold; color: #38bdf8; margin-bottom: 8px; border-bottom: 1px solid #333; padding-bottom: 5px; }
        .mockup-img { width: 100%; height: 160px; background: #333; border-radius: 6px; object-fit: cover; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; color: #777; font-size: 11px; }
        .mockup-caption { word-break: break-all; color: #e2e8f0; font-size: 12px; margin-bottom: 8px; }
        
        button.submit-btn { background: #0284c7; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; }
        button.submit-btn:hover { background: #0369a1; }
        .message { background: #065f46; color: #a7f3d0; padding: 12px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
    <script>
        function switchTab(evt, tabName) {
            let tabs = document.getElementsByClassName("tab-content");
            for (let t of tabs) { t.classList.remove("active"); }
            let btns = document.getElementsByClassName("tab-btn");
            for (let b of btns) { b.classList.remove("active"); }
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
        function updatePreview() {
            let title = document.getElementById("title").value;
            let quote = document.getElementById("quote").value;
            let hashtags = document.getElementById("hashtags").value;
            
            document.getElementById("prev-title").innerText = title;
            document.getElementById("prev-text").innerText = quote + " " + hashtags;
            
            let charCount = quote.length;
            document.getElementById("char-count").innerText = charCount + " / 2200 characters";
        }
    </script>
</head>
<body>
    <div class="main-wrapper">
        <div class="form-container">
            <h1>🚀 Dizlyzen AI Marketing Manager (Pro Phase 1)</h1>
            
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

                <!-- Platform Specific Tabs -->
                <div class="section-box">
                    <label>Platform-Specific Optimization Tabs:</label>
                    <div class="tabs">
                        <button type="button" class="tab-btn active" onclick="switchTab(event, 'insta-tab')">Instagram</button>
                        <button type="button" class="tab-btn" onclick="switchTab(event, 'fb-tab')">Facebook</button>
                        <button type="button" class="tab-btn" onclick="switchTab(event, 'yt-tab')">YouTube</button>
                    </div>

                    <div id="insta-tab" class="tab-content active">
                        <label><input type="checkbox" name="insta_reel" checked> Share as Reel (Auto-audio)</label>
                    </div>
                    <div id="fb-tab" class="tab-content">
                        <label><input type="checkbox" name="fb_story"> Also post to Facebook Story</label>
                    </div>
                    <div id="yt-tab" class="tab-content">
                        <label for="yt_tags">YouTube Specific Tags (comma separated):</label>
                        <input type="text" name="yt_tags" placeholder="shorts, trending, educational">
                    </div>
                </div>

                <!-- Media Upload -->
                <div class="section-box">
                    <label for="post_format">Post Format:</label>
                    <select name="post_format" id="post_format">
                        <option value="Reel">Reel / Video</option>
                        <option value="Single Image">Single Image Post</option>
                    </select>

                    <label for="campaign_file">Upload Media (Photo/Video):</label>
                    <input type="file" name="campaign_file" id="campaign_file">
                </div>

                <!-- Caption, Hashtags & Character Counter -->
                <div class="section-box">
                    <label for="title">Campaign Title:</label>
                    <input type="text" name="title" id="title" value="DR. A.P.J. ABDUL KALAM TRIBUTE" oninput="updatePreview()" required>

                    <label for="quote">Campaign Caption / Description:</label>
                    <textarea name="quote" id="quote" rows="3" oninput="updatePreview()">"Dreams are not what you see in sleep, is the thing which doesn't let you sleep."</textarea>
                    <span id="char-count" class="counter">78 / 2200 characters</span>

                    <label for="hashtags">Automatic Hashtags:</label>
                    <input type="text" name="hashtags" id="hashtags" value="#InstaReel #Marketing #DizlyzenAI" oninput="updatePreview()">

                    <label for="first_comment">First Comment Automation (Optional - e.g. Link/Hashtags):</label>
                    <input type="text" name="first_comment" placeholder="Drop extra hashtags or link in first comment...">
                </div>

                <!-- CTA & Link -->
                <div class="section-box">
                    <label for="cta">Call to Action (CTA):</label>
                    <select name="cta" id="cta">
                        <option value="Shop Now">Shop Now</option>
                        <option value="Learn More">Learn More</option>
                        <option value="Sign Up">Sign Up</option>
                        <option value="Message Us">Message Us</option>
                    </select>

                    <label for="destination_link">Destination Link (URL):</label>
                    <input type="text" name="destination_link" placeholder="https://yourwebsite.com">
                </div>

                <!-- Scheduling -->
                <div class="section-box">
                    <label>Schedule Publish Time (24-Hour Format):</label>
                    <input type="date" name="schedule_date">
                    <input type="time" name="schedule_time" value="09:00">
                </div>

                <button type="submit" class="submit-btn">✨ Generate & Publish Campaign</button>
            </form>
        </div>

        <!-- Live Preview Sidebar -->
        <div class="preview-container">
            <h3 style="text-align: center; color: #38bdf8; margin-top: 0;">📱 Live Preview</h3>
            <div class="mobile-mockup">
                <div class="mockup-screen">
                    <div class="mockup-header" id="prev-title">DR. A.P.J. ABDUL KALAM TRIBUTE</div>
                    <div class="mockup-img">Media Preview</div>
                    <div class="mockup-caption" id="prev-text">"Dreams are not what you see in sleep, is the thing which doesn't let you sleep." #InstaReel #Marketing #DizlyzenAI</div>
                </div>
            </div>
            <p style="font-size: 11px; text-align: center; color: #94a3b8; margin-top: 10px;">Yeh live preview dikhata hai ki post social media par kaisi lagegi.</p>
        </div>
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
        title = request.form.get("title")
        platforms = request.form.getlist("platforms")
        file = request.files.get("campaign_file")
        
        if not file or file.filename == "":
            return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message="⚠️ Kripya ek media file select karein!")

        success_msg = f"✅ Campaign '{title}' successfully processed with Phase 1 Pro features for {', '.join(platforms)}!"
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=success_msg)

    except Exception as e:
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, message=f"❌ Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)