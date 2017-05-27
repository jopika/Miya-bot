import discord
import asyncio
from pathlib import Path
import yaml

# Bot token
token = ""
# Admin ID used to debug the bot and shutdown remotely
admin_id = ""
# Client Object for the bot
client = discord.Client()
# Debug Variable
DEBUG = False
# whitelist or blacklist for roles 
# False for blacklist, True for whitelist
whitelist = False
# Role List Filter
roleList = []

################################################################
################ COMMAND LIST (IMPLEMENTATIONS) ################
################################################################

### !help - prints the commands that are useable to the public
async def help(message):
    await client.send_message(message.author, "-----------------------\n!help - gives you this message \n !listRoles - gives you the list of roles \n !addRole [roles]    - adds the space separated roles to the user (if allowed) \n !removeRole [roles] - removes the space separated roles to the user (if allowed) \n !purge - cleans bot messages\n-----------------------------------")

async def invalidCommand(message):
    await client.send_message(message.channel, "Invalid command, use !help for list of commands")

### !listRoles - lists the roles 
async def listRoles(message):
    server = message.server
    messageString = ""
    for role in server.roles[1:]:
        messageString += str(role)
        messageString += " "
    await client.send_message(message.channel, messageString)

### !addRole [listOfRoles] - adds the role(s) to the user
async def addRole(message):
    roleList = get_roles(message)
    for role in message.server.roles[1:]:
        if str(role).lower() in roleList:
            if DEBUG:
                print("User: ", message.author, " has added role: ", role)
            await client.add_roles(message.author, role)
    await client.send_message(message.channel, "done!")

### !removeRole [listOfRoles] - remove the role(s) to the user
async def removeRole(message):
    roleList = get_roles(message)
    for role in message.server.roles[1:]:
        if str(role).lower() in roleList:
            if DEBUG:
                print("User: ", message.author, " has removed role: ", role)
            await client.remove_roles(message.author, role)
    await client.send_message(message.channel, "done!")

### !purge - clears the last few messages sent by the bot
async def purge(message):
    await client.purge_from(message.channel, limit=100, check=is_me)

### *admin* !purge [x=50] - clears out the last x messages (default is 50)
async def nuke(message):
    if message.author.id == admin_id:
        commandParams = message.content.split()[1:]
        count = 50
        if len(commandParams) == 1:
            count = int(commandParams[0])
        await client.purge_from(message.channel, limit=count)

### *admin* !quit - shutdown the bot gracefully
async def quit(message):
    if message.author.id == admin_id:
        if DEBUG:
            await client.send_message(message.channel, "Shutting down")
        await client.close()
    else:
        if DEBUG:
            await client.send_message(message.channel, "Not authorized to use this command!")

################################################################
################################################################

func_dict = {
    'help':help, 
    'addRole':addRole, 
    'listRoles': listRoles, 
    'removeRole': removeRole,
    'purge': purge,
    'nuke': nuke,
    'quit':quit}

######### HELPER FUNCTIONS #########
def is_me(message):
    return message.author == client.user

def get_roles(message):
    theList = list(map(str.lower, message.content.split()[1:]))
    cleanedList = []
    for role in theList:
        if (not (whitelist ^ bool(role in roleList))):
            cleanedList.append(role)
    return cleanedList

def prompt():
    config_file = Path("./config.yaml")
    global token
    global admin_id
    global client
    global whitelist
    global roleList
    token = input("What is the bot's Token ID?: ")
    print("What is the owner's admin_id")
    admin_id = input("You can retrieve the ID by using '\@<username>': ")
    print("Do you wish to use a whitelist or blacklist?")
    userInput = input("Whitelist? (yes/no): ")
    if userInput == "" or userInput.lower().startswith("y"):
        whitelist = True
    else:
        whitelist = False
    print("What roles do you want to white/black list?")
    roleList = input("Please separate roles by spaces: ").lower().split()
    data = dict(
        token = token,
        admin_id = admin_id,
        whitelist = whitelist,
        roleList = roleList)
    with config_file.open('w') as stream:
        yaml.dump(data, stream, default_flow_style=False)
    return
    
######### DRIVER FUNCTIONS #########
@client.event
async def on_ready():
    print("--------------------------------")
    print('Logged in:')
    print("Client Username: ", client.user.name)
    print("Client ID: ", client.user.id)
    if(whitelist):
        print("Whitelist: ", roleList)
    else:
        print("Blacklist: ", roleList)
    print("--------------------------------")

@client.event
async def on_message(message):
    if DEBUG:
        print(message.author, ": ", message.content)
    if(not message.author.bot and message.content.startswith('!')):
        command = message.content.split()[0][1:]
        await func_dict.get(command, invalidCommand)(message)

def main():
    config_file = Path("./config.yaml")
    global token
    global admin_id
    global client
    global whitelist
    global roleList
    if config_file.is_file():
        # read file
        with config_file.open('r') as stream:
            try:
                config = yaml.load(stream)
                token = config["token"]
                admin_id = config["admin_id"]
                whitelist = bool(config["whitelist"])
                roleList = config["roleList"].lower().split()
            except yaml.YAMLError as exc:
                print(exec)
                prompt()
    else:
        # prompt user
        prompt()

    client.run(token)

if __name__ == '__main__':
    main()

