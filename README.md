# 🤖 AI Companion Chatbot

A personal AI chatbot that runs in your terminal

> Features

- Talks like a real friend
- Detects your mood from your messages
- Remembers the full conversation context
- Save your chats and continue later
- lean and beautiful interface

> How to Run

# Step 1 : Install dependencies
```bash
pip install -r requirements.txt
```

# Step 2 : Get your API Key
Get a free API key from: https://console.anthropic.com/

# Step 3 : Run the chatbot
```bash
python chatbot.py
```

Enter your API key when asked, and start chatting!

> Commands

 Command : What it does 
 `quit`  : Exit the chatbot 
 `save`  : Save chat history to file 
 `clear` : Clear conversation memory 

> Structure

```
AI-Companion-Chatbot/
│
├── chatbot.py          # Main chatbot file
├── requirements.txt    # Dependencies
├── chat_history.json   # Saved chats (auto-created)
└── README.md           # This file
```

> 🛠️ Built With

- Python 3.x
- A.I. API

> 📸 Preview

```
╔══════════════════════════════════════════╗
║        🤖  AI COMPANION CHATBOT  🤖     ║
║     Your personal AI friend : always     ║
║         here to chat with you!           ║
╚══════════════════════════════════════════╝

  👤 What should I call you? Vikash

  Hey Vikash! I'm Nova, your AI companion. 😊

  Vikash: I'm feeling bored today
  [14:32] Mood detected: 😑 bored
  Nova is thinking...

  Nova: Aw, bored days are the worst! Want me to
  tell you something interesting or maybe we can
  brainstorm something fun to do? 😄
```
