import telebot
import google.generativeai as genai
import pymongo
import os
from telebot.types import Message, InputFile
import fitz
from googletrans import Translator
from PIL import Image
import io


# Load API Keys
TELEGRAM_BOT_TOKEN = "7383549657:AAE-rO1OhgMVoplcbmJ7yrXAyh8RVJOQg-U"
GEMINI_API_KEY = "AIzaSyALcBnSV_M4wbQOiXXuNY-uDMlCl4adqF4"
MONGO_URI = "mongodb://localhost:27017/"

# Initialize APIs
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
client = pymongo.MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_col = db["users"]

# initialize translator
translator = Translator()


# Register User
@bot.message_handler(commands=["start"])
def register_user(message: Message):
    user = {
        "first_name": message.from_user.first_name,
        "username": message.from_user.username,
        "chat_id": message.chat.id,
    }
    users_col.update_one({"chat_id": message.chat.id}, {"$set": user}, upsert=True)
    bot.send_message(
        message.chat.id, "Welcome! You can chat with me or send an image for analysis."
    )


# Gemini AI Chat
@bot.message_handler(func=lambda message: True, content_types=["text"])
def chat_with_gemini(message: Message):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(message.text)
    bot.send_message(message.chat.id, response.text)


# Image Analysis
@bot.message_handler(content_types=["photo"])
def analyze_image(message: Message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

    # Open the image using PIL
    image = Image.open(io.BytesIO(downloaded_file))

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Describe this image in detail."

    # Use the correct input format (PIL.Image.Image)
    response = model.generate_content([prompt, image]) 

    MAX_LENGTH = 4000  # Telegram message limit (slightly less than 4096)
    response_text = response.text
    # Send both text and image

    for i in range(0, len(response_text), MAX_LENGTH):
        bot.send_message(message.chat.id, response_text[i : i + MAX_LENGTH])

# Web Search
@bot.message_handler(commands=["search"])
def web_search(message: Message):
    query = message.text.replace("/search ", "")
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Search the web for: {query}")
    bot.send_message(message.chat.id, response.text)


# current date and time
import datetime
import pytz  #  convert to your desired time zone

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    # Get current date and time
    local_tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")

    # Get the user query
    query = message.text.lower()

    # Generate AI response (assuming 'genai' is your AI library)
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(query)

    # Send back the response along with current time
    bot.send_message(
        message.chat.id, f"Current time: {current_time}\n\n{response.text}"
    )


# Summarize PDF
@bot.message_handler(content_types=["document"])
def summarize_pdf(message: Message):
    if message.document.mime_type == "application/pdf":
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        # Save the PDF file locally
        with open("document.pdf", "wb") as f:
            f.write(downloaded_file)

        # Extract text from PDF
        doc = fitz.open("document.pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        # Summarize the text using Gemini AI
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"Summarize the following PDF content: {text}"
        )

        # Send summarized response back
        summary = response.text

        # Create a new PDF with the summary
        doc_summary = fitz.open()  # Create a new empty PDF
        page = doc_summary.new_page()  # Create a new page

        # Insert the summary text into the new page
        page.insert_text(
            (72, 72), summary, fontsize=12
        )  # Position the text at the top left (72, 72)

        # Save the summary as a new PDF
        doc_summary.save("summary.pdf")

        # Send the summarized PDF back to the user
        with open("summary.pdf", "rb") as f:
            bot.send_document(message.chat.id, f)
        os.remove("document.pdf")
        os.remove("summary.pdf")


# Auto Translation Feature
@bot.message_handler(commands=["translate"])
def translate_message(message: Message):
    # Extract the text after the /translate command
    text_to_translate = message.text.replace("/translate ", "")

    # Detect language and translate to English (or any other language)
    translated_text = translator.translate(text_to_translate, dest="en").text
    bot.send_message(message.chat.id, f"Translated: {translated_text}")


# Start bot
bot.polling()




# to start the bot type: python bot.py 