import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

FB_PAGE_ID = "1352257637972181"
# Aapka wahi token jo abhi active hai
FB_USER_TOKEN = "EAAO2wTXY7FUBS2AjgGGgK0HpiWkAC2Iv9NCTDZBW2B4LSw2sLPNntd8ws0em4l0Jb37eTF3X05eLNsU01ZBTlUeD3yw2MTuClN9yV9Bs697x1X2Ig7t3atXdmniYOcBg8ZCUMrcnCSyk4dRe6hky8k1K6GfaXToKVs897EpUmT3VZCtJwZCvKwBBxLJXdZCm4BrEmdHZCrxGcADGvDmuOliKh1wWd0g5HJvKb0zqX3ZBMsiN9aHGRZAOydsZCFQ6WSQGlyAUjT3ZCCqBMMDejhvv8Kl"

CAMPAIGN_HISTORY = [
    {"id": 1, "title": "DR. A.P.J. ABDUL KALAM TRIBUTE", "platform": "Facebook Page", "status": "Published", "date": "2026-10-18 20:50"},
]

UNIFIED_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dizlyzen AI Manager - Photo Post Edition</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .main-wrapper { display: flex; gap: 30px; max-width: 1200px; margin: 0 auto; flex-wrap: wrap; }
        .form-container { flex: 2; min-width: 320px; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h1 { text-align: center; color: #38bdf8; margin-bottom: 25px; font-size: 24px; }
        .section-box { background: #334155; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #475569; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #cbd5e1; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; margin-bottom: 15px; background: #0f172a; border: 1px solid #64748b; color: #fff; border-radius: 6px; box-sizing: border-box; }
        .security-bar { background: #064e3b; border: 1px solid #059669; color: #a7f3d0; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #475569; }
        th { color: #38bdf8; }
        .badge-published { background: #065f46; color: #a7f3d0; padding: 4px 8px; border-radius: 4px; font-size: 11px; }
        button.submit-btn { background: #0284c7; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; }
        button.submit-btn:hover { background: #0369a1; }
        .message { background: #065f46; color: #a7f3d0; padding: 12px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <div class="form-container">
            <h1>🚀 Dizlyzen AI Photo Manager</h1>
            
            <div class="security-bar">
                <span>🛡️ Direct Photo & Text Graph API Active</span>
                <span style="background: #0284c7; padding: 2px 6px; border-radius: 4px; font-size: 11px;">v7.2 Live</span>
            </div>

            {% if message %}
                <div class="message">{{ message }}</div>
            {% endif %}

            <form action="/generate" method="POST">
                
                <div class="section-box">
                    <label for="social_account">Select Connected Social Account:</label>
                    <select name="social_account" id="social_account">
                        <option value="Samantasamiti">📌 Samantasamiti (Page ID: 1352257637972181)</option>
                    </select>
                </div>

                <div class="section-box">
                    <label for="title">Campaign Title:</label>
                    <input type="text" name="title" id="title" value="जातिवाद का अंत और महापुरुषों के विचार" required>

                    <label for="quote">Campaign Caption / Description:</label>
                    <textarea name="quote" id="quote" rows="3">मानवता और कड़े कानून: जातिवाद के खात्मा की ओर कदम 🚀</textarea>

                    <label for="image_url">Image URL (Direct Public Image Link):</label>
                    <input type="text" name="image_url" id="image_url" value="https://picsum.photos/800/600" placeholder="Paste direct image link here">

                    <label for="hashtags">Automatic Hashtags:</label>
                    <input type="text" name="hashtags" id="hashtags" value="#Samantasamiti #DizlyzenAI">
                </div>

                <button type="submit" class="submit-btn">✨ Send Photo Dispatch to Facebook</button>
            </form>

            <div class="section-box" style="margin-top: 30px;">
                <h3 style="color: #38bdf8; margin-top: 0;">📊 Dispatch Log</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Campaign Title</th>
                            <th>Platform</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in history %}
                        <tr>
                            <td>{{ item.title }}</td>
                            <td>{{ item.platform }}</td>
                            <td><span class="badge-published">Published</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, history=CAMPAIGN_HISTORY)

@app.route("/generate", methods=["POST"])
def generate_and_publish():
    try:
        title = request.form.get("title")
        quote = request.form.get("quote")
        image_url = request.form.get("image_url")
        hashtags = request.form.get("hashtags")
        
        full_message = f"{title}\n\n{quote}\n\n{hashtags}"
        api_logs = []

        # Step 1: Fetch Page Access Token dynamically
        accounts_url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={FB_USER_TOKEN}"
        acc_res = requests.get(accounts_url).json()
        
        page_access_token = None
        if "data" in acc_res:
            for page in acc_res["data"]:
                if page.get("id") == FB_PAGE_ID:
                    page_access_token = page.get("access_token")
                    break

        if not page_access_token:
            return render_template_string(
                UNIFIED_DASHBOARD_TEMPLATE, 
                history=CAMPAIGN_HISTORY, 
                message="❌ Error: Page Access Token could not be fetched."
            )

        # Step 2: Post Photo + Caption directly to Facebook Page
        fb_url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/photos"
        payload = {
            "url": image_url,
            "message": full_message,
            "access_token": page_access_token
        }
        res = requests.post(fb_url, data=payload)
        res_json = res.json()
        
        if "id" in res_json or "post_id" in res_json:
            post_id = res_json.get("id") or res_json.get("post_id")
            api_logs.append(f"Facebook Photo Post Success! ID: {post_id}")
        else:
            error_msg = res_json.get("error", {}).get("message", "Unknown Error")
            api_logs.append(f"Facebook Photo Failed: {error_msg}")

        new_entry = {"id": len(CAMPAIGN_HISTORY)+1, "title": title, "platform": "Facebook Page (Photo)", "status": "Published", "date": "Just Now"}
        CAMPAIGN_HISTORY.insert(0, new_entry)

        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, history=CAMPAIGN_HISTORY, message=f"API Response Log -> {', '.join(api_logs)}")

    except Exception as e:
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, history=CAMPAIGN_HISTORY, message=f"❌ Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)