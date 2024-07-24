# Telegram Game Bot

A Telegram bot that provides users with information about games, allows adding new games, and sends out newsletters. This bot supports English and Russian languages and can be customized for your own needs.

## Features

- **User Registration**: Users are welcomed with a confirmation message and can interact with the bot after confirming.
- **Game Management**: Admins can add new games to the database, including details such as description, download link, and tags.
- **Game Discovery**: Users can discover games either randomly or by searching with tags.
- **Instructions**: Users can receive instructions on how to download games.
- **Contact Information**: Users can obtain contact details for technical or advertising inquiries.
- **Language Support**: The bot supports English and Russian languages.
- **System Selection**: Users can select their system (Android or Windows) to get appropriate game recommendations.
- **Admin Commands**: Admins can manage users, clear user data, check user status, and add news updates.

### Prerequisites

- Python 3.x
- Telegram Bot Token (get it from BotFather)
- SQLite3

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/justoperator/game-download-telegram-bot.git
    ```

2. **Install Dependencies**: Ensure you have the necessary Python packages installed. You can use pip to install them:
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Bot Token and Admin ID**:
    - Open `main.py` and replace `PASTE HERE YOUR API KEY` with your bot token.
    - Replace `PASTE HERE YOUR TELEGRAM ID` in the admins list with your own Telegram ID.

4. **Run the Bot**:
    ```bash
    python main.py
    ```

## Admin commands

- `/start` - Starts the bot and shows the welcome message.
- `/addgame` - Allows admins to add a new game.
- `/clearusers` - Clears the users table.
- `/list` - Shows user statistics.
- `/addnews` - Adds a news update.
- `/addnewsru` - Adds a news update in Russian.

## Configuration

- **Language Support**: The bot supports English and Russian. Users can change the language using the language menu.
- **System Selection**: Users must select their system to get appropriate game recommendations.
