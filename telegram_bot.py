# export HF_TOKEN="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"
# Add this token 
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
token = '8476940849:AAHriD7wBYe2mssZdc1F0xJFV1UBXC77itM'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your Telegram bot.')

# /ask command handler
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Please provide a question after /ask.')
        return
    user_input = ' '.join(context.args)
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ["HF_TOKEN"],
        )
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324:fireworks-ai",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )
        reply = completion.choices[0].message.content if hasattr(completion.choices[0].message, 'content') else str(completion.choices[0].message)
    except Exception as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('ask', ask))
    print('Bot is running...')
    app.run_polling()
