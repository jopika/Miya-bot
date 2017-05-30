import bot.handler as handler


async def invalidCommand(message):
    """Default function that runs if user attempts to run an invalid command"""
    await client.send_message(message.channel, "Invalid command, use !help for list of commands")


### !help - prints the commands that are useable to the public
async def help(message):
    await client.send_message(message.author, "-----------------------\n!help - gives you this message \n !listRoles "
                                              "- gives you the list of roles \n !addRole [roles]    - adds the space "
                                              "separated roles to the user (if allowed) \n !removeRole [roles] - "
                                              "removes the space separated roles to the user (if allowed) \n !purge - "
                                              "cleans bot messages\n-----------------------------------")


async def unauthorizedCommand(message):
    await client.send_message(message.channel, "You are not authorized to use this command!")


# !listRoles - lists the roles
async def listRoles(message):
    if authorized(message.author.id, 'listRoles'):
        server = message.server
        serverRoles = server.roles
        listOfRoles = []
        for role in serverRoles:
            listOfRoles.append(str(role))
        listOfRoles = filter_roles(listOfRoles)
        messageString = ""
        for role in filter_roles(listOfRoles):
            messageString += str(role)
            messageString += " "
        await client.send_message(message.channel, messageString)
    else:
        unauthorizedCommand(message)


# !addRole [listOfRoles] - adds the role(s) to the user
async def addRole(message):
    if authorized(message.author.id, 'addRole'):
        role_list = get_roles_in_message(message)
        for role in message.server.roles[1:]:
            if str(role).lower() in role_list:
                if DEBUG:
                    print("User: ", message.author, " has added role: ", role)
                await client.add_roles(message.author, role)
        await client.send_message(message.channel, "done!")
    else:
        unauthorizedCommand(message)


# !removeRole [listOfRoles] - remove the role(s) to the user
async def removeRole(message):
    if authorized(message.author.id, 'removeRole'):
        role_list = get_roles_in_message(message)
        for role in message.server.roles[1:]:
            if str(role).lower() in role_list:
                if DEBUG:
                    print("User: ", message.author, " has removed role: ", role)
                await client.remove_roles(message.author, role)
        await client.send_message(message.channel, "done!")
    else:
        unauthorizedCommand(message)

# !purge - clears the last few messages sent by the bot
async def purge(message):
    if authorized(message.author.id, 'purge'):
        await client.purge_from(message.channel, limit=100, check=is_me)
    else:
        unauthorizedCommand(message)

# *admin* !nuke [x=50] - clears out the last x messages (default is 50)
async def nuke(message):
    if authorized(message.author.id, 'nuke'):
        command_params = message.content.split()[1:]
        count = 50
        if len(command_params) == 1:
            count = int(command_params[0])
        await client.purge_from(message.channel, limit=count)
    else:
        unauthorizedCommand(message)

# *owner* !quit - shutdown the bot gracefully
async def quit(message):
    if is_owner(message.author.id):
        if DEBUG:
            await client.send_message(message.channel, "Shutting down")
        await client.close()
    else:
        if DEBUG:
            await client.send_message(message.channel, "Not authorized to use this command!")


# *admin* !allowCommand [function_name] - allows the function to be run by users
async def allowCommand(message):
    if authorized(message.author.id, 'allowFunction'):
        command = message.content.split()[1]
        if whitelist_commands:
            if command in func_dict.keys() and command not in commandList:
                commandList.append(command)
                handler.update_config()
        else:
            if command in func_dict.keys() and command in commandList:
                commandList.remove(command)
                handler.update_config()
    else:
        unauthorizedCommand(message)

########## Function Dictionary ##########
func_dict = {
    'help': help,
    'listRoles': listRoles,
    'addRole': addRole,
    'removeRole': removeRole,
    'allowCommand': allowCommand,
    'purge': purge,
    'nuke': nuke,
    'quit': quit}


########## HELPER FUNCTIONS ##########

def is_me(message):
    return message.author == client.user


# TODO: Restructure this
def get_roles_in_message(message):
    """Retrieves the list of roles in a message, delimited by spaces"""
    theList = list(map(str.lower, message.content.split()[1:]))
    return filter_roles(theList)


def filter_roles(list_of_roles):
    """Filters the list_of_roles to keep only the valid server roles (by using the blacklist/whitelist)
    Consumes a list of strings and outputs a list a strings"""
    cleanedList = []
    for role in list_of_roles:
        if not (whitelist_roles ^ bool(role.lower() in roleList)):
            cleanedList.append(role)
    return cleanedList


def authorized(user_id, command_name):
    return user_id == owner_id or (user_id in adminList) or not (
        whitelist_commands ^ bool(command_name in commandList))


def is_owner(user_id):
    """Checks if the user is the bot's owner"""
    return user_id == owner_id


def init():
    global client
    global DEBUG
    global owner_id
    global adminList
    global whitelist_roles
    global whitelist_commands
    global roleList
    global commandList
    client = handler.client
    DEBUG = handler.DEBUG
    owner_id = handler.owner_id
    adminList = handler.adminList
    whitelist_roles = handler.whitelist_roles
    whitelist_commands = handler.whitelist_commands
    roleList = handler.roleList
    commandList = handler.commandList
