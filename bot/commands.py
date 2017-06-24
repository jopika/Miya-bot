import asyncio

import bot.handler as handler
import bot.permissions as permissions


async def invalid_command(message):
    """Default function that runs if user attempts to run an invalid command"""
    await client.send_message(message.channel, "Invalid command, use !help for list of commands")


async def help(message):
    """Prints the commands that are runnable by the user"""
    message_string = '---------------------------------------------------\n'
    for key in func_help.keys():
        if is_owner(message.author.id):
            message_string += "{Owner, "
        else:
            message_string += "{"
        if authorized(message, key):
            message_string += "Admin"
            if not (whitelist_commands ^ bool(key.lower() in commandList)):
                message_string += ", User"
            message_string += "}:        " + func_help[key] + "\n"
    message_string += "-----------------------------------------------------------\n"
    await client.send_message(message.author, message_string)


async def unauthorized_command(message):
    await client.send_message(message.channel, "You are not authorized to use this command!")


async def no_permissions_command(message, channel=''):
    if channel == '':
        the_channel = message.channel
    else:
        the_channel = channel
    await client.send_message(the_channel, "Bot does not have permissions! Contact Server Admin")


async def list_roles(message):
    """Lists the roles the user is allowed to add or remove from self"""
    if authorized(message, 'listroles'):
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
        await unauthorized_command(message)


async def add_role(message, user='', roles=[], channel=''):
    """Adds the role(s) to the given user"""
    if not has_permissions(message, permissions.MANAGE_ROLES, channel):
        await no_permissions_command(message, channel)
    if authorized(message, 'addrole', user):
        await role_modify(message, 'add', user, roles)


async def remove_role(message, user='', roles=[], channel=''):
    """Removes the role(s) from the given user"""
    if not has_permissions(message, permissions.MANAGE_ROLES, channel):
        await no_permissions_command(message, channel)
    if authorized(message, 'removerole', user):
        await role_modify(message, 'del', user, roles)


async def role_modify(message, action, user='', roles=[]):
    if user != '' and roles != []:
        user_obj = user
        role_string_list = filter_roles(roles)
    else:
        user_obj = message.author
        role_string_list = get_roles_in_message(message)
    if action.lower() == 'add':
        role_string_list = diff(role_string_list, list(map(lambda x: str(x).lower(), user_obj.roles)))
    else:
        role_string_list = siml(role_string_list, list(map(lambda x: str(x).lower(), user_obj.roles)))
    role_list = retrieve_roles(user_obj.server, role_string_list)
    if action.lower() == 'add':
        await client.add_roles(user_obj, *role_list)
        if DEBUG:
            print("User: ", user_obj, " has added roles: ", role_string_list, " Current roles: ",
                  list(map(lambda x: str(x), user_obj.roles)))
    else:
        await client.remove_roles(user_obj, *role_list)
        if DEBUG:
            print("User: ", user_obj, " has removed roles: ", role_string_list, " Current roles: ",
                  list(map(lambda x: str(x), user_obj.roles)))
    if user == '' and roles == []:
        if len(role_list) > 0:
            await client.send_message(message.channel, "Finished modifying roles of user: " + user_obj.mention)
        else:
            await client.send_message(message.channel, "Unable to modify any roles of user: " + user_obj.mention)


async def purge(message):
    """Clears recent bot messages from the channel"""
    if not has_permissions(message, permissions.MANAGE_MESSAGES):
        await no_permissions_command(message)
    if authorized(message, 'purge'):
        await client.purge_from(message.channel, limit=100, check=is_me)
    else:
        await unauthorized_command(message)


async def nuke(message):
    """Clears out the last x(=50) messages from the channel"""
    if not has_permissions(message, permissions.MANAGE_MESSAGES):
        await no_permissions_command(message)
    if authorized(message, 'nuke'):
        command_params = message.content.split()[1:]
        count = 50
        if len(command_params) == 1:
            count = int(command_params[0])
        await client.purge_from(message.channel, limit=count)
    else:
        await unauthorized_command(message)


async def quit(message):
    """Shuts down the bot gracefully"""
    if is_owner(message.author.id):
        if DEBUG:
            await client.send_message(message.channel, "Shutting down")
        await client.close()
    else:
        if DEBUG:
            await client.send_message(message.channel, "Not authorized to use this command!")


async def allow_command(message):
    """Allows the function to be run by users"""
    if authorized(message, 'allowcommand'):
        await modify_command_permissions(message, True)
    else:
        await unauthorized_command(message)


