from server import app, load_clubs, load_competitions, get_club, get_competition
import pytest


class Test:
    def setup_method(self):
        self.clubs = load_clubs()
        self.competitions = load_competitions()
        self.test_client = app.test_client()

    def teardown_method(self):
        pass

    def test_get_index(self):
        response = self.test_client.get('/', content_type='html/text')
        assert response.status_code == 200

    @pytest.mark.parametrize("email, status", [("admin@irontemple.com", 200), ("admin@iroemple.com", 403)])
    def test_input_email(self, email, status):
        response = self.test_client.post('/showSummary', data=dict(email=email))
        assert response.status_code == status
    
    @pytest.mark.parametrize("club_id, competition_id, "
                            "number_of_places, club_points, "
                            "competition_places, messages",
                            [
                             (3, 3, 10, 12, 8, ['There are not enough places in this competition. Try with a smaller number of seats than the available seats.']), 
                             ((2, 2, 5, 4, 13, ['You don&#39;t have enough points. Try with a number smaller than your total points.'])), 
                             ((1, 1, 14, 13, 25, ['You can&#39;t book more than 12 places in a competition.'])), 
                             (1, 1, 11, 2, 14, ['Great-booking complete!'])
                            ])
    def test_purchase_places(self, club_id, competition_id, number_of_places, club_points, competition_places, messages):
        response = self.test_client.post('/purchasePlaces', data=dict(club=club_id, competition=competition_id, places=number_of_places))
        assert response.status_code == 200
        assert str.encode(f"Points available: {club_points}") in response.data
        assert str.encode(f"Number of Places: {competition_places}") in response.data
        for message in messages:
            assert str.encode(message) in response.data

    @pytest.mark.parametrize("club_id, competition_id, messages", [(1, 1, ["This competition is over, you can't book any place."]), (3, 3, ["How many places ?"])])
    def test_book(self, club_id, competition_id, messages):
        response = self.test_client.get(f'/book/{club_id}/{competition_id}', content_type='html/text')
        assert response.status_code == 200
        for message in messages:
            assert str.encode(message) in response.data
