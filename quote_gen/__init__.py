from flask import Flask
# from quote_gen.config import Config

# import the routes from users module

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config_class)


    from quote_gen.main.routes import main

    app.register_blueprint(main)

    return app
