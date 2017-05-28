import discord
import asyncio
from pathlib import Path
import yaml
import bot.handler
import bot.commands as commands


######### DRIVER FUNCTIONS #########
@bot.handler.client.event
async def on_ready():
    print("--------------------------------")
    print('Logged in:')
    print("Client Username: ", client.user.name)
    print("Client ID: ", client.user.id)
    if whitelist:
        print("Whitelist: ", roleList)
    else:
        print("Blacklist: ", roleList)
    print("--------------------------------")


@bot.handler.client.event
async def on_message(message):
    if DEBUG:
        print(message.author, ": ", message.content)
    if not message.author.bot and message.content.startswith('!'):
        command = message.content.split()[0][1:]
        await commands.func_dict.get(command, commands.invalidCommand)(message)


def main():
    global token
    global client
    global DEBUG
    global whitelist
    global roleList
    bot.handler.init()
    bot.commands.init()
    token = bot.handler.token
    client = bot.handler.client
    DEBUG = bot.handler.DEBUG
    whitelist = bot.handler.whitelist
    roleList = bot.handler.roleList

    client.run(token)


if __name__ == '__main__':
    main()
