from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Create new config", callback_data="new_config")],
        [InlineKeyboardButton(text="Manage configs", callback_data="manage_configs")],
    ]
)

protocols_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="AWG", callback_data="awg"),
            InlineKeyboardButton(text="XRay", callback_data="xray"),
        ],
    ]
)
