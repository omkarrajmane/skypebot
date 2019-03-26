from microsoftbotframework import MsBot
from start import Start

bot = MsBot()
start_obj = Start()
bot.add_process(start_obj.process_message)

if __name__ == '__main__':
    bot.run()
