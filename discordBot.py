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
    if whitelist_roles:
        print("Whitelisted Roles: ", roleList)
    else:
        print("Blacklisted Roles: ", roleList)
    if whitelist_commands:
        print("Whitelisted Commands: ", commandList)
    else:
        print("Blacklisted Commands", commandList)
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
    global whitelist_roles
    global roleList
    global whitelist_commands
    global commandList

    handler.init()
    commands.init()

    token = handler.token
    client = handler.client
    DEBUG = handler.DEBUG
    whitelist_roles = handler.whitelist_roles
    roleList = handler.roleList
    whitelist_commands = handler.whitelist_commands
    commandList = handler.commandList

    client.run(token)


if __name__ == '__main__':
    main()
