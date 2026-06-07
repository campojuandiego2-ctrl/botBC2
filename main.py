import discord
from discord.ext import commands
import sqlite3
import os

# CONFIG BOT
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="-",
    intents=intents
)

# BASE DE DATOS
conexion = sqlite3.connect("rpg.db")
cursor = conexion.cursor()

# TABLA JUGADORES
cursor.execute("""
CREATE TABLE IF NOT EXISTS jugadores (

    usuario_id INTEGER,

    puntos_disponibles INTEGER,

    fuerza INTEGER,
    resistencia INTEGER,
    agilidad INTEGER,
    mana INTEGER,
    poder_magico INTEGER,

    slot_hechizo INTEGER,
    evoluciones INTEGER,

    estrellas INTEGER,
    rango TEXT,
    misiones INTEGER,

    entrenamientos INTEGER,
    ultimo_entrenamiento TEXT
)
""")

conexion.commit()

# CREAR JUGADOR
def crear_jugador(usuario_id):

    cursor.execute("""
    INSERT INTO jugadores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        usuario_id,

        50,

        0,
        0,
        0,
        0,
        0,

        0,
        0,

        0,
        "Unranked",
        0,

        0,
        None
    ))

    conexion.commit()

# IMPORTAR COMANDOS
import addevolution
import profile_command
import editstats
import removestats
import addpoints
import removepoints
import train
import addslots
import use
import addrank
import count

# SETUP COMANDOS
profile_command.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

editstats.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

removestats.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

addpoints.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

removepoints.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

train.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

addslots.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

addevolution.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

use.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

addrank.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

count.setup(bot)

# BOT ONLINE
@bot.event
async def on_ready():

    print(f"Conectado como {bot.user}")

# TOKEN
bot.run(os.getenv("TOKEN"))