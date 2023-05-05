# Application entry point.
from flask_script import Manager
from app import app

manager = Manager(app)


@manager.command
def hello():
    print('Dashboard WebApp version 1.0')


if __name__ == '__main__':
    manager.run()
