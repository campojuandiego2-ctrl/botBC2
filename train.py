import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    # CREAR COLUMNAS SI NO EXISTEN
    try:

        cursor.execute("""
        ALTER TABLE jugadores
        ADD COLUMN entrenamientos INTEGER
        """)

    except:
        pass

    try:

        cursor.execute("""
        ALTER TABLE jugadores
        ADD COLUMN ultimo_entrenamiento TEXT
        """)

    except:
        pass

    conexion.commit()

    @bot.command()
    async def train(ctx):

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
        puntos_actuales = jugador[1]

        entrenamientos = jugador[12]
        ultimo_entrenamiento = jugador[13]

        # SI ES NULL
        if entrenamientos is None:
            entrenamientos = 0

        ahora = datetime.now()

        # SI ES NULL
        if ultimo_entrenamiento is None:

            ultimo_entrenamiento = (
                ahora - timedelta(hours=7)
            )

        else:

            ultimo_entrenamiento = datetime.fromisoformat(
                ultimo_entrenamiento
            )

        # RESETEAR ENTRENAMIENTOS
        if ahora.date() != ultimo_entrenamiento.date():

            entrenamientos = 0

        # LIMITE DIARIO
        if entrenamientos >= 2:

            embed = discord.Embed(
                description=(
                    "<a:time:1512589244378644550> "
                    "Alcanzaste el límite "
                    "de entrenamientos diarios.\n\n"
                    "Tus entrenamientos "
                    "se reiniciarán al "
                    "comenzar un nuevo día."
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed)
            return

        # COOLDOWN
        diferencia = (
            ahora - ultimo_entrenamiento
        )

        if diferencia < timedelta(hours=6):

            restante = (
                timedelta(hours=6)
                - diferencia
            )

            horas = restante.seconds // 3600

            minutos = (
                restante.seconds % 3600
            ) // 60

            embed = discord.Embed(
                description=(
                    "<a:time:1512589244378644550> "
                    "Debes esperar "
                    "para volver a entrenar.\n\n"
                    f"Tiempo restante: "
                    f"**{horas}h {minutos}m**"
                ),
                color=0xff0000
            )

            await ctx.send(embed=embed)
            return

        # PROBABILIDADES
        probabilidades = random.randint(1, 100)

        if probabilidades <= 20:

            recompensa = 2

        elif probabilidades <= 60:

            recompensa = 3

        elif probabilidades <= 90:

            recompensa = 4

        else:

            recompensa = 5

        nuevos_puntos = (
            puntos_actuales + recompensa
        )

        nuevos_entrenamientos = (
            entrenamientos + 1
        )

        # ACTUALIZAR DATOS
        cursor.execute("""
        UPDATE jugadores
        SET puntos_disponibles = ?,
            entrenamientos = ?,
            ultimo_entrenamiento = ?
        WHERE usuario_id = ?
        """, (
            nuevos_puntos,
            nuevos_entrenamientos,
            ahora.isoformat(),
            usuario_id
        ))

        conexion.commit()

        # EMBED FINAL
        embed = discord.Embed(
            title="⊂🏋️ ▻ Training Complete",
            description=(
                f"{ctx.author.mention} "
                "ha completado una sesión "
                "de entrenamiento."
            ),
            color=0x00ff00
        )

        embed.add_field(
            name="📊 Stats Obtenidas",
            value=f"+{recompensa}",
            inline=True
        )

        embed.add_field(
            name="📖 Entrenamientos",
            value=f"{nuevos_entrenamientos}/2",
            inline=True
        )

        embed.add_field(
            name="⏰ Próximo entrenamiento",
            value="En 6 horas",
            inline=True
        )

        embed.set_footer(
            text=(
                f"Progreso Registrado para "
                f"{ctx.author.display_name}"
            )
        )

        await ctx.send(embed=embed)