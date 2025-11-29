from locust import HttpUser, task, between
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenBMCTest(HttpUser):
    wait_time = between(2, 5)
    
    host = "https://localhost:2443"
    
    def on_start(self):

        username_password = "root:0penBmc"
        encoded = base64.b64encode(username_password.encode()).decode()
        self.auth_headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }
    
    @task(3) 
    def get_system_info(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            headers=self.auth_headers,
            verify=False,  
            name="OpenBMC - Информация о системе"
        )
    
    @task(2) 
    def check_power(self):
        self.client.get(
            "/redfish/v1/Systems/system", 
            headers=self.auth_headers,
            verify=False,
            name="OpenBMC - Состояние питания"
        )

class PublicAPITest(HttpUser):

    wait_time = between(1, 3)
    
    host = "https://jsonplaceholder.typicode.com"
    
    @task(3)  
    def get_all_posts(self):
        self.client.get(
            "/posts",
            name="JSONPlaceholder - Все посты"
        )
    
    @task(1)  
    def get_weather(self):
        self.client.get(
            "http://wttr.in/?format=3",
            name="wttr.in - Погода"
        )