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
        puntos_disponibles = jugador["puntos_disponibles"]

        fuerza = jugador["fuerza"]
        vitalidad = jugador["vitalidad"]
        agilidad = jugador["agilidad"]
        mana = jugador["mana"]
        inteligencia = jugador["inteligencia"]
        poder_magico = jugador["poder_magico"]

        estrellas = jugador["estrellas"]
        rango = jugador["rango"]
        misiones = jugador["misiones"]

        # VIDA Y MANA REALES
        vida = vitalidad * 5
        mana_total = mana * 5

        # DEFENSA MÁGICA
        defensa_magica = (
            vida + poder_magico
        ) // 2

        # TOTAL STATS
        estadisticas_totales = (
            fuerza
            + vida
            + agilidad
            + mana_total
            + inteligencia
            + poder_magico
            + defensa_magica
        )

        # EMBED
        embed = discord.Embed(
    title=f"⊂📊⊃ Estadísticas de {ctx.author.display_name}",
    color=0x5865F2
        )

        # FOTO PERFIL
        embed.set_thumbnail(
            url=ctx.author.avatar.url
        )

        # DESCRIPCION
        embed.description = f"""
> -# ⊩┇RANK: **{rango}**

╰┈➤ `🧮` **STATS BASE**
> -# ⊩┇FUERZA: **{fuerza}**
> -# ⊩┇VITALIDAD: **{vitalidad}**
> -# ⊩┇AGILIDAD: **{agilidad}**
> -# ⊩┇MANA: **{mana}**
> -# ⊩┇INTELIGENCIA: **{inteligencia}**
> -# ⊩┇PODER MÁGICO: **{poder_magico}**

╰┈➤ `🎯` **TOTAL STATS**
> -# ⊩┇FUERZA: **{fuerza}**
> -# ⊩┇VIDA: **{vida}**
> -# ⊩┇AGILIDAD: **{agilidad}**
> -# ⊩┇MANA: **{mana_total}**
> -# ⊩┇INTELIGENCIA: **{inteligencia}**
> -# ⊩┇PODER MÁGICO: **{poder_magico}**
> -# ⊩┇DEFENSA MÁGICA: **{defensa_magica}**

╰┈➤ `📍` **OFF-ROL**
> -# ⊩┇Puntos Disponibles: **{puntos_disponibles}**
> -# ⊩┇Estadísticas Totales: **{estadisticas_totales}**
> -# ⊩┇Estrellas: **{estrellas}**
> -# ⊩┇Misiones Completadas: **{misiones}**
"""

        await ctx.send(embed=embed)