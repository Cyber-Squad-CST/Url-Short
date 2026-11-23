import json
import os
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

import pyshorteners

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False


HISTORY_FILE = "shortened_urls_history.json"


# --- Color & UI Helpers ---
def c(text, color_name):
    if not HAS_COLORAMA:
        return text
    colors = {
        "cyan": Fore.CYAN + Style.BRIGHT,
        "green": Fore.GREEN + Style.BRIGHT,
        "yellow": Fore.YELLOW + Style.BRIGHT,
        "red": Fore.RED + Style.BRIGHT,
        "magenta": Fore.MAGENTA + Style.BRIGHT,
        "blue": Fore.BLUE + Style.BRIGHT,
        "white": Fore.WHITE + Style.BRIGHT,
        "reset": Style.RESET_ALL,
    }
    return f"{colors.get(color_name, '')}{text}{Style.RESET_ALL}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_block_banner(banner_color="cyan", author_tag="INTERACTIVE CLI URL SHORTENER & CUSTOMIZER"):
    """Displays the solid ASCII block art banner"""
    clear_screen()
    ascii_block_art = r"""
  ██╗   ██╗██████╗ ██╗         ███████╗██╗  ██╗ ██████╗ ██████╗ ████████╗
  ██║   ██║██╔══██╗██║         ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚══██╔══╝
  ██║   ██║██████╔╝██║         ███████╗███████║██║   ██║██████╔╝   ██║   
  ██║   ██║██╔══██╗██║         ╚════██║██╔══██║██║   ██║██╔══██╗   ██║   
  ╚██████╔╝██║  ██║███████╗    ███████║██║  ██║╚██████╔╝██║  ██║   ██║   
   ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
    """
    print(c(ascii_block_art, banner_color))
    print(c("  ╔══════════════════════════════════════════════════════════════════════╗", "blue"))
    print(c(f"  ║  ⚡ {author_tag:<64} ║", "magenta"))
    print(c("  ╚══════════════════════════════════════════════════════════════════════╝", "blue"))


def processing_step(message, steps=3, delay=0.22):
    """Displays step-by-step block progress animation during processing"""
    sys.stdout.write(c(f"  [PROCESS] {message} ", "yellow"))
    sys.stdout.flush()
    for _ in range(steps):
        time.sleep(delay)
        sys.stdout.write(c("█", "cyan"))
        sys.stdout.flush()
    print(c(" [DONE]", "green"))


def is_valid_url(url):
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def save_to_history(record):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    history = data
        except Exception:
            history = []

    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def view_history():
    print(c("\n  📜 Saved Short URL History (Last 10 Entries):", "cyan"))
    if not os.path.exists(HISTORY_FILE):
        print(c("  [!] No history saved yet.", "yellow"))
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception as e:
        print(c(f"  [!] Failed to read history: {e}", "red"))
        return

    if not history:
        print(c("  [!] History is currently empty.", "yellow"))
        return

    for idx, item in enumerate(history[-10:], start=1):
        print(c(f"  {idx}. [{item.get('custom_name', 'Untitled')}]", "green"))
        print(f"     Service : {item.get('service', 'N/A')}")
        print(f"     Short   : {c(item.get('short_url', ''), 'cyan')}")
        print(f"     Long    : {item.get('long_url', '')}")
        print(f"     Time    : {item.get('timestamp', '')}")


