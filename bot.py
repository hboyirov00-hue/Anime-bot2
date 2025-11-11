from aiogram import Bot, Dispatcher, types, executor
import json
from dotenv import load_dotenv
import os

# === Konfiguratsiya ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # .env fayldan token olinadi

# Bir nechta kanallarni shu ro‘yxatga yozamiz
CHANNELS = [ "@Doramalar_Ozbek_Tilida_Kanal"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Rasm yoki video file_id olish ---
@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def get_media_file_id(message: types.Message):
    if message.photo:
        photo = message.photo[-1]
        await message.reply(
            f"🖼 <b>Photo file_id:</b>\n<code>{photo.file_id}</code>",
            parse_mode="HTML"
        )
    elif message.video:
        await message.reply(
            f"🎞 <b>Video file_id:</b>\n<code>{message.video.file_id}</code>",
            parse_mode="HTML"
        )

# === JSON'dan ANIME ma'lumotlarini yuklash ===
with open("data/animes.json", "r", encoding="utf-8") as file:
    ANIMES = json.load(file)



# === Obuna tekshirish funksiyasi (bir nechta kanal uchun) ===
async def check_subscriptions(user_id):
    """Foydalanuvchi barcha kanallarga obuna bo‘lganligini tekshiradi"""
    result = []
    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status in ["member", "administrator", "creator"]:
                result.append(True)
            else:
                result.append(False)
        except:
            result.append(False)
    return all(result)  # faqat hammasiga obuna bo‘lsa True qaytaradi

# === /start handler ===
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    # === Obuna tekshirish ===
    if not await check_subscriptions(user_id):
        markup = types.InlineKeyboardMarkup()
        # Har bir kanal uchun tugma qo‘shamiz
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton(
                f"🔗 {ch.strip('@')} kanaliga obuna bo‘lish",
                url=f"https://t.me/{ch.strip('@')}"
            ))
        markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_subs"))
        await message.answer("❗️ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
        return

    # === Agar obuna bo‘lgan bo‘lsa ===
    if args in ANIMES:
        anime = ANIMES[args]
        if "photo" in anime:
            await bot.send_photo(message.chat.id, anime["photo"], caption=f"📺 {anime['title']}")
        await message.answer(f"📺 *{anime['title']}* qismlari:", parse_mode="Markdown")
        for part in anime["parts"]:
            if isinstance(part, dict):
                video_id = part.get("video")
                desc = part.get("description", "")
                await bot.send_video(message.chat.id, video=video_id, caption=desc)
            else:
                await bot.send_video(message.chat.id, video=part)
    else:
        await message.answer(
            "👋 Xush kelibsiz!\nAnime ko‘rish uchun kanal postidagi tugmani bosing yoki to‘g‘ri kod yuboring."
        )

# === Tekshirish tugmasi uchun handler ===
@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def check_subs_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if await check_subscriptions(user_id):
        await callback_query.message.edit_text("✅ Siz barcha kanallarga obuna bo‘lgansiz! Endi botdan foydalanishingiz mumkin.")
    else:
        await callback_query.answer("❗️ Hali barcha kanallarga obuna bo‘lmagansiz!", show_alert=True)

# === Botni ishga tushurish ===
if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)


    # python "D:/anime_Bot/bot.py"


#     git add .
# git commit -m "add new animes"
# git push
