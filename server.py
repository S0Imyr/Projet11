import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash,url_for


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

@app.route('/showSummary', methods=['POST'])
def showSummary():
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


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    club = get_club(int(request.form['club']), clubs)
    competition = get_competition(int(request.form['competition']), competitions)
    placesRequested = int(request.form['places'])
    if placesRequested > 12:
        flash("You can't book more than 12 places in a competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        if placesRequested > int(club['points']):
            flash("You don't have enough points. Try with a number smaller than your total points.")
            return render_template('welcome.html', club=club, competitions=competitions)
        elif placesRequested > int(competition['numberOfPlaces']):
            flash("There are not enough places in this competition. Try with a smaller number of seats than the available seats.")
            return render_template('welcome.html', club=club, competitions=competitions)
        club['points'] = int(club['points']) - placesRequested
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequested
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))