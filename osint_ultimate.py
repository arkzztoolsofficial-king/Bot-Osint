#!/usr/bin/env python3
# OSINT ULTIMATE BOT - ARKZZKING 🗿
# ALL FITUR DASAR + OP BANGSAT!

import telebot
import requests
import json
import re
import time
import os
import socket
import whois
import dns.resolver
import subprocess
from datetime import datetime
from colorama import init, Fore, Style
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import shodan
import exifread
from PIL import Image
import hashlib

init(autoreset=True)

# ========== KONFIGURASI BANGSAT ==========
BOT_TOKEN = "8614906184:AAGa1ffyrkxz-44ATVsoR55B_DGb5I1x0dE"  # GANTI GOBLOK!
CHAT_ID = "7586973446"  # GANTI KONTOL!
SHODAN_API = "Dr69CTWsGiBulU9OfwC4BltFVF3vFqdq"  # DAFTAR di shodan.io (gratis)
# ========================================

bot = telebot.TeleBot(BOT_TOKEN)

# ========== FITUR DASAR (MEDIUM) ==========

# 1. CEK USERNAME DI 20+ PLATFORM
def cek_username_all(username):
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter": f"https://twitter.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "GitHub": f"https://github.com/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Telegram": f"https://t.me/{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Medium": f"https://medium.com/@{username}",
        "DevianArt": f"https://www.deviantart.com/{username}",
        "Tumblr": f"https://{username}.tumblr.com/",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Mixcloud": f"https://www.mixcloud.com/{username}/",
        "Patreon": f"https://www.patreon.com/{username}",
        "BitBucket": f"https://bitbucket.org/{username}/",
        "VK": f"https://vk.com/{username}",
        "Weibo": f"https://weibo.com/{username}",
        "AskFM": f"https://ask.fm/{username}",
    }
    
    hasil = {}
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                hasil[platform] = f"✅ ADA: {url}"
            else:
                hasil[platform] = "❌ Tidak ditemukan"
        except:
            hasil[platform] = "❌ Error"
        time.sleep(0.3)
    
    return hasil

