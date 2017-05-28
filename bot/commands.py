import discord
import bot.handler


### !help - prints the commands that are useable to the public
async def help(message):
    await client.send_message(message.author, "-----------------------\n!help - gives you this message \n !listRoles "
                                              "- gives you the list of roles \n !addRole [roles]    - adds the space "
                                              "separated roles to the user (if allowed) \n !removeRole [roles] - "
                                              "removes the space separated roles to the user (if allowed) \n !purge - "
                                              "cleans bot messages\n-----------------------------------")


async def invalidCommand(message):
    """Default function that runs if user attempts to run an invalid command"""
    await client.send_message(message.channel, "Invalid command, use !help for list of commands")


# !listRoles - lists the roles
async def listRoles(message):
    server = message.server
    messageString = ""
    for role in server.roles[1:]:
        messageString += str(role)
        messageString += " "
    await client.send_message(message.channel, messageString)


# !addRole [listOfRoles] - adds the role(s) to the user
async def addRole(message):
    roleList = get_roles_in_message(message)
    for role in message.server.roles[1:]:
        if str(role).lower() in roleList:
            if DEBUG:
                print("User: ", message.author, " has added role: ", role)
            await client.add_roles(message.author, role)
    await client.send_message(message.channel, "done!")


# !removeRole [listOfRoles] - remove the role(s) to the user
async def removeRole(message):
    roleList = get_roles_in_message(message)
    for role in message.server.roles[1:]:
        if str(role).lower() in roleList:
            if DEBUG:
                print("User: ", message.author, " has removed role: ", role)
            await client.remove_roles(message.author, role)
    await client.send_message(message.channel, "done!")


# !purge - clears the last few messages sent by the bot
async def purge(message):
    await client.purge_from(message.channel, limit=100, check=is_me)


# *admin* !nuke [x=50] - clears out the last x messages (default is 50)
async def nuke(message):
    if authorized(message.author.id):
        command_params = message.content.split()[1:]
        count = 50
        if len(command_params) == 1:
            count = int(command_params[0])
        await client.purge_from(message.channel, limit=count)


# *admin* !quit - shutdown the bot gracefully
async def quit(message):
    if authorized(message.author.id):
        if DEBUG:
            await client.send_message(message.channel, "Shutting down")
        await client.close()
    else:
        if DEBUG:
            await client.send_message(message.channel, "Not authorized to use this command!")


# *admin* !allowFunction [function_name] - allows the function to be run by users
async def allowFunction(message):
    if authorized(message.author.id):
        pass
    else:
        pass


########## Function Dictionary ##########

func_dict = {
    'help': help,
    'addRole': addRole,
    'listRoles': listRoles,
    'removeRole': removeRole,
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
    """Filters the list_of_roles to keep only the valid server roles (by using the blacklist/whitelist"""
    cleanedList = []
    for role in list_of_roles:
        if not (whitelist_roles ^ bool(role in roleList)):
            cleanedList.append(role)
    return cleanedList


# TODO: Make this to check if the command is blacklisted or not as well
# TODO: Make an "admin list" and check if that is authorized correctly
def authorized(user_id):
    return user_id == owner_id


def is_owner(user_id):
    """Checks if the user is the bot's owner"""
    return user_id == owner_id

def init():
    global client
    global DEBUG
    global owner_id
    global whitelist_roles
    global roleList
    global commandList
    client = bot.handler.client
    DEBUG = bot.handler.DEBUG
    owner_id = bot.handler.owner_id
    whitelist_roles = bot.handler.whitelist_roles
    roleList = bot.handler.roleList
    commandList = bot.handler.commandList
