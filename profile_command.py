import discord

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def profile(ctx):

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

        # DATOS
        puntos_disponibles = jugador[1]

        fuerza = jugador[2]
        resistencia = jugador[3]
        agilidad = jugador[4]
        mana = jugador[5]
        poder_magico = jugador[6]

        slot_hechizo = jugador[7]
        evoluciones = jugador[8]

        estrellas = jugador[9]
        rango = jugador[10]
        misiones = jugador[11]

        # DEFENSA MAGICA
        defensa_magica = (
            resistencia + poder_magico
        ) // 2

        # TOTAL STATS
        estadisticas_totales = (
            fuerza
            + resistencia
            + agilidad
            + mana
            + poder_magico
        )

        # EMBED
        embed = discord.Embed(
            title=(
                f"⊂📊` ▻ Profile de "
                f"{ctx.author.display_name}"
            ),
            color=0x5865F2
        )

        # FOTO PERFIL
        embed.set_thumbnail(
            url=ctx.author.avatar.url
        )

        # DESCRIPCION
        embed.description = f"""
-# **Puntos Disponibles:** {puntos_disponibles}
-# **Estadísticas Totales:** {estadisticas_totales}

╰┈➤ `🧮` **STATS BASE**
> -# ⊩┇FUERZA: **{fuerza}**
> -# ⊩┇RESISTENCIA: **{resistencia}**
> -# ⊩┇AGILIDAD: **{agilidad}**
> -# ⊩┇MANA: **{mana}**
> -# ⊩┇PODER MÁGICO: **{poder_magico}**

╰┈➤ `🛡️` **DEFENSAS**
> -# ⊩┇DEFENSA MÁGICA: **{defensa_magica}**

╰┈➤ `📕` **GRIMORIO**
> -# ⊩┇SLOTS DE HECHIZO: **{slot_hechizo}**
> -# ⊩┇EVOLUCIONES: **{evoluciones}**

╰┈➤ `🎯` **PROGRESO**
> -# ⊩┇ESTRELLAS: **{estrellas}**
> -# ⊩┇RANK: **{rango}**
> -# ⊩┇MISIONES COMPLETADAS: **{misiones}**
"""

        await ctx.send(embed=embed)