import os
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

GEMINI_API_KEY = "AQ.Ab8RN6JqBbJv_buodJvubLlvSty5dqCowUVrTN0pfqBiQGYBjQ"
TELEGRAM_TOKEN = "8722152372:AAFYT0Cszea6HbP3DRw5fmmvJX0mQuSDli8"

ai_client = genai.Client(api_key=GEMINI_API_KEY)

# پێناسەکردنی زانیاری ٨ بەرهەمەکە بۆ ژیری دەستکرد (AI)
MENU_CONTEXT = """
تۆ یارمەتیدەرێکی ژیری دەستکردی بۆ وەڵامدانەوەی بەکارهێنەران دەربارەی بەرهەمەکانی ئێمە.
تکایە بەپێی ئەم زانیارییانەی خوارەوە بە کوردی وەڵامی پرسیارەکان بدەرەوە:

بەرهەمەکان و نرخ و تایبەتمەندییەکان:

١. بەرهەمی ۱ (سەعاتی زیرەک / Smart Watch):
- نرخ: $25
- خاڵە باشەکان: شاشەی ڕوون، پێوانی لێدانی دڵ، پاتری ٥ ڕۆژ دەستێنێت.
- خاڵە خراپەکان: دژە ئاو نییە بۆ مەلەکردن.

٢. بەرهەمی ۲ (هێدفۆنی بێسیم / Wireless Earbuds):
- نرخ: $20
- خاڵە باشەکان: دەنگی بەهێز و باسی بەرز، لەرزینی کەم، پاتری باش.
- خاڵە خراپەکان: مایکی بۆ شوێنی زۆر دەنگەدەنگ مامناوەندە.

٣. بەرهەمی ۳ (پاوەربانک 20000mAh):
- نرخ: $30
- خاڵە باشەکان: شەحنی خێرا (Fast Charge)، توانای بەرز، بارگاوی کردنی دوو ئامێر بەیەکەوە.
- خاڵە خراپەکان: کەمێک قورسە لە دەستدا.

٤. بەرهەمی ٤ (سپیکەری بلوتوث):
- نرخ: $35
- خاڵە باشەکان: دەنگی زۆر بڵند، دژە ئاوە، ڕووناکی RGBی هەیە.
- خاڵە خراپەکان: قەبارەی کەمێک گەورەیە بۆ بەرهەمێکی گوازراوە.

٥. بەرهەمی ٥ (ماوسی گەیمینگ / Gaming Mouse):
- نرخ: $18
- خاڵە باشەکان: DPIی بەرز و قابل دەستکاری، دوگمەی زیادە، دیزاینی ئەرگۆنۆمی.
- خاڵە خراپەکان: تەنها بە وایەر کاردەکات.

٦. بەرهەمی ٦ (کیبۆردی میكانیكی / Mechanical Keyboard):
- نرخ: $45
- خاڵە باشەکان: دوگمەی خێرا و خۆش، ڕووناکی RGBی جۆراوجۆر، کوالێتی بەرز.
- خاڵە خراپەکان: دەنگی کەمێک بەرزە لە کاتی نووسیندا.

٧. بەرهەمی ٧ (کامێرای چاودێری زیرەک / Smart Cam):
- نرخ: $40
- خاڵە باشەکان: کوالێتی Full HD، بینینی شەوانە، پەیوەستبوون بە مۆبایل.
- خاڵە خراپەکان: پێویستی بە ئینتەرنێتی بەردەوام هەیە.

٨. بەرهەمی ٨ (شەحندەری خێرا 65W):
- نرخ: $15
- خاڵە باشەکان: زۆر خێرایە، گونجاوە بۆ مۆبایل و ئایپاد و لاپتۆپ، پارێزراوە لە گەرمبوون.
- خاڵە خراپەکان: تەنها یەک پۆرتی Type-C هەیە.

ڕێنمایی کڕین:
بۆ کڕین یان داواکردنی هەر کاڵایەک، ڕاستەوخۆ پەیام بۆ ئەم ئایدییە بنێرن: @rasha_kalary06
"""

# فەرمانی /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! بەخێر بێیت.\n"
        "دەتوانیت فەرمانی /menu بنووسیت یان وشەی 'مینۆ' بنێریت بۆ بینینی بەرهەمەکان.\n"
        "یان ڕاستەوخۆ هەر پرسیارێکت هەیە لێم بپرسە!"
    )

