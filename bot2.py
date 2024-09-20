import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://uchar:Lalaku007@cluster0.qpkevc2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
BOT_TOKEN = '7927679229:AAGc-6c0s1LZRd6F_QMlFA47UPND3rvjVpY'
ADMIN_ID = 6414918275

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = MongoClient(MONGODB_URI)
db = client['kiber_xavfsizlik_bot']
users_collection = db['users']

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔒 Premium Kurslar", callback_data='premium_courses')],
        [InlineKeyboardButton("ℹ️ Bot Haqida", callback_data='about')],
        [InlineKeyboardButton("💬 Admin bilan Aloqa", callback_data='contact_admin')],
        [InlineKeyboardButton("⭐️ Premiumga Ulanish", callback_data='get_premium')]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('🛡️ Asosiy menu bo\'limni tanlang! 🚀', reply_markup=get_main_menu_keyboard())

async def edit_message_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup: InlineKeyboardMarkup) -> None:
    query = update.callback_query
    try:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error editing message: {e}")
        await query.answer("Xatolik yuz berdi. Iltimos, /start buyrug'ini yuboring.")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'premium_courses':
        user = users_collection.find_one({"user_id": query.from_user.id})
        if user and user.get("is_premium"):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🕵️ Xakerlik Asoslari", callback_data='course_hacking')],
                [InlineKeyboardButton("📚 50-100 GB Kurslar", callback_data='course_network')],
                [InlineKeyboardButton("🔍 Penetration Testing", callback_data='course_pentest')],
                [InlineKeyboardButton("📱 Dasturlash kurslari Mega", callback_data='course_pro')],
                [InlineKeyboardButton("◀️ Orqaga", callback_data='back_to_menu')]
            ])
            await edit_message_text(update, context, "🔒 Premium Kurslar:", keyboard)
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⭐️ Premiumga Ulanish", callback_data='get_premium')],
                [InlineKeyboardButton("◀️ Orqaga", callback_data='back_to_menu')]
            ])
            await edit_message_text(update, context, "Siz hali premium foydalanuvchi emassiz. Premium kurslardan foydalanish uchun obuna bo'ling.", keyboard)
    
    elif query.data == 'free_lessons':
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 @Alltekin Tg kanali", callback_data='lesson_internet')],
            [InlineKeyboardButton("◀️ Orqaga", callback_data='back_to_menu')]
        ])
        await edit_message_text(update, context, "📘 Bepul Darslar:", keyboard)
    
    elif query.data == 'about':
        about_text = "🚀 E'tibor bering! 💰\n\n" \
                     "Bir martalik to'lov bilan millionlab pullik kurslarni qo'lga kiritishingiz mumkin! 🔥 \n\n" \
                     "✅ Kurslar ro'yxati: \n\n" \
                     "Hacking kurslari (500-800 $) 🕵️‍♂️\n"\
                     "Black Hat kurslar (100-500 GB) 💻\n"\
                     "Android RATlar dasturlash 📱\n"\
                     "Frond-end va Back-end dasturlash 🌐\n"\
                     "Udemy dan 200 GB lik mega kurslar 📚\n\n"\
                     "Kurslar ingliz tilida bo'lib, premium hisobga ega bo'lsangiz, to'liq foydalana olasiz! 🎓"\
                     "\n Agar qandaydir muammo yuzaga kelsa, Menudan admin bilan aloqani bosib, admin bilan bog'laning! 📩 \n"\
                     "🔑 Bu imkoniyatni qo'ldan boy bermang! ✨"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data='back_to_menu')]])
        await edit_message_text(update, context, about_text, keyboard)
    
    elif query.data == 'contact_admin':
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data='back_to_menu')]])
        await edit_message_text(update, context, "Admin bilan bog'lanish uchun @Sezdiz ga murojaat qiling.", keyboard)
    
    elif query.data == 'get_premium':
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 UzCard/Humo", callback_data='pay_uzcard')],
            [InlineKeyboardButton("◀️ Orqaga", callback_data='back_to_menu')]
        ])
        await edit_message_text(update, context, "⭐️ Premium obuna bo'lish uchun to'lov usulini tanlang:", keyboard)
    
    elif query.data in ['pay_uzcard', 'pay_crypto']:
        payment_info = "UzCard/Humo: `9860126602196910`" if query.data == 'pay_uzcard' else "BTC: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh\nETH: 0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data='get_premium')]])
        await edit_message_text(
    update,
    context,
    text=(
        f"{payment_info}\n\n"
        "👤 Ism: Pulatov A\n"
        "💰 Meblag: 30 ming so'm\n\n"
        "✅ To'lovni amalga oshirgach, chekni yuboring.\n\n"
        "⏳ To'lov 10 daqiqada tasdiqlanadi, aks holda admin bilan bog'laning! 📞"
    ),
    reply_markup=keyboard
)

    elif query.data.startswith('course_') or query.data.startswith('lesson_'):
        content = {
            'course_hacking': "🕵️ 'https://t.me/+nBif-rtOln5lZWVi'",
            'course_network': "🛡️ 'https://t.me/+nBif-rtOln5lZWVi'",
            'course_pentest': "🔍 'https://t.me/+nBif-rtOln5lZWVi'",
            'course_pro': "🔍 'https://t.me/+NECjG8nBdUg3NjAy' preium channel",
            'lesson_passwords': "' https://t.me/+nBif-rtOln5lZWVi'",
            'lesson_mobile': "📱 Mobil Qurilmalar Himoyasi darsi haqida ma'lumot...",
            'lesson_internet': "🌐 Internet Xavfsizligi darsi haqida ma'lumot..."
        }
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data='premium_courses' if query.data.startswith('course_') else 'free_lessons')]])
        await edit_message_text(update, context, content.get(query.data, "Ma'lumot topilmadi."), keyboard)
    
    elif query.data == 'back_to_menu':
        await edit_message_text(update, context, '🛡️ Kiber Xavfsizlik Darslariga Xush Kelibsiz! 🚀', get_main_menu_keyboard())

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    
    await update.message.reply_text("Iltimos kuting, to'lov tekshirilmoqda... ⏳")
    
    admin_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user_id}")],
        [InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}")]
    ])
    
    admin_id = int(ADMIN_ID)
    await context.bot.send_photo(
        chat_id=admin_id,
        photo=update.message.photo[-1].file_id,
        caption=f"Foydalanuvchi: @{username}\nID: {user_id}\nPremium ulanish uchun so'rov",
        reply_markup=admin_keyboard
    )

