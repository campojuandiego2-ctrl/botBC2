import discord

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def addpoints(
        ctx,
        miembro: discord.Member,
        puntos=None
    ):

        # VERIFICAR PERMISOS
        if not (
            ctx.author.guild_permissions.administrator
            or any(
                role.name in [
                    "❪🍷 ❫  ❱❱ Administrador",
                    "❪🍷 ❫  ❱❱ Moderador",
                    "❪🍷 ❫  ❱❱ Game Masters"
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
        if puntos is None:

            embed_error = discord.Embed(
                description=(
                    "<a:error:1512895443250577629> "
                    "Uso correcto:\n"
                    "-addpoints @usuario 10"
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

        puntos_actuales = jugador[1]

        nuevos_puntos = (
            puntos_actuales + puntos
        )

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
            title="⊂📊 ▻ PUNTOS AÑADIDOS",
            description=(
                f"✅ Se añadieron "
                f"**{puntos}** puntos "
                f"disponibles a "
                f"{miembro.mention} "
                f"con éxito."
            ),
            color=0x00ff00
        )

        embed.set_footer(
            text=(
                f"Puntos disponibles: "
                f"{nuevos_puntos}"
            )
        )

        await ctx.send(embed=embed)