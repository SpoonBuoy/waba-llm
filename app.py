from src import config, app
from src.routes import api
from src.controllers import chat_controller

if __name__ == '__main__':
    # Register blueprints here
    app.register_blueprint(api, url_prefix='/api')
    app.run(host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG)
