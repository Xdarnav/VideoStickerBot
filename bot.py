from pystark import Stark
from pyromod import listen
from database.users_sql import Users


bot = Stark()
Users.__table__.create(checkfirst=True)
bind
if __name__ == "__main__":
    bot.activate()
