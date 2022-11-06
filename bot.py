from pyArnavje import Arnavje
from pyromod import listen
from database.users_sql import Users


bot = Arnavje()
Users.__table__.create(checkfirst=True)

if __name__ == "__main__":
    bot.activate()
