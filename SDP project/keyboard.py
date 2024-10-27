from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создание клавиатуры с постоянными кнопками
reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Help❔️')],
        [KeyboardButton(text='My History🗒️'),
         KeyboardButton(text='Delete my history 🗑️')],
    ],
    resize_keyboard=True,
    input_field_placeholder="Menu:"
)

