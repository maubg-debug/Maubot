import re, math, random

import discord
from discord.ext import commands
from os import environ as env
import math

from termcolor import cprint
import asyncio, json

class Help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ["⏮️", "◀️", "❌", "▶️", "⏭️", "📝"] 

    async def ayuda(self, ctx, cog, cogs, paginasTotales, embed):
        cog = int(cog)
        if cog > paginasTotales or cog < 1:
            return await ctx.send(f"Numero invalido: `{cog}`. Porfavor escoje de {paginasTotales} paginas.\nO tambien lo que puedes hacer es que puedes pone {ctx.prefix}help [categoria]") 

        embed.set_footer(
            text=f"Puedes poner @Maubot#6247 para mas info | Pagina {cog} de {paginasTotales}"
        )
        embed.description = f"**Prefijos:** `{json.load(open(env['JSON_DIR'] + 'prefix.json'))[str(ctx.guild.id)]}, m., m-`\nMaubot tiene una pagina web, si quieres visitarla dale **[aqui](https://maubot.maucode.com)**\n-=-=-=-=-=-=-=-=-=-="

        CogsNecesitados = []
        for i in range(4):
            x = i + (int(cog) - 1) * 4
            try:
                CogsNecesitados.append(cogs[x])
            except IndexError as e:
                cprint(f"[Log] Un error en el commando de ayuda: {e}", 'red')
            
        for cog in CogsNecesitados:
            ListaDeComandos = ""
            cmds = 0
            for comando in self.bot.get_cog(cog).walk_commands():
        
                if comando.hidden:
                    continue

                ListaDeComandos += f"`{ctx.prefix}{comando.name}` **⦂** "
                cmds += 1
            ListaDeComandos = ListaDeComandos[:-6]
            embed.add_field(name=f"{cog} | (`{cmds}`)", value=ListaDeComandos, inline=False)
        return embed

        cprint(f"[Log] caracteres de 'help':  {len(ListaDeComandos)}", 'yellow')

    async def ayuda_reaccionada(self, ctx, cog, cogs, paginasTotales, embed):
        if int(cog) == 0 and embed is None:
            embedhs = discord.Embed(title="-=-=-=-=-= Ayuda -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")
            embedhs.description = "Si tienes alguna duda con maubot puedes verla [aqui](https://discord.gg/mwDBgubwdP)"
            embedhs.add_field(name="-=-=-=-  Buscar por paginas  -=-=-=-", value=f"En el comando de ayuda puedes buscar con las paginas poniendo `m.help <numero de pagina>` | Puedes escoger de {paginasTotales} paginas\n**eg. m.help {random.randint(2, 7)}**", inline=False)
            embedhs.add_field(name="-=-=-=-  Buscar por cogs  -=-=-=-", value=f"Si no te gustan los numeros puedes buscar por los nombres de los cogs que tendras que ir viendo entre las paginas para ver mas informacion como uso | Puedes escoger de {paginasTotales} paginas\n**eg. m.help {random.choice(cogs).lower()}**")                
            cogsL = ""
            for i in cogs:
                cogsL += f"`{i.lower()}` **|** "
            embedhs.add_field(name="-=-=-=-  Cogs  -=-=-=-", value=f"**-> e.x:** `{ctx.prefix}help [Cog]`\n\n{cogsL[:-6]}", inline=False)
            return embedhs        
        if int(cog) > int(paginasTotales):
            cog = paginasTotales
        if int(cog) < 1: 
            cog = 1
        return await self.ayuda(ctx, str(cog), cogs, paginasTotales, embed)

    @commands.command(description="Ayuda para los comandos", usage="[cog]")
    async def help(self, ctx, cog="0"):
        if cog == "0":
            embedhs = discord.Embed(title="-=-=-=-=-= Ayuda -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")
            cogs = [c for c in self.bot.cogs.keys()]
            paginasTotales = math.ceil(len(cogs) / 6)
            embedhs.description = "Si tienes alguna duda con maubot puedes verla [aqui](https://discord.gg/mwDBgubwdP)"
            embedhs.add_field(name="-=-=-=-  Buscar por paginas  -=-=-=-", value=f"En el comando de ayuda puedes buscar con las paginas poniendo `m.help <numero de pagina>` | Puedes escoger de {paginasTotales} paginas\n**eg. m.help {random.randint(2, 7)}**", inline=False)
            embedhs.add_field(name="-=-=-=-  Buscar por cogs  -=-=-=-", value=f"Si no te gustan los numeros puedes buscar por los nombres de los cogs que tendras que ir viendo entre las paginas para ver mas informacion como uso | Puedes escoger de {paginasTotales} paginas\n**eg. m.help {random.choice(cogs).lower()}**")                
            cogsL = ""
            for i in cogs:
                cogsL += f"`{i.lower()}` **|** "
            embedhs.add_field(name="-=-=-=-  Cogs  -=-=-=-", value=f"**-> e.x:** `{ctx.prefix}help [Cog]`\n\n{cogsL[:-6]}", inline=False)
            msg = await ctx.send(embed=embedhs)
            for m in self.emojis: 
                await msg.add_reaction(m)
            def _check(r, m):
                return m == ctx.author
            cogsR = int(cog)
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=_check, timeout=120.0)

                await reaction.remove(ctx.author)
                if reaction.emoji == self.emojis[0]:
                    cogsR = 1
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))
                if reaction.emoji == self.emojis[1]:
                    cogsR = int(cogsR) - 1
                    if int(cogsR) < 1: cogsR = 1
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))                        
                if reaction.emoji == self.emojis[2]:
                    await ctx.message.delete()
                    await msg.delete()
                    # await ctx.author.message.delete()
                    return                       
                if reaction.emoji == self.emojis[3]:
                    cogsR = int(cogsR) + 1
                    if int(cogsR) > paginasTotales: cogsR = paginasTotales
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))
                if reaction.emoji == self.emojis[4]:
                    cogsR = paginasTotales
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))
                if reaction.emoji == self.emojis[5]:
                    cogsR = 0
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, None))
            return

        embed = discord.Embed(title=f"-=-=-=-=-= Ayuda {cog} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")

        cogs = [c for c in self.bot.cogs.keys()]
        cprint(f"[Log] Cogs: {len(cogs)}", 'yellow')
        paginasTotales = math.ceil(len(cogs) / 6)

        if re.search(r"\d", str(cog)):

            embedh = await self.ayuda(ctx, cog, cogs, paginasTotales, embed)

            msg = await ctx.send(embed=embedh)

            for m in self.emojis: 
                await msg.add_reaction(m)

            def _check(r, m):
                return m == ctx.author
            cogsR = int(cog)
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=_check, timeout=120.0)
                await reaction.remove(ctx.author)
                if reaction.emoji == self.emojis[0]:
                    cogsR = 1
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))
                if reaction.emoji == self.emojis[1]:
                    cogsR = int(cogsR) - 1
                    if int(cogsR) < 1: cogsR = 1
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))                        
                if reaction.emoji == self.emojis[2]:
                    await ctx.message.delete()
                    await msg.delete()
                    # await ctx.author.message.delete()
                    return                       
                if reaction.emoji == self.emojis[3]:
                    cogsR = int(cogsR) + 1
                    if int(cogsR) > 9: cogsR = 9
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))
                if reaction.emoji == self.emojis[4]:
                    cogsR = paginasTotales
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, discord.Embed(title=f"-=-=-=-=-= Ayuda {cogsR} -=-=-=-=-=", color=int(env["COLOR"])).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-icon.png")))
                if reaction.emoji == self.emojis[5]:
                    cogsR = 0
                    await msg.edit(embed=await self.ayuda_reaccionada(ctx, str(cogsR), cogs, paginasTotales, None))

        elif re.search(r"[a-zA-Z]", str(cog)):
            congMinusculas = [c.lower() for c in cogs]
            if cog.lower() not in congMinusculas:
                return await ctx.send(f"Argumento invalido: `{cog}`. Porfavor escoje de {paginasTotales} paginas.\nO tambien lo que puedes hacer es que puedes pone {ctx.prefix}help [categoria]")

            embed.set_footer(
                text=f"Puedes poner @Maubot#6247 para mas info | Cog {congMinusculas.index(cog.lower())+1} de {len(congMinusculas)}"
            )

            textoDeAyuda = ""

            for comando in self.bot.get_cog(cogs[congMinusculas.index(cog.lower())]).walk_commands():
                if comando.hidden:
                    continue
                
                textoDeAyuda += "\n"

                textoDeAyuda += f"**-> {comando.name} ** (`{comando.description}`)\n"

                if len(comando.aliases) > 0:
                    c = ""
                    for i in comando.aliases:
                        c += f"`{i}` **|** "
                    textoDeAyuda += f"**Aliados -> ** {c}\n"
                textoDeAyuda += ''


                prefijo = ctx.prefix

                textoDeAyuda += f"**Formateo:** `{prefijo}{comando.name}{ ' ' + comando.usage if comando.usage is not None else ''}`\n"
            embed.description = textoDeAyuda

            await ctx.send(embed=embed)

def setup(bot): 
    bot.add_cog(Help(bot))
