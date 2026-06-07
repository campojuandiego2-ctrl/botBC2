import discord
from discord.ext import commands

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def addslots(
        ctx,
        miembro: discord.Member,
        slots=None
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
        if slots is None:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Uso correcto:\n"
                    "-addslots @usuario 1"
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

            slots = int(slots)

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

        slots_actuales = jugador[7]

        nuevos_slots = (
            slots_actuales + slots
        )

        # ACTUALIZAR SLOTS
        cursor.execute("""
        UPDATE jugadores
        SET slot_hechizo = ?
        WHERE usuario_id = ?
        """, (
            nuevos_slots,
            usuario_id
        ))

        conexion.commit()

        # EMBED FINAL
        embed = discord.Embed(
            description=(
                f"✅ Se añadieron "
                f"**{slots}** slots de "
                f"hechizo a "
                f"{miembro.mention} "
                f"con éxito."
            ),
            color=0x00ff00
        )

        embed.set_footer(
            text=(
                f"Slots actuales: "
                f"{nuevos_slots}"
            )
        )

        await ctx.send(embed=embed)