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

# PERMITE ACCEDER A LAS COLUMNAS POR NOMBRE
conexion.row_factory = sqlite3.Row

cursor = conexion.cursor()

# TABLA JUGADORES
cursor.execute("""
CREATE TABLE IF NOT EXISTS jugadores (

    usuario_id INTEGER,
    oro INTEGER,
    exp INTEGER,
    puntos_disponibles INTEGER,

    fuerza INTEGER,
    vitalidad INTEGER,
    agilidad INTEGER,
    mana INTEGER,
    inteligencia INTEGER,
    poder_magico INTEGER,

    estrellas INTEGER,
    rango TEXT,
    misiones INTEGER,

    entrenamientos INTEGER,
    ultimo_entrenamiento TEXT

)
""")

conexion.commit()
# TABLA INVENTARIO
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario (

    usuario_id INTEGER,

    objeto TEXT,

    cantidad INTEGER

)
""")

conexion.commit()

# CREAR JUGADOR
def crear_jugador(usuario_id):

    cursor.execute("""
    INSERT INTO jugadores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        usuario_id,

        500,      # Oro
        0,      # EXP
        30,

        0,  # Fuerza
        0,  # Vitalidad
        0,  # Agilidad
        0,  # Mana
        0,  # Inteligencia
        0,  # Poder Mágico

        0,              # Estrellas
        "Unranked",     # Rango
        0,              # Misiones

        0,              # Entrenamientos
        None            # Último entrenamiento

    ))

    conexion.commit()
       

# IMPORTAR COMANDOS
import profile_command
import editstats
import removestats
import addpoints
import removepoints
import train
import use
import addrank
import count
import prueba
import mision
import canales
import roles
import saycomands
import shop
import bal

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

shop.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)

bal.setup(
    bot,
    cursor,
    conexion,
    crear_jugador
)
count.setup(bot)
prueba.setup(bot)
mision.setup(bot)
canales.setup(bot)
roles.setup(bot) 
saycomands.setup(bot)

# BOT ONLINE
@bot.event
async def on_ready():

    print(f"Conectado como {bot.user}")

# TOKEN
bot.run(os.getenv("TOKEN"))