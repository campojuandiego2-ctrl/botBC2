import discord
import asyncio

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def editstats(ctx):

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

        puntos_disponibles = jugador[1]

        # EMBED 1
        embed = discord.Embed(
            title="⊂📊 ▻ DISTRIBUIR PUNTOS",
            color=0xff0000
        )

        embed.description = f"""
-# **Puntos Disponibles:** {puntos_disponibles}

╰┈➤ `🧮` **STATS EDITABLES**
> -# ⊩┇FUERZA
> -# ⊩┇RESISTENCIA
> -# ⊩┇AGILIDAD
> -# ⊩┇MANA
> -# ⊩┇PODER MAGICO

-# Escribe el nombre de la stats.
"""

        await ctx.send(embed=embed)

        # VERIFICAR MENSAJE
        def check(m):

            return (
                m.author == ctx.author
                and m.channel == ctx.channel
            )

        # ESPERAR STAT
        try:

            mensaje_stat = await bot.wait_for(
                "message",
                timeout=30,
                check=check
            )

        except asyncio.TimeoutError:

            embed_timeout = discord.Embed(
                description=(
                    "<a:time:1512589244378644550> "
                    "Tiempo agotado."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_timeout)
            return

        stat = mensaje_stat.content.lower()

        # STATS VALIDAS
        stats_validas = {
            "fuerza": 2,
            "resistencia": 3,
            "agilidad": 4,
            "mana": 5,
            "poder_magico": 6
        }

        # VERIFICAR STAT
        if stat not in stats_validas:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629>  Stat inválida."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        # EMBED 2
        embed2 = discord.Embed(
            title="⊂📥 ▻ INGRESAR PUNTOS",
            description=(
                f"¿Cuántos puntos deseas "
                f"colocar en {stat.upper()}?"
            ),
            color=0x5865F2
        )

        embed2.set_footer(
            text=(
                f"Máximo: "
                f"{puntos_disponibles}"
            )
        )

        await ctx.send(embed=embed2)

        # ESPERAR PUNTOS
        try:

            mensaje_puntos = await bot.wait_for(
                "message",
                timeout=30,
                check=check
            )

        except asyncio.TimeoutError:

            embed_timeout = discord.Embed(
                description=(
                    "<a:time:1512589244378644550> "
                    "Tiempo agotado."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_timeout)
            return

        # CONVERTIR A NUMERO
        try:

            puntos = int(
                mensaje_puntos.content
            )

        except:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629>  Debes ingresar un número."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        # VERIFICAR PUNTOS
        if puntos > puntos_disponibles:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629>  No tienes suficientes puntos."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        indice = stats_validas[stat]

        valor_actual = jugador[indice]

        nuevo_valor = (
            valor_actual + puntos
        )

        nuevos_puntos = (
            puntos_disponibles - puntos
        )

        # ACTUALIZAR STAT
        cursor.execute(f"""
        UPDATE jugadores
        SET {stat} = ?
        WHERE usuario_id = ?
        """, (
            nuevo_valor,
            usuario_id
        ))

        # ACTUALIZAR PUNTOS
        cursor.execute("""
        UPDATE jugadores
        SET puntos_disponibles = ?
        WHERE usuario_id = ?
        """, (
            nuevos_puntos,
            usuario_id
        ))

        conexion.commit()

        # EMBED 3
        embed3 = discord.Embed(
            title="⊂📊 ▻ PUNTOS ACTUALIZADOS",
            description=(
                f"✅ +{puntos} puntos "
                f"añadidos a "
                f"{stat.upper()}"
            ),
            color=0x00ff00
        )

        embed3.set_footer(
            text=(
                f"Puntos restantes: "
                f"{nuevos_puntos}"
            )
        )

        await ctx.send(embed=embed3)