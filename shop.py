import discord
from discord.ext import commands

# ==========================================
# PAGINAS DE LA TIENDA
# ==========================================

PAGINAS = [

    {
        "titulo": "🏇 OBJETOS",
        "contenido": """
## ﹒⊂SHOP⊃﹑ `🏇` OBJETOS

-# Usa `-buy "nombre del item"` para comprar.
-# Usa `-infoitem "nombre del item"` para ver la información.

`➤` **❝ Escoba Mágica ❞**
`250 Monedas`

`➤` **❝ Herramienta de Comunicación ❞**
`300 Monedas`

`➤` **❝ Varita Mágica ❞**
`400 Monedas`

`➤` **❝ Arma Mágica ❞**
`600 Monedas`

`➤` **❝ Armadura de Combate ❞**
`800 Monedas`
"""
    },

    {
        "titulo": "🏇 PÍLDORAS",
        "contenido": """
## ﹒⊂SHOP⊃﹑ `🏇` PÍLDORAS

-# Usa `-buy "nombre del item"` para comprar.
-# Usa `-infoitem "nombre del item"` para ver la información.

`➤` **❝ Píldora STR ❞**
`500 Monedas`

`➤` **❝ Píldora AGI ❞**
`500 Monedas`

`➤` **❝ Píldora RES ❞**
`500 Monedas`

`➤` **❝ Píldora MANA ❞**
`500 Monedas`

`➤` **❝ Píldora PM ❞**
`500 Monedas`

`➤` **❝ Poción de Mana ❞**
`750 Monedas`

`➤` **❝ Poción de Vida ❞**
`750 Monedas`

`➤` **❝ Poción de PM ❞**
`750 Monedas`
"""
    },

    {
        "titulo": "🏇 PERGAMINOS",
        "contenido": """
## ﹒⊂SHOP⊃﹑ `🏇` PERGAMINOS

-# Usa `-buy "nombre del item"` para comprar.
-# Usa `-infoitem "nombre del item"` para ver la información.

`➤` **❝ Pergamino de Hechizo [E] ❞**
`1.000 Monedas`

`➤` **❝ Pergamino de Hechizo [D] ❞**
`2.500 Monedas`

`➤` **❝ Pergamino de Hechizo [C] ❞**
`5.000 Monedas`

`➤` **❝ Pergamino de Hechizo [B] ❞**
`10.000 Monedas`

`➤` **❝ Pergamino de Hechizo [A] ❞**
`20.000 Monedas`
"""
    },

    {
        "titulo": "🏇 CASAS",
        "contenido": """
## ﹒⊂SHOP⊃﹑ `🏇` CASAS

-# Usa `-buy "nombre del item"` para comprar.
-# Usa `-infoitem "nombre del item"` para ver la información.

`➤` **❝ Casa Pequeña ❞**
`2.500 Monedas`

`➤` **❝ Casa Mediana ❞**
`5.000 Monedas`

`➤` **❝ Mansión ❞**
`10.000 Monedas`

`➤` **❝ Castillo ❞**
`20.000 Monedas`
"""
    },

    {
        "titulo": "🏇 EXP",
        "contenido": """
## ﹒⊂SHOP⊃﹑ `🏇` EXP

-# Usa `-buy "nombre del item"` para comprar.
-# Usa `-infoitem "nombre del item"` para ver la información.

`➤` **❝ 1 Punto de Estadística ❞**
`20 EXP`

`➤` **❝ Training Express ❞**
`150 EXP`

`➤` **❝ Reinicio de Estadísticas ❞**
`300 EXP`

`➤` **❝ Ticket de Evento ❞**
`400 EXP`

`➤` **❝ Pergamino Aleatorio ❞**
`600 EXP`

`➤` **❝ Cambio de Atributo Mágico ❞**
`1.000 EXP`

`➤` **❝ Pergamino de Evolución ❞**
`1.500 EXP`
"""
    }

]

# ==========================================
# CREAR EMBED
# ==========================================

def crear_embed(pagina):

    embed = discord.Embed(

        description=PAGINAS[pagina]["contenido"],

        color=0x5865F2

    )

    embed.set_footer(

        text=f"Página {pagina + 1} de {len(PAGINAS)}"

    )

    return embed

# ==========================================
# SHOP VIEW
# ==========================================

class ShopView(discord.ui.View):

    def __init__(self, autor):

        super().__init__(timeout=None)

        self.autor = autor
        self.pagina = 0    # ==========================
    # ACTUALIZAR BOTONES
    # ==========================

    def actualizar_botones(self):

        self.boton_anterior.disabled = (
            self.pagina == 0
        )

        self.boton_siguiente.disabled = (
            self.pagina == len(PAGINAS) - 1
        )

    # ==========================
    # BOTON ANTERIOR
    # ==========================

    @discord.ui.button(
        emoji="⬅️",
        style=discord.ButtonStyle.secondary,
        disabled=True
    )
    async def boton_anterior(

        self,

        interaction: discord.Interaction,

        button: discord.ui.Button

    ):

        # SOLO EL AUTOR
        if interaction.user != self.autor:

            await interaction.response.send_message(

                "⚠️ Solo quien abrió la tienda puede cambiar de página.",

                ephemeral=True

            )

            return

        # PAGINA
        self.pagina -= 1

        # BOTONES
        self.actualizar_botones()

        # EDITAR
        await interaction.response.edit_message(

            embed=crear_embed(

                self.pagina

            ),

            view=self

        )

    # ==========================
    # BOTON SIGUIENTE
    # ==========================

    @discord.ui.button(
        emoji="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def boton_siguiente(

        self,

        interaction: discord.Interaction,

        button: discord.ui.Button

    ):

        # SOLO EL AUTOR
        if interaction.user != self.autor:

            await interaction.response.send_message(

                "⚠️ Solo quien abrió la tienda puede cambiar de página.",

                ephemeral=True

            )

            return

        # PAGINA
        self.pagina += 1

        # BOTONES
        self.actualizar_botones()

        # EDITAR
        await interaction.response.edit_message(

            embed=crear_embed(

                self.pagina

            ),

            view=self

        )# ==========================================
# COMANDO SHOP
# ==========================================

def setup(
    bot,
    cursor,
    conexion,
    crear_jugador
):

    @bot.command()
    async def shop(ctx):

        view = ShopView(
            ctx.author
        )

        view.actualizar_botones()

        await ctx.send(

            embed=crear_embed(0),

            view=view

        )