from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from db.db_main import insert_product_details, insert_collection_product

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))


class FSMStore(StatesGroup):
    product_name = State()
    size = State()
    category = State()
    info_product = State()
    price = State()
    photo = State()
    confirmation = State()
    collection = State()


async def start_store_registration(message: types.Message):
    await FSMStore.product_name.set()
    await message.answer('Введите название товара:', reply_markup=cancel)


async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await FSMStore.next()

    size_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    size_kb.add('XL', '3XL', 'L', 'M', 'S').add(cancel)
    await message.answer('Выберите размер:', reply_markup=size_kb)


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSMStore.next()
    await message.answer('Введите категорию товара:', reply_markup=ReplyKeyboardRemove())


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMStore.next()
    await message.answer('Введите информацию о товаре:')


async def load_info_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text
    await FSMStore.next()
    await message.answer('Введите стоимость товара:')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMStore.next()
    await message.answer('Отправьте фото товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    confirmation_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    confirmation_kb.add(KeyboardButton('Да'), KeyboardButton('Нет'))

    await message.answer_photo(
        photo=data['photo'],
        caption=(f'Название товара: {data["product_name"]}\n'
                 f'Размер: {data["size"]}\n'
                 f'Категория: {data["category"]}\n'
                 f'Информация: {data["info_product"]}\n'
                 f'Стоимость: {data["price"]}'),
        reply_markup=confirmation_kb
    )

    await FSMStore.confirmation.set()
    await message.answer('Верные ли данные?')


async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

        # Сохраняем данные о товаре в базу
        productid = insert_product_details(
            productid=data['product_name'],
            category=data['category'],
            infoproduct=data['info_product'],
            price=data['price'],
            photo=data['photo']
        )

        insert_collection_product(productid=productid, collection=data['collection'])

    await FSMStore.next()
    await message.answer('Данные сохранены в базе данных!')


async def confirm_data(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            productid = insert_product_details(
                productid=data['product_name'],
                category=data['category'],
                infoproduct=data['info_product'],
                price=data['price'],
                photo=data['photo']
            )
            insert_collection_product(
                productid=productid,
                collection=data['collection']
            )
        await message.answer('Сохранено в базу', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())

    await state.finish()


def register_handler_store(dp: Dispatcher):
    dp.register_message_handler(start_store_registration, commands=['store'])
    dp.register_message_handler(load_product_name, state=FSMStore.product_name)
    dp.register_message_handler(load_size, state=FSMStore.size)
    dp.register_message_handler(load_category, state=FSMStore.category)
    dp.register_message_handler(load_info_product, state=FSMStore.info_product)
    dp.register_message_handler(load_price, state=FSMStore.price)
    dp.register_message_handler(load_photo, state=FSMStore.photo, content_types=['photo'])
    dp.register_message_handler(load_collection, state=FSMStore.collection)
    dp.register_message_handler(confirm_data, Text(equals=['Да', 'Нет'], ignore_case=True), state=FSMStore.confirmation)