from pyrogram import Client

api_id = 22232960          # তোমার API ID বসাও
api_hash = "86b621b89263ef81728ea992262c8e27"    # তোমার API_HASH বসাও

with Client("new_account", api_id=api_id, api_hash=api_hash) as app:
    print("✨ Session String:")
    print(app.export_session_string())