# 2. CEK EMAIL DENGAN HIBP
def cek_email_advanced(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {'hibp-api-key': ''}  # API key gratis dari HIBP
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            breach_count = len(data)
            breaches = [b['Name'] for b in data[:5]]
            return f"⚠️ EMAIL BOCOR! Ditemukan di {breach_count} breach.\nContoh: {', '.join(breaches)}"
        elif response.status_code == 404:
            return "✅ Aman! Tidak ditemukan di database breach."
        else:
            return "❌ API limit atau error"
    except:
        return "❌ Gagal cek breach"

# 3. CEK NOMOR LENGKAP
def cek_nomor_lengkap(nomor):
    try:
        # Format nomor Indonesia
        nomor_clean = re.sub(r'[^0-9+]', '', nomor)
        if nomor_clean.startswith('0'):
            nomor_clean = '+62' + nomor_clean[1:]
        elif not nomor_clean.startswith('+'):
            nomor_clean = '+' + nomor_clean
        
        phone_obj = phonenumbers.parse(nomor_clean, None)
        
        hasil = f"""
📱 CEK NOMOR LENGKAP:
═══════════════════════
Nomor: {phonenumbers.format_number(phone_obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}
Valid: {'✅ Ya' if phonenumbers.is_valid_number(phone_obj) else '❌ Tidak'}
Provider: {carrier.name_for_number(phone_obj, 'id') or 'Tidak diketahui'}
Lokasi: {geocoder.description_for_number(phone_obj, 'id')}
Timezone: {', '.join(timezone.time_zones_for_number(phone_obj))}
"""
        return hasil
    except:
        return "❌ Format nomor salah! Gunakan: 08123456789"

# 4. GEOLOKASI IP LENGKAP
def cek_ip_lengkap(ip):
    try:
        # IP-API
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting,query", timeout=10)
        data = response.json()
        
        if data.get('status') == 'success':
            hasil = f"""
🌍 GEOLOKASI IP: {ip}
═══════════════════════
Negara: {data.get('country', '-')} ({data.get('countryCode', '-')})
Region: {data.get('regionName', '-')}
Kota: {data.get('city', '-')}
Kode Pos: {data.get('zip', '-')}
Koordinat: {data.get('lat', '-')}, {data.get('lon', '-')}
ISP: {data.get('isp', '-')}
Provider: {data.get('org', '-')}
AS: {data.get('as', '-')}
Mobile: {'Ya' if data.get('mobile') else 'Tidak'}
Proxy: {'Ya' if data.get('proxy') else 'Tidak'}
Hosting: {'Ya' if data.get('hosting') else 'Tidak'}
Timezone: {data.get('timezone', '-')}
"""
            return hasil
        else:
            return "❌ IP tidak valid"
    except:
        return "❌ Error koneksi"

# 5. WHOIS LOOKUP
def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        hasil = f"""
📋 WHOIS LOOKUP: {domain}
═══════════════════════
Domain: {w.domain_name}
Registrar: {w.registrar}
Creation Date: {w.creation_date}
Expiration Date: {w.expiration_date}
Name Server: {w.name_servers}
Status: {w.status}
"""
        return hasil
    except:
        return "❌ Gagal mengambil whois"

# 6. DNS LOOKUP
def dns_lookup(domain):
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    hasil = f"\n🔍 DNS LOOKUP: {domain}\n═══════════════════\n"
    
    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            for answer in answers:
                hasil += f"\n{record}: {answer}"
        except:
            hasil += f"\n{record}: Tidak ditemukan"
    
    return hasil

# 7. SUBDOMAIN SCANNER
def subdomain_scan(domain):
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'dns', 'blog', 'shop',
        'admin', 'dev', 'test', 'api', 'vps', 'server', 'cloud', 'backup', 'secure'
    ]
    
    ditemukan = []
    for sub in subdomains:
        try:
            target = f"{sub}.{domain}"
            socket.gethostbyname(target)
            ditemukan.append(target)
        except:
            pass
        time.sleep(0.1)
    
    if ditemukan:
        return f"✅ Subdomain ditemukan:\n" + "\n".join(ditemukan)
    else:
        return "❌ Tidak ada subdomain ditemukan"

# 8. WAYBACK MACHINE
def wayback_archive(url):
    try:
        api = f"https://archive.org/wayback/available?url={url}"
        response = requests.get(api, timeout=10)
        data = response.json()
        
        if data['archived_snapshots']:
            snapshot = data['archived_snapshots']['closest']
            hasil = f"📜 ARCHIVE DITEMUKAN!\nURL: {snapshot['url']}\nTimestamp: {snapshot['timestamp']}"
        else:
            hasil = "❌ Tidak ada archive ditemukan"
        return hasil
    except:
        return "❌ Gagal mengambil archive"

# ========== FITUR OP (OVER POWER) ==========

# 9. REVERSE IMAGE SEARCH (Pake API Google/Bing)
def reverse_image_search(image_url):
    # Pake api.tineye.com (butuh API key)
    hasil = "🔍 FITUR REVERSE IMAGE: \n"
    hasil += "1. Google Images: https://images.google.com/searchbyimage?image_url={image_url}\n"
    hasil += "2. Yandex: https://yandex.com/images/search?url={image_url}\n"
    hasil += "3. Bing: https://www.bing.com/images/searchbyimage?imgurl={image_url}"
    return hasil

# 10. METADATA EXTRACT (Dari foto)
def extract_metadata(image_path):
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            
        hasil = "📷 METADATA FOTO:\n═══════════════════\n"
        for tag, value in tags.items():
            if 'GPS' in tag or 'DateTime' in tag or 'Make' in tag or 'Model' in tag:
                hasil += f"\n{tag}: {value}"
        
        if len(hasil) < 100:
            hasil += "\n⚠️ Tidak ada metadata yang ditemukan"
        return hasil
    except:
        return "❌ Gagal membaca metadata"

# 11. SOCIAL MEDIA STALKER (Instagram)
def stalk_instagram(username):
    # Pake unofficial API (instaloader)
    hasil = f"🔍 STALK INSTAGRAM: @{username}\n═══════════════════\n"
    hasil += "Link: https://www.instagram.com/{username}/\n"
    hasil += "Tips: Gunakan Instaloader untuk download foto/video\n"
    hasil += "Cek followers/following pake rapidtags.io"
    return hasil

