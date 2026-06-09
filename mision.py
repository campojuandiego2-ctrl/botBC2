import discord
from discord.ext import commands
import random

def setup(bot):

    class MisionView(discord.ui.View):

        def __init__(
            self,
            rango,
            descripcion,
            canal
        ):

            super().__init__(timeout=None)

            self.rango = rango
            self.descripcion = descripcion
            self.canal = canal

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
                    embed=discord.Embed(
                        description=(
                            "⊂❌ ▻ **MISIÓN**\n"
                            "Ya estás en esta misión."
                        ),
                        color=0xFF0000
                    ),
                    ephemeral=True
                )

                return

            # LIMITE
            if len(self.participantes) >= 5:

                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=(
                            "⊂❌ ▻ **MISIÓN LLENA**\n"
                            "No puedes unirte."
                        ),
                        color=0xFF0000
                    ),
                    ephemeral=True
                )

                return

            # AGREGAR PARTICIPANTE
            self.participantes.append(usuario)

            # LISTA
            lista = "\n".join(
                [
                    f"> {u.mention}"
                    for u in self.participantes
                ]
            )

            # ESTADO
            estado = (
                "Completa"
                if len(self.participantes) >= 5
                else "Disponible"
            )

            # EMBED
            embed = discord.Embed(

                description=(

                    f"⊂📜 ▻ **MISSION AVAILABLE**\n"
                    f"-# **Rango:** {self.rango}\n"
                    f"-# **Estado:** {estado}\n\n"

                    f"╰┈➤ `📍` **CANAL**\n"
                    f"> {self.canal.mention}\n\n"

                    f"╰┈➤ `📝` **DESCRIPCIÓN**\n"
                    f"> {self.descripcion}\n\n"

                    f"╰┈➤ `👤` **PARTICIPANTES**\n"
                    f"{lista}"

                ),

                color=0x5865F2
            )

            # DESACTIVAR BOTON
            if len(self.participantes) >= 5:

                button.disabled = True

            await interaction.response.edit_message(
                embed=embed,
                view=self
            )

    @bot.command()
    async def addmission(ctx):

        def check(m):

            return (
                m.author == ctx.author
                and m.channel == ctx.channel
            )

        # RANGO
        await ctx.send(
            embed=discord.Embed(
                description=(
                    "⊂📜 ▻ **CREAR MISIÓN**\n"
                    "¿Qué rango tendrá la misión?"
                ),
                color=0x5865F2
            )
        )

        rango_msg = await bot.wait_for(
            "message",
            check=check
        )

        rango = rango_msg.content

        # CATEGORIA
        await ctx.send(
            embed=discord.Embed(
                description=(
                    "⊂📂 ▻ **CATEGORÍA**\n"
                    "¿En qué categoría se realizará?"
                ),
                color=0x5865F2
            )
        )

        categoria_msg = await bot.wait_for(
            "message",
            check=check
        )

        nombre_categoria = categoria_msg.content.lower()

        # BUSCAR CATEGORIA
        categoria = None

        for cat in ctx.guild.categories:

            if nombre_categoria in cat.name.lower():

                categoria = cat
                break

        if categoria is None:

            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "⊂❌ ▻ **ERROR**\n"
                        "No encontré esa categoría."
                    ),
                    color=0xFF0000
                )
            )

            return

        # CANALES
        canales = [

            canal
            for canal in categoria.text_channels
        ]

        if not canales:

            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "⊂❌ ▻ **ERROR**\n"
                        "Esa categoría no tiene canales."
                    ),
                    color=0xFF0000
                )
            )

            return

        # CANAL RANDOM
        canal_random = random.choice(canales)

        # DESCRIPCION
        await ctx.send(
            embed=discord.Embed(
                description=(
                    "⊂📝 ▻ **DESCRIPCIÓN**\n"
                    "Describe la misión."
                ),
                color=0x5865F2
            )
        )

        descripcion_msg = await bot.wait_for(
            "message",
            check=check
        )

        descripcion = descripcion_msg.content

        # EMBED FINAL
        embed = discord.Embed(

            description=(

                f"⊂📜 ▻ **MISSION AVAILABLE**\n"
                f"-# **Rango:** {rango}\n"
                f"-# **Estado:** Disponible\n\n"

                f"╰┈➤ `📍` **CANAL**\n"
                f"> {canal_random.mention}\n\n"

                f"╰┈➤ `📝` **DESCRIPCIÓN**\n"
                f"> {descripcion}\n\n"

                f"╰┈➤ `👤` **PARTICIPANTES**\n"
                f"> *Nadie se ha unido todavía.*"

            ),

            color=0x5865F2
        )

        await ctx.send(

            embed=embed,

            view=MisionView(
                rango,
                descripcion,
                canal_random
            )
        )