from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    ban_user_id: State = State()
    unban_user_id: State = State()


class MailingStates(StatesGroup):
    edit_text: State = State()
    edit_media: State = State()
    edit_button_text: State = State()
    edit_button_url: State = State()
    edit_schedule: State = State()


class ManageMailingsStates(StatesGroup):
    update_mailing_id: State = State()
    delete_mailing_id: State = State()
