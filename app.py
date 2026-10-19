import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Samanta Samiti Auto Post</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 20px; display: flex; justify-content: center; }
        .card { background: #1e293b; padding: 30px; border-radius: 10px; width: 650px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        input, textarea, select { width: 100%; padding: 10px; margin: 10px 0; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 5px; box-sizing: border-box; }
        input[type="file"] { padding: 8px; background: #334155; cursor: pointer; }
        button { width: 100%; padding: 12px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .btn-save { background: #3b82f6; color: #fff; }
        .btn-pub { background: #ef4444; color: #fff; }
        #status { margin-top: 15px; font-weight: bold; text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <h2>✨ Samanta Samiti Media & Publisher Dashboard</h2>
        <form id="credForm">
            <label>Meta Access Token (User Token):</label>
            <input type="text" name="meta_access_token" id="tokenInput" placeholder="Paste your Graph API Explorer token here">
            <button type="button" class="btn-save" onclick="saveCreds()">💾 Save & Auto-Fetch Page Token</button>
        </form>
        <hr style="border-color: #475569; margin: 20px 0;">
        <form id="pubForm" onsubmit="publishPost(event)">
            <label>Title / Heading:</label>
            <input type="text" id="title" value="जातिवाद का अंत और महापुरुषों के विचार">
            
            <label>Campaign Description / Message:</label>
            <textarea id="description">मानवता और कड़े कानून: जातिवाद के खात्मा की ओर कदम 🚀</textarea>
            
            <label>Upload Image or Video from Computer:</label>
            <input type="file" id="mediaFile" accept="image/*,video/*">

            <button type="submit" class="btn-pub">✨ Upload Media & Publish to Facebook</button>
        </form>
        <div id="status"></div>
    </div>
    <script>
        async function saveCreds() {
            let token = document.getElementById('tokenInput').value;
            let res = await fetch('/onboard-client', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'meta_access_token=' + encodeURIComponent(token)
            });
            let data = await res.json();
            document.getElementById('status').innerText = data.message;
            document.getElementById('status').style.color = '#10b981';
        }
        async function publishPost(e) {
            e.preventDefault();
            document.getElementById('status').innerText = "Uploading media and posting to Facebook...";
            document.getElementById('status').style.color = '#f59e0b';
            
            let formData = new FormData();
            formData.append('title', document.getElementById('title').value);
            formData.append('description', document.getElementById('description').value);
            let fileInput = document.getElementById('mediaFile').files[0];
            if(fileInput) {
                formData.append('media', fileInput);
            }

            let res = await fetch('/trigger-upload', {
                method: 'POST',
                body: formData
            });
            let data = await res.json();
            if(res.ok) {
                document.getElementById('status').innerText = "✅ Successfully posted to Facebook! Post ID: " + data.post_id;
                document.getElementById('status').style.color = '#10b981';
            } else {
                document.getElementById('status').innerText = "❌ " + data.message;
                document.getElementById('status').style.color = '#ef4444';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/onboard-client', methods=['POST'])
def onboard_client():
    data = request.form or request.json or {}
    token = data.get('meta_access_token') or data.get('token')
    
    page_token = token
    if token:
        try:
            acc_res = requests.get("https://graph.facebook.com/v18.0/me/accounts", params={'access_token': token})
            acc_data = acc_res.json()
            if 'data' in acc_data and len(acc_data['data']) > 0:
                page_token = acc_data['data'][0]['access_token']
                print(f"✅ Page Access Token fetched for: {acc_data['data'][0].get('name')}")
        except Exception as e:
            print(f"⚠️ Auto-fetch warning: {e}")

    os.makedirs('clients/client_1', exist_ok=True)
    config_path = 'clients/client_1/config.json'
    
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
            except:
                pass
                
    if page_token:
        config['meta_access_token'] = page_token
        
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
        
    return jsonify({"status": "success", "message": "Credentials saved & Page Token auto-fetched successfully!"})

def perform_facebook_upload(title, description, file_path):
    config_path = 'clients/client_1/config.json'
    if not os.path.exists(config_path):
        print("❌ Config file not found!")
        return False
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    token = config.get('meta_access_token')
    smart_desc = f"{title}\n\n{description}"
    
    if not token:
        print("❌ Facebook Error: Missing Token.")
        return False

    # Agar user ne file upload ki hai toh usko multipart/form-data se bhejenge
    if file_path and os.path.exists(file_path):
        # Check if it's video or image based on extension
        is_video = file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
        url = f"https://graph.facebook.com/v18.0/me/{'videos' if is_video else 'photos'}"
        
        with open(file_path, 'rb') as media_file:
            files = {'source' if is_video else 'file': media_file}
            payload = {'description' if is_video else 'caption': smart_desc, 'access_token': token}
            res = requests.post(url, data=payload, files=files)
    else:
        # Fallback to text post if no media attached
        url = "https://graph.facebook.com/v18.0/me/feed"
        payload = {'message': smart_desc, 'access_token': token}
        res = requests.post(url, data=payload)
    
    result = res.json()
    print(f"🎉 Facebook Upload Response: {result}")
    return result.get('post_id') or result.get('id')

@app.route('/trigger-upload', methods=['POST'])
def trigger_upload():
    title = request.form.get('title', 'Samantasamiti Post')
    description = request.form.get('description', '')
    
    saved_file_path = None
    if 'media' in request.files:
        file = request.files['media']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_file_path)
    
    post_id = perform_facebook_upload(title, description, saved_file_path)
    if post_id:
        return jsonify({"status": "success", "post_id": post_id})
    else:
        return jsonify({"status": "error", "message": "Publishing failed! Check terminal logs."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)