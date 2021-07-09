import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash,url_for


PLACE_COST = 3
MAXIMUM_PLACE_BOOK_IN_COMPETITION = 12

def load_clubs(file='clubs.json'):
    with open(file) as clubs_file:
        clubs = json.load(clubs_file)['clubs']
        return clubs


def load_competitions(file='competitions.json'):
    with open(file) as competitions_file:
        competitions = json.load(competitions_file)['competitions']
        return competitions


def get_club(club_id, clubs):
    found_club = None
    for club in clubs:
        if club['id'] == club_id:
            found_club = club
    return found_club


def get_competition(competition_id, competitions):
    found_competition = None
    for competition in competitions:
        if competition['id'] == competition_id:
            found_competition = competition
    return found_competition


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_summary', methods=['POST'])
def show_summary():
    email = request.form['email']
    for competition in competitions:
        competition["active"] = datetime.fromisoformat(competition['date']) + timedelta(days=1) > datetime.now()
    for club in clubs:
        if club['email'] == email:
            return render_template('welcome.html', club=club, competitions=competitions)
    flash("Unknown email")
    return render_template('index.html'), 403


@app.route('/book/<int:competition_id>/<int:club_id>')
def book(competition_id, club_id):
    found_club = get_club(club_id, clubs)
    found_competition = get_competition(competition_id, competitions)
    if found_club and found_competition:
        if datetime.fromisoformat(found_competition['date']) < datetime.now() + timedelta(days=1):
            flash("This competition is over, you can't book any place.")
            return render_template('welcome.html', club=found_club, competitions=competitions)
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Competition or club not found.")
        return render_template('welcome.html', club={"id": 0}, competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    club = get_club(int(request.form['club']), clubs)
    competition = get_competition(int(request.form['competition']), competitions)
    placesRequested = int(request.form['places'])
    points_requested = PLACE_COST * placesRequested
    if placesRequested > MAXIMUM_PLACE_BOOK_IN_COMPETITION:
        flash("You can't book more than {MAXIMUM_PLACE_BOOK_IN_COMPETITION} places in a competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        if points_requested > int(club['points']):
            flash("You don't have enough points. Try with a number smaller than your total points.")
            return render_template('welcome.html', club=club, competitions=competitions)
        elif placesRequested > int(competition['numberOfPlaces']):
            flash("There are not enough places in this competition. Try with a smaller number of seats than the available seats.")
            return render_template('welcome.html', club=club, competitions=competitions)
        club['points'] = int(club['points']) - points_requested
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequested
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/board', methods=['GET'])
def board():
    return render_template('board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))