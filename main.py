import logging
import sys
from typing import Final
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ============================================================
# SETTINGS & CONFIGURATION
# ============================================================

TOKEN: Final[str] = "8926073785:AAEM-BIWs-xrZGNXXawCTRf0Yeok8-JmGFE"
GEMINI_API_KEY: Final[str] = "AQ.Ab8RN6KngHonQ68ua1CX5Z5BRe_03oqb5Tt-5JUjjMCS1234qw"
AI_MODEL: Final[str] = "gemini-3.8-flash"

ADMIN_USERNAME: Final[str] = "@rasha_kalary06"
ADMIN_URL: Final[str] = "https://t.me/rasha_kalary06"

# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("RashaBot")

# ============================================================
# INITIALIZE GEMINI AI
# ============================================================

ai_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PERSONA = """
تۆ یاریدەدەرێکی زیرەکی دەستکردی پێشکەوتووی تایبەت بە فرۆشگای @rasha_kalary06 ـیت.
دەتوانیت وەڵامی هەموو پرسیارێکی بەکارهێنەر بدەیتەوە لە هەموو بوارەکاندا و بە هەر زمانێک کە بەکارهێنەر قسەی پێبکات (کوردی، ئینگلیزی، عەرەبی، فارسی، هتد).
هەروەها زانیاری ئەم کاڵایانەی خوارەوەشت پێلەسەرە بۆ فرۆشتن:
- Smart Watch: $35 (شاشەی ڕوون، پاتری 7 ڕۆژ، دژەئاو نییە بۆ مەلە)
- Earbuds: $25 (دەنگی بەرز، ANC هەیە، کەیسەکەی خلیسکێنە)
- Powerbank 20000mAh: $30 (شەحنی خێرا PD، شاشەی پیشاندانی شەحن، کەمێک قورسە)
- Bluetooth Speaker: $20 (دەنگی بەهێز، دژەئاو، پاتری 10 کاتژمێر)

بۆ کڕینی کاڵاکان یان داواکارییەکان، بەکارهێنەر ڕێنمایی بکە بۆ پەیوەندیکردن بە خاوەنکار لە ڕێگەی @rasha_kalary06.
لە هەموو بارودۆخێکدا بە زمانی خۆی بەکارهێنەر وەڵام بدەرەوە و هاوکاربە.
"""

# ============================================================
# CATALOG DATABASE
# ============================================================

CATALOG = {
    "item_watch": {
        "title": "⌚ Smart Watch",
        "content": (
            "<b>⌚ سەعاتی زیرەک (Smart Watch)</b>\n\n"
            "💵 نرخ: <b>$35</b>\n\n"
            "🟢 <b>تایبەتمەندییەکان:</b>\n"
            "• ڕێنیشاندەری تەندروستی\n"
            "• ڕوونمایەکی زۆر ڕوون\n"
            "• پاتری تا 7 ڕۆژ دەبڕێت\n\n"
            "🔴 <b>خراپییەکەشی:</b>\n"
            "• بۆ مەلەکردن دژەئاو نییە\n\n"
            f"📩 بۆ داواکردن: {ADMIN_USERNAME}"
        ),
    },
    "item_buds": {
        "title": "🎧 Earbuds",
        "content": (
            "<b>🎧 سماڵی بێوەڵد (Earbuds)</b>\n\n"
            "💵 نرخ: <b>$25</b>\n\n"
            "🟢 <b>تایبەتمەندییەکان:</b>\n"
            "• کوالێتی دەنگی بەرز و پوخت\n"
            "• سیستەمی ANC بۆ بڕینی دەنگی دەرەوە\n\n"
            "🔴 <b>خراپییەکەشی:</b>\n"
            "• کەیسەکەی لووسە و زوو لە دەست دەخلیسکێت\n\n"
            f"📩 بۆ داواکردن: {ADMIN_USERNAME}"
        ),
    },
    "item_power": {
        "title": "🔋 Powerbank 20000mAh",
        "content": (
            "<b>🔋 پاوەربانکی 20 هەزاری</b>\n\n"
            "💵 نرخ: <b>$30</b>\n\n"
            "🟢 <b>تایبەتمەندییەکان:</b>\n"
            "• پشتگیری شەحنی خێرا PD\n"
            "• شاشەی ژمارەیی بۆ پیشاندانی ڕێژەی شەحن\n\n"
            "🔴 <b>خراپییەکەشی:</b>\n"
            "• قەبارەکەی کەمێک قورسە\n\n"
            f"📩 بۆ داواکردن: {ADMIN_USERNAME}"
        ),
    },
    "item_speaker": {
        "title": "🔊 Bluetooth Speaker",
        "content": (
            "<b>🔊 سپیکەری بلوتوس</b>\n\n"
            "💵 نرخ: <b>$20</b>\n\n"
            "🟢 <b>تایبەتمەندییەکان:</b>\n"
            "• دەنگی زۆر بەهێز و پڕ\n"
            "• دژەئاوە\n"
            "• بەرگەگرتنی پاتری تا 10 کاتژمێر\n\n"
            "🔴 <b>خراپییەکەشی:</b>\n"
            "• بەرزکردنەوەی فۆلیۆم بۆ کۆتا ئاست کاریگەری لەسەر بیس هەبێت\n\n"
            f"📩 بۆ داواکردن: {ADMIN_USERNAME}"
        ),
    },
}

