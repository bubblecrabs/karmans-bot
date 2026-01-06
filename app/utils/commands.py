from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

user_commands: dict[str, dict[str, str]] = {
    "en": {
        "start": "Start the bot",
        "help": "Help & commands",
    },
    "ru": {
        "start": "Запустить бота",
        "help": "Помощь и команды",
    },
    "uk": {
        "start": "Запустити бота",
        "help": "Довідка і команди",
    },
}


async def setup_commands(bot: Bot) -> None:
    for language_code, commands in user_commands.items():
        await bot.set_my_commands(
            commands=[BotCommand(command=comm, description=desc) for comm, desc in commands.items()],
            scope=BotCommandScopeDefault(),
            language_code=language_code,
        )


async def delete_commands(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
