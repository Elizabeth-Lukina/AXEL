<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=FF69B4&height=200&section=header&text=AXIOM%20Project&fontSize=48&fontColor=ffffff" width="100%" />
</p>

<p align="center"> Axiom is a smart personal assistant Telegram bot that helps you stay organized.
It manages your to-do list and sends you a personalized morning digest at your chosen time — including weather, currency rates, inspirational quotes, and more.
Designed to think ahead, speak your language, and evolve with you.</p>

## About AXIOM
- 🌤 Daily weather, 💱 exchange rates, and 🧠 thought of the day
- ⏰ Smart scheduled reports
- ✍️ Task management with NLP (understands "Buy milk tomorrow")
- 🧵 Voice support, AI replies, feedback system
- 📊 Custom user analytics
- 🎯 Future goals: voice interaction, smart home control, full JARVIS prototype

## Roadmap

- [x] Telegram Bot MVP
- [x] Daily reports (weather, quote, currency)
- [ ] 🧠 NLP-powered task parsing
- [ ] 🗣 Voice-to-text command support
- [ ] 📈 Advanced analytics on task completion
- [ ] 🏠 Smart Home integration
- [ ] 🤖 Fine-tune AI for personal responses (like mini GPT)


## Tech Stack
- 🐍 Python 3.10+  
- 🤖 Telebot (pyTelegramBotAPI)  
- 🗃 PostgreSQL  
- 📅 APScheduler  
- 📈 Matplotlib / Pandas  
- 🔐 python-dotenv  
- 🌦 Weather API: OpenWeatherMap  
- 💱 Currency: exchangerate.host  
- 🧠 NLP: dateparser / nltk  

## 🛤 Future Plans
- ✅ Add /addtask and /done to manage tasks in chat
- 🔄 Google Calendar sync
- 💬 Inline buttons for task management
- 🌐 Deploy to cloud with webhook support


## ⚙️ Installation

### 🖥️ On Windows (CMD / PowerShell)

python -m venv venv   
.\venv\Scripts\activate  
pip install -r requirements.txt  
copy .env.example .env  
notepad .env   
python bot.py  

### 🐧 On Linux / macOS (bash)
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
cp .env.example .env  
nano .env   
python3 bot.py

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=FF69B4&height=120&section=footer" width="100%" />
</p>