from .app import app , db
from .models import *

@app.cli. command()
def loaddb():
    print("Deleting database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()

    print("Inserting data...")

    # Insertion des utilisateurs
    print("Inserting users...")
    db.session.add_all([
        Utilisateur(nom="adm", password="86f65e28a754e1a71b2df9403615a6c436c32c42a75a10d02813961b86f1e428", monRole="Admin"),
        Utilisateur(nom="user", password="04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb", monRole="Utilisateur")
    ])

    # Insertion des festivals
    print("Inserting festivals...")
    db.session.add_all([
        Festival(nomFestival="FestIUT'O", villeFestival="Orléans", codePostalFestival="45000", debutFest="2024-01-20", finFest="2024-01-23"),
        Festival(nomFestival="FestIUT'P", villeFestival="Paris", codePostalFestival="75000", debutFest="2025-01-20", finFest="2025-01-22")
    ])

    # Insertion des events
    print("Inserting events...")
    db.session.add_all([
        Event(idFestival=1, nomEvent="Concert de l'orchestre", typeEvent="Concert", dateHeureDebutEvent="2025-01-19 20:00:00", dateHeureFinEvent="2025-01-19 22:00:00", estGratuit=False, adresseEvent="1 rue de la Paix", nbPlaceEvent=100),
        Event(idFestival=1, nomEvent="Interviews de groupe", typeEvent="interview", dateHeureDebutEvent="2025-01-20 10:00:00", dateHeureFinEvent="2025-01-20 12:00:00", estGratuit=False, adresseEvent="1 rue de la Paix", nbPlaceEvent=25),
        Event(idFestival=1, nomEvent="La pluie", typeEvent="Show case", dateHeureDebutEvent="2025-01-21 20:00:00", dateHeureFinEvent="2025-01-21 22:00:00", estGratuit=False, adresseEvent="2 rue de la Paix", nbPlaceEvent=0),
    ])

    # Insertion des groupes
    print("Inserting groups...")
    db.session.add_all([
        Groupe(nomGroupe="La pluie"),
        Groupe(nomGroupe="L'orage")
    ])

    # Insertion des artistes
    db.session.add_all([
        Artiste(nomArtiste="M. Soleil", nomGroupe="La pluie", styleArtiste="Rap", urlInstaArtiste="https://www.instagram.com/msoleil/", urlYoutubeArtiste="https://www.youtube.com/channel/UCZpX9r7l2Z5Xf5VwXW8kD3g"),
        Artiste(nomArtiste="M. Pluie", nomGroupe="La pluie", styleArtiste="Rap Pop", urlInstaArtiste="https://www.instagram.com/mpluie/", urlYoutubeArtiste="https://www.youtube.com/channel/UCZpX9r7l2Z5Xf5VwXW8kD3g"),
        Artiste(nomArtiste="M. Orage", nomGroupe="L'orage", styleArtiste="Classique", urlInstaArtiste="https://www.instagram.com/morage/", urlYoutubeArtiste="https://www.youtube.com/channel/UCZpX9r7l2Z5Xf5VwXW8kD3g")
    ])
    
    db.session.commit()