def shorten_single_url(shortener, service, long_url, custom_name="My Link"):
    print()
    processing_step("Validating URL format", steps=3, delay=0.18)
    if not is_valid_url(long_url):
        if not long_url.startswith(("http://", "https://")):
            long_url = "https://" + long_url
        if not is_valid_url(long_url):
            print(c("  [ERROR] Invalid URL provided! (Include http:// or https://)", "red"))
            return None

    processing_step(f"Connecting to {service.upper()} server", steps=4, delay=0.2)
    processing_step("Generating and verifying short URL", steps=4, delay=0.2)

    try:
        if service == "tinyurl":
            short_url = shortener.tinyurl.short(long_url)
        elif service == "isgd":
            short_url = shortener.isgd.short(long_url)
        elif service == "dagd":
            short_url = shortener.dagd.short(long_url)
        else:
            short_url = shortener.tinyurl.short(long_url)

        record = {
            "custom_name": custom_name.strip() or "Unnamed Link",
            "service": service,
            "long_url": long_url,
            "short_url": short_url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_to_history(record)

        print(c("\n  ╔══════════════════════════════════════════════════════════════════════╗", "green"))
        print(c("  ║                  ✨ SHORT URL GENERATED SUCCESSFULLY! ✨              ║", "green"))
        print(c("  ╚══════════════════════════════════════════════════════════════════════╝", "green"))
        print(f"  🏷️  Custom Name : {c(record['custom_name'], 'magenta')}")
        print(f"  🌐 Service     : {c(service.upper(), 'yellow')}")
        print(f"  🔗 Short URL   : {c(short_url, 'cyan')}")
        print(f"  📄 Long URL    : {long_url}")
        print(f"  🕒 Timestamp   : {record['timestamp']}")
        return record

    except Exception as e:
        print(c(f"\n  [ERROR] Failed to shorten URL: {e}", "red"))
        return None


def choose_service():
    print(c("\n  Select Shortener Service:", "yellow"))
    print("   [1] TinyURL (Default & Fast)")
    print("   [2] is.gd")
    print("   [3] da.gd")
    choice = input(c("  Enter choice (1-3, default 1): ", "cyan")).strip()

    mapping = {
        "1": "tinyurl",
        "2": "isgd",
        "3": "dagd",
        "": "tinyurl",
    }
    return mapping.get(choice, "tinyurl")


def choose_banner_color():
    print(c("\n  Select Banner Theme Color:", "yellow"))
    print("   [1] Cyan (Default)")
    print("   [2] Green")
    print("   [3] Magenta")
    print("   [4] Yellow")
    choice = input(c("  Enter color number (1-4): ", "cyan")).strip()
    colors = {
        "1": "cyan",
        "2": "green",
        "3": "magenta",
        "4": "yellow",
    }
    return colors.get(choice, "cyan")


def main():
    shortener = pyshorteners.Shortener()
    default_service = "tinyurl"
    default_prefix = "CustomLink"
    banner_color = "cyan"
    author_tag = "INTERACTIVE CLI URL SHORTENER & CUSTOMIZER"

    while True:
        print_block_banner(banner_color=banner_color, author_tag=author_tag)
        print(f"  Service: {c(default_service.upper(), 'yellow')} | Default Label: {c(default_prefix, 'magenta')} | Theme: {c(banner_color.upper(), banner_color)}")
        print(c("  ────────────────────────────────────────────────────────────────────────", "blue"))
        print("  [1] Shorten Single URL (with Custom Name)")
        print("  [2] Shorten Multiple URLs (Batch Mode)")
        print("  [3] Customization Settings (Banner Tag, Color, Service)")
        print("  [4] View Saved History")
        print("  [0] Exit Program")
        print(c("  ────────────────────────────────────────────────────────────────────────", "blue"))

        mode = input(c("  Select Mode: ", "cyan")).strip()

        if mode == "1":
            long_url = input(c("\n  Enter Long URL: ", "white")).strip()
            custom_name = input(c(f"  Enter Custom Name for this link [Default: {default_prefix}]: ", "white")).strip()
            if not custom_name:
                custom_name = default_prefix

            service = choose_service()
            shorten_single_url(shortener, service, long_url, custom_name)
            input(c("\n  Press Enter to return to main menu...", "yellow"))

        elif mode == "2":
            print(c("\n  Enter multiple URLs (type 'DONE' and press Enter when finished):", "white"))
            urls = []
            while True:
                u = input(c("  URL > ", "cyan")).strip()
                if u.upper() == "DONE":
                    break
                if u:
                    urls.append(u)

            if not urls:
                print(c("  [!] No URLs entered.", "yellow"))
            else:
                batch_tag = input(c(f"  Enter Batch Custom Name [Default: {default_prefix}]: ", "white")).strip() or default_prefix
                service = choose_service()
                print(c(f"\n  Starting batch processing for {len(urls)} URL(s)...", "yellow"))
                for i, u in enumerate(urls, start=1):
                    print(c(f"\n  --- Item #{i} ---", "blue"))
                    shorten_single_url(shortener, service, u, f"{batch_tag} #{i}")

            input(c("\n  Press Enter to return to main menu...", "yellow"))

        elif mode == "3":
            print(c("\n  ⚙️  Customization Settings:", "yellow"))
            new_tag = input(c("  Enter new banner tagline (leave blank to keep current): ", "white")).strip()
            if new_tag:
                author_tag = new_tag[:64]

            new_prefix = input(c(f"  Enter new default custom name (current: {default_prefix}): ", "white")).strip()
            if new_prefix:
                default_prefix = new_prefix

            banner_color = choose_banner_color()
            default_service = choose_service()
            print(c("  [✔] All customizations saved!", "green"))
            time.sleep(1)

        elif mode == "4":
            view_history()
            input(c("\n  Press Enter to return to main menu...", "yellow"))

        elif mode == "0":
            print(c("\n  Thank you! Exiting tool... 👋", "green"))
            break

        else:
            print(c("  [!] Invalid option! Please enter a valid number.", "red"))
            time.sleep(1)


if __name__ == "__main__":
    main()
