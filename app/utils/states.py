from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    block_user: State = State()
    unblock_user: State = State()
    add_premium_user: State = State()
    add_premium_tier: State = State()
    add_channel: State = State()


class MailingStates(StatesGroup):
    edit_text: State = State()
    edit_media: State = State()
    edit_button_text: State = State()
    edit_button_url: State = State()
    edit_schedule: State = State()


class ManageMailingsStates(StatesGroup):
    update_mailing_id: State = State()
    delete_mailing_id: State = State()
