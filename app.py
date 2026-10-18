import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

FB_PAGE_ID = "1352257637972181"
IG_USER_ID = "17841425343804485"
# Fresh Live Page Access Token embedded
FB_ACCESS_TOKEN = "EAAO2wTXY7FUBS3PqAn8aTAljlN9FwCXPZCNEnc9CoSBMcaumLrbKF7eZBwCIkkTeiddPfO2TtY4ZCKiTc4O4CPg3ziUh1azpZAp5u3IZB0Fy6HGpbIMVxfHmg6R7b1ri0z2YnwYLXeIbZC00ZBXiRJV7IcnddYrbwKCZCeIfkKlFHFiuLIhy5ynIX4eUTe7iZAOztCx4Qy6duarAwJ7htFjm7YZCR7dBsVn0RmGs0XKCavtMZBa2cYDwOSUunH1W0LdjYwQuPq97Yn2qZBnThP3NnRZBI"

CAMPAIGN_HISTORY = [
    {"id": 1, "title": "DR. A.P.J. ABDUL KALAM TRIBUTE", "platform": "Instagram, Facebook, YouTube", "status": "Published", "date": "2026-10-18 19:25"},
]

UNIFIED_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dizlyzen AI Manager - Live Production</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .main-wrapper { display: flex; gap: 30px; max-width: 1200px; margin: 0 auto; flex-wrap: wrap; }
        .form-container { flex: 2; min-width: 320px; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .preview-container { flex: 1; min-width: 280px; background: #1e293b; padding: 20px; border-radius: 12px; height: fit-content; position: sticky; top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #475569; }
        h1 { text-align: center; color: #38bdf8; margin-bottom: 25px; font-size: 24px; }
        .section-box { background: #334155; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #475569; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #cbd5e1; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; margin-bottom: 15px; background: #0f172a; border: 1px solid #64748b; color: #fff; border-radius: 6px; box-sizing: border-box; }
        .checkbox-group { display: flex; gap: 20px; margin-bottom: 15px; flex-wrap: wrap; }
        .checkbox-group label { font-weight: normal; color: #e2e8f0; cursor: pointer; }
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
            <h1>🚀 Dizlyzen AI Manager</h1>
            
            <div class="security-bar">
                <span>🛡️ Real Graph API Execution Mode Active</span>
                <span style="background: #0284c7; padding: 2px 6px; border-radius: 4px; font-size: 11px;">v7.0 Live</span>
            </div>

            {% if message %}
                <div class="message">{{ message }}</div>
            {% endif %}

            <form action="/generate" method="POST" enctype="multipart/form-data">
                
                <div class="section-box">
                    <label for="social_account">Select Connected Social Account:</label>
                    <select name="social_account" id="social_account">
                        <option value="Samantasamiti">📌 Samantasamiti (Page ID: 1352257637972181)</option>
                    </select>

                    <label>Select Target Platforms:</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" name="platforms" value="Facebook" checked> Facebook Page</label>
                    </div>
                </div>

                <div class="section-box">
                    <label for="title">Campaign Title:</label>
                    <input type="text" name="title" id="title" value="जातिवाद का अंत और महापुरुषों के विचार" required>

                    <label for="quote">Campaign Caption / Description:</label>
                    <textarea name="quote" id="quote" rows="3">मानवता और कड़े कानून: जातिवाद के खात्मा की ओर कदम 🚀</textarea>

                    <label for="hashtags">Automatic Hashtags:</label>
                    <input type="text" name="hashtags" id="hashtags" value="#Samantasamiti #DizlyzenAI">
                </div>

                <button type="submit" class="submit-btn">✨ Send Dispatch to APIs</button>
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
        hashtags = request.form.get("hashtags")
        
        full_message = f"{title}\n\n{quote}\n\n{hashtags}"
        api_logs = []

        # Direct Facebook Graph API POST Request
        fb_url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/feed"
        payload = {"message": full_message, "access_token": FB_ACCESS_TOKEN}
        res = requests.post(fb_url, data=payload)
        res_json = res.json()
        
        if "id" in res_json:
            api_logs.append("Facebook: Success! Post Live Published ID: " + res_json["id"])
        else:
            error_msg = res_json.get("error", {}).get("message", "Unknown Error")
            api_logs.append(f"Facebook Failed: {error_msg}")

        new_entry = {"id": len(CAMPAIGN_HISTORY)+1, "title": title, "platform": "Facebook Page", "status": "Published", "date": "Just Now"}
        CAMPAIGN_HISTORY.insert(0, new_entry)

        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, history=CAMPAIGN_HISTORY, message=f"API Response Log -> {', '.join(api_logs)}")

    except Exception as e:
        return render_template_string(UNIFIED_DASHBOARD_TEMPLATE, history=CAMPAIGN_HISTORY, message=f"❌ Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)