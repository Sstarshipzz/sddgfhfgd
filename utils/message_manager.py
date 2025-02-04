from telegram import Update
from telegram.ext import ContextTypes

class MessageManager:
    def __init__(self, bot):
        self.bot = bot

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Message de bienvenue"""
        welcome_text = (
            "*👋 Bienvenue !*\n\n"
            "Je suis votre assistant shopping.\n"
            "Que souhaitez-vous faire ?"
        )
    
        if update.callback_query:
            await update.callback_query.message.edit_text(
                welcome_text,
                reply_markup=self.bot.keyboard_manager.get_start_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                welcome_text,
                reply_markup=self.bot.keyboard_manager.get_start_keyboard(),
                parse_mode='Markdown'
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les callbacks des messages"""
        query = update.callback_query
        await query.answer()

        if query.data == "show_catalog":
            await self.show_categories(update, context)
        elif query.data == "show_help":
            await self.show_help(update, context)

    async def show_product(self, update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: str):
        """Affiche un produit"""
        product = next(p for p in self.bot.catalog["products"] if p["id"] == product_id)
    
        message = (
            f"*{product['name']}*\n\n"
            f"{product['description']}\n\n"
            f"💰 Prix: {product['price']}"  # Le prix est affiché tel quel
        )

    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Affiche l'aide"""
        help_text = (
            "*❓ AIDE*\n\n"
            "Voici comment utiliser le bot :\n\n"
            "1️⃣ Utilisez /start pour afficher le menu principal\n"
            "2️⃣ Cliquez sur 📦 Catalogue pour voir les produits\n"
            "3️⃣ Pour toute question, contactez @votre_username"
        )
    
        if update.callback_query:
            await update.callback_query.message.edit_text(
                help_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Retour", callback_data="start")
                ]])
            )
        else:
            await update.message.reply_text(
                help_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Retour", callback_data="start")
                ]])
            )

    async def send_error(self, update: Update, message: str):
        """Envoie un message d'erreur"""
        if update.callback_query:
            await update.callback_query.message.reply_text(
                f"❌ {message}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"❌ {message}",
                parse_mode='Markdown'
            )

    async def send_success(self, update: Update, message: str):
        """Envoie un message de succès"""
        if update.callback_query:
            await update.callback_query.message.reply_text(
                f"✅ {message}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"✅ {message}",
                parse_mode='Markdown'
            )