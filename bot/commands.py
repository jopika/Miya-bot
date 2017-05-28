import discord
import bot.handler

global client
global DEBUG
global admin_id


### !help - prints the commands that are useable to the public
async def help(message):
    await client.send_message(message.author, "-----------------------\n!help - gives you this message \n !listRoles "
                                              "- gives you the list of roles \n !addRole [roles]    - adds the space "
                                              "separated roles to the user (if allowed) \n !removeRole [roles] - "
                                              "removes the space separated roles to the user (if allowed) \n !purge - "
                                              "cleans bot messages\n-----------------------------------")


async def invalidCommand(message):
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
    roleList = get_roles(message)
    for role in message.server.roles[1:]:
        if str(role).lower() in roleList:
            if DEBUG:
                print("User: ", message.author, " has added role: ", role)
            await client.add_roles(message.author, role)
    await client.send_message(message.channel, "done!")


# !removeRole [listOfRoles] - remove the role(s) to the user
async def removeRole(message):
    roleList = get_roles(message)
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
    if message.author.id == admin_id:
        commandParams = message.content.split()[1:]
        count = 50
        if len(commandParams) == 1:
            count = int(commandParams[0])
        await client.purge_from(message.channel, limit=count)


# *admin* !quit - shutdown the bot gracefully
async def quit(message):
    if message.author.id == admin_id:
        if DEBUG:
            await client.send_message(message.channel, "Shutting down")
        await client.close()
    else:
        if DEBUG:
            await client.send_message(message.channel, "Not authorized to use this command!")


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
# TODO: Make this function
def get_roles(message):
    theList = list(map(str.lower, message.content.split()[1:]))
    cleanedList = []
    for role in theList:
        if not (whitelist ^ bool(role in roleList)):
            cleanedList.append(role)
    return cleanedList


def init():
    global client
    global DEBUG
    global admin_id
    global whitelist
    global roleList
    client = bot.handler.client
    DEBUG = bot.handler.DEBUG
    admin_id = bot.handler.admin_id
    whitelist = bot.handler.whitelist
    roleList = bot.handler.roleList
