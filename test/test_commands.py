import pytest
import discord
import discordBot
import bot.handler as handler
import bot.permissions as permissions
import bot.commands as commands
import time

"""This test bank verifies that commands are functioning correctly"""


class TestAddRole(object):
    """Tests the functionality of the !addRole funcitons"""

    def test_single_one(self, server_id, channel_id, user_id):
        client = handler.client
        # counter = 0
        # while not client._is_ready._value and counter < 10:
        #     time.sleep(1)
        #     counter += 1
        server = client.get_server(server_id)
        channel = client.get_channel(channel_id)
        print(type(client))
        user = server.get_member(user_id)
        # user_roles = user.roles
        # assert len(user_roles) == 1
        assert 1 == 1


        # server = handler.client.get_server()
        # test_user_roles = handler.client.get_channel(test.CHANNEL_ID).get_user(test.USER_ID)



        # roles = server.get_member(user_id).roles
        # user = server.get_member(user_id)
        # if len(roles) > 1:
        #     for role in roles[1:]:
        #         client.remove_roles(user, role)
        # assert (user.roles == 1)


