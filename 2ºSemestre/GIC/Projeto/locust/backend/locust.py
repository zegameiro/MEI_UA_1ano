from locust import HttpUser, task, between
import random

class BackendUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.bytebazaar.k3s/api" 

    registered_users = []

    @staticmethod
    def register_accounts(client):
        # Only register if not already done
        if BackendUser.registered_users:
            return

        for i in range(3):
            email = f"locustuser{i}@test.com"
            password = f"Pa$$w0rd{i}!"
            display_name = f"LocustUser{i}"
            # resp = client.post("/account/register", json={
            #     "displayName": display_name,
            #     "email": email,
            #     "password": password
            # }, verify=False)
            # if resp.status_code == 200:
            BackendUser.registered_users.append({"email": email, "password": password})
            # else:
            #     print(f"Registration failed for {email}: {resp.text}")

    def on_start(self):
        # Register accounts if not already done
        self.register_accounts(self.client)

        # Pick a random registered user for this simulated user
        user = random.choice(self.registered_users)
        response = self.client.post("/Account/login", json={
            "email": user["email"],
            "password": user["password"]
        }, verify=False)
        token = response.json().get("token")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        # Fetch products and store their IDs
        resp = self.client.get("/products", verify=False)
        if resp.status_code == 200:
            self.product_ids = [p["id"] for p in resp.json().get("data", [])]
        else:
            self.product_ids = []

        # Fetch delivery methods for orders
        resp = self.client.get("/orders/deliveryMethods", verify=False)
        if resp.status_code == 200:
            self.delivery_methods = resp.json()
        else:
            self.delivery_methods = []

    @task(2)
    def get_products(self):
        self.client.get("/products",verify=False)

    @task(3)
    def get_single_product(self):
        if hasattr(self, "product_ids") and self.product_ids:
            product_id = random.choice(self.product_ids)
            self.client.get(f"/products/{product_id}", verify=False)

    @task(3)
    def get_types(self):
        self.client.get("/products/types", verify=False)    

    @task(3)
    def get_brands(self):
        self.client.get("/products/brands", verify=False)

    @task(3)
    def get_basket(self):
        self.client.get("/basket?id=test-basket",verify=False)

    @task(3)
    def get_orders(self):
        self.client.get("/orders",verify=False)

    @task(1)
    def ensure_basket_and_create_order(self):
        # Ensure basket has at least one item
        if hasattr(self, "product_ids") and self.product_ids:
            product_id = random.choice(self.product_ids)
            product_resp = self.client.get(f"/products/{product_id}", verify=False)
            if product_resp.status_code == 200:
                product = product_resp.json()
                basket_item = {
                    "id": product["id"],
                    "productName": product["name"],
                    "price": product["price"],
                    "quantity": 1,
                    "pictureUrl": product["pictureUrl"],
                    "brand": product["productBrand"],
                    "type": product["productType"]
                }
                basket = {
                    "id": "test-basket",
                    "items": [basket_item]
                }
                self.client.post("/basket", json=basket, verify=False)

        # Now create the order
        if hasattr(self, "delivery_methods") and self.delivery_methods:
            delivery_method_id = random.choice(self.delivery_methods)["id"]
            address = {
                "firstName": "Test",
                "lastName": "User",
                "street": "123 Main St",
                "city": "Testville",
                "state": "TS",
                "zipcode": "12345"
            }
            order = {
                "basketId": "test-basket",
                "deliveryMethodId": delivery_method_id,
                "shipToAddress": address
            }
            self.client.post("/orders", json=order, verify=False)


    @task(2)
    def add_random_product_to_basket(self):
        if hasattr(self, "product_ids") and self.product_ids:
            product_id = random.choice(self.product_ids)
            # You may want to fetch product details for price, etc.
            product_resp = self.client.get(f"/products/{product_id}", verify=False)
            if product_resp.status_code == 200:
                product = product_resp.json()
                basket_item = {
                    "id": product["id"],
                    "productName": product["name"],
                    "price": product["price"],
                    "quantity": random.randint(1, 10),
                    "pictureUrl": product["pictureUrl"],
                    "brand": product["productBrand"],
                    "type": product["productType"]
                }
                basket = {
                    "id": "test-basket",
                    "items": [basket_item]
                }
                self.client.post("/basket", json=basket, verify=False)
    
    @task(1)
    def delete_random_item_from_basket(self):
        # Get the current basket
        resp = self.client.get("/basket?id=test-basket", verify=False)
        if resp.status_code == 200:
            basket = resp.json()
            items = basket.get("items", [])
            if items:
                item = random.choice(items)
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                    new_items = [i if i["id"] != item["id"] else item for i in items]
                else:
                    new_items = [i for i in items if i["id"] != item["id"]]
                updated_basket = {
                    "id": basket["id"],
                    "items": new_items
                }
                self.client.post("/basket", json=updated_basket, verify=False)
