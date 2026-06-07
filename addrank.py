import discord
from discord.ext import commands

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def addrank(
        ctx,
        miembro: discord.Member,
        *,
        rango_adquirido=None
    ):

        # VERIFICAR PERMISOS
        if not (
            ctx.author.guild_permissions.administrator
            or any(
                role.name in [
                    "❪🍷 ❫  ❱❱ Administrador",
                    "❪🍷 ❫  ❱❱ Moderador",
                    "❪🍷 ❫  ❱❱ Game Masters",
                    "❪🍷 ❫  ❱❱ Verificador"
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

        # VERIFICAR RANGO
        if rango_adquirido is None:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Uso correcto:\n"
                    "-addrank @usuario "
                    "Caballero Mágico"
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

        # ACTUALIZAR RANGO
        cursor.execute("""
        UPDATE jugadores
        SET rango = ?
        WHERE usuario_id = ?
        """, (
            rango_adquirido,
            usuario_id
        ))

        conexion.commit()

        # EMBED FINAL
        embed = discord.Embed(
            description=(
                f"✅ {miembro.mention} "
                f"ha adquirido el rango:\n\n"
                f"**{rango_adquirido}**"
            ),
            color=0x00ff00
        )

        embed.set_footer(
            text=(
                f"Nuevo rango registrado"
            )
        )

        await ctx.send(embed=embed)