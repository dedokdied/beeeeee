from telegram.ext import Application, MessageHandler, filters
import subprocess
import re

def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

async def get_model_response(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:1b", prompt],  
            capture_output=True,
            text=True,
            encoding="utf-8" 
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0: 
            return f"Не удалось получить ответ от модели. Ошибка: {result.stderr.strip()}"


        response = clean_ansi(result.stdout.strip())
        if not response:
            return "Извините, я не смог сгенерировать ответ. Попробуйте другой запрос."

        return response
    except Exception as e:
        return f"Произошла ошибка при обработке запроса: {str(e)}"

async def handle_message(update, context):
    user_input = update.message.text  
    bot_response = await get_model_response(user_input)  

    if bot_response.strip():
        max_length = 4096
        for i in range(0, len(bot_response), max_length):
            chunk = bot_response[i:i + max_length]
            await update.message.reply_text(chunk) 
    else:
        await update.message.reply_text("Извините, я не смог сгенерировать ответ. Попробуйте другой запрос.")

def main():
    application = Application.builder().token("7597191272:AAGeni2mTRmCEI6raqzucWMfBYvPNggcn9w").build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот успешно запущен!")

    application.run_polling()

if __name__ == "__main__":
    main()