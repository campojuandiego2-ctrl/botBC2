import discord
from discord.ext import commands
import random

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def raza(ctx):

        razas = [

            {
                "nombre": "Humano",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Humano.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha decidido "
                    "que pertenezcas a la raza Humana, seres "
                    "conocidos por su capacidad de adaptación, "
                    "ambición y enorme potencial dentro del "
                    "mundo mágico. Su diversidad les ha permitido "
                    "sobresalir en incontables caminos.*"
                ),

                "probabilidad": 55,

                "color": 0xB0C4DE,

                "gif": "https://cdn.discordapp.com/attachments/1447332084577210410/1513293852117831730/47B039E5-3B3A-4289-93B6-B919AB4F9799.gif?ex=6a273439&is=6a25e2b9&hm=cc8ecf69345db3b2157b9bee125206e38d403feca60f443c90c2a800fe1de133"
            },

            {
                "nombre": "Enano",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Enano.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha decidido "
                    "otorgarte la sangre de los Enanos, una "
                    "raza reconocida por su resistencia, "
                    "fortaleza y gran habilidad para la "
                    "creación y manejo de recursos mágicos.*"
                ),

                "probabilidad": 15,

                "color": 0x8B4513,

                "gif": "https://cdn.discordapp.com/attachments/1452748369914237100/1504318628751868014/dYJSrGr_-_Imgur.gif?ex=6a26da25&is=6a2588a5&hm=2a26d3931d4503e33d27575902364478a5e19fc2a67692b383b6d91121c1ddb1"
            },

            {
                "nombre": "Bruja",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Bruja.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha decidido "
                    "concederte el linaje de una Bruja, seres "
                    "ligados profundamente al mana y reconocidos "
                    "por sus extrañas habilidades, conocimientos "
                    "mágicos y afinidad con hechizos únicos.*"
                ),

                "probabilidad": 20,

                "color": 0x800080,

                "gif": "https://cdn.discordapp.com/attachments/1452748369914237100/1504318377320124506/undefined_-_Imgur.gif?ex=6a26d9ea&is=6a25886a&hm=3c97ece2a2cd5a2f553f60043c47aba46e8a9d2aa57665180428822edf8a62d5"
            },

            {
                "nombre": "Elfo",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Elfo.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha decidido "
                    "bendecirte con la sangre de los Elfos, "
                    "una raza admirada por su inmenso poder "
                    "mágico y extraordinaria conexión con el "
                    "mana natural.*"
                ),

                "probabilidad": 10,

                "color": 0x00FF7F,

                "gif": "https://cdn.discordapp.com/attachments/1452748369914237100/1504318883438264511/5bjrZzO_-_Imgur.gif?ex=6a26da62&is=6a2588e2&hm=e1926f126af4a492a5e9b22221b64a90df827dc5ceab09226096bd0173c72432"
            }
        ]

        resultado = random.choices(

            razas,

            weights=[
                r["probabilidad"]
                for r in razas
            ],

            k=1

        )[0]

        embed = discord.Embed(

            description=resultado["mensaje"],

            color=resultado["color"]
        )

        # GIF
        embed.set_image(
            url=resultado["gif"]
        )

        await ctx.send(embed=embed)