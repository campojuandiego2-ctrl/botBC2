import discord
from discord.ext import commands
import unicodedata

def setup(bot):

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def addchannels(ctx):

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

            ).lower().replace(
                ".", ""
            ).replace(
                ",", ""
            ).strip()

        # PREGUNTAR CATEGORIA
        await ctx.send(

            "📂 ¿En qué categoría deseas "
            "agregar canales?"

        )

        categoria_msg = await bot.wait_for(
            "message",
            check=check
        )

        nombre_categoria = limpiar(
            categoria_msg.content
        )

        categoria = None

        # BUSCAR CATEGORIA
        for cat in ctx.guild.categories:

            nombre_cat = limpiar(
                cat.name
            )

            if nombre_categoria in nombre_cat:

                categoria = cat
                break

        # SI NO EXISTE
        if categoria is None:

            await ctx.send(
                "❌ No encontré esa categoría."
            )

            return

        # PREGUNTAR CANALES
        await ctx.send(

            "📝 Mándame los nombres de los "
            "canales separados por comas.\n\n"

            "Ejemplo:\n"
            "`reglas, anuncios, chat-general`"

        )

        canales_msg = await bot.wait_for(
            "message",
            check=check
        )

        # SEPARAR CANALES
        nombres_canales = [

            canal.strip()

            for canal in canales_msg.content.split(",")

            if canal.strip()

        ]

        creados = []

        # CREAR CANALES
        for nombre in nombres_canales:

            canal = await ctx.guild.create_text_channel(

                name=nombre.lower().replace(
                    " ",
                    "-"
                ),

                category=categoria

            )

            creados.append(
                canal.mention
            )

        # RESULTADO
        await ctx.send(

            "✅ Canales creados correctamente.\n\n"

            + "\n".join(creados)

        )