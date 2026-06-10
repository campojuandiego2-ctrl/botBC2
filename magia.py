import discord
from discord.ext import commands
import random

def setup(bot):

    @bot.command()
    async def magia(ctx):

        rand = random.randint(1, 100)

        # MAGIA COMÚN
        if rand <= 50:

            await ctx.send(

                f"# *— ૮`⭐️`୭ Mi elección es…. Magia Común.๑ {ctx.author.mention}*\n\n"

                "*Eres un usuario cuya magia es complicada sobresalir sobre la mayoría "
                "de todas las que hay, te espera un largo y duro camino por delante, "
                "solo tú convicción va a ser tú acompañante ante este desafiante mundo mágico*\n\n"

                "> **IMG:** https://imgur.com/a/kxHince"

            )

        # MAGIA RARA
        elif rand <= 85:

            await ctx.send(

                f"# *— ૮`⭐️`୭ Mi elección es…. Magia Rara.๑ {ctx.author.mention}*\n\n"

                "*Vaya, lograste adquirir una magia cuya rareza se separa del promedio, "
                "igual no te confíes, habrán desafíos y retos los cuáles tendrás que "
                "enfrentarte, prepárate*\n\n"

                "> **IMG:** https://imgur.com/a/ltj6EWY"

            )

        # MAGIA ÉPICA
        elif rand <= 95:

            await ctx.send(

                f"# *— ૮`⭐️`୭ Mi elección es…. Magia Épica.๑ {ctx.author.mention}*\n\n"

                "*Felicidades, fuiste afortunado de ser bendecido con una magia fuera "
                "de la categoría común, con esto podrás emprender tu aventura, "
                "poner cara en frente y desafiar este mundo*\n\n"

                "> **IMG:** https://imgur.com/a/TR5LAv3"

            )

        # MAGIA LEGENDARIA
        else:

            await ctx.send(

                f"# *— ૮`⭐️`୭ Mi elección es…. Magia Legendaria.๑ {ctx.author.mention}*\n\n"

                "*Tu magia pertenece al nivel de las leyendas, un poder que pocos llegan "
                "a despertar. Desde ahora, el destino pondrá frente a ti pruebas dignas "
                "de alguien excepcional.*\n\n"

                "> **IMG:** https://i.imgur.com/PGygtA7.gif"

            )