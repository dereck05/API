from flask_script import Manager,Command
from flask_migrate import Migrate, MigrateCommand
from Endpoints import app, db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
