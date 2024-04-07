#this is just a testpad for the app
# https://stackoverflow.com/questions/73012152/importerror-cannot-import-name-app-from-partially-initialized-module-market
# https://stackoverflow.com/questions/22711087/flask-importerror-no-module-named-app
# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x

from app.models import User, DJ, Song
from app import db, app


print("main")


def seed_database():

# #for test purposes
#     app.app_context().push()

    dj=DJ(username='orelsan', phone='2111110000', email='orelsan@example.com', password='abcd')

    u1 = User()
    u2 = User()

    s1 = Song(name='a', artist='rocker', genre='rock')
    s2 = Song(name='b', artist='rocker', genre='rock')
    s3 = Song(name='c', artist='rocker', genre='rock')
    s4 = Song(name='d', artist='rocker', genre='rock')
    s5 = Song(name='e', artist='rocker', genre='rock')
    

    db.session.add(dj)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    

    db.session.commit()
    print("the party is ready to start")
    

if __name__ == "__main__":
    # seed_database()
    app.run(debug=True)


# if any change is done to the database you have to run these:
# flask db init (if new db)
# flask db migrate
# flask db upgrade

# if you want to go back to the previous version of the db:
# flask db downgrade