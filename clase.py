import discord
from discord.ext import commands
import random

def setup(bot):

    @bot.command()
    async def clase(ctx):

        clases = [

            {
                "nombre": "Plebeyo",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Plebeyo.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha hablado y parece "
                    "que te ha tocado nacer como un Plebeyo. "
                    "Son conocidos por su perseverancia y esfuerzo, "
                    "demostrando que incluso alguien común puede "
                    "alcanzar grandes objetivos en este vasto "
                    "mundo mágico.*"
                ),

                "probabilidad": 60,

                "color": 0x808080,

                "gif": "https://cdn.discordapp.com/attachments/1447814353268248769/1513296885870493777/A50DB257-C9DD-4733-998B-D9A60EBDA5EF.gif?ex=6a27370d&is=6a25e58d&hm=ba0c5cff9ddf056eb9dfecfaabb2c45db1d2d9f37e9007aa7eda11e8c1fee40a"
            },

            {
                "nombre": "Noble",

                "mensaje": (
                    f"# *— Mi elección es…. "
                    f"Noble.๑ {ctx.author.mention}*\n\n"

                    "*¡Felicidades! El destino ha decidido otorgarte "
                    "el linaje de un Noble, individuos reconocidos "
                    "por su gran poder mágico, prestigio y posición "
                    "dentro del reino. Muchos esperan grandes cosas "
                    "de aquellos nacidos bajo esta distinguida sangre.*"
                ),

                "probabilidad": 40,

                "color": 0xFFD700,

                "gif": "https://cdn.discordapp.com/attachments/1447332084577210410/1504901129358544996/e31cd8e08bf7383c5f1fd9ec28897441.gif?ex=6a26fe64&is=6a25ace4&hm=9f2f9095472592fcf07d921e2f99427ea16ca38ee6603dae7cee101a14f8da13"
            }
        ]

        resultado = random.choices(

            clases,

            weights=[
                c["probabilidad"]
                for c in clases
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