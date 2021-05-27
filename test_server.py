import server
from server import app


test_clubs = [
        {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        },
        {
            "name":"Iron Temple",
            "email": "admin@irontemple.com",
            "points":"4"
        },
        {   "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"12"
        }
    ]


test_competitions = [
        {
            "name": "Spring Festival",
            "date": "2021-08-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]



class TestIndex:
    test_client = app.test_client()

    def test_get_page(self):
        response = self.test_client.get('/', content_type='html/text')
        assert response.status_code == 200


class TestShowSummary:
    server.clubs = test_clubs
    server.competitions = test_competitions
    test_client = app.test_client()

    def test_input_known_email(self):
        response = self.test_client.post('/showSummary', data=dict(email="admin@irontemple.com"))
        assert response.status_code == 200
    
    def test_input_unknown_email(self):
        response = self.test_client.post('/showSummary', data=dict(email="admin@iroemple.com"))
        assert response.status_code == 403
