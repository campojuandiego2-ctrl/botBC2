import discord
from discord.ext import commands

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def addevolution(
        ctx,
        miembro: discord.Member,
        evoluciones=None
    ):

        # VERIFICAR PERMISOS
        if not (
            ctx.author.guild_permissions.administrator
            or any(
                role.name in [
                    "❪🍷 ❫  ❱❱ Administrador",
                    "❪🍷 ❫  ❱❱ Moderador"
                ]
                for role in ctx.author.roles
            )
        ):

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "No tienes permisos "
                    "para usar este comando."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        # VERIFICAR DATOS
        if evoluciones is None:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Uso correcto:\n"
                    "-addevolution @usuario 1"
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        usuario_id = miembro.id

        # BUSCAR JUGADOR
        cursor.execute("""
        SELECT * FROM jugadores
        WHERE usuario_id = ?
        """, (usuario_id,))

        jugador = cursor.fetchone()

        # SI NO EXISTE
        if jugador is None:

            crear_jugador(usuario_id)

            cursor.execute("""
            SELECT * FROM jugadores
            WHERE usuario_id = ?
            """, (usuario_id,))

            jugador = cursor.fetchone()

        # CONVERTIR NUMERO
        try:

            evoluciones = int(evoluciones)

        except:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Debes ingresar un número."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        evoluciones_actuales = jugador[8]

        nuevas_evoluciones = (
            evoluciones_actuales + evoluciones
        )

        # ACTUALIZAR EVOLUCIONES
        cursor.execute("""
        UPDATE jugadores
        SET evoluciones = ?
        WHERE usuario_id = ?
        """, (
            nuevas_evoluciones,
            usuario_id
        ))

        conexion.commit()

        # EMBED FINAL
        embed = discord.Embed(
            description=(
                f"✅ Se añadieron "
                f"**{evoluciones}** evoluciones a "
                f"{miembro.mention} "
                f"con éxito."
            ),
            color=0x00ff00
        )

        embed.set_footer(
            text=(
                f"Evoluciones actuales: "
                f"{nuevas_evoluciones}"
            )
        )

        await ctx.send(embed=embed)