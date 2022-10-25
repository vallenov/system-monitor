from flask import Flask
from services.services_task import ServicesTask


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        ServicesTask.run()
        super().__init__(*args, **kwargs)


app = MyApp(__name__)
