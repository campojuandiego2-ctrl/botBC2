import discord
from discord.ext import commands
import random

def setup(bot):

    @bot.command()
    async def magia(ctx):

        magias = [

            {
                "mensaje": (
                    f"# *— ૮` ⭐️ `୭ Mi elección es…. "
                    f"Magia de 1 Estrella.๑*\n"

                    f"*➤ ¡Felicidades! El destino te ha "
                    f"concedido una Magia de 1 Estrella.*"
                ),

                "probabilidad": 45,

                "color": 0x808080,

                "imagen": "https://cdn.discordapp.com/attachments/1490797969425825822/1513647665345331504/968BE6C9-D595-45CB-9F7C-2447C6114E32.png?ex=6a287dbd&is=6a272c3d&hm=a53b65e9784eecde450cb41434dcedab79ef379dc6d537e80bdfff643f995a1d&"
            },

            {
                "mensaje": (
                    f"# *— ૮` ⭐️ `୭ Mi elección es…. "
                    f"Magia de 2 Estrellas.๑*\n"

                    f"*➤ ¡Felicidades! El destino te ha "
                    f"concedido una Magia de 2 Estrellas.*"
                ),

                "probabilidad": 35,

                "color": 0x3498DB,

                "imagen": "https://cdn.discordapp.com/attachments/1490797969425825822/1513647673423560895/F8993B75-EF3A-42DA-8674-3E951B32D64D.png?ex=6a287dbf&is=6a272c3f&hm=97204d38d9804a74ae27b8ea6b91c73b89b371456658514988f4fdd75d08df10&"
            },

            {
                "mensaje": (
                    f"# *— ૮` ⭐️ `୭ Mi elección es…. "
                    f"Magia de 3 Estrellas.๑*\n"

                    f"*➤ ¡Felicidades! El destino te ha "
                    f"concedido una Magia de 3 Estrellas.*"
                ),

                "probabilidad": 15,

                "color": 0x9B59B6,

                "imagen": "https://media.discordapp.net/attachments/1447807305059012639/1513730626401075240/BF45C4FE-12B3-42BE-BAF2-4EC757239161.png?ex=6a28cb01&is=6a277981&hm=66c0849dd590ef3e81e20156749cdc4bd4e762c7d678064ed6c1563d93f6c224&=&format=webp&quality=lossless&width"
            },

            {
                "mensaje": (
                    f"# *— ૮` ⭐️ `୭ Mi elección es…. "
                    f"Magia de 4 Estrellas.๑*\n"

                    f"*➤ ¡Felicidades! El destino te ha "
                    f"concedido una Magia de 4 Estrellas.*"
                ),

                "probabilidad": 5,

                "color": 0xF1C40F,

                "imagen": "https://media.discordapp.net/attachments/1447807305059012639/1513729930142154956/F134902B-0217-46E9-9D5B-7FC7F664BFBA.png?ex=6a28ca5b&is=6a2778db&hm=a6c0305cb2f95a0824274f9cd3dc89f56fcd561fec2fce69b406b927a37671dc&=&format=webp&quality=lossless&width=1169&height=779"
            }
        ]

        resultado = random.choices(

            magias,

            weights=[
                m["probabilidad"]
                for m in magias
            ],

            k=1

        )[0]

        embed = discord.Embed(

            description=(
                f"{resultado['mensaje']}\n\n"
                f"{ctx.author.mention}"
            ),

            color=resultado["color"]
        )

        embed.set_image(
            url=resultado["imagen"]
        )

        await ctx.send(embed=embed)