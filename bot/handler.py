import discord
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
        token=token,
        admin_id=admin_id,
        whitelist=whitelist,
        roleList=roleList)
    with config_file.open('w') as stream:
        yaml.dump(data, stream, default_flow_style=False)
    return


def init():
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
            except Exception as exc:
                print(exec)
                prompt()
    else:
        # prompt user
        prompt()

#
#
# def init():
#     config_file = Path("./config.yaml")
#     global token
#     global admin_id
#     if config_file.is_file():
#         # read file
#         with config_file.open('r') as stream:
#             try:
#                 config = yaml.load(stream)
#                 token = config["token"]
#                 admin_id = config["admin_id"]
#             except yaml.YAMLError as exc:
#                 print(exec)
#                 return
#     else:
#         # prompt user
#         token = input("What is the bot's Token ID?")
#         print("What is the owner's admin_id")
#         admin_id = input("You can retrieve the ID by using '\@<username>'")
#         data = dict(
#             token=token,
#             admin_id=admin_id)
#         with config_file.open('w') as stream:
#             yaml.dump(data, stream, default_flow_style=False)
