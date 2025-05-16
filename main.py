
import os
import asyncio
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands
from keep_alive import keep_alive

from keep_alive import keep_alive

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1216781760155881613  # ID du salon

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author.mention} !")

CHANNEL_ID = 1216781760155881613  # ID du salon

# Configuration complète des intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

ROLES = {
    "🔰• Wilford Security Solutions": 1298636409166626826,
    "💵• Département des Ventes et du Développement Commercial": 1298352921871782003,
    "👥• Ressources Humaines": 1216515880922386452,
    "🛠️• Recherche et Développement •🛠️": 1216515780724658368
}

DIRECTION = 1151179209675378698
PERSONNEL = 1158798630254280855
STAGIAIRE = 1352013993539014726
APPRENTI = 1352013998572306462

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    print(f"Le bot est présent dans {len(bot.guilds)} serveurs")

    # Lancer la tâche de mise à jour automatique
    bot.loop.create_task(update_effectif())

async def update_effectif():
    await bot.wait_until_ready()  # Attendre que le bot soit complètement prêt

    # Récupérer le salon où envoyer le message
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Salon avec ID {CHANNEL_ID} introuvable ! Vérifiez l'ID du salon.")
        return

    while True:
        try:
            # Préparer le message
            message = ""
            total_members = set()

            # Ajouter le rôle DIRECTION
            direction_role = channel.guild.get_role(DIRECTION)
            if direction_role:
                members = set(direction_role.members)
                total_members.update(members)
                message += f" ## {direction_role.mention}\n"
                if members:
                    message += "\n".join(f"- {member.mention}" for member in members) + "\n"
                else:
                    message += "Aucun membre\n"
                message += f"Nombre : {len(members)}\n"
                message += "━" * 50 + "\n"
            else:
                message += f"Rôle non trouvé : DIRECTION (ID: {DIRECTION})\n"
                message += "━" * 50 + "\n"

            # Ajouter les autres rôles
            for role_name, role_id in ROLES.items():
                role = channel.guild.get_role(role_id)
                if role:
                    members = set(role.members)
                    total_members.update(members)

                    message += f"{role.mention}\n"
                    if members:
                        message += "\n".join(f"- {member.mention}" for member in members) + "\n"
                    else:
                        message += "Aucun membre\n"
                    message += f"Nombre : {len(members)}\n"
                    message += "━" * 50 + "\n"
                else:
                    message += f"Rôle non trouvé : {role_name} (ID: {role_id})\n"
                    message += "━" * 50 + "\n"

            # Ajouter les apprentis
            apprentis_role = channel.guild.get_role(APPRENTI)
            if apprentis_role:
                members = set(apprentis_role.members)
                total_members.update(members)
                message += f" {apprentis_role.mention}\n"
                if members:
                    message += "\n".join(f"- {member.mention}" for member in members) + "\n"
                else:
                    message += "\n"
                message += f"Nombre : {len(members)}\n"
                message += "━" * 50 + "\n"
            else:
                message += f"Rôle non trouvé : APPRENTI (ID: {APPRENTI})\n"
                message += "━" * 50 + "\n"

            # Ajouter les stagiaires
            stagiaires_role = channel.guild.get_role(STAGIAIRE)
            if stagiaires_role:    
                members = set(stagiaires_role.members)
                total_members.update(members)
                message += f" {stagiaires_role.mention}\n"
                if members:
                    message += "\n".join(f"- {member.mention}" for member in members) + "\n"
                else:
                    message += "N/A\n"
                message += f"Nombre : {len(members)}\n"
                message += "━" * 50 + "\n"
            else:
                message += f"Rôle non trouvé : STAGIAIRE (ID: {STAGIAIRE})\n"
                message += "━" * 50 + "\n"

            # Ajouter personnel
            personnel_role = channel.guild.get_role(PERSONNEL)

            # Calculer le total sans la direction
            direction_count = len(direction_role.members) if direction_role else 0
            members_without_direction = len(total_members) - direction_count

            # Calculer le total avec la direction
            total_members_with_direction = len(personnel_role.members) if personnel_role else 0

            # Ajouter le total à la fin du message
            message += f"**Total des membres (hors direction) : {members_without_direction}**\n"
            message += f"**Total des membres (avec direction) : {total_members_with_direction}**\n"

            # Vérifier si un message existe déjà dans le salon
            async for msg in channel.history(limit=1):
                if msg.author == bot.user:  # Vérifier si c'est un message du bot
                    await msg.edit(content=message)  # Mettre à jour le message
                    print("Message mis à jour.")
                    break
            else:
                # Si aucun message du bot n'existe, en créer un nouveau
                await channel.send(message)
                print("Nouveau message envoyé.")

        except Exception as e:
            print(f"Erreur lors de la mise à jour du message : {str(e)}")

        # Attendre 60 secondes avant la prochaine mise à jour
        await asyncio.sleep(60)

