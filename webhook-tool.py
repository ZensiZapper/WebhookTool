import requests
import json
import time
import os
import sys
import threading
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ═══════════════════════════════════════════
#          COLOR SHORTCUTS
# ═══════════════════════════════════════════
R = Fore.RED
G = Fore.GREEN
B = Fore.BLUE
Y = Fore.YELLOW
C = Fore.CYAN
M = Fore.MAGENTA
W = Fore.WHITE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

class WebhookTool:
    def __init__(self):
        self.webhook_url = None
        self.webhook_info = None
        self.message_history = []

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        self.clear()
        ascii_art = f"""{C}
  __      __   _    _             _     _____         _ 
  \\ \\    / /__| |__| |_  ___  ___| |__ |_   _|__  ___| |
   \\ \\/\\/ / -_) '_ \\ ' \\/ _ \\/ _ \\ / /   | |/ _ \\/ _ \\ |
    \\_/\\_/\\___|_.__/_||_\\___/\\___/_\\_\\   |_|\\___/\\___/_|
{RESET}"""
        print(ascii_art)
        print(f"{M}{'═' * 60}")
        print(f"{Y}  ⚡ Discord Webhook Tool")
        print(f"{G}  ⚡ Github/ZensiZapper ")
        print(f"{C}  ⚡ Version: v1")
        print(f"{M}{'═' * 60}\n")

    def set_webhook(self):
        print(f"\n{C}[?] Enter Webhook URL: {W}", end="")
        url = input().strip()
        if not url.startswith("https://discord.com/api/webhooks/") and \
           not url.startswith("https://discordapp.com/api/webhooks/"):
            print(f"{R}[✘] Invalid webhook URL!")
            return False
        self.webhook_url = url
        print(f"{G}[✔] Webhook URL set successfully!")
        return True

    def check_webhook(self):
        if not self._check_url():
            return
        try:
            r = requests.get(self.webhook_url)
            if r.status_code == 200:
                data = r.json()
                self.webhook_info = data
                print(f"\n{G}[✔] Webhook is VALID!\n")
                print(f"{C}  ╔══════════════════════════════════════")
                print(f"{C}  ║ {W}Name      : {Y}{data.get('name', 'N/A')}")
                print(f"{C}  ║ {W}ID        : {Y}{data.get('id', 'N/A')}")
                print(f"{C}  ║ {W}Token     : {Y}{data.get('token', 'N/A')[:20]}...")
                print(f"{C}  ║ {W}Guild ID  : {Y}{data.get('guild_id', 'N/A')}")
                print(f"{C}  ║ {W}Channel ID: {Y}{data.get('channel_id', 'N/A')}")
                print(f"{C}  ║ {W}Type      : {Y}{data.get('type', 'N/A')}")
                avatar = data.get('avatar')
                if avatar:
                    avatar_url = f"https://cdn.discordapp.com/avatars/{data['id']}/{avatar}.png"
                    print(f"{C}  ║ {W}Avatar    : {Y}{avatar_url}")
                else:
                    print(f"{C}  ║ {W}Avatar    : {Y}Default")
                print(f"{C}  ╚══════════════════════════════════════")
            else:
                print(f"{R}[✘] Webhook is INVALID! Status: {r.status_code}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_message(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] Enter message content: {W}", end="")
        content = input().strip()
        print(f"{C}[?] Custom username (leave empty for default): {W}", end="")
        username = input().strip()
        print(f"{C}[?] Avatar URL (leave empty for default): {W}", end="")
        avatar_url = input().strip()
        print(f"{C}[?] TTS (Text-to-Speech)? (y/n): {W}", end="")
        tts = input().strip().lower() == 'y'

        payload = {"content": content, "tts": tts}
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url

        try:
            r = requests.post(self.webhook_url, json=payload)
            if r.status_code == 204:
                print(f"{G}[✔] Message sent successfully!")
                self.message_history.append({
                    "type": "message",
                    "content": content,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
                print(f"{R}    Response: {r.text}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_embed(self):
        if not self._check_url():
            return

        print(f"\n{M}{'─' * 40}")
        print(f"{Y}  📋 Embed Builder")
        print(f"{M}{'─' * 40}\n")

        print(f"{C}[?] Embed Title: {W}", end="")
        title = input().strip()
        print(f"{C}[?] Embed Description: {W}", end="")
        description = input().strip()
        print(f"{C}[?] Embed Color (hex, e.g., FF5733): {W}", end="")
        color_hex = input().strip()
        print(f"{C}[?] Author Name (leave empty to skip): {W}", end="")
        author_name = input().strip()
        print(f"{C}[?] Author Icon URL (leave empty to skip): {W}", end="")
        author_icon = input().strip()
        print(f"{C}[?] Footer Text (leave empty to skip): {W}", end="")
        footer_text = input().strip()
        print(f"{C}[?] Footer Icon URL (leave empty to skip): {W}", end="")
        footer_icon = input().strip()
        print(f"{C}[?] Thumbnail URL (leave empty to skip): {W}", end="")
        thumbnail = input().strip()
        print(f"{C}[?] Image URL (leave empty to skip): {W}", end="")
        image = input().strip()
        print(f"{C}[?] URL (clickable title link, leave empty to skip): {W}", end="")
        url = input().strip()
        print(f"{C}[?] Add timestamp? (y/n): {W}", end="")
        timestamp = input().strip().lower() == 'y'
        print(f"{C}[?] Custom username (leave empty for default): {W}", end="")
        username = input().strip()

        fields = []
        print(f"\n{C}[?] How many fields? (0 for none): {W}", end="")
        try:
            num_fields = int(input().strip())
        except ValueError:
            num_fields = 0

        for i in range(num_fields):
            print(f"\n{Y}  Field {i + 1}:")
            print(f"{C}    [?] Name: {W}", end="")
            f_name = input().strip()
            print(f"{C}    [?] Value: {W}", end="")
            f_value = input().strip()
            print(f"{C}    [?] Inline? (y/n): {W}", end="")
            f_inline = input().strip().lower() == 'y'
            fields.append({"name": f_name, "value": f_value, "inline": f_inline})

        embed = {}
        if title:
            embed["title"] = title
        if description:
            embed["description"] = description
        if color_hex:
            try:
                embed["color"] = int(color_hex, 16)
            except ValueError:
                embed["color"] = 0
        if url:
            embed["url"] = url
        if timestamp:
            embed["timestamp"] = datetime.utcnow().isoformat()
        if author_name:
            embed["author"] = {"name": author_name}
            if author_icon:
                embed["author"]["icon_url"] = author_icon
        if footer_text:
            embed["footer"] = {"text": footer_text}
            if footer_icon:
                embed["footer"]["icon_url"] = footer_icon
        if thumbnail:
            embed["thumbnail"] = {"url": thumbnail}
        if image:
            embed["image"] = {"url": image}
        if fields:
            embed["fields"] = fields

        payload = {"embeds": [embed]}
        if username:
            payload["username"] = username

        print(f"\n{C}[?] Message content with embed (leave empty for none): {W}", end="")
        msg_content = input().strip()
        if msg_content:
            payload["content"] = msg_content

        try:
            r = requests.post(self.webhook_url, json=payload)
            if r.status_code == 204:
                print(f"{G}[✔] Embed sent successfully!")
                self.message_history.append({
                    "type": "embed",
                    "title": title,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
                print(f"{R}    Response: {r.text}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_multiple_embeds(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] How many embeds? (max 10): {W}", end="")
        try:
            num = min(int(input().strip()), 10)
        except ValueError:
            print(f"{R}[✘] Invalid number!")
            return

        embeds = []
        for i in range(num):
            print(f"\n{Y}{'─' * 30} Embed {i + 1} {'─' * 30}")
            print(f"{C}[?] Title: {W}", end="")
            title = input().strip()
            print(f"{C}[?] Description: {W}", end="")
            desc = input().strip()
            print(f"{C}[?] Color (hex): {W}", end="")
            color = input().strip()

            embed = {}
            if title:
                embed["title"] = title
            if desc:
                embed["description"] = desc
            if color:
                try:
                    embed["color"] = int(color, 16)
                except ValueError:
                    pass
            embeds.append(embed)

        payload = {"embeds": embeds}
        try:
            r = requests.post(self.webhook_url, json=payload)
            if r.status_code == 204:
                print(f"{G}[✔] {num} embeds sent successfully!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def spam_messages(self):
        if not self._check_url():
            return
        print(f"\n{R}⚠ WARNING: Use responsibly! Spamming violates Discord TOS!")
        print(f"{C}[?] Message to spam: {W}", end="")
        content = input().strip()
        print(f"{C}[?] Number of messages: {W}", end="")
        try:
            count = int(input().strip())
        except ValueError:
            print(f"{R}[✘] Invalid number!")
            return
        print(f"{C}[?] Delay between messages (seconds, min 0.5): {W}", end="")
        try:
            delay = max(float(input().strip()), 0.5)
        except ValueError:
            delay = 1.0

        print(f"{C}[?] Custom username (leave empty for default): {W}", end="")
        username = input().strip()

        print(f"\n{Y}[⚡] Starting spam... ({count} messages, {delay}s delay)")

        success = 0
        failed = 0
        for i in range(count):
            payload = {"content": content}
            if username:
                payload["username"] = username
            try:
                r = requests.post(self.webhook_url, json=payload)
                if r.status_code == 204:
                    success += 1
                    print(f"{G}  [✔] Message {i + 1}/{count} sent")
                elif r.status_code == 429:
                    retry_after = r.json().get("retry_after", 1)
                    print(f"{Y}  [⏳] Rate limited! Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    r = requests.post(self.webhook_url, json=payload)
                    if r.status_code == 204:
                        success += 1
                        print(f"{G}  [✔] Message {i + 1}/{count} sent (retry)")
                    else:
                        failed += 1
                else:
                    failed += 1
                    print(f"{R}  [✘] Message {i + 1}/{count} failed ({r.status_code})")
            except Exception as e:
                failed += 1
                print(f"{R}  [✘] Error: {e}")
            time.sleep(delay)

        print(f"\n{M}{'─' * 40}")
        print(f"{G}  ✔ Success: {success}")
        print(f"{R}  ✘ Failed:  {failed}")
        print(f"{M}{'─' * 40}")

    def threaded_spam(self):
        if not self._check_url():
            return
        print(f"\n{R}⚠ WARNING: Threaded spam! Use with extreme caution!")
        print(f"{C}[?] Message to spam: {W}", end="")
        content = input().strip()
        print(f"{C}[?] Number of threads: {W}", end="")
        try:
            num_threads = int(input().strip())
        except ValueError:
            print(f"{R}[✘] Invalid number!")
            return
        print(f"{C}[?] Messages per thread: {W}", end="")
        try:
            msgs_per_thread = int(input().strip())
        except ValueError:
            print(f"{R}[✘] Invalid number!")
            return

        results = {"success": 0, "failed": 0}
        lock = threading.Lock()

        def spam_thread(thread_id):
            for i in range(msgs_per_thread):
                try:
                    r = requests.post(self.webhook_url, json={"content": content})
                    with lock:
                        if r.status_code == 204:
                            results["success"] += 1
                            print(f"{G}  [Thread-{thread_id}] Message {i + 1} sent")
                        elif r.status_code == 429:
                            retry_after = r.json().get("retry_after", 2)
                            print(f"{Y}  [Thread-{thread_id}] Rate limited! Waiting {retry_after}s")
                            time.sleep(retry_after)
                        else:
                            results["failed"] += 1
                except Exception:
                    with lock:
                        results["failed"] += 1
                time.sleep(0.5)

        print(f"\n{Y}[⚡] Launching {num_threads} threads...")
        threads = []
        for t in range(num_threads):
            thread = threading.Thread(target=spam_thread, args=(t + 1,))
            threads.append(thread)
            thread.start()

        for t in threads:
            t.join()

        print(f"\n{M}{'─' * 40}")
        print(f"{G}  ✔ Total Success: {results['success']}")
        print(f"{R}  ✘ Total Failed:  {results['failed']}")
        print(f"{M}{'─' * 40}")

    def delete_webhook(self):
        if not self._check_url():
            return
        print(f"\n{R}⚠ This will PERMANENTLY delete the webhook!")
        print(f"{C}[?] Are you sure? (yes/no): {W}", end="")
        confirm = input().strip().lower()
        if confirm == 'yes':
            try:
                r = requests.delete(self.webhook_url)
                if r.status_code == 204:
                    print(f"{G}[✔] Webhook deleted successfully!")
                    self.webhook_url = None
                    self.webhook_info = None
                else:
                    print(f"{R}[✘] Failed! Status: {r.status_code}")
            except Exception as e:
                print(f"{R}[✘] Error: {e}")
        else:
            print(f"{Y}[!] Cancelled.")

    def edit_webhook(self):
        if not self._check_url():
            return
        print(f"\n{M}{'─' * 40}")
        print(f"{Y}  ✏ Edit Webhook")
        print(f"{M}{'─' * 40}\n")

        print(f"{C}[?] New name (leave empty to skip): {W}", end="")
        name = input().strip()
        print(f"{C}[?] New avatar URL (leave empty to skip): {W}", end="")
        avatar_url = input().strip()

        payload = {}
        if name:
            payload["name"] = name
        if avatar_url:
            try:
                img_data = requests.get(avatar_url).content
                import base64
                encoded = base64.b64encode(img_data).decode('utf-8')
                if avatar_url.lower().endswith('.png'):
                    payload["avatar"] = f"data:image/png;base64,{encoded}"
                elif avatar_url.lower().endswith('.gif'):
                    payload["avatar"] = f"data:image/gif;base64,{encoded}"
                else:
                    payload["avatar"] = f"data:image/jpeg;base64,{encoded}"
            except Exception as e:
                print(f"{R}[✘] Failed to fetch avatar: {e}")

        if not payload:
            print(f"{Y}[!] Nothing to update.")
            return

        try:
            r = requests.patch(self.webhook_url, json=payload)
            if r.status_code == 200:
                print(f"{G}[✔] Webhook updated successfully!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
                print(f"{R}    Response: {r.text}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_file(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] File path: {W}", end="")
        file_path = input().strip()

        if not os.path.exists(file_path):
            print(f"{R}[✘] File not found!")
            return

        print(f"{C}[?] Message with file (leave empty for none): {W}", end="")
        content = input().strip()
        print(f"{C}[?] Custom username (leave empty for default): {W}", end="")
        username = input().strip()

        payload = {}
        if content:
            payload["content"] = content
        if username:
            payload["username"] = username

        try:
            with open(file_path, 'rb') as f:
                files = {"file": (os.path.basename(file_path), f)}
                if payload:
                    r = requests.post(self.webhook_url, data={"payload_json": json.dumps(payload)}, files=files)
                else:
                    r = requests.post(self.webhook_url, files=files)
            if r.status_code == 200:
                print(f"{G}[✔] File sent successfully!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
                print(f"{R}    Response: {r.text}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_json_payload(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] Enter raw JSON payload:")
        print(f"{Y}    Example: {W}" + '{"content": "Hello!", "username": "Bot"}')
        print(f"{C}    > {W}", end="")
        raw = input().strip()

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            print(f"{R}[✘] Invalid JSON!")
            return

        try:
            r = requests.post(self.webhook_url, json=payload)
            if r.status_code in [200, 204]:
                print(f"{G}[✔] Payload sent successfully!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
                print(f"{R}    Response: {r.text}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def message_scheduler(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] Message to send: {W}", end="")
        content = input().strip()
        print(f"{C}[?] Delay in seconds before sending: {W}", end="")
        try:
            delay = float(input().strip())
        except ValueError:
            print(f"{R}[✘] Invalid delay!")
            return

        print(f"{Y}[⏳] Message scheduled! Sending in {delay} seconds...")
        time.sleep(delay)

        try:
            r = requests.post(self.webhook_url, json={"content": content})
            if r.status_code == 204:
                print(f"{G}[✔] Scheduled message sent!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def embed_from_json(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] Enter path to JSON file (or paste JSON):")
        print(f"{C}    > {W}", end="")
        user_input = input().strip()

        if os.path.exists(user_input):
            with open(user_input, 'r') as f:
                raw = f.read()
        else:
            raw = user_input

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            print(f"{R}[✘] Invalid JSON!")
            return

        try:
            r = requests.post(self.webhook_url, json=payload)
            if r.status_code in [200, 204]:
                print(f"{G}[✔] JSON embed sent successfully!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
                print(f"{R}    Response: {r.text}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def webhook_validator(self):
        print(f"\n{C}[?] Enter webhook URLs (one per line, empty line to finish):")
        urls = []
        while True:
            print(f"{C}    > {W}", end="")
            url = input().strip()
            if not url:
                break
            urls.append(url)

        if not urls:
            print(f"{Y}[!] No URLs provided.")
            return

        print(f"\n{Y}[⚡] Validating {len(urls)} webhooks...\n")

        valid = 0
        invalid = 0
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    print(f"{G}  [✔] VALID   - {data.get('name', 'Unknown')} (ID: {data.get('id', 'N/A')})")
                    valid += 1
                else:
                    print(f"{R}  [✘] INVALID - {url[:50]}... ({r.status_code})")
                    invalid += 1
            except Exception:
                print(f"{R}  [✘] ERROR   - {url[:50]}...")
                invalid += 1

        print(f"\n{M}{'─' * 40}")
        print(f"{G}  ✔ Valid:   {valid}")
        print(f"{R}  ✘ Invalid: {invalid}")
        print(f"{M}{'─' * 40}")

    def send_poll_embed(self):
        if not self._check_url():
            return
        print(f"\n{Y}  📊 Poll Creator\n")
        print(f"{C}[?] Poll question: {W}", end="")
        question = input().strip()
        print(f"{C}[?] Number of options: {W}", end="")
        try:
            num = int(input().strip())
        except ValueError:
            print(f"{R}[✘] Invalid number!")
            return

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        options = []
        for i in range(min(num, 10)):
            print(f"{C}    Option {i + 1}: {W}", end="")
            opt = input().strip()
            options.append(f"{emojis[i]} {opt}")

        description = "\n\n".join(options)

        embed = {
            "title": f"📊 {question}",
            "description": description,
            "color": int("3498db", 16),
            "footer": {"text": "React to vote!"},
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            r = requests.post(self.webhook_url, json={"embeds": [embed]})
            if r.status_code == 204:
                print(f"{G}[✔] Poll sent successfully!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_with_mentions(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] Message content: {W}", end="")
        content = input().strip()

        print(f"\n{Y}  Mention Options:")
        print(f"{W}  1. @everyone")
        print(f"{W}  2. @here")
        print(f"{W}  3. User mention (ID)")
        print(f"{W}  4. Role mention (ID)")
        print(f"{W}  5. No extra mention")
        print(f"{C}  > {W}", end="")
        choice = input().strip()

        if choice == "1":
            content = "@everyone " + content
        elif choice == "2":
            content = "@here " + content
        elif choice == "3":
            print(f"{C}[?] User ID: {W}", end="")
            uid = input().strip()
            content = f"<@{uid}> " + content
        elif choice == "4":
            print(f"{C}[?] Role ID: {W}", end="")
            rid = input().strip()
            content = f"<@&{rid}> " + content

        try:
            r = requests.post(self.webhook_url, json={"content": content})
            if r.status_code == 204:
                print(f"{G}[✔] Message with mention sent!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def send_emoji_message(self):
        if not self._check_url():
            return
        print(f"\n{Y}  😀 Emoji Message Sender\n")
        print(f"{C}[?] Message content: {W}", end="")
        content = input().strip()

        print(f"\n{C}[?] Add custom server emojis? (y/n): {W}", end="")
        if input().strip().lower() == 'y':
            while True:
                print(f"{C}    Emoji name: {W}", end="")
                emoji_name = input().strip()
                if not emoji_name:
                    break
                print(f"{C}    Emoji ID: {W}", end="")
                emoji_id = input().strip()
                print(f"{C}    Animated? (y/n): {W}", end="")
                animated = input().strip().lower() == 'y'

                if animated:
                    emoji_str = f"<a:{emoji_name}:{emoji_id}>"
                else:
                    emoji_str = f"<:{emoji_name}:{emoji_id}>"

                content += f" {emoji_str}"
                print(f"{G}    Added: {emoji_str}")
                print(f"{C}    Add another? (leave name empty to finish)")

        try:
            r = requests.post(self.webhook_url, json={"content": content})
            if r.status_code == 204:
                print(f"{G}[✔] Emoji message sent!")
            else:
                print(f"{R}[✘] Failed! Status: {r.status_code}")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def export_webhook_info(self):
        if not self._check_url():
            return
        try:
            r = requests.get(self.webhook_url)
            if r.status_code == 200:
                data = r.json()
                filename = f"webhook_{data.get('id', 'unknown')}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"{G}[✔] Webhook info exported to {filename}")
            else:
                print(f"{R}[✘] Failed to fetch webhook info!")
        except Exception as e:
            print(f"{R}[✘] Error: {e}")

    def view_history(self):
        if not self.message_history:
            print(f"\n{Y}[!] No message history yet.")
            return

        print(f"\n{M}{'─' * 50}")
        print(f"{Y}  📜 Message History ({len(self.message_history)} entries)")
        print(f"{M}{'─' * 50}\n")

        for i, entry in enumerate(self.message_history, 1):
            msg_type = entry.get("type", "unknown")
            time_sent = entry.get("time", "N/A")
            if msg_type == "message":
                content = entry.get("content", "N/A")[:50]
                print(f"{C}  [{time_sent}] {G}MSG  {W}| {content}")
            elif msg_type == "embed":
                title = entry.get("title", "N/A")[:50]
                print(f"{C}  [{time_sent}] {M}EMBED{W}| {title}")

    def repeat_message(self):
        if not self._check_url():
            return
        print(f"\n{C}[?] Message content: {W}", end="")
        content = input().strip()
        print(f"{C}[?] Interval in seconds: {W}", end="")
        try:
            interval = float(input().strip())
        except ValueError:
            print(f"{R}[✘] Invalid interval!")
            return
        print(f"{C}[?] How many times? (0 = infinite, Ctrl+C to stop): {W}", end="")
        try:
            times = int(input().strip())
        except ValueError:
            times = 0

        print(f"\n{Y}[⚡] Starting repeated messages... (Ctrl+C to stop)")

        count = 0
        try:
            while True:
                if times > 0 and count >= times:
                    break
                r = requests.post(self.webhook_url, json={"content": content})
                count += 1
                if r.status_code == 204:
                    print(f"{G}  [✔] #{count} sent at {datetime.now().strftime('%H:%M:%S')}")
                elif r.status_code == 429:
                    retry = r.json().get("retry_after", 2)
                    print(f"{Y}  [⏳] Rate limited, waiting {retry}s...")
                    time.sleep(retry)
                    continue
                else:
                    print(f"{R}  [✘] #{count} failed ({r.status_code})")
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{Y}[!] Stopped after {count} messages.")

    def _check_url(self):
        if not self.webhook_url:
            print(f"\n{R}[✘] No webhook URL set! Use option 1 first.")
            return False
        return True

    def menu(self):
        while True:
            self.banner()

            status = f"{G}✔ Connected" if self.webhook_url else f"{R}✘ Not set"
            print(f"  {W}Webhook Status: {status}")
            if self.webhook_url:
                print(f"  {W}URL: {C}{self.webhook_url[:60]}...\n")
            else:
                print()

            print(f"  {M}═══════════ SETUP ═══════════")
            print(f"  {C}[{W}01{C}] {W}Set Webhook URL")
            print(f"  {C}[{W}02{C}] {W}Check/Validate Webhook")
            print(f"  {C}[{W}03{C}] {W}Edit Webhook (Name/Avatar)")

            print(f"\n  {M}═══════════ MESSAGES ═══════════")
            print(f"  {C}[{W}04{C}] {W}Send Message")
            print(f"  {C}[{W}05{C}] {W}Send Embed")
            print(f"  {C}[{W}06{C}] {W}Send Multiple Embeds")
            print(f"  {C}[{W}07{C}] {W}Send File/Attachment")
            print(f"  {C}[{W}08{C}] {W}Send Raw JSON Payload")
            print(f"  {C}[{W}09{C}] {W}Send from JSON File")
            print(f"  {C}[{W}10{C}] {W}Send with Mentions")
            print(f"  {C}[{W}11{C}] {W}Send with Server Emojis (by ID)")
            print(f"  {C}[{W}12{C}] {W}Create Poll Embed")

            print(f"\n  {M}═══════════ AUTOMATION ═══════════")
            print(f"  {C}[{W}13{C}] {W}Spam Messages")
            print(f"  {C}[{W}14{C}] {W}Threaded Spam")
            print(f"  {C}[{W}15{C}] {W}Schedule Message")
            print(f"  {C}[{W}16{C}] {W}Repeat Message (Loop)")

            print(f"\n  {M}═══════════ TOOLS ═══════════")
            print(f"  {C}[{W}17{C}] {W}Bulk Webhook Validator")
            print(f"  {C}[{W}18{C}] {W}Export Webhook Info")
            print(f"  {C}[{W}19{C}] {W}View Message History")
            print(f"  {C}[{W}20{C}] {W}Delete Webhook")

            print(f"\n  {C}[{W}00{C}] {R}Exit")

            print(f"\n{M}{'═' * 60}")
            print(f"{C}  ➤ Select option: {W}", end="")

            choice = input().strip()

            actions = {
                "1": self.set_webhook, "01": self.set_webhook,
                "2": self.check_webhook, "02": self.check_webhook,
                "3": self.edit_webhook, "03": self.edit_webhook,
                "4": self.send_message, "04": self.send_message,
                "5": self.send_embed, "05": self.send_embed,
                "6": self.send_multiple_embeds, "06": self.send_multiple_embeds,
                "7": self.send_file, "07": self.send_file,
                "8": self.send_json_payload, "08": self.send_json_payload,
                "9": self.embed_from_json, "09": self.embed_from_json,
                "10": self.send_with_mentions,
                "11": self.send_emoji_message,
                "12": self.send_poll_embed,
                "13": self.spam_messages,
                "14": self.threaded_spam,
                "15": self.message_scheduler,
                "16": self.repeat_message,
                "17": self.webhook_validator,
                "18": self.export_webhook_info,
                "19": self.view_history,
                "20": self.delete_webhook,
                "0": None, "00": None,
            }

            if choice in ["0", "00"]:
                print(f"\n{G}[✔] Goodbye! 👋\n")
                sys.exit(0)
            elif choice in actions:
                actions[choice]()
                print(f"\n{C}[Press Enter to continue...]{W}", end="")
                input()
            else:
                print(f"{R}[✘] Invalid option!")
                time.sleep(1)


if __name__ == "__main__":
    tool = WebhookTool()
    tool.menu()