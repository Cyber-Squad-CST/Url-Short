# 🔗 URL SHORT — Interactive CLI URL Shortener & Customizer

**URL SHORT** is a sleek, interactive Command-Line Interface (CLI) tool built with Python that transforms long, cluttered URLs into clean, shareable short links. Designed with a bold **Solid ASCII Block Art** banner, real-time step-by-step block progress animations, multi-service support, and full UI customization, it brings a modern terminal experience to link management.

---

## ✨ Key Features

- **Solid ASCII Block Art Banner:** Crisp, dependency-free block-character header (`URL SHORT`) compatible with any terminal environment (Linux, Termux, Windows CMD/PowerShell, macOS).
- **Multiple Shortening Services:** Supports **TinyURL**, **is.gd**, and **da.gd** out of the box.
- **Interactive Modes:**
  - **Single URL Mode:** Shorten an individual URL and assign a custom label/name to it.
  - **Batch Mode:** Process and shorten multiple URLs in a single session with automatic numbering.
- **Step-by-Step Processing Animation:** Visualizes URL validation, server connection, and link generation with animated block progress bars (`█`).
- **Full CLI Customization:** Customize the banner tagline, switch between 4 vibrant terminal color themes (**Cyan**, **Green**, **Magenta**, **Yellow**), and set default preferences.
- **Persistent JSON History:** Automatically logs every shortened link with its custom name, service provider, original URL, and timestamp into `shortened_urls_history.json` for easy viewing anytime.

---

## 🛠️ Prerequisites & Installation

Ensure you have **Python 3.7+** installed on your system.

### 1. Clone or Download the Project
Save the script as `url_shortener_cli.py` in your working directory:
```bash
git clone https://github.com/Cyber-Squad-CST/Url-Short.git
cd Url-Short
```

### 2. Install Required Libraries
Install the required Python packages using `pip`:
```bash
pip install pyshorteners colorama
```

| Package | Purpose |
| :--- | :--- |
| `pyshorteners` | Core library used to communicate with URL shortening APIs (TinyURL, is.gd, da.gd). |
| `colorama` | Enables cross-platform colored terminal text and stylized CLI UI elements. |

---

## 🚀 Usage & How It Works

Run the script from your terminal:
```bash
python url_shortener_cli.py
```

### Workflow Overview
1. **Launch & Dashboard:** The application clears the terminal and displays the ASCII block banner along with your active default service, label, and color theme.
2. **Select a Mode:**
   - **`[1]` Shorten Single URL:** Paste your long URL (automatically prepends `https://` if omitted), give it a custom name, pick a service, and watch the live processing steps generate your short link.
   - **`[2]` Batch Mode:** Enter multiple URLs one by one, type `DONE`, and let the tool shorten all of them sequentially.
   - **`[3]` Customization Settings:** Personalize your banner subtitle, default custom label prefix, theme color, and default shortening engine.
   - **`[4]` View Saved History:** Inspect the last 10 shortened links stored locally in `shortened_urls_history.json`.
   - **`[0]` Exit Program:** Cleanly exits the CLI tool.

---

## 📂 Project Structure

```text
├── url_shortener_cli.py         # Main interactive CLI application
├── shortened_urls_history.json  # Auto-generated JSON log of shortened URLs
└── README.md                    # Project documentation
```

---

## 👨‍💻 Developer Information

- **Developer:** *[MD IMRAN HOSSEN / Handle]*
- **Role:** Python & CLI Tool Developer
- **GitHub:** *[https://github.com/Cyber-Squad-CST]*
- **Contact / Portfolio:** *[srimran122334@gmail.com]*

> *Built with passion for clean command-line utilities. Feel free to fork, customize, and contribute!*
