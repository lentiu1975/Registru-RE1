#!/home/lentiuro/virtualenv/vama_backend/3.11/bin/python
# -*- coding: utf-8 -*-
"""
CGI Script pentru rularea setup-ului prin browser
Accesați: https://vama.lentiu.ro/run_setup.cgi
"""

import cgitb
cgitb.enable()  # Afișează erorile în browser

print("Content-Type: text/html; charset=utf-8")
print()

print("""
<!DOCTYPE html>
<html>
<head>
    <title>Setup Deployment - Registru import RE1</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #1e1e1e;
            color: #00ff00;
            padding: 20px;
            margin: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #000;
            padding: 20px;
            border: 2px solid #00ff00;
            border-radius: 5px;
        }
        h1 { color: #00ff00; text-align: center; }
        .output {
            background: #0a0a0a;
            padding: 15px;
            border: 1px solid #00ff00;
            margin: 20px 0;
            white-space: pre-wrap;
            font-size: 14px;
        }
        .success { color: #00ff00; }
        .error { color: #ff0000; }
        .warning { color: #ffff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Setup Deployment</h1>
        <div class="output">
""")

try:
    # Importă și rulează setup
    import sys
    import os

    # Adaugă calea către aplicație
    app_path = '/home/lentiuro/vama_backend'
    sys.path.insert(0, app_path)
    os.chdir(app_path)

    # Rulează setup
    from setup_deployment import run_setup
    result = run_setup()

    if result:
        print('<span class="success">✓ Setup finalizat cu SUCCES!</span>')
    else:
        print('<span class="error">✗ Setup finalizat cu ERORI!</span>')

except Exception as e:
    print(f'<span class="error">EROARE: {str(e)}</span>')
    import traceback
    print(f'<pre>{traceback.format_exc()}</pre>')

print("""
        </div>
        <p style="text-align: center; color: #888;">
            După rularea setup-ului, restart aplicația în cPanel Python App
        </p>
    </div>
</body>
</html>
""")
