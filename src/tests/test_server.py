from src.server import app, load_clubs, load_competitions, MAXIMUM_PLACE_BOOK_IN_COMPETITION
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
        response = self.test_client.post('/show_summary', data=dict(email=email))
        assert response.status_code == status
    
    @pytest.mark.parametrize("club_id, competition_id, "
                            "number_of_places, club_points, "
                            "competition_places, messages",
                            [
                             (3, 3, 2, 12, 1, ['There are not enough places in this competition. Try with a smaller number of seats than the available seats.']), 
                             ((2, 2, 5, 4, 13, ['You don&#39;t have enough points. Try with a number smaller than your total points.'])), 
                             ((1, 1, 14, 13, 25, [f'You can&#39;t book more than {MAXIMUM_PLACE_BOOK_IN_COMPETITION} places in a competition.'])), 
                             (1, 1, 4, 1, 21, ['Great-booking complete!'])
                            ])
    def test_purchase_places(self, club_id, competition_id, number_of_places, club_points, competition_places, messages):
        response = self.test_client.post('/purchase_places', data=dict(club=club_id, competition=competition_id, places=number_of_places))
        assert response.status_code == 200
        assert str.encode(f"Points available: {club_points}") in response.data
        assert str.encode(f"Number of Places: {competition_places}") in response.data
        for message in messages:
            assert str.encode(message) in response.data

    @pytest.mark.parametrize("club_id, competition_id, page, messages", 
                             [
                              (1, 1, "Booking for Spring Festival || GUDLFT", ["How many places ?"]), 
                              (3, 3, "Summary | GUDLFT Registration", ["This competition is over, you can&#39;t book any place."]),
                              (3, 15, "Summary | GUDLFT Registration", ["Competition or club not found."]), 
                              (15, 3, "Summary | GUDLFT Registration", ["Competition or club not found."])
                             ])
    def test_book(self, club_id, competition_id, page, messages):
        response = self.test_client.get(f'/book/{competition_id}/{club_id}', content_type='html/text')
        assert response.status_code == 200
        assert str.encode(page) in response.data
        for message in messages:
            assert str.encode(message) in response.data

    def test_logout(self):
        response = self.test_client.get("/logout")
        assert response.status_code == 302

    def test_board(self):
        response = self.test_client.get("/board")
        assert response.status_code == 200
