import discord
from discord.ext import commands

def setup(bot):

    @bot.command()
    async def count(ctx, *, mensaje=None):

        # SI RESPONDE A UN MENSAJE
        if ctx.message.reference:

            mensaje_referenciado = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )

            texto = mensaje_referenciado.content

        # SI ESCRIBE TEXTO NORMAL
        elif mensaje:

            texto = mensaje

        else:

            return await ctx.send(
                "Debes escribir un mensaje o responder a uno."
            )

        cantidad = len(texto)

        embed = discord.Embed(

            description=(

                f"⊂📊 ▻ **CHARACTER VERIFIER**\n\n"

                f"mensaje de {ctx.author.mention}"
            ),

            color=0xFF0000
        )

        embed.set_footer(
            text=f"🧮 caracteres totales: {cantidad}"
        )

        await ctx.send(embed=embed)