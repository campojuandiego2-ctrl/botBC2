import discord
from discord.ext import commands

def setup(bot):

    class ParticiparView(discord.ui.View):

        def __init__(self):

            super().__init__(timeout=None)

            self.participantes = []

        @discord.ui.button(
            label="Unirse",
            style=discord.ButtonStyle.primary,
            emoji="⚔️"
        )
        async def unirse(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
        ):

            usuario = interaction.user

            # EVITAR DUPLICADOS
            if usuario in self.participantes:

                await interaction.response.send_message(
                    "Ya te uniste.",
                    ephemeral=True
                )

                return

            # AGREGAR USUARIO
            self.participantes.append(usuario)

            # LISTA PARTICIPANTES
            lista = "\n".join(
                [
                    f"• {u.mention}"
                    for u in self.participantes
                ]
            )

            # EMBED
            embed = discord.Embed(

                description=(
                    f"👥 **Participantes:** "
                    f"{len(self.participantes)}/3\n\n"
                    f"{lista}"
                ),

                color=0x5865F2
            )

            await interaction.response.edit_message(
                embed=embed,
                view=self
            )

    @bot.command()
    async def prueba(ctx):

        embed = discord.Embed(

            description=(
                "👥 **Participantes:** 0/3"
            ),

            color=0x5865F2
        )

        await ctx.send(
            embed=embed,
            view=ParticiparView()
        )