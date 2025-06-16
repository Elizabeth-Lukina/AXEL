# AXIOM 🤖

A smart personal assistant Telegram bot written in Python. It sends users a daily digest every morning at 07:30 Moscow time (MSK) including:


- 📋 Your to-do list for today
- Daily digest via APScheduler:
    - 🌤 Current weather in their chosen city
    - 💱 Currency rates (USD and EUR to RUB)
    - 🧠 A smart or funny quote of the day
- 📈 Analytics 

## 💡 Features

- Custom city selection per user

- PostgreSQL database: stores users, tasks, preferences
- Weather from OpenWeatherMap API
- Currency from exchangerate.host
- Quotes from zenquotes.io
- User-specific statistics and graphs


## 🧪 Available Commands
 | Command             | Description                                           |
|---------------------|-------------------------------------------------------|
| `/start`            | Register user and set default city                    |
| `/currency_history` | Show weekly chart of USD/EUR → RUB exchange rates     |
| `/my_stats`         | Analyze your to-do stats (total, completed, average)  |
| `/stats`            | Bot usage statistics (for debugging/demo)             |
| `/chart`            | Most queried cities (can be disabled later)           |


## 🛠 Tech Stack
- Python 3.10+
- Telebot (pyTelegramBotAPI)
- PostgreSQL
- APScheduler
- Matplotlib / Requests / Dotenv

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

### 👤 Author
Made with ❤️ by Elizabeth Lukina  
_“Always learning, always shipping.”_