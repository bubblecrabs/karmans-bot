START_MESSAGE_KEY: str = "✋ <b>Hi</b>"
BANNED_MESSAGE_KEY: str = "🚫 <b>You have been blocked by the administrator.</b>"

MENU_MESSAGE_KEY: str = "⬇️ <b>What do you want to do?</b>"

STATS_MESSAGE_KEY: str = """📊 <b>Statistics:</b>

👥 <b>Number of users:</b> {total_users}
📈 <b>New users today:</b> {new_users_today}
🚫 <b>Blocked users:</b> {banned_users}

👤 <b>Last registered:</b> {last_user}
🕒 <b>Registration time:</b> {joined_at}"""

MANAGE_USERS_MESSAGE_KEY: str = "➡️ <b>Enter the Telegram user ID:</b>"
WRONG_ID_MESSAGE_KEY: str = "⁉️ <b>Incorrect Telegram user ID.</b>"
USER_BLOCKED_SUCCESS_KEY: str = "✅ <b>User {user_id} has been blocked.</b>"
USER_UNBLOCKED_SUCCESS_KEY: str = "✅ <b>User {user_id} has been unblocked.</b>"
USER_NOT_FOUND_KEY: str = "❌ <b>User {user_id} not found.</b>"
UNKNOWN_OPERATION_KEY: str = "❌ <b>Unknown operation.</b>"