# 12. DATA BREACH CHECK (Hash Password)
def check_password_breach(password):
    # Pake API haveibeenpwned
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=10)
        
        if suffix in response.text:
            return "⚠️ PASSWORD INI TERMASUK DALAM BREACH! Segera ganti password!"
        else:
            return "✅ Password aman (tidak ditemukan di breach)"
    except:
        return "❌ Gagal cek password"

# 13. SHODAN SEARCH (Cari device/bocoran)
def shodan_search(query):
    if not SHODAN_API or SHODAN_API == "MASUKIN_SHODAN_API":
        return "❌ Setup SHODAN_API dulu di script!"
    
    try:
        api = shodan.Shodan(SHODAN_API)
        results = api.search(query, limit=5)
        
        hasil = f"🔍 SHODAN SEARCH: {query}\n═══════════════════\n"
        for result in results['matches']:
            hasil += f"\nIP: {result['ip_str']}\nPort: {result['port']}\nInfo: {result['data'][:100]}...\n"
        return hasil
    except Exception as e:
        return f"❌ Shodan error: {str(e)}"

# 14. TELEGRAM OSINT
def telegram_osint(username):
    hasil = f"🔍 TELEGRAM OSINT: @{username}\n═══════════════════\n"
    hasil += f"Link: https://t.me/{username}\n"
    hasil += f"Username: @{username}\n"
    hasil += "\nCek via @userinfobot atau @tgdb_bot"
    return hasil

# 15. EMAIL REPUTATION & GRAB CONTACTS
def email_reputation(email):
    try:
        # Pake hunter.io atau emailrep.io
        url = f"https://emailrep.io/{email}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        hasil = f"📧 EMAIL REPUTATION: {email}\n═══════════════════\n"
        hasil += f"Reputation: {data.get('reputation', 'Unknown')}\n"
        hasil += f"Suspicious: {'Ya' if data.get('suspicious') else 'Tidak'}\n"
        hasil += f"Domain: {data.get('details', {}).get('domain', 'Unknown')}\n"
        return hasil
    except:
        return "❌ Gagal cek reputasi email"

# 16. CREDIT CARD LEAK CHECK (Simulasi)
def check_cc_leak(cc_number):
    # Pake API atau database leak
    return "⚠️ FITUR CEK CC LEAK: Gunakan database leak di dark web (need API)."

# 17. DARK WEB MONITORING (Simulasi)
def dark_web_search(query):
    return """
🌑 DARK WEB SEARCH:
═══════════════════════════════
Gunakan Tor browser: https://www.torproject.org/
Search engine: Ahmia, Torch, Not Evil
Untuk monitor email breach: haveibeenpwned.com
Untuk cek dark web: intelligencex.com
"""

# 18. WHATSAPP OSINT
def whatsapp_osint(nomor):
    return f"""
💬 WHATSAPP OSINT: {nomor}
═══════════════════════
Cek: https://wa.me/{nomor}
Tools: WhatsApp Sniffer (butuh MITM)
WASpam: WhatsApp Bomber
"""

# ========== COMMAND TELEGRAM ==========

@bot.message_handler(commands=['start', 'help'])
def help_menu(m):
    help_text = """
╔══════════════════════════════════════╗
║   🔥 OSINT ULTIMATE BOT 🔥           ║
║        BY: ARKZZKING 👑              ║
╚══════════════════════════════════════╝

🟢 FITUR DASAR:
════════════════════
/user [username] - Cek username di 20+ platform
/email [email] - Cek email breach (HIBP)
/nomor [nomor] - Verifikasi nomor lengkap
/ip [ip/domain] - Geolokasi IP lengkap
/whois [domain] - WHOIS lookup
/dns [domain] - DNS lookup
/subdomain [domain] - Scan subdomain
/archive [url] - Wayback machine archive

🔴 FITUR OP (OVER POWER):
════════════════════
/reverse [url] - Reverse image search
/metadata - Extract metadata foto
/stalk [username] - Social media stalker
/pwd [password] - Cek password breach
/shodan [query] - Shodan device search
/tgosint [username] - Telegram OSINT
/emailrep [email] - Email reputation
/cc [cc_number] - Cek CC leak (simulasi)
/darkweb [query] - Dark web search
/wa [nomor] - WhatsApp OSINT

📊 OTHER:
════════════════════
/report [target] - FULL OSINT report
    """
    bot.reply_to(m, help_text)

