from locust import HttpUser, task, between

class PerfUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post('/show_summary',  data={"email": "admin@irontemple.com"})

    @task
    def book(self):
        competition_id = 2
        club_id = 1
        self.client.get(f"/book/{competition_id}/{club_id}")

    @task
    def purchasePlaces(self):
        competition = 2
        club = 1
        places = "22"
        self.client.post("/purchasePlaces", data={ "competition": competition, "club": club, "places": places })

    @task
    def board(self):
        self.client.get('/board')

    @task
    def perf_logout(self):
        self.client.get("/logout")