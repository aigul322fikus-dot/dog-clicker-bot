import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# User data storage
user_data = {}

# Initialize user data
def init_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'clicks': 0,
            'level': 1,
            'per_click': 1,
            'total_earned': 0
        }

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id)
    
    message = """
🐕 **Добро пожаловать в Dog Clicker!**

Это игра про клик по собаке! Каждый клик приносит вам очки.

**Команды:**
/click - Кликнуть на собаку 🖱️
/stats - Посмотреть вашу статистику 📊
/upgrade - Улучшить награду за клик ⬆️
/help - Справка по командам 📖

Начните с команды /click!
"""
    await update.message.reply_text(message, parse_mode='Markdown')

# Click command
async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id)
    
    reward = user_data[user_id]['per_click']
    user_data[user_id]['clicks'] += reward
    user_data[user_id]['total_earned'] += reward
    
    # Level up every 100 clicks
    level = user_data[user_id]['clicks'] // 100 + 1
    user_data[user_id]['level'] = level
    
    emoji = ['🐕', '🐶', '🦮'][user_data[user_id]['level'] % 3]
    message = f"{emoji} **Клик!** +{reward}\n\nВсего очков: {user_data[user_id]['clicks']}"
    
    await update.message.reply_text(message, parse_mode='Markdown')

# Stats command
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id)
    
    data = user_data[user_id]
    message = f"""
📊 **Ваша статистика:**

💰 Очки: {data['clicks']}
📈 Уровень: {data['level']}
🎯 Награда за клик: {data['per_click']}
✅ Всего заработано: {data['total_earned']}
"""
    await update.message.reply_text(message, parse_mode='Markdown')

# Upgrade command
async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id)
    
    data = user_data[user_id]
    cost = 50 * data['level']
    
    if data['clicks'] >= cost:
        data['clicks'] -= cost
        data['per_click'] += 1
        message = f"✅ **Улучшение куплено!**\n\nНовая награда за клик: {data['per_click']}\nОставшиеся очки: {data['clicks']}"
    else:
        needed = cost - data['clicks']
        message = f"❌ **Недостаточно очков!**\n\nНужно: {cost}\nНе хватает: {needed}"
    
    await update.message.reply_text(message, parse_mode='Markdown')

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
📖 **Справка по командам:**

/start - Начать игру
/click - Кликнуть на собаку 🖱️
/stats - Посмотреть статистику 📊
/upgrade - Улучшить награду за клик (стоит 50 × уровень) ⬆️
/help - Показать эту справку

**Как играть:**
1. Используйте /click для клика по собаке
2. Зарабатывайте очки
3. Используйте /upgrade для улучшения награды
4. Достигайте новых уровней!
"""
    await update.message.reply_text(message, parse_mode='Markdown')

# Main function
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("click", click))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CommandHandler("help", help_command))
    
    print("🚀 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()