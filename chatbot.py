import os
import json
import datetime
import urllib.request
import urllib.error

# ─────────────────────────────────────────────
#  COLOR CODES FOR TERMINAL
# ─────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"
    DIM     = "\033[2m"

# ─────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────
def print_banner():
    banner = f"""
{Color.CYAN}{Color.BOLD}
  ╔══════════════════════════════════════════╗
  ║        🤖  AI COMPANION CHATBOT  🤖      ║
  ║     Your personal AI friend — always     ║
  ║         here to chat with you!           ║
  ╚══════════════════════════════════════════╝
{Color.RESET}"""
    print(banner)

# ─────────────────────────────────────────────
#  MOOD DETECTOR
# ─────────────────────────────────────────────
def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["sad", "unhappy", "crying", "depressed", "upset", "hurt"]):
        return "😢 sad"
    elif any(w in text for w in ["happy", "great", "awesome", "amazing", "excited", "good"]):
        return "😄 happy"
    elif any(w in text for w in ["angry", "frustrated", "annoyed", "mad", "hate"]):
        return "😠 angry"
    elif any(w in text for w in ["scared", "afraid", "nervous", "anxious", "worried"]):
        return "😰 anxious"
    elif any(w in text for w in ["bored", "boring", "nothing to do"]):
        return "😑 bored"
    else:
        return "🙂 neutral"

# ─────────────────────────────────────────────
#  SAVE CHAT HISTORY
# ─────────────────────────────────────────────
def save_history(history, filename="chat_history.json"):
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)
    print(f"{Color.DIM}  💾 Chat saved to {filename}{Color.RESET}")

# ─────────────────────────────────────────────
#  LOAD CHAT HISTORY
# ─────────────────────────────────────────────
def load_history(filename="chat_history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# ─────────────────────────────────────────────
#  CALL CLAUDE API
# ─────────────────────────────────────────────
def ask_claude(messages, api_key):
    url = "https://api.anthropic.com/v1/messages"
    
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 500,
        "system": (
            "You are a friendly, fun, and supportive AI companion. "
            "You talk in a casual, warm, and engaging way. "
            "Keep responses short and conversational (2-4 sentences). "
            "You remember the conversation context and refer back to it naturally."
        ),
        "messages": messages
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return f"[API Error {e.code}]: {error_body}"
    except Exception as e:
        return f"[Error]: {str(e)}"

# ─────────────────────────────────────────────
#  MAIN CHAT LOOP
# ─────────────────────────────────────────────
def main():
    print_banner()

    # Get API Key
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print(f"{Color.YELLOW}  🔑 Enter your Anthropic API Key:{Color.RESET} ", end="")
        api_key = input().strip()
        if not api_key:
            print(f"{Color.RED}  ❌ No API key provided. Exiting.{Color.RESET}")
            return

    # Ask to load previous chat
    history_msgs = []
    saved = load_history()
    if saved:
        print(f"\n{Color.YELLOW}  📂 Found previous chat history ({len(saved)} messages).{Color.RESET}")
        print(f"  Load it? {Color.BOLD}(y/n){Color.RESET}: ", end="")
        choice = input().strip().lower()
        if choice == "y":
            history_msgs = saved
            print(f"{Color.GREEN}  ✅ Previous chat loaded!{Color.RESET}")

    # Bot name
    bot_name = "Nova"
    user_name = ""
    print(f"\n{Color.CYAN}  👤 What should I call you?{Color.RESET} ", end="")
    user_name = input().strip() or "Friend"

    print(f"\n{Color.GREEN}  Hey {user_name}! I'm {bot_name}, your AI companion. 😊")
    print(f"  Type {Color.BOLD}'quit'{Color.RESET}{Color.GREEN} to exit, {Color.BOLD}'save'{Color.RESET}{Color.GREEN} to save chat, {Color.BOLD}'clear'{Color.RESET}{Color.GREEN} to reset.{Color.RESET}\n")
    print(f"{Color.DIM}  {'─'*44}{Color.RESET}\n")

    while True:
        # User input
        print(f"{Color.BLUE}{Color.BOLD}  {user_name}:{Color.RESET} ", end="")
        user_input = input().strip()

        if not user_input:
            continue

        # Special commands
        if user_input.lower() == "quit":
            print(f"\n{Color.MAGENTA}  {bot_name}: Bye {user_name}! Come back soon 👋{Color.RESET}\n")
            save_choice = input(f"  💾 Save chat before exit? (y/n): ").strip().lower()
            if save_choice == "y":
                save_history(history_msgs)
            break

        if user_input.lower() == "save":
            save_history(history_msgs)
            continue

        if user_input.lower() == "clear":
            history_msgs = []
            print(f"{Color.YELLOW}  🗑️  Chat history cleared!{Color.RESET}\n")
            continue

        # Detect mood
        mood = detect_mood(user_input)
        timestamp = datetime.datetime.now().strftime("%H:%M")
        print(f"{Color.DIM}  [{timestamp}] Mood detected: {mood}{Color.RESET}")

        # Add to history and call API
        history_msgs.append({"role": "user", "content": user_input})
        
        print(f"{Color.DIM}  {bot_name} is thinking...{Color.RESET}")
        response = ask_claude(history_msgs, api_key)

        # Add bot response to history
        history_msgs.append({"role": "assistant", "content": response})

        # Print response
        print(f"\n{Color.MAGENTA}{Color.BOLD}  {bot_name}:{Color.RESET}{Color.WHITE} {response}{Color.RESET}\n")
        print(f"{Color.DIM}  {'─'*44}{Color.RESET}\n")

# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
