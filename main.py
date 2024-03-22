#this is just a testpad for the app
# https://stackoverflow.com/questions/73012152/importerror-cannot-import-name-app-from-partially-initialized-module-market
# https://stackoverflow.com/questions/22711087/flask-importerror-no-module-named-app
# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x

from app.models import User, DJ, Song
from app import db, app


print("main")


def tryout():

#for test purposes


    dj=DJ(username='orelsan', phone='2111110000', email='orelsan@example.com', password='abcd')

    u1 = User()
    u2 = User()

    s1 = Song(name='a', artist='rocker', genre='rock')
    s2 = Song(name='b', artist='rocker', genre='rock')
    s3 = Song(name='c', artist='rocker', genre='rock')
    s4 = Song(name='d', artist='rocker', genre='rock')
    s5 = Song(name='e', artist='rocker', genre='rock')
    s6 = Song(name='f', artist='rocker', genre='rock')
    s7 = Song(name='g', artist='rocker', genre='rock')
    s8 = Song(name='h', artist='rocker', genre='rock')
    s9 = Song(name='i', artist='rocker', genre='rock')
    s10 = Song(name='j', artist='rocker', genre='rock')
    s11 = Song(name='k', artist='rocker', genre='rock')
    s12 = Song(name='l', artist='rocker', genre='rock')
    s13 = Song(name='m', artist='rocker', genre='rock')
    s14 = Song(name='n', artist='rocker', genre='rock')
    s15 = Song(name='o', artist='rocker', genre='rock')
    s16 = Song(name='p', artist='rocker', genre='rock')
    s17 = Song(name='q', artist='rocker', genre='rock')
    s18 = Song(name='r', artist='rocker', genre='rock')
    s19 = Song(name='s', artist='rocker', genre='rock')
    s20 = Song(name='t', artist='rocker', genre='rock')

    db.session.add(dj)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.add(s6)
    db.session.add(s7)
    db.session.add(s8)
    db.session.add(s9)
    db.session.add(s10)
    db.session.add(s11)
    db.session.add(s12)
    db.session.add(s13)
    db.session.add(s14)
    db.session.add(s15)
    db.session.add(s16)
    db.session.add(s17)
    db.session.add(s18)
    db.session.add(s19)
    db.session.add(s20)
    db.session.commit()
    print("the party is ready to start")
    #for test purposes

    # songs = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20]

    # incoming_requests = []
    # user = u1
    # count=0

    # for song in songs:

    #     if count==11:
    #         user=u2

    #     incoming_requests.append(user.create_request(song.id,dj.id))

    #     count+=1

    # print(len(incoming_requests))

    # for req in incoming_requests:
    #     dj.add_to_session(req)

    # add = True

    # for req in dj.session:
    #     add = not add

    #     dj.manage_session(add,req)
    #     song = Song.query.get(req.song_id)
    #     song_title= song.name
    #     print(f'{song_title}')

    # dj.accepted_requests += dj.end_job()
    
    

if __name__ == "__main__":
    app.run(debug=True)


# if any change is done to the database you have to run these:
# flask db init (if new db)
# flask db migrate
# flask db upgrade

# if you want to go back to the previous version of the db:
# flask db downgrade