import discord

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def removestats(
        ctx,
        miembro: discord.Member,
        stat=None,
        puntos=None
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
        if stat is None or puntos is None:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Uso correcto:\n"
                    "-removestats "
                    "@usuario fuerza 10"
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
                    "<a:error:1512895443250577629> "
                    "Stat inválida."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        # CONVERTIR PUNTOS
        try:

            puntos = int(puntos)

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

        indice = stats_validas[stat]

        valor_actual = jugador[indice]

        # EVITAR NEGATIVOS
        if puntos > valor_actual:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "No puedes remover "
                    "más puntos de los existentes."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed_error)
            return

        nuevo_valor = (
            valor_actual - puntos
        )

        puntos_disponibles = jugador[1]

        nuevos_puntos = (
            puntos_disponibles + puntos
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

        # EMBED FINAL
        embed = discord.Embed(
            title="⊂📊 ▻ STATS REMOVIDAS",
            description=(
                f"✅ Se removieron "
                f"**{puntos}** puntos de "
                f"**{stat.upper()}** "
                f"a {miembro.mention} "
                f"con éxito."
            ),
            color=0xff0000
        )

        embed.set_footer(
            text=(
                f"Puntos disponibles: "
                f"{nuevos_puntos}"
            )
        )

        await ctx.send(embed=embed)