# دروستکردنی مینۆی ٨ بەرهەمەکە
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⌚ 1. سەعاتی زیرەک ($25)", callback_data='item_1'), InlineKeyboardButton("🎧 2. هێدفۆنی بێسیم ($20)", callback_data='item_2')],
        [InlineKeyboardButton("🔋 3. پاوەربانک ($30)", callback_data='item_3'), InlineKeyboardButton("🔊 4. سپیکەری بلوتوث ($35)", callback_data='item_4')],
        [InlineKeyboardButton("🖱️ 5. ماوسی گەیمینگ ($18)", callback_data='item_5'), InlineKeyboardButton("⌨️ 6. کیبۆردی میكانیكی ($45)", callback_data='item_6')],
        [InlineKeyboardButton("📹 7. کامێرای چاودێری ($40)", callback_data='item_7'), InlineKeyboardButton("⚡ 8. شەحندەری 65W ($15)", callback_data='item_8')],
        [InlineKeyboardButton("🛒 چۆنیەتی کڕین و داواکردن", callback_data='how_to_buy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text_msg = "تکایە بەشێک لە مینۆکە هەڵبژێرە بۆ بینینی نرخ و باشی و خراپی کاڵاکە:"
    if update.message:
        await update.message.reply_text(text_msg, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text_msg, reply_markup=reply_markup)

# وەڵامی کلیک کردنی دوگمەکان
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    details = {
        'item_1': "⌚ **١. سەعاتی زیرەک**\n💵 **نرخ:** $25\n✅ **باشی:** پێوانی لێدانی دڵ، پاتری ٥ ڕۆژ دەستێنێت.\n❌ **خراپی:** دژە ئاو نییە بۆ مەلەکردن.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_2': "🎧 **٢. هێدفۆنی بێسیم**\n💵 **نرخ:** $20\n✅ **باشی:** دەنگی بەهێز، لەرزینی کەم، پاتری باش.\n❌ **خراپی:** مایکی لە شوێنی زۆر دەنگەدەنگ مامناوەندە.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_3': "🔋 **٣. پاوەربانک 20000mAh**\n💵 **نرخ:** $30\n✅ **باشی:** شەحنی خێرا، بارگاوی کردنی دوو ئامێر بەیەکەوە.\n❌ **خراپی:** کەمێک قورسە.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_4': "🔊 **٤. سپیکەری بلوتوث**\n💵 **نرخ:** $35\n✅ **باشی:** دەنگی زۆر بڵند، دژە ئاوە، ڕووناکی RGB.\n❌ **خراپی:** قەبارەی کەمێک گەورەیە.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_5': "🖱️ **٥. ماوسی گەیمینگ**\n💵 **نرخ:** $18\n✅ **باشی:** DPIی بەرز، دوگمەی زیادە، دیزاینی ئەرگۆنۆمی.\n❌ **خراپی:** تەنها بە وایەر کاردەکات.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_6': "⌨️ **٦. کیبۆردی میكانیكی**\n💵 **نرخ:** $45\n✅ **باشی:** دوگمەی خێرا، ڕووناکی RGB، کوالێتی بەرز.\n❌ **خراپی:** دەنگی کەمێک بەرزە.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_7': "📹 **٧. کامێرای چاودێری زیرەک**\n💵 **نرخ:** $40\n✅ **باشی:** Full HD، بینینی شەوانە، بەستنەوە بە مۆبایل.\n❌ **خراپی:** پێویستی بە ئینتەرنێتی بەردەوام هەیە.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'item_8': "⚡ **٨. شەحندەری خێرا 65W**\n💵 **نرخ:** $15\n✅ **باشی:** زۆر خێرایە، گونجاوە بۆ لاپتۆپ و مۆبایل.\n❌ **خراپی:** تەنها یەک پۆرتی Cی هەیە.\n\n📩 بۆ کڕین پەیام بنێرە بۆ: @rasha_kalary06",
        'how_to_buy': "🛒 **چۆنیەتی کڕینی کاڵاکان:**\nبۆ داواکردن و کڕینی هەر بەرهەمێک، ڕاستەوخۆ نامە بنێرن بۆ خاوەنی بۆتەکە:\n👉 @rasha_kalary06"
    }

    text = details.get(query.data, "زانیاری نەدۆزرایەوە.")
    await query.edit_message_text(text=text, parse_mode='Markdown')

# وەڵامدانەوەی پرسیارەکان لە ڕێگەی Gemini AI
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text.lower() in ["مینۆ", "menu", "بەرهەمەکان"]:
        await show_menu(update, context)
        return

    try:
        prompt = f"{MENU_CONTEXT}\n\nپرسیاری بەکارهێنەر: {user_text}"
        
        interaction = ai_client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )
        await update.message.reply_text(interaction.output_text)
    except Exception as e:
        print(f"Error details: {e}")
        await update.message.reply_text("ببوورە، کێشەیەک ڕوویدا.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("بۆتی AI لەگەڵ ٨ بەرهەمەکە چالاک بوو...")
    app.run_polling()
