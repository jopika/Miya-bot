import bot.handler as handler
import bot.permissions as permissions


async def invalid_command(message):
    """Default function that runs if user attempts to run an invalid command"""
    await client.send_message(message.channel, "Invalid command, use !help for list of commands")


### !help - prints the commands that are useable to the public
async def help(message):
    await client.send_message(message.author, "-----------------------\n!help - gives you this message \n !listRoles "
                                              "- gives you the list of roles \n !addRole [roles]    - adds the space "
                                              "separated roles to the user (if allowed) \n !removeRole [roles] - "
                                              "removes the space separated roles to the user (if allowed) \n !purge - "
                                              "cleans bot messages\n-----------------------------------")


async def unauthorized_command(message):
    await client.send_message(message.channel, "You are not authorized to use this command!")


async def no_permissions_command(message):
    await client.send_message(message.channel, "Bot does not have permissions! Contact Server Admin")


# !listRoles - lists the roles
async def list_roles(message):
    if authorized(message.author.id, 'listroles'):
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
        unauthorized_command(message)


# !addRole [listOfRoles] - adds the role(s) to the user
async def add_role(message, user='', roles=''):
    if not has_permissions(message, permissions.MANAGE_ROLES):
        no_permissions_command(message)
    if authorized(message.author.id, 'addrole'):
        await role_modify(message, 'add')


# !remove_role [listOfRoles] - remove the role(s) to the user
async def remove_role(message, user='', roles=''):
    if not has_permissions(message, permissions.MANAGE_ROLES):
        no_permissions_command(message)
    if authorized(message.author.id, 'removerole'):
        await role_modify(message, 'del')


async def role_modify(message, action, user='', roles=[]):
    user_obj = ''
    role_string_list = ''
    if user!='' and roles!='':
        user_obj = user
        role_string_list = roles
    else:
        user_obj = message.author
        role_string_list = get_roles_in_message(message)
    if action.lower() == 'add':
        role_string_list = diff(role_string_list, list(map(lambda x: str(x).lower(), user_obj.roles)))
    else:
        role_string_list = siml(role_string_list, list(map(lambda x: str(x).lower(), user_obj.roles)))
    role_list = retrieve_roles(message, role_string_list)
    if action.lower() == 'add':
        if DEBUG:
            print("User: ", user_obj, " has added roles: ", role_string_list)
        await client.add_roles(user_obj, *role_list)
    else:
        if DEBUG:
            print("User: ", user_obj, " has removed roles: ", role_string_list)
        await client.remove_roles(user_obj, *role_list)


# !purge - clears the last few messages sent by the bot
async def purge(message):
    if not has_permissions(message, permissions.MANAGE_MESSAGES):
        no_permissions_command(message)
    if authorized(message.author.id, 'purge'):
        await client.purge_from(message.channel, limit=100, check=is_me)
    else:
        unauthorized_command(message)


# *admin* !nuke [x=50] - clears out the last x messages (default is 50)
async def nuke(message):
    if not has_permissions(message, permissions.MANAGE_MESSAGES):
        no_permissions_command(message)
    if authorized(message.author.id, 'nuke'):
        command_params = message.content.split()[1:]
        count = 50
        if len(command_params) == 1:
            count = int(command_params[0])
        await client.purge_from(message.channel, limit=count)
    else:
        unauthorized_command(message)


# *owner* !quit - shutdown the bot gracefully
async def quit(message):
    if is_owner(message.author.id):
        if DEBUG:
            await client.send_message(message.channel, "Shutting down")
        await client.close()
    else:
        if DEBUG:
            await client.send_message(message.channel, "Not authorized to use this command!")


# *admin* !allowcommand [function_name] - allows the function to be run by users
async def allow_command(message):
    if authorized(message.author.id, 'allowcommand'):
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
        unauthorized_command(message)

# TODO: Complete this
async def testing_bank(message):
    passed_tests = 0
    failed_tests = 0
    if is_owner(message.author.id):
        owner_roles = message.author.roles


########## Function Dictionary ##########
func_dict = {
    'help': help,
    'listroles': list_roles,
    'addrole': add_role,
    'removerole': remove_role,
    'allowcommand': allow_command,
    'purge': purge,
    'nuke': nuke,
    'quit': quit}


########## HELPER FUNCTIONS ##########

def is_me(message):
    """Checks if the message was sent by the bot, returns true if yes"""
    return message.author == client.user


def has_permissions(message, action):
    """Checks if the bot has permissions to do a certain action, returns true if yes"""
    server = message.server
    channel = message.channel
    member_obj = server.get_member(client.user.id)
    return bool(channel.permissions_for(member_obj).value & int(action))


# TODO: Restructure this
def get_roles_in_message(message):
    """Retrieves the list of roles in a message, delimited by spaces"""
    theList = list(map(str.lower, message.content.split()[1:]))
    return filter_roles(theList)


def filter_roles(list_of_roles):
    """Filters a list of strings to keep only valid server roles

    Consumes a list of strings and keeps only the roles that are
    valid, in reference to the whitelist/blacklist.
    :parameter: list_of_roles - list of strings to filter
    :returns: list of strings
    """
    cleanedList = []
    for role in list_of_roles:
        if not (whitelist_roles ^ bool(role.lower() in roleList)):
            cleanedList.append(role)
    return cleanedList


def authorized(user_id, command_name):
    """Checks if the user is authorized to run the command, returns true if yes"""
    return user_id == owner_id or (user_id in adminList) or not (
        whitelist_commands ^ bool(command_name.lower() in commandList))


def is_owner(user_id):
    """Checks if the user is the bot's owner"""
    return user_id == owner_id


def diff(list_a, list_b):
    """Takes the difference between list_a and list_b

    :return = list_a - list_b
    """
    set_b = set(list_b)
    return [item for item in list_a if item not in set_b]

def siml(list_a, list_b):
    """Takes the similarities between list_a and list_b

    :return = list_a & list_b 
    """
    set_b = set(list_b)
    return [item for item in list_a if item in set_b]


def retrieve_roles(message, list_of_roles):
    """Returns a list of role objects that are associated with the list_of_roles

    :return a list of roles
    """
    server_roles = message.server.roles
    return [role for role in server_roles if str(role).lower() in list_of_roles]


########## INITIALIZER ##########


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