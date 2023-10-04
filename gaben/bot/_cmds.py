from config import admins


def get_bot_input_cmd(bot):
    @bot.message_handler(commands=['start'], chat_types=['private'])
    def command(m):
        cid = m.from_user.id

        if cid in admins:
            pass
            # bot_menu.main(cid)















