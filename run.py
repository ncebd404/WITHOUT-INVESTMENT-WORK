#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import telebot
import time
import threading
from telebot import apihelper

# 64-bit check
if '64' not in os.uname().machine:
    sys.exit("[-] Only 64-bit device supported!")

# Auto update
try:
    print("[*] Checking for updates...")
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Update completed!")
except:
    print("[!] Update skipped.")

try:
    import tool
    print("[+] tool loaded successfully!")

    bot = tool.bot
    BOT_TOKEN = tool.BOT_TOKEN if hasattr(tool, 'BOT_TOKEN') else None

    if not BOT_TOKEN:
        print("[-] BOT_TOKEN not found!")
        sys.exit(1)

    print(f"[+] Bot is running with token: {BOT_TOKEN[:15]}...")

    # === নেটওয়ার্ক সমস্যা কমানোর জন্য গুরুত্বপূর্ণ সেটিংস ===
    apihelper.SESSION_TIME_TO_LIVE = 5 * 60      # প্রতি ৫ মিনিটে session refresh
    apihelper.READ_TIMEOUT = 60
    apihelper.CONNECT_TIMEOUT = 15

    print("[+] Anti-idle & reconnect settings applied")

    # === Robust Polling Function (নেট কাটলেও চালু থাকবে) ===
    def start_bot():
        print("[*] Starting robust Telegram Bot (will auto-reconnect on network loss)...")
        
        while True:                     # এই লুপটা খুব জরুরি
            try:
                bot.infinity_polling(
                    none_stop=True,
                    interval=1,
                    timeout=90,               # long polling
                    long_polling_timeout=60,
                    skip_pending=True,
                    allowed_updates=None,
                    logger_level=0            # অপ্রয়োজনীয় error log কমায়
                )
            except Exception as e:
                error_str = str(e).lower()
                if "connection" in error_str or "timeout" in error_str or "abort" in error_str or "reset" in error_str:
                    print(f"[!] Network issue detected: {e}")
                    print("[*] Waiting for network to come back... Retrying in 8 seconds")
                else:
                    print(f"[!] Unexpected error: {e}")
                
                time.sleep(8)   # নেট না থাকলে ৮ সেকেন্ড পর আবার চেষ্টা করবে

    # Bot চালু করো
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    print("\n" + "="*50)
    print("✅ Bot is now LIVE & RESILIENT!")
    print("✅ নেট কাটলেও ক্র্যাশ করবে না")
    print("✅ নেট ফিরলে আপনা-আপনি reconnect হয়ে যাবে")
    print("✅ Send /start or any command from Telegram")
    print("="*50)

    # Main loop — script চালু রাখার জন্য
    while True:
        time.sleep(10)

except Exception as e:
    print(f"[-] Critical Error: {e}")