# ============================================================
# KEYBOARD GENERATORS (INLINE MENU)
# ============================================================

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⌚ Smart Watch ($35)", callback_data="item_watch")],
        [InlineKeyboardButton("🎧 Earbuds ($25)", callback_data="item_buds")],
        [InlineKeyboardButton("🔋 Powerbank ($30)", callback_data="item_power")],
        [InlineKeyboardButton("🔊 Speaker ($20)", callback_data="item_speaker")],
        [InlineKeyboardButton("🌐 پەیوەندی کردن بە خاوەنکار", url=ADMIN_URL)],
    ])

def get_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 داواکردنی ئەم کاڵایە", url=ADMIN_URL)],
        [InlineKeyboardButton("🔙 گەڕانەوە بۆ لیست", callback_data="nav_home")],
    ])

# ============================================================
# AI ENGINE (GEMINI)
# ============================================================

def process_ai_query(user_query: str) -> str:
    try:
        full_prompt = f"{SYSTEM_PERSONA}\n\nپرسیاری بەکارهێنەر: {user_query}"
        response = ai_client.models.generate_content(
            model=AI_MODEL,
            contents=full_prompt,
        )
        if response and response.text:
            return response.text.strip()
    except Exception as err:
        log.error(f"Gemini AI Error: {err}")
    return "ببوورە لە ئێستادا کێشەیەک لە سێرڤەردا هەیە، تکایە ڕاستەوخۆ پەیوەندی بکە بە @rasha_kalary06"

# ============================================================
# BOT COMMANDS & EVENT HANDLERS
# ============================================================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    
    greeting = (
        "<b>سڵاو و ڕێز! 👋</b>\n\n"
        f"بەخێربێیت بۆ بۆتی فەرمی <b>{ADMIN_USERNAME}</b> 🤖\n\n"
        "دەتوانیت لە خوارەوە کاڵاکان هەڵبژێریت یان هەر پرسیارێک یان داواکارییەکت لە هەر بوارێک و بە هەر زمانێک هەبێت ڕاستەوخۆ بۆم بنووسە:"
    )
    
    await update.message.reply_text(
        text=greeting,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
    )

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    
    await query.answer()
    data = query.data

    if data == "nav_home":
        await query.message.edit_text(
            text="📦 <b>لیستی بەردەستم:</b>\nتكایە کاڵایەک هەڵبژێرە بۆ بینینی وردەکاری:",
            reply_markup=get_main_menu(),
            parse_mode="HTML",
        )
        return

    product = CATALOG.get(data)
    if product:
        await query.message.edit_text(
            text=product["content"],
            reply_markup=get_back_menu(),
            parse_mode="HTML",
        )

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text.strip()
    if not user_text:
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    ai_response = process_ai_query(user_text)
    await update.message.reply_text(ai_response)

# ============================================================
# MAIN APPLICATION LAUNCHER
# ============================================================

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(handle_callbacks, pattern=r"^(item_|nav_)"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    log.info("System initializing with Gemini 3.8 Flash & Interactive Inline Menu...")
    
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
