def get_bot_input_text(bot):
    @bot.message_handler(func=lambda message: True, content_types=['text'], chat_types=['private'])
    def command(m):
        cid = m.chat.id
        mid = m.message_id
        bot.delete_message(cid, mid)

