import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Set up the SQLite database
def setup_db():
    conn = sqlite3.connect('job_forms.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS forms
                 (job_role TEXT, form_link TEXT)''')
    conn.commit()
    conn.close()

# Function to add a job form
def add_form(job_role, form_link):
    conn = sqlite3.connect('job_forms.db')
    c = conn.cursor()
    c.execute("INSERT INTO forms (job_role, form_link) VALUES (?, ?)", (job_role, form_link))
    conn.commit()
    conn.close()

# Function to check if a form is filled
def is_form_filled(job_role, form_link):
    conn = sqlite3.connect('job_forms.db')
    c = conn.cursor()
    c.execute("SELECT * FROM forms WHERE job_role = ? AND form_link = ?", (job_role, form_link))
    result = c.fetchone()
    conn.close()
    return result is not None

# Command handler to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Please enter the job role and the form link.")

# Handler for new messages (job role + link)
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    try:
        job_role, form_link = text.split(' ', 1)  # Expecting the format: <job_role> <form_link>
        
        if is_form_filled(job_role, form_link):
            await update.message.reply_text(f"You have already filled the form for {job_role}.")
        else:
            add_form(job_role, form_link)
            await update.message.reply_text(f"Form for {job_role} has been saved successfully.")
    except ValueError:
        await update.message.reply_text("Please enter both job role and form link in the format: <job_role> <form_link>.")

def main():
    setup_db()  # Set up the database
    TOKEN = '7561680081:AAG5i9zRKqFxOLiIh-8qWFdN0dJJ0S2qtR0'  # Your provided bot API token

    # Create an Application instance
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
