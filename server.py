import json
from flask import Flask, render_template, request, redirect, flash,url_for


def loadClubs():
    with open('clubs.json') as clubs:
         listOfClubs = json.load(clubs)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as competitions:
         listOfCompetitions = json.load(competitions)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<int:competition_id>/<int:club_id>')
def book(competition_id, club_id):
    found_club = None
    found_competition = None
    for club in clubs:
        if club['id'] == club_id:
            found_club = club
    for competition in competitions:
        if competition['id'] == competition_id:
            found_competition = competition
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=found_club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    found_club = None
    found_competition = None
    for club in clubs:
        if club['id'] == int(request.form['club']):
            found_club = club
    for competition in competitions:
        if competition['id'] == int(request.form['competition']):
            found_competition = competition
    placesRequired = int(request.form['places'])
    found_competition['numberOfPlaces'] = int(found_competition['numberOfPlaces']) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=found_club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))