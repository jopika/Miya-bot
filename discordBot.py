import bot.handler as handler
import bot.commands as commands


######### DRIVER FUNCTIONS #########
@handler.client.event
async def on_ready():
    print("--------------------------------")
    print('Logged in:')
    print("Client Username: ", client.user.name)
    print("Client ID: ", client.user.id)
    print("Owner ID: ", handler.owner_id)
    print("Admin List: ", handler.adminList)
    if handler.whitelist_roles:
        print("Whitelisted Roles: ", handler.roleList)
    else:
        print("Blacklisted Roles: ", handler.roleList)
    if handler.whitelist_commands:
        print("Whitelisted Commands: ", handler.commandList)
    else:
        print("Blacklisted Commands", handler.commandList)
    print("--------------------------------")


@handler.client.event
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

    handler.init()
    commands.init()

    token = handler.token
    client = handler.client
    DEBUG = handler.DEBUG

    client.run(token)


if __name__ == '__main__':
    main()
