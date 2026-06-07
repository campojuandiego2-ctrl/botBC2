import discord
from discord.ext import commands

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def use(
        ctx,
        cantidad=None,
        tipo=None
    ):

        # VERIFICAR DATOS
        if cantidad is None or tipo is None:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Uso correcto:\n"
                    "-use 1 slot\n"
                    "-use 1 evolucion"
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        # CONVERTIR NUMERO
        try:

            cantidad = int(cantidad)

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

        usuario_id = ctx.author.id

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

        tipo = tipo.lower()

        # USAR SLOT
        if tipo == "slot":

            slots_actuales = jugador[7]

            # VERIFICAR
            if cantidad > slots_actuales:

                embed_error = discord.Embed(
                    description=(
                        "<a:error:1512895443250577629> "
                        "No tienes suficientes "
                        "slots de hechizo."
                    ),
                    color=0xff0000
                )

                await ctx.send(embed=embed_error)
                return

            nuevos_slots = (
                slots_actuales - cantidad
            )

            # ACTUALIZAR
            cursor.execute("""
            UPDATE jugadores
            SET slot_hechizo = ?
            WHERE usuario_id = ?
            """, (
                nuevos_slots,
                usuario_id
            ))

            conexion.commit()

            embed = discord.Embed(
                description=(
                    f"✅ Usaste "
                    f"**{cantidad}** slot de hechizo."
                ),
                color=0x00ff00
            )

            embed.set_footer(
                text=(
                    f"Slots restantes: "
                    f"{nuevos_slots}"
                )
            )

            await ctx.send(embed=embed)
            return

        # USAR EVOLUCION
        elif tipo == "evolucion":

            evoluciones_actuales = jugador[8]

            # VERIFICAR
            if cantidad > evoluciones_actuales:

                embed_error = discord.Embed(
                    description=(
                        "<a:error:1512895443250577629> "
                        "No tienes suficientes "
                        "evoluciones."
                    ),
                    color=0xff0000
                )

                await ctx.send(embed=embed_error)
                return

            nuevas_evoluciones = (
                evoluciones_actuales - cantidad
            )

            # ACTUALIZAR
            cursor.execute("""
            UPDATE jugadores
            SET evoluciones = ?
            WHERE usuario_id = ?
            """, (
                nuevas_evoluciones,
                usuario_id
            ))

            conexion.commit()

            embed = discord.Embed(
                description=(
                    f"✅ Usaste "
                    f"**{cantidad}** evolución."
                ),
                color=0x00ff00
            )

            embed.set_footer(
                text=(
                    f"Evoluciones restantes: "
                    f"{nuevas_evoluciones}"
                )
            )

            await ctx.send(embed=embed)
            return

        # TIPO INVALIDO
        else:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Opciones válidas:\n"
                    "slot\n"
                    "evolucion"
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)