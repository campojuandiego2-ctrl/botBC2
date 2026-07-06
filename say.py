import discord
from discord.ext import commands
import unicodedata

def setup(bot):

    # ==========================
    # FUNCIONES AUXILIARES
    # ==========================

    def limpiar(texto):

        texto = "".join(

            c for c in unicodedata.normalize(
                "NFD",
                texto
            )

            if unicodedata.category(c) != "Mn"

        )

        texto = (
            texto
            .lower()
            .replace(".", "")
            .replace(",", "")
            .replace("#", "")
            .replace("│", "")
            .replace("┃", "")
            .replace("・", "")
            .replace("•", "")
            .replace("✦", "")
            .replace("✧", "")
            .replace("─", "")
            .replace("—", "")
            .strip()
        )

        return texto


    def buscar_canal(guild, texto):

        # SI ES MENCION
        if texto.startswith("<#") and texto.endswith(">"):

            canal_id = int(
                texto.replace("<#", "").replace(">", "")
            )

            return guild.get_channel(canal_id)

        texto = limpiar(texto)

        for canal in guild.text_channels:

            nombre = limpiar(canal.name)

            if texto in nombre:

                return canal

        return None


    @bot.command()
    @commands.has_permissions(administrator=True)
    async def say(ctx):

        def check(m):

            return (
                m.author == ctx.author
                and m.channel == ctx.channel
            )

        # ==========================
        # MENU
        # ==========================

        await ctx.send(

            "**¿Qué deseas enviar?**\n\n"

            "`1.` Texto normal\n"
            "`2.` Embed\n"
            "`3.` Copiar un mensaje"

        )

        opcion = await bot.wait_for(

            "message",

            check=check

        )

        opcion = opcion.content.strip()

        # ==========================
        # OPCION 1
        # ==========================

        if opcion == "1":

            await ctx.send(

                "📝 Escribe el mensaje."

            )

            mensaje = await bot.wait_for(

                "message",

                check=check

            )

            contenido = mensaje.content

            await ctx.send(

                "📍 ¿En qué canal?"

            )

            canal_msg = await bot.wait_for(

                "message",

                check=check

            )

            canal = buscar_canal(

                ctx.guild,

                canal_msg.content

            )

            if canal is None:

                await ctx.send(

                    "❌ No encontré ese canal."

                )

                return

            await canal.send(

                contenido

            )

            await ctx.send(

                "✅ Mensaje enviado."

            )        # ==========================
        # OPCION 2
        # ==========================

        elif opcion == "2":

            # TITULO
            await ctx.send(

                "📝 Escribe el título del embed."

            )

            titulo = await bot.wait_for(

                "message",

                check=check

            )

            titulo = titulo.content

            # DESCRIPCION
            await ctx.send(

                "📖 Escribe la descripción."

            )

            descripcion = await bot.wait_for(

                "message",

                check=check

            )

            descripcion = descripcion.content

            # IMAGEN
            await ctx.send(

                "🖼️ Envía el link de la imagen o escribe `omitir`."

            )

            imagen = await bot.wait_for(

                "message",

                check=check

            )

            imagen = imagen.content

            # COLOR
            await ctx.send(

                "🎨 Escribe el color hexadecimal (ej: FF0000) o escribe `omitir`."

            )

            color = await bot.wait_for(

                "message",

                check=check

            )

            color = color.content

            if color.lower() == "omitir":

                color = discord.Color.blurple()

            else:

                try:

                    color = discord.Color(
                        int(color.replace("#", ""), 16)
                    )

                except:

                    color = discord.Color.blurple()

            # CANAL
            await ctx.send(

                "📍 ¿En qué canal deseas enviarlo?"

            )

            canal_msg = await bot.wait_for(

                "message",

                check=check

            )

            canal = buscar_canal(

                ctx.guild,

                canal_msg.content

            )

            if canal is None:

                await ctx.send(

                    "❌ No encontré ese canal."

                )

                return

            embed = discord.Embed(

                title=titulo,

                description=descripcion,

                color=color

            )

            if imagen.lower() != "omitir":

                embed.set_image(

                    url=imagen

                )

            await canal.send(

                embed=embed

            )

            await ctx.send(

                "✅ Embed enviado correctamente."

            )        # ==========================
        # OPCION 3
        # ==========================

        elif opcion == "3":

            # COMPROBAR RESPUESTA
            if ctx.message.reference is None:

                await ctx.send(

                    "❌ Debes responder al mensaje que deseas copiar."

                )

                return

            try:

                mensaje_original = await ctx.channel.fetch_message(

                    ctx.message.reference.message_id

                )

            except:

                await ctx.send(

                    "❌ No pude obtener ese mensaje."

                )

                return

            # PEDIR CANAL
            await ctx.send(

                "📍 ¿A qué canal deseas copiar el mensaje?"

            )

            canal_msg = await bot.wait_for(

                "message",

                check=check

            )

            canal = buscar_canal(

                ctx.guild,

                canal_msg.content

            )

            if canal is None:

                await ctx.send(

                    "❌ No encontré ese canal."

                )

                return

            # TEXTO
            if mensaje_original.content:

                await canal.send(

                    mensaje_original.content

                )

            # EMBEDS
            for embed in mensaje_original.embeds:

                await canal.send(

                    embed=embed

                )

            # ARCHIVOS
            archivos = []

            for adjunto in mensaje_original.attachments:

                archivos.append(

                    await adjunto.to_file()

                )

            if archivos:

                await canal.send(

                    files=archivos

                )

            await ctx.send(

                "✅ Mensaje copiado correctamente."

            )

        # ==========================
        # OPCION INVALIDA
        # ==========================

        else:

            await ctx.send(

                "❌ Opción inválida."

            )