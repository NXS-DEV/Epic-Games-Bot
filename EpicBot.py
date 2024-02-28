import discord
import requests
# Création du client Discord
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print("Bot connected to Discord!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Games"))
    # Récupération des jeux gratuits
    free_games = get_free_games()

    # Recherche du canal Discord spécifié
    channel = client.get_channel(int(CHANNEL_ID))

    if channel:
        # Envoi des jeux gratuits dans le canal sous forme d'embed
        await send_embed(channel, "Jeux gratuits disponibles", free_games)
    else:
        print("Channel not found!")

# Paramètres du bot Discord
CHANNEL_ID = "1200798737249882232"

# Paramètres de l'API Epic Games
EPIC_API_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

# Fonction pour envoyer un embed dans un canal Discord


async def send_embed(channel, title, games):
    embed = discord.Embed(title=title, color=discord.Color.blue())  # Changer la couleur ici

    for game in games:
        embed.add_field(name=game["title"],
                        value=f"*Date de fin*: {game.get('end_date', 'Non spécifiée')}\nDescription: {game['description']}",
                        inline=False)
        embed.set_thumbnail(url=game.get("image_url", ""))  # URL de l'image de la couverture du jeu
        embed.add_field(name="Plateformes", value=", ".join(game["platforms"]), inline=False)
        embed.add_field(name="Développeurs", value=", ".join(game["developers"]), inline=False)
        embed.add_field(name="Éditeurs", value=", ".join(game["publishers"]), inline=False)
        embed.set_image(url=game["image_url"])
        # Ajout du lien de redirection vers le jeu sur le store
        game_url = f"https://www.epicgames.com/store/en-US/p/{game['title'].replace(' ', '-')}"
        embed.add_field(name="Lien vers le jeu", value=game_url, inline=False)

    await channel.send(embed=embed)

# Fonction pour récupérer les jeux gratuits depuis l'API Epic Games
def get_free_games():
    response = requests.get(EPIC_API_URL)
    data = response.json()
    free_games = []

    if "data" in data:
        for entry in data["data"]["Catalog"]["searchStore"]["elements"]:
            if entry.get("promotions") and entry["promotions"].get("promotionalOffers"):
                game_info = {}
                game_info["title"] = entry["title"]
                game_info["description"] = entry["description"]
                game_info["start_date"] = entry["effectiveDate"]

                # Vérifier si la clé "expirationDate" existe
                if "expirationDate" in entry:
                    game_info["end_date"] = entry["expirationDate"]
                else:
                    game_info["end_date"] = "Date de fin non spécifiée"

                # Récupération de l'image du jeu
                if entry["keyImages"]:
                    game_info["image_url"] = entry["keyImages"][0]["url"]
                else:
                    game_info["image_url"] = "URL de l'image non disponible"

                # Récupération des plateformes disponibles
                platforms = []
                for platform in entry.get("categories", []):
                    if platform["path"] == "games/pc":
                        platforms.append("PC")
                    elif platform["path"] == "games/ps5":
                        platforms.append("PlayStation 5")
                    # Ajoutez d'autres plateformes selon vos besoins
                game_info["platforms"] = platforms

                # Vérification des informations sur les plateformes
                if not game_info["platforms"]:
                    game_info["platforms"] = ["Inconnu"]

                # Récupération des développeurs et éditeurs
                game_info["developers"] = [developer["name"] for developer in entry.get("developerDisplayName", [])]
                game_info["publishers"] = [publisher["name"] for publisher in entry.get("publisherDisplayName", [])]

                # Vérification des développeurs et éditeurs
                if not game_info["developers"]:
                    game_info["developers"] = ["Inconnu"]
                if not game_info["publishers"]:
                    game_info["publishers"] = ["Inconnu"]

                free_games.append(game_info)

    return free_games
def print_epic_games_info():
    EPIC_API_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    response = requests.get(EPIC_API_URL)
    data = response.json()

    if "data" in data:
        for entry in data["data"]["Catalog"]["searchStore"]["elements"]:
            if entry.get("promotions") and entry["promotions"].get("promotionalOffers"):
                print("Title:", entry["title"])
                print("Description:", entry["description"])
                print("Start Date:", entry["effectiveDate"])
                print("End Date:", entry.get("expirationDate", "No expiration date specified"))
                print("Image URL:", entry["keyImages"][0]["url"])
                print("Platform(s):", ", ".join([platform["path"].split("/")[-1] for platform in entry.get("categories", [])]))
                print("Developers:", ", ".join([developer["name"] for developer in entry.get("developerDisplayName", [])]))
                print("Publishers:", ", ".join([publisher["name"] for publisher in entry.get("publisherDisplayName", [])]))
                print("----------------------------------------------------------")

# Appel de la fonction pour imprimer les informations
print_epic_games_info()


client.run(token)

