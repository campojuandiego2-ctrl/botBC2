import discord
from discord.ext import commands
import unicodedata

def setup(bot):

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def addroles(ctx):

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

        # PREGUNTAR ROLES
        await ctx.send(

            "🎭 Mándame los nombres de los "
            "roles separados por comas.\n\n"

            "Ejemplo:\n"
            "`capitan, vice-capitan, noble`"

        )

        roles_msg = await bot.wait_for(
            "message",
            check=check
        )

        # SEPARAR ROLES
        nombres_roles = [

            rol.strip()

            for rol in roles_msg.content.split(",")

            if rol.strip()

        ]

        creados = []

        # CREAR ROLES
        for nombre in nombres_roles:

            rol = await ctx.guild.create_role(

                name=nombre

            )

            creados.append(
                rol.mention
            )

        # RESULTADO
        await ctx.send(

            "✅ Roles creados correctamente.\n\n"

            + "\n".join(creados)

        )

