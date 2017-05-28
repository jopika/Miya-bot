import discord
from pathlib import Path
import yaml

# Bot token
token = ""
# Owner ID used to debug the bot and shutdown remotely
owner_id = ""
# Client Object for the bot
client = discord.Client()
# Debug Variable
DEBUG = False
# whitelist or blacklist for roles
# False for blacklist, True for whitelist
whitelist_roles = False
# Role List Filter
roleList = []
# whitelist or blacklist for commands
# False for blacklist, True for whitelist
whitelist_commands = False
# Command List
commandList = []


def prompt():
    config_file = Path("./config.yaml")
    global token
    global owner_id
    global adminList
    global client
    global whitelist_roles
    global roleList
    global whitelist_commands
    global commandList
    token = input("What is the bot's Token ID?: ")
    print("What is the owner's id?")
    owner_id = input("You can retrieve the ID by using '\@<username>': ")
    print("What are the admin ID's? The owner is automatically conisdered an admin.")
    adminList = input("Please separate by spaces: ").split()
    print("Do you wish to use a whitelist or blacklist for user roles?")
    userInput = input("Whitelist? (yes/no): ")
    if userInput == "" or userInput.lower().startswith("y"):
        whitelist_roles = True
    else:
        whitelist_roles = False
    print("You are able to change the list of roles later")
    roleList = input("Please separate roles by spaces: ").lower().split()
    print("What roles do you want to white/black list for commands?")
    userInput = input("Whitelist? (yes/no): ")
    if userInput == "" or userInput.lower().startswith("y"):
        whitelist_commands = True
    else:
        whitelist_commands = False
    print("You are able to change the list of commands later")
    commandList = input("Please separate commands by spaces").lower().split()

    data = dict(
        token=token,
        owner_id=owner_id,
        adminList=adminList,
        whitelist_roles=whitelist_roles,
        whitelist_commands=whitelist_commands,
        roleList=roleList,
        commandList=commandList)

    with config_file.open('w') as stream:
        yaml.dump(data, stream, default_flow_style=False)
    return


def init():
    config_file = Path("./config.yaml")
    global token
    global owner_id
    global adminList
    global client
    global whitelist_roles
    global roleList
    global whitelist_commands
    global commandList
    if config_file.is_file():
        # read file
        with config_file.open('r') as stream:
            try:
                config = yaml.load(stream)
                token = config["token"]
                owner_id = config["owner_id"]
                adminList = config["adminList"]
                whitelist_roles = bool(config["whitelist_roles"])
                roleList = config["roleList"]
                whitelist_commands = bool(config["whitelist_commands"])
                commandList = config["commandList"]
            except yaml.YAMLError as exc:
                print(exc)
                prompt()
    else:
        # prompt user
        prompt()