async def handle_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:
        action, user_id = query.data.split('_')
        user_id = int(user_id)
    except ValueError:
        logger.error(f"Invalid callback data: {query.data}")
        await query.edit_message_text("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        return

    try:
        if action == 'approve':
            users_collection.update_one({"user_id": user_id}, {"$set": {"is_premium": True}}, upsert=True)
            
            await context.bot.send_message(
                chat_id=user_id,
                text="🎉 Tabriklaymiz! Sizning premium obunangiz tasdiqlandi. Endi siz premium kurslardan foydalana olasiz.",
                reply_markup=get_main_menu_keyboard()
            )
            await query.edit_message_text(text=f"✅ Foydalanuvchi {user_id} uchun premium obuna tasdiqlandi.")
            
            # Send confirmation to admin
            admin_id = int(ADMIN_ID)
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"✅ Foydalanuvchi {user_id} uchun premium obuna muvaffaqiyatli tasdiqlandi."
            )
        
        elif action == 'reject':
            await context.bot.send_message(
                chat_id=user_id,
                text="😔 Afsuski, sizning to'lovingiz rad etildi. Iltimos, to'lov ma'lumotlarini tekshirib, qaytadan urinib ko'ring.",
                reply_markup=get_main_menu_keyboard()
            )
            await query.edit_message_text(text=f"❌ Foydalanuvchi {user_id} uchun premium obuna rad etildi.")
    
    except Exception as e:
        logger.error(f"Error in handle_admin_action: {e}")
        await query.edit_message_text("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^(?!approve_|reject_)'))  # Handles all callbacks except approve/reject
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CallbackQueryHandler(handle_admin_action, pattern='^(approve|reject)_'))

    application.run_polling()

if __name__ == '__main__':
    main()