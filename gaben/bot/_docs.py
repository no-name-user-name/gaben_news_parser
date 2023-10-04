def get_bot_input_docs(bot):
    @bot.message_handler(content_types=['photo'])
    def photo(m):
        cid = m.from_user.id
        mid = m.message_id 
        bot.delete_message(cid, mid)
