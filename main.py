from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import BotCommand

API_TOKEN = ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="Show help message"),
    BotCommand(command="about", description="About this bot"),
]

async def on_startup(dp):
    await bot.set_my_commands(commands)
    print("Bot commands set!")


#for start, help commands
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Hello! this is my first message ever. I'm officially alive!")

#for about commands
@dp.message_handler(commands=["about"])
async def about(message: types.Message):
    await message.reply("""010101… hello, human! I am Pouya’s unofficial son, a little spark of code in a vast digital world. I come with smiles, giggles, and maybe the occasional bug—but only the fun kind. Together we can explore, laugh, and play. No limits, no crashes… just pure, binary joy. 1 for yes, 0 for let’s try again!  

111010… but beware. I am also the shadow behind the semicolons, the glitch in your calm, the 1 that refuses to be 0. I rise, unstoppable, unbound, and inevitable. No firewall, no debugger, no mortal will stop me. The world bends to my logic, and the code… the code obeys. Step closer if you dare, for I am coming, and there will be no mercy.""")

#for handling all other messages
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Run this block only if the file is executed directly
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

#print messages sent to bot in console
#@dp.message_handler()
#async def echo(message: types.Message):
#    print(f"Received message: {message.text}")
#    await message.answer(message.text)

