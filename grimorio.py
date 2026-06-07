import discord
from discord.ext import commands
import random

def setup(bot):

    @bot.command()
    async def grimorio(ctx):

        grimorios = [

            {
                "nombre": "Grimorio de 3 Hojas",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Grimorio de 3 Hojas.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha decidido "
                    "otorgarte un Grimorio de 3 Hojas, símbolo "
                    "de esperanza, fe y amor. Este tipo de "
                    "grimorio es el más común dentro del Reino "
                    "Clover, utilizado por innumerables magos "
                    "para recorrer su propio camino.*"
                ),

                "probabilidad": 85,

                "color": 0x2ECC71,

                "gif": "https://cdn.discordapp.com/attachments/1452748369914237100/1513298274067419207/IMG_0762.jpg?ex=6a273858&is=6a25e6d8&hm=763fdb19d093107282ed65d7e7b99636fa2d503628a9c15e2bc70f4d6eeca3d6"
            },

            {
                "nombre": "Grimorio de 4 Hojas",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Grimorio de 4 Hojas.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino te ha bendecido "
                    "con un raro Grimorio de 4 Hojas, reconocido "
                    "como símbolo de buena fortuna y un talento "
                    "mágico excepcional. Muy pocos son elegidos "
                    "por este distinguido poder dentro del reino.*"
                ),

                "probabilidad": 15,

                "color": 0xFFD700,

                "gif": "https://cdn.discordapp.com/attachments/1452748369914237100/1513298263644573888/IMG_0763.jpg?ex=6a273855&is=6a25e6d5&hm=75cbb6a324bdd2acb31b6b8847ffa7897c04bf853b19f2b13ad57689987ee462"
            }
        ]

        resultado = random.choices(

            grimorios,

            weights=[
                g["probabilidad"]
                for g in grimorios
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