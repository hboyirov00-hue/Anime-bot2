from aiogram import Bot, Dispatcher, executor, types

# === Sozlamalar ===
API_TOKEN = "8321369455:AAHmMSD0H_W57_aBKqk7RsTrNxcUgmXlAT4"
CHANNEL_ID = "@Anime_lar_New"  # <-- Kanal username
OWNER_ID = 6627829267  # <-- Bu o'zing ID'ing

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# === PHOTO ID olish ===
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message):
    await message.reply(f"🖼 Rasm file_id:\n<code>{message.photo[-1].file_id}</code>", parse_mode="HTML")

# === /sendpost komandasi ===
@dp.message_handler(commands=["sendpost"])
async def send_post(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.reply("⛔ Sizda bu buyruqni bajarish huquqi yo'q.")
        return

    # Rasm file_id
    photo_file_id = "AgACAgIAAxkBAAPbaQx9SpkhKcV3icEgh1-5Zt-BlKIAAqoMaxu0mGlI2tzlx_M4pgUBAAMCAAN5AAM2BA"

    # Post caption
    caption = (
        "*Yolg'izlikda Daraja Ko'tarish Fasl-2*\n\n"
        "╭──────────────\n"
        "├‣ Holati: Tugallangan\n"
        "├‣ Sifat: 720p\n"
        "├‣ Janr: Fantastika, Ekshin\n"
        # "├‣ Kanal: @Anime_lar_New\n"
        "├‣ Qism: 13\n"
        "╰──────────────\n\n"
        "👇 Pastdagi tugmani bosing 👇"
    )

    # Tugma
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="▶️ Tomosha qilish",
            url="https://t.me/New_Anime_lar_Bot?start=solo_leveling-fasl2"
        )
    )

    try:
        # Rasm + caption bilan kanalga post yuborish
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo_file_id,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        await message.reply("✅ Post kanalga muvaffaqiyatli yuborildi!")
    except Exception as e:
        await message.reply(f"⚠️ Xatolik yuz berdi:\n`{e}`", parse_mode="Markdown")

# === Botni ishga tushurish ===
if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)

# python "D:/anime_Bot/channel_post_sender.py"