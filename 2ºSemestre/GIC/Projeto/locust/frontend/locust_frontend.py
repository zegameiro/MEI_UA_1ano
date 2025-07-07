from locust import HttpUser, task, between
import random
import urllib3

class FrontendUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://bytebazaar.k3s"

    def on_start(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.client.verify = False  # Disable SSL verification for testing
        
    @task(1)
    def load_homepage(self):
        self.client.get("/")

    @task(3)
    def load_products_page(self):
        self.client.get("/shop")

    @task(2)
    def load_product_details(self):
        product_ids = [1, 5, 3, 10, 6, 7, 8, 11, 2, 9]
        product_id = random.choice(product_ids)
        self.client.get(f"/products/{product_id}")  # Example product ID