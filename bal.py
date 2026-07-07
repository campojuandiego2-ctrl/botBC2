import discord

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def bal(ctx):

        usuario_id = ctx.author.id

        # BUSCAR JUGADOR
        cursor.execute("""
        SELECT *
        FROM jugadores
        WHERE usuario_id = ?
        """, (usuario_id,))

        jugador = cursor.fetchone()

        # SI NO EXISTE
        if jugador is None:

            crear_jugador(usuario_id)

            cursor.execute("""
            SELECT *
            FROM jugadores
            WHERE usuario_id = ?
            """, (usuario_id,))

            jugador = cursor.fetchone()

        # DATOS
        oro = jugador["oro"]
        exp = jugador["exp"]
        estrellas = jugador["estrellas"]

        # TOP GLOBAL
        cursor.execute("""
        SELECT usuario_id
        FROM jugadores
        ORDER BY oro DESC
        """)

        ranking = cursor.fetchall()

        top = 1

        for posicion, fila in enumerate(ranking, start=1):

            if fila["usuario_id"] == usuario_id:

                top = posicion
                break

        # EMBED
               # EMBED
        embed = discord.Embed(

            title=f"﹒⊂BALANCE⊃ de {ctx.author.display_name}",

            color=0xF1C40F

        )

        # MEDALLA DEL TOP
        if top == 1:
            emoji_top = "🥇"
        elif top == 2:
            emoji_top = "🥈"
        elif top == 3:
            emoji_top = "🥉"
        else:
            emoji_top = "🏅"

        # DESCRIPCIÓN
        embed.description = f"""
<:moneda:1523753650529239210> Moneda: **{oro}**
<:EXP:1523754729379860570> EXP: **{exp}**
⭐️ Estrellas: **{estrellas}**

-# {emoji_top} Rango Global: **Top #{top}**
"""

        # ENVIAR
        await ctx.send(
            embed=embed
        )