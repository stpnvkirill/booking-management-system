from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.fsm.booking_states import BookingStates
from app.bot.keyboards import get_resource_type_keyboard

router = Router()


def get_booking_router():
    return router


@router.message(lambda m: m.text == "📅 Забронировать")
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingStates.resource_type)
    await message.answer(
        "Выберите тип ресурса:", reply_markup=get_resource_type_keyboard(),
    )
