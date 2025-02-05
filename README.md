
# Python-Telegram-Bot
A simple Python Telegram AI chatbot using the [python-telegram-bot] that provides various features and functionalities. This bot allows users to interact with a Telegram bot and perform various tasks, such as **user registration**, **chat history tracking**, **web searches**, and more. 
## Features

- User Registration
- Web searches
- AI chatting
- PDF summariser
- Image analysis
- Chat history


## Required Installation

- Install python latest version, Telegram bot API, generativeai and mongodb.

```bash
  pip install pyTelegramBotAPI google-generativeai pymongo

```
- Create Telegram Bot using Botfather and the token from your Telegram Bot API.

- Sign up in Google Gemini API and get the API key (token) from it.

- Install MongoDB or you can use web version of mongodb if you don't want localhost. Get the MongoDB URI.


## Setup Instructions

- Setup your MongoDB, so it can connect with your program and store data from Telegram bot. Make sure your database name, username and password credential should match, so remember it.

- Once you install all the requirements, then put all your API's and URI in the main file.

- Now, setup is ready you can run it locally or deploy it.


## Run Locally

To run tests, run the following command

```bash
  python bot.py
```


## Usage
Once the bot is running, you can interact with it directly in Telegram. The bot will respond based on the commands and the features you’ve implemented. You can summarise or analyse an image, pdf or file. 




