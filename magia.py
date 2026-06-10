import discord
from discord.ext import commands
import random

def setup(bot):

    @bot.command()
    async def magia(ctx):

        rand = random.randint(1, 100)

        # MAGIA COMÚN
        if rand <= 50:

            embed = discord.Embed(
                description=(
                    f"# *— ૮`⭐️`୭ Mi elección es…. Magia Común.๑ {ctx.author.mention}*\n\n"
                    "*Eres un usuario cuya magia es complicada sobresalir sobre la mayoría "
                    "de todas las que hay, te espera un largo y duro camino por delante, "
                    "solo tú convicción va a ser tú acompañante ante este desafiante mundo mágico*"
                ),
                color=0xA9A9A9
            )

            embed.set_image(
                url="https://imgur.com/a/kxHince"
            )

            await ctx.send(embed=embed)

        # MAGIA RARA
        elif rand <= 85:

            embed = discord.Embed(
                description=(
                    f"# *— ૮`⭐️`୭ Mi elección es…. Magia Rara.๑ {ctx.author.mention}*\n\n"
                    "*Vaya, lograste adquirir una magia cuya rareza se separa del promedio, "
                    "igual no te confíes, habrán desafíos y retos los cuáles tendrás que "
                    "enfrentarte, prepárate*"
                ),
                color=0x3498DB
            )

            embed.set_image(
                url="https://imgur.com/a/ltj6EWY"
            )

            await ctx.send(embed=embed)

        # MAGIA ÉPICA
        elif rand <= 95:

            embed = discord.Embed(
                description=(
                    f"# *— ૮`⭐️`୭ Mi elección es…. Magia Épica.๑ {ctx.author.mention}*\n\n"
                    "*Felicidades, fuiste afortunado de ser bendecido con una magia fuera "
                    "de la categoría común, con esto podrás emprender tu aventura, "
                    "poner cara en frente y desafiar este mundo*"
                ),
                color=0x9B59B6
            )

            embed.set_image(
                url="https://imgur.com/a/TR5LAv3"
            )

            await ctx.send(embed=embed)

        # MAGIA LEGENDARIA
        else:

            embed = discord.Embed(
                description=(
                    f"# *— ૮`⭐️`୭ Mi elección es…. Magia Legendaria.๑ {ctx.author.mention}*\n\n"
                    "*Tu magia pertenece al nivel de las leyendas, un poder que pocos llegan "
                    "a despertar. Desde ahora, el destino pondrá frente a ti pruebas dignas "
                    "de alguien excepcional.*"
                ),
                color=0xFFD700
            )

            embed.set_image(
                url="https://i.imgur.com/PGygtA7.gif"
            )

            await ctx.send(embed=embed)