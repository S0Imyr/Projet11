
from datetime import datetime, timedelta

from flask import render_template, request, redirect, flash, url_for

from .load_data import get_club, get_competition
from .server import competitions, clubs, app

PLACE_COST = 3
MAXIMUM_PLACE_BOOK_IN_COMPETITION = 12


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/board', methods=['GET'])
def board():
    return render_template('board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


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
    places_requested = int(request.form['places'])
    points_requested = PLACE_COST * places_requested
    if places_requested > MAXIMUM_PLACE_BOOK_IN_COMPETITION:
        flash(f"You can't book more than {MAXIMUM_PLACE_BOOK_IN_COMPETITION} places in a competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        if points_requested > int(club['points']):
            flash("You don't have enough points. Try with a number smaller than your total points.")
            return render_template('welcome.html', club=club, competitions=competitions)
        elif places_requested > int(competition['numberOfPlaces']):
            flash("There are not enough places in this competition."
                  " Try with a smaller number of seats than the available seats.")
            return render_template('welcome.html', club=club, competitions=competitions)
        club['points'] = int(club['points']) - points_requested
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_requested
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)