async def restrict_command(message):
    """Restricts the command to not be run by users"""
    if authorized(message, 'restrictcommand'):
        await modify_command_permissions(message, False)
    else:
        await unauthorized_command(message)


async def modify_command_permissions(message, allow=True):
    """Helper function to aide with allow_command and restrict_command"""
    command = message.content.split()[1]
    if (whitelist_commands and allow) or not whitelist_commands:
        if command in func_dict.keys() and command not in commandList:
            commandList.append(command)
            handler.update_config()
    else:
        if command in func_dict.keys() and command in commandList:
            commandList.remove(command)
            handler.update_config()


async def allow_role_modification(message):
    if not authorized(message, 'allowrolemodification'):
        await unauthorized_command(message)
    else:
        await modify_role_permissions(message, True)


async def restrict_role_modification(message):
    if not authorized(message, 'restrictrolemodification'):
        await unauthorized_command(message)
    else:
        await modify_role_permissions(message, False)


async def modify_role_permissions(message, allow=True):
    role = str(message.content.split()[1]).lower()
    if (whitelist_roles and allow) or not whitelist_roles:
        if role not in roleList:
            roleList.append(role)
            handler.update_config()
    else:
        if role in roleList:
            roleList.remove(role)
            handler.update_config()
    await client.send_message(message.channel, "Role List Modification complete. Current List: {}".format(roleList))


async def send_complete(message):
    pass


# Current Status: async calls are troublesome to test
# async def testing_bank(message):
#     if is_owner(message.author.id):
#         await client.send_message(message.channel, "Running tests...   ")
#         await test_begin()
#         loop = asyncio.get_event_loop()
#         loop.stop()
#         future = asyncio.Future()
#         asyncio.ensure_future(first_test(future))
#         loop.run_until_complete(future)
#         # await asyncio.sleep(1)
#         # await test_one()
#         # await asyncio.sleep(1)
#         # await test_two()
#         # await asyncio.sleep(1)
#         # await test_three()
#         # await asyncio.sleep(2)
#         # await test_four()
#         # await asyncio.sleep(1)
#         # await test_five()
#         # await asyncio.sleep(1)
#         # await test_six()
#         # await asyncio.sleep(1)
#         await test_end(message)


func_dict = {
    'help': help,
    'listroles': list_roles,
    'addrole': add_role,
    'removerole': remove_role,
    'allowcommand': allow_command,
    'restrictcommand': restrict_command,
    'allowrolemodification': allow_role_modification,
    'restrictrolemodification': restrict_role_modification,
    'purge': purge,
    'nuke': nuke,
    # 'test': testing_bank,
    'quit': quit
}

func_help = {
    'help': "!help - Displays this command",
    'listroles': "!listroles - Displays the list of roles that may be added or removed",
    'addrole': "!addrole [roles] - Adds the roles to yourself, roles can be separated by spaces",
    'removerole': "!removerole [roles] - Removes the roles from yourself, roles can be separated by spaces",
    'allowcommand': "!allowcommand [command] - Allows the command to be used",
    'restrictcommand': "!restrictcommand [command] - Restricts the command from being used",
    'allowrolemodification': "!allowrolemodification [role] - Allows the role to be modified using "
                             "addrole/removerole commands",
    'restrictrolemodification': "!restrictrolemodification [role] - Restricts the role to be modified"
                                "using the addrole/removerole commands",
    'purge': "!purge - Cleans the last few bot messages",
    'nuke': "!nuke [n=100] - Removes the last [n] messages from the channel"
    # 'quit': "!quit - Shutdown the bot gracefully"
}


########## Function Dictionary ##########


########## HELPER FUNCTIONS ##########

def is_me(message):
    """Checks if the message was sent by the bot, returns true if yes"""
    return message.author == client.user


def has_permissions(message, action, the_channel=''):
    """Checks if the bot has permissions to do a certain action, returns true if yes"""
    if the_channel == '':
        server = message.server
        channel = message.channel
    else:
        server = the_channel.server
        channel = the_channel
    member_obj = server.get_member(client.user.id)
    return bool(channel.permissions_for(member_obj).value & int(action))


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


def authorized(message, command_name, user=''):
    """Checks if the user is authorized to run the command, returns true if yes"""
    if user == '':
        user_id = message.author.id
    else:
        user_id = user.id
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


def retrieve_roles(server, list_of_roles):
    """Returns a list of role objects that are associated with the list_of_roles

    :return a list of roles
    """
    server_roles = server.roles
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