# Commandes supplémentaires pour tester

@bot.command()
async def ping(ctx):
    await ctx.send("Ne vous inquiétez-vous donc pas cher maître, je suis là.")

@bot.command()
async def earl(ctx):
    await ctx.send("C'est un spécimen unique en son genre, maigre, boutonneux et binoclard. Il ne ferait même pas mal à une mouche.")

@bot.command()
async def hawk(ctx):
    await ctx.send("Ce type vit dans le passé, il se prend pour un cowboy alors que c'est un femboy.")

@bot.command()
async def edouard(ctx):
    await ctx.send("C'est l'homme le plus gros que j'ai connu. Un virage, un accident. Il a beau être gros même le Dodge Ram le subit ! ")

@bot.command()
async def gunter(ctx):
    await ctx.send("Il aime que les trombonnes soient à leur place. Recalé par l'école d'art, il commence sa carrière politique. «Nein! Nein! Nein!git status» a-t-il dit.")

@bot.command()
async def joe(ctx):
    await ctx.send("Souvent confondu avec un camionneur, ce commissaire de police est redouté pour les BL qui partent vite.")

@bot.command()
async def micheal(ctx):
    await ctx.send("Amateur professionnel de jeunes asiatiques, il les dévore comme du popcorn. Pop!")

@bot.command()
async def angus(ctx):
    await ctx.send("Cet homme est un multi-aliment, il a le nom d'une race bovine écossaise, et peut-être aussi un jus de fruit. Bon appétit!")

@bot.command()
async def vlad(ctx):
    await ctx.send("Cet homme, féru de frites, aime bien dénigrer la France, parce que pourquoi pas, et si tu oses le contredire, il te sortira un (olala).")

@bot.command()
async def thomas(ctx):
    await ctx.send("Lui c'est juste une salope qui se fait ban H24, mais il détruit tout le monde sur les points, donc en vrai pas grave, on l'excuse.") 

@bot.command()
async def tony(ctx):
    await ctx.send("Attention! Si votre véhicule est coincé ne l'appelé pas, il va vite perdre patience et tout faire péter!") 

message_dodgeram = [
    "Pas de bol ! Tu as fait un carkill massif et Gustavo était dans les parages...",
        "Tu as fait voler une voiture et Tyler a tout vu...",
        "Tu roulais à 244km/h et par chance tu n'as tué personne !"
]

@bot.command()
async def dodgeram(ctx):
    await ctx.send(random.choice(message_dodgeram))

@bot.command()
async def roll(ctx):
    await ctx.send(random.randint(1, 10))

@bot.command()
async def ntm(ctx):
     await ctx.send(f"C'est une injure très vulgaire et malpolie. Je ne peux pas vous laisser sans punition {ctx.author.mention}.")

@bot.command()
async def pileouface(ctx):
    await ctx.send(random.choice(["Pile", "Face"]))





token = os.getenv('DISCORD_TOKEN')
keep_alive()
bot.run(token)