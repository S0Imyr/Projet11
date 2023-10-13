import json

DATA_PATH = 'data/'


def load_clubs(file: str = DATA_PATH + 'clubs.json') -> list:
    """
    Charge les données des clubs à partir d'un fichier JSON.

    :param file: Le chemin du fichier JSON contenant les données des clubs.
    :return: Une liste de dictionnaires représentant les clubs.
    """
    with open(file) as clubs_file:
        clubs = json.load(clubs_file)['clubs']
        return clubs


def load_competitions(file: str = DATA_PATH + 'competitions.json') -> list:
    """
    Charge les données des compétitions à partir d'un fichier JSON.

    :param file: Le chemin du fichier JSON contenant les données des compétitions.
    :return: Une liste de dictionnaires représentant les compétitions.
    """
    with open(file) as competitions_file:
        competitions = json.load(competitions_file)['competitions']
        return competitions


def get_club(club_id: int, clubs: list) -> dict or None:
    """
    Récupère un club à partir de sa ID dans la liste des clubs.

    :param club_id: L'identifiant du club à rechercher.
    :param clubs: La liste des clubs à parcourir.
    :return: Un dictionnaire représentant le club trouvé ou None s'il n'existe pas.
    """
    found_club = None
    for club in clubs:
        if club['id'] == club_id:
            found_club = club
            break
    return found_club


def get_competition(competition_id: int, competitions: list) -> dict or None:
    """
    Récupère une compétition à partir de sa ID dans la liste des compétitions.

    :param competition_id: L'identifiant de la compétition à rechercher.
    :param competitions: La liste des compétitions à parcourir.
    :return: Un dictionnaire représentant la compétition trouvée ou None si elle n'existe pas.
    """
    found_competition = None
    for competition in competitions:
        if competition['id'] == competition_id:
            found_competition = competition
            break
    return found_competition
