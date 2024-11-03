from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from Gemini import gpt
from texts import help, welcome
import requestsDB as rq
import keyboard as kb
from DatabaseFacade import DatabaseFacade
from notification_service import NotificationService, UserObserver

router = Router()
db_facade = DatabaseFacade()
notification_service = NotificationService()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await db_facade.set_user(message.from_user.id)
    user_observer = UserObserver(message.from_user.id, message.bot) 
    notification_service.subscribe(user_observer)
    await message.answer(welcome, reply_markup=kb.reply_kb)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(help, reply_markup=kb.reply_kb)

@router.message(Command('history'))
async def cmd_get_history(message: Message):
    history = await db_facade.get_history(message.from_user.id)
    await message.reply(history, reply_markup=kb.reply_kb)

@router.message(Command('del_history'))
async def cmd_del_history(message: Message):
    del_history = await db_facade.delete_history(message.from_user.id)
    await message.reply(del_history, reply_markup=kb.reply_kb)
    await notification_service.notify(f"History has been deleted for user {message.from_user.id}.")  

@router.message(F.text)
async def cmd_default(message: Message):
    history = await db_facade.get_history(message.from_user.id)
    response = await gpt(message.text, history)
    await message.reply(response)
    await db_facade.save_history(message.from_user.id, f'{message.text}\n{response}')


# @router.callback_query(F.data == 'help')
# async def call_help(callback: CallbackQuery):
#     await callback.message.reply(help, reply_markup=kb.reply_kb)
#
#
# @router.callback_query(F.data == 'history')
# async def call_history(callback: CallbackQuery):
#     history = await rq.get_history(callback.message.from_user.id)
#     await callback.message.reply(history, reply_markup=kb.reply_kb)
#
#
# @router.callback_query(F.data == 'del_history')
# async def call_del_history(callback: CallbackQuery):
#     del_history = await rq.delete_history(callback.message.from_user.id)
#     await callback.message.reply(del_history, reply_markup=kb.reply_kb)

@router.message(F.text == 'Help❔️')
async def cmd_answer(message: Message):
    await message.answer(help, reply_markup=kb.reply_kb)


@router.message(F.text == 'My History🗒️')
async def cmd_answer(message: Message):
    history = await rq.get_history(message.from_user.id)
    await message.reply(history, reply_markup=kb.reply_kb)


@router.message(F.text == 'Delete my history 🗑️')
async def cmd_answer(message: Message):
    del_history = await rq.delete_history(message.from_user.id)
    await message.reply(del_history, reply_markup=kb.reply_kb)


@router.message(F.text)
async def cmd_answer(message: Message):
    history = await rq.get_history(message.from_user.id)
    response = await gpt(message.text, history)
    await message.reply(response)
    await rq.save_history(message.from_user.id, f'{message.text}\n{response}')
