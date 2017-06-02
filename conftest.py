import pytest
import discord
import discordBot
import bot.handler as handler
import bot.permissions as permissions
import bot.commands as commands

SERVER_ID = "152522880733675522"
CHANNEL_ID = "319657072792829954"
USER_ID = "319258867089539074"


# @pytest.fixture(scope="session", autouse=True)
# def init(request):
#     global token
#     global owner_id
#     global adminList
#     global client
#     global whitelist_roles
#     global roleList
#     global whitelist_commands
#     global commandList
#     handler.init("./test_config.yaml")
#     token = handler.token
#     owner_id = handler.owner_id
#     adminList = handler.adminList
#     client = handler.client
#     whitelist_roles = handler.whitelist_roles
#     roleList = handler.roleList
#     whitelist_commands = handler.whitelist_commands
#     commandList = handler.commandList
#     request.addfinalizer(client.close)


@pytest.fixture(scope="session", autouse=True)
async def init():
    handler.init("./test_config.yaml")
    print(handler.token)
    await handler.client.run(handler.token)
    # request.addfinalizer(handler.client.close)


@pytest.fixture(scope="session")
def server_id():
    return SERVER_ID


@pytest.fixture(scope="session")
def channel_id():
    return CHANNEL_ID


@pytest.fixture(scope="session")
def user_id():
    return USER_ID

# @pytest.fixture(scope="session")
# def client():
#     return handler.client
#
#
# @pytest.fixture(scope="session")
# def server(client):
#     return handler.client.get_server(SERVER_ID)
#
#
# @pytest.fixture(scope="session")
# def channel(client):
#     return handler.client.get_server(SERVER_ID).get_channel(CHANNEL_ID)
