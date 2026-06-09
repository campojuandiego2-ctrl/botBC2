import discord
from discord.ext import commands
import random
import unicodedata

def setup(bot):

    CANAL_MISIONES = 1504551609542377513

    class MisionView(discord.ui.View):

        def __init__(
            self,
            creador,
            rango,
            canal_mision
        ):

            super().__init__(timeout=None)

            self.creador = creador
            self.rango = rango
            self.canal_mision = canal_mision

            self.participantes = []

            self.mision_iniciada = False

        # ACTUALIZAR EMBED
        async def actualizar_embed(
            self,
            interaction
        ):

            participantes_texto = (

                "\n".join(
                    [
                        f"> {u.mention}"
                        for u in self.participantes
                    ]
                )

                if self.participantes
                else "*Nadie se ha unido todavía.*"
            )

            estado = (
                "En Curso"
                if self.mision_iniciada
                else "En Preparación"
            )

            embed = discord.Embed(

                description=(

                    "## ﹒⊂NUEVA MISIÓN DISPONIBLE⊃﹑\n\n"

                    "`⚠️` Una nueva misión ha sido emitida "
                    "por el Reino del Trébol.\n\n"

                    f"➤ **Rango:** {self.rango}\n"
                    f"➤ **Canal:** {self.canal_mision.mention}\n"
                    f"➤ **Estado:** {estado}\n"
                    f"➤ **Participantes:**\n"
                    f"{participantes_texto}\n\n"

                    "> Los detalles completos de la misión "
                    "serán entregados próximamente a los "
                    "participantes seleccionados."

                ),

                color=0x5865F2
            )

            embed.set_image(
                url="https://media.discordapp.net/attachments/923040988950327359/1513903525581820035/bc4140e497cea9a20726db93ffb83db6.jpg"
            )

            await interaction.message.edit(
                embed=embed,
                view=self
            )

        # BOTON UNIRSE
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

            # YA ESTA
            if usuario in self.participantes:

                await interaction.response.send_message(
                    "Ya estás en la misión.",
                    ephemeral=True
                )

                return

            # MISION INICIADA
            if self.mision_iniciada:

                await interaction.response.send_message(
                    "La misión ya inició.",
                    ephemeral=True
                )

                return

            # LIMITE
            if len(self.participantes) >= 5:

                await interaction.response.send_message(
                    "La misión está llena.",
                    ephemeral=True
                )

                return

            # AGREGAR
            self.participantes.append(
                usuario
            )

            await interaction.response.defer()

            await self.actualizar_embed(
                interaction
            )

        # BOTON INICIAR
        @discord.ui.button(
            label="Iniciar Misión",
            style=discord.ButtonStyle.success,
            emoji="🚩"
        )
        async def iniciar(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
        ):

            # SOLO CREADOR
            if interaction.user != self.creador:

                await interaction.response.send_message(
                    "Solo el creador puede iniciar la misión.",
                    ephemeral=True
                )

                return

            # YA INICIO
            if self.mision_iniciada:

                await interaction.response.send_message(
                    "La misión ya fue iniciada.",
                    ephemeral=True
                )

                return

            self.mision_iniciada = True

            # DESACTIVAR BOTON UNIRSE
            for item in self.children:

                if item.label == "Unirse":

                    item.disabled = True

            # PING PARTICIPANTES
            menciones = " ".join(

                [
                    u.mention
                    for u in self.participantes
                ]
            )

            await self.canal_mision.send(

                f"{menciones}\n\n"

                "## ⊂⚔️ MISIÓN INICIADA⊃\n\n"

                "Los caballeros seleccionados "
                "han sido convocados."

            )

            await interaction.response.defer()

            await self.actualizar_embed(
                interaction
            )

    @bot.command()
    async def addmission(ctx):

        def check(m):

            return (
                m.author == ctx.author
                and m.channel == ctx.channel
            )

        # LIMPIAR TEXTO
        def limpiar(texto):

            return "".join(

                c for c in unicodedata.normalize(
                    "NFD",
                    texto
                )

                if unicodedata.category(c) != "Mn"

            ).lower()

        # PREGUNTAR RANGO
        await ctx.send(
            "¿Qué rango tendrá la misión?"
        )

        rango_msg = await bot.wait_for(
            "message",
            check=check
        )

        rango = rango_msg.content

        # PREGUNTAR REGION
        await ctx.send(
            "¿En qué región se realizará?"
        )

        categoria_msg = await bot.wait_for(
            "message",
            check=check
        )

        nombre_categoria = categoria_msg.content

        nombre_categoria_limpio = limpiar(
            nombre_categoria
        )

        categoria = None

        for cat in ctx.guild.categories:

            nombre_cat = limpiar(
                cat.name
            )

            if nombre_categoria_limpio in nombre_cat:

                categoria = cat
                break

        # NO EXISTE
        if categoria is None:

            await ctx.send(
                "No encontré esa región."
            )

            return

        # CANALES
        canales = categoria.text_channels

        if not canales:

            await ctx.send(
                "Esa región no tiene canales."
            )

            return

        # RANDOM
        canal_random = random.choice(
            canales
        )

        # CANAL MISIONES
        canal_misiones = bot.get_channel(
            CANAL_MISIONES
        )

        # ROL MISION
        rol_mision = discord.utils.get(
            ctx.guild.roles,
            name="Mision"
        )

        ping = (
            rol_mision.mention
            if rol_mision
            else "@Mision"
        )

        # EMBED
        embed = discord.Embed(

            description=(

                "## ﹒⊂NUEVA MISIÓN DISPONIBLE⊃﹑\n\n"

                "`⚠️` Una nueva misión ha sido emitida "
                "por el Reino del Trébol.\n\n"

                f"➤ **Rango:** {rango}\n"
                f"➤ **Canal:** {canal_random.mention}\n"
                f"➤ **Estado:** En Preparación\n"
                f"➤ **Participantes:**\n"
                f"*Nadie se ha unido todavía.*\n\n"

                "> Los detalles completos de la misión "
                "serán entregados próximamente a los "
                "participantes seleccionados."

            ),

            color=0x5865F2
        )

        embed.set_image(
            url="https://i.pinimg.com/originals/80/a4/88/80a488dc6bca2d704932c2dd0b77d34e.gif"
        )

        await canal_misiones.send(

            ping,

            embed=embed,

            view=MisionView(
                ctx.author,
                rango,
                canal_random
            )
        )