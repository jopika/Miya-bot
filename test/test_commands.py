import pytest
import discord
import discordBot
import bot.handler as handler
import bot.permissions as permissions
import bot.commands as commands

"""This test bank verifies that commands are functioning correctly"""


class TestAddRole(object):
    """Tests the functionality of the !addRole funcitons"""

    def test_single_one(self, client, server, channel, user_id):
        roles = server.get_member(user_id).roles
        user = server.get_member(user_id)
        if len(roles) > 1:
            for role in roles[1:]:
                client.remove_roles(user, role)
        assert (user.roles == 1)


