from discord.ext.commands import Cog

roles_emojis = {
    "💣": 822580998171787275,
    "📈": 822581458652758107,
    "🏹": 822581710783905873,
    "👑": 822581800919892008
}


class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.reaction_message = await self.bot.get_channel(816694604840828949).fetch_message(824483191813177416)
            self.bot.cogs_ready.ready_up("reactions")

    # @Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     print(f"{user.display_name} reacted with {reaction.emoji.name}")
    # @Cog.listener()
    # async def on_reaction_remove(self, reaction, user):
    #     pass

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.message_id == self.reaction_message.id:
            role = self.bot.guild.get_role(roles_emojis.get(payload.emoji.name))
            await payload.member.add_roles(role, reason="Emoji role reaction.")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.guild
        member = guild.get_member(payload.user_id)
        if self.bot.ready and payload.message_id == self.reaction_message.id:
            role = guild.get_role(roles_emojis.get(payload.emoji.name))
            await member.remove_roles(role, reason="Emoji role reaction.")


def setup(bot):
    bot.add_cog(Reactions(bot))
