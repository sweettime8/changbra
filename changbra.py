from app import app, db
import webview
from routers.dashboard import dashboard
from routers.products import products
from routers.warehouse import warehouse
from routers.orders import order_router
import configparser

app.register_blueprint(dashboard)
app.register_blueprint(products)
app.register_blueprint(order_router)
app.register_blueprint(warehouse)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    parser = configparser.ConfigParser()
    parser.read("./config/config.txt")
    http_port = parser.get("config", "http_port")
    http_server = parser.get("config", "http_server")
    app_width = parser.get("config", "app_width")
    app_height = parser.get("config", "app_height")
    window = webview.create_window('Chang\'s Bra', app , width=int(app_width), height=int(app_height))
    webview.start(http_port=int(http_port), http_server=True)
