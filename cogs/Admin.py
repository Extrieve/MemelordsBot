# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Admin(commands.Cog):
    """Administrative command list"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', aliases=['k'], pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @commands.command(name='ban', aliases=['b'], pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @commands.command(name='unban', aliases=['ub'], pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unban a member from the server."""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
            
        await ctx.send(f'Could not find {member} in the ban list.')

    @commands.command(name='clear', aliases=['c'], pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        """Clear a certain amount of messages."""
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared {amount} messages.')

    @commands.command(name='mute', aliases=['m'], pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mute a member from the server."""
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role, reason=reason)
        await ctx.send(f'Muted {member.mention}')

    @commands.command(name='unmute', aliases=['um'], pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """Unmute a member from the server."""
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role, reason=reason)
        await ctx.send(f'Unmuted {member.mention}')
    

def setup(bot):
    bot.add_cog(Admin(bot))