@bot.message_handler(commands=['user'])
def user_cmd(m):
    username = m.text.replace('/user ', '').strip()
    if not username:
        bot.reply_to(m, "❌ PAKE: /user [username]")
        return
    
    bot.reply_to(m, f"🔍 Mencari @{username} di 20+ platform... (bisa makan waktu)")
    hasil = cek_username_all(username)
    
    response = f"📊 HASIL PENCARIAN: @{username}\n═══════════════════\n"
    for platform, status in hasil.items():
        response += f"\n📱 {platform}: {status}"
    
    for i in range(0, len(response), 4000):
        bot.reply_to(m, response[i:i+4000])

@bot.message_handler(commands=['email'])
def email_cmd(m):
    email = m.text.replace('/email ', '').strip()
    if not email or '@' not in email:
        bot.reply_to(m, "❌ PAKE: /email [email]")
        return
    
    bot.reply_to(m, f"🔍 Memeriksa {email}...")
    hasil = cek_email_advanced(email)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['nomor'])
def nomor_cmd(m):
    nomor = m.text.replace('/nomor ', '').strip()
    if not nomor:
        bot.reply_to(m, "❌ PAKE: /nomor [08123456789]")
        return
    
    bot.reply_to(m, f"🔍 Verifikasi nomor {nomor}...")
    hasil = cek_nomor_lengkap(nomor)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['ip'])
def ip_cmd(m):
    ip = m.text.replace('/ip ', '').strip()
    if not ip:
        bot.reply_to(m, "❌ PAKE: /ip [ip/domain]")
        return
    
    bot.reply_to(m, f"🔍 Melacak {ip}...")
    hasil = cek_ip_lengkap(ip)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['whois'])
def whois_cmd(m):
    domain = m.text.replace('/whois ', '').strip()
    if not domain:
        bot.reply_to(m, "❌ PAKE: /whois [domain.com]")
        return
    
    bot.reply_to(m, f"🔍 WHOIS lookup {domain}...")
    hasil = whois_lookup(domain)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['dns'])
def dns_cmd(m):
    domain = m.text.replace('/dns ', '').strip()
    if not domain:
        bot.reply_to(m, "❌ PAKE: /dns [domain.com]")
        return
    
    bot.reply_to(m, f"🔍 DNS lookup {domain}...")
    hasil = dns_lookup(domain)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['subdomain'])
def subdomain_cmd(m):
    domain = m.text.replace('/subdomain ', '').strip()
    if not domain:
        bot.reply_to(m, "❌ PAKE: /subdomain [domain.com]")
        return
    
    bot.reply_to(m, f"🔍 Scanning subdomain {domain}...")
    hasil = subdomain_scan(domain)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['archive'])
def archive_cmd(m):
    url = m.text.replace('/archive ', '').strip()
    if not url:
        bot.reply_to(m, "❌ PAKE: /archive [url]")
        return
    
    bot.reply_to(m, f"🔍 Cek archive {url}...")
    hasil = wayback_archive(url)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['reverse'])
def reverse_cmd(m):
    img_url = m.text.replace('/reverse ', '').strip()
    if not img_url:
        bot.reply_to(m, "❌ PAKE: /reverse [url_gambar]")
        return
    
    hasil = reverse_image_search(img_url)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['pwd'])
def pwd_cmd(m):
    password = m.text.replace('/pwd ', '').strip()
    if not password:
        bot.reply_to(m, "❌ PAKE: /pwd [password]")
        return
    
    bot.reply_to(m, f"🔍 Cek password di database breach...")
    hasil = check_password_breach(password)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['shodan'])
def shodan_cmd(m):
    query = m.text.replace('/shodan ', '').strip()
    if not query:
        bot.reply_to(m, "❌ PAKE: /shodan [query]")
        return
    
    bot.reply_to(m, f"🔍 Shodan search {query}...")
    hasil = shodan_search(query)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['tgosint'])
