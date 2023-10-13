from locust import HttpUser, task, between

class PerfUser(HttpUser):
    wait_time = between(1, 2.5)

    def on_start(self):
        self.client.get("/")
        self.client.post("/show_summary", {"email": "john@simplylift.co"})

    def on_stop(self):
        self.client.get("/logout")

    @task
    def index(self):
        self.client.get("/")

    @task
    def book(self):
        competition_id = 2
        club_id = 1
        self.client.get(f"/book/{competition_id}/{club_id}")

    @task
    def purchase_places(self):
        competition = 2
        club = 1
        places = 3
        self.client.post("/purchase_places", data={ "competition": competition, "club": club, "places": places })

    @task
    def board(self):
        self.client.get('/board')
