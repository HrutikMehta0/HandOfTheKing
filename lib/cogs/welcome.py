from discord.ext.commands import Cog

#from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        #db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        await self.bot.welcome.send(
            f"Welcome to **{member.guild.name}** {member.mention}! Check out our <#816489394612600832> and head over "
            f"to <#816694604840828949> for roles.")


def setup(bot):
    bot.add_cog(Welcome(bot))