def tgosint_cmd(m):
    username = m.text.replace('/tgosint ', '').strip()
    if not username:
        bot.reply_to(m, "❌ PAKE: /tgosint [username]")
        return
    
    hasil = telegram_osint(username)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['emailrep'])
def emailrep_cmd(m):
    email = m.text.replace('/emailrep ', '').strip()
    if not email or '@' not in email:
        bot.reply_to(m, "❌ PAKE: /emailrep [email]")
        return
    
    hasil = email_reputation(email)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['cc'])
def cc_cmd(m):
    cc = m.text.replace('/cc ', '').strip()
    if not cc:
        bot.reply_to(m, "❌ PAKE: /cc [nomor_credit_card]")
        return
    
    hasil = check_cc_leak(cc)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['darkweb'])
def darkweb_cmd(m):
    query = m.text.replace('/darkweb ', '').strip()
    hasil = dark_web_search(query)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['wa'])
def wa_cmd(m):
    nomor = m.text.replace('/wa ', '').strip()
    if not nomor:
        bot.reply_to(m, "❌ PAKE: /wa [08123456789]")
        return
    
    hasil = whatsapp_osint(nomor)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['stalk'])
def stalk_cmd(m):
    username = m.text.replace('/stalk ', '').strip()
    if not username:
        bot.reply_to(m, "❌ PAKE: /stalk [username]")
        return
    
    hasil = stalk_instagram(username)
    bot.reply_to(m, hasil)

@bot.message_handler(commands=['metadata'])
def metadata_cmd(m):
    bot.reply_to(m, "📷 Kirim foto untuk extract metadata!")
    # Handle photo nanti pake message handler khusus

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    file_id = m.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("temp_photo.jpg", 'wb') as f:
        f.write(downloaded_file)
    
    hasil = extract_metadata("temp_photo.jpg")
    bot.reply_to(m, hasil)
    os.remove("temp_photo.jpg")

@bot.message_handler(commands=['report'])
def report_cmd(m):
    target = m.text.replace('/report ', '').strip()
    if not target:
        bot.reply_to(m, "❌ PAKE: /report [target]")
        return
    
    bot.reply_to(m, f"📊 MEMBUAT FULL REPORT UNTUK: {target}\n⏳ Mohon tunggu...")
    
    if '@' in target:
        hasil = f"📧 REPORT EMAIL: {target}\n═══════════════════\n"
        hasil += cek_email_advanced(target) + "\n"
        hasil += email_reputation(target)
        
    elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        hasil = f"🌍 REPORT IP: {target}\n═══════════════════\n"
        hasil += cek_ip_lengkap(target) + "\n"
        hasil += "\n🔍 Subdomain & Port scan..."
        hasil += "\n" + subdomain_scan(target)
        
    elif target.replace('+', '').replace('-', '').isdigit() or target.startswith('0') or target.startswith('+'):
        hasil = f"📱 REPORT NOMOR: {target}\n═══════════════════\n"
        hasil += cek_nomor_lengkap(target) + "\n"
        hasil += whatsapp_osint(target)
        
    else:
        hasil = f"👤 REPORT USERNAME: @{target}\n═══════════════════\n"
        results = cek_username_all(target)
        for platform, status in results.items():
            if "ADA" in status:
                hasil += f"\n✅ {platform}: {status}"
    
    bot.reply_to(m, hasil[:4000])

# ========== JALANKAN BOT ==========
print(Fore.RED + """
╔════════════════════════════════════════════════╗
║       🔥 OSINT ULTIMATE BOT 🔥                 ║
║          ARKZZKING - ALL FITUR                 ║
╚════════════════════════════════════════════════╝
""")
print(Fore.GREEN + f"[+] BOT TOKEN: {BOT_TOKEN[:15]}...")
print(Fore.YELLOW + f"[+] CHAT ID: {CHAT_ID}")
print(Fore.RED + "[+] BOT JALAN DENGAN SEMUA FITUR KONTOL!")
print(Style.RESET_ALL)

bot.infinity_polling()
