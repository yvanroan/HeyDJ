#all the data coming from the front end will be sent here
#this is where we will be creating the instances and adding them to the database
# functions from each class will be used here to implement the actual flow of the app
# https://stackoverflow.com/questions/73012152/importerror-cannot-import-name-app-from-partially-initialized-module-market
# https://stackoverflow.com/questions/22711087/flask-importerror-no-module-named-app
# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x

from app.models import User, DJ, Song
from app import db, create_app
# from flask import current_app


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

    # r1 = Request(Status=False, DJ_id= dj.id,song_id= s1.id, user_id = u1.id )
    # r2 = Request(Status=False, DJ_id= dj.id,song_id= s2.id, user_id = u1.id )
    # r3 = Request(Status=False, DJ_id= dj.id,song_id= s3.id, user_id = u1.id )
    # r4 = Request(Status=False, DJ_id= dj.id,song_id= s4.id, user_id = u1.id )
    # r5 = Request(Status=False, DJ_id= dj.id,song_id= s5.id, user_id = u1.id )
    # r6 = Request(Status=False, DJ_id= dj.id,song_id= s6.id, user_id = u1.id )
    # r7 = Request(Status=False, DJ_id= dj.id,song_id= s7.id, user_id = u1.id )
    # r8 = Request(Status=False, DJ_id= dj.id,song_id= s8.id, user_id = u1.id )
    # r9 = Request(Status=False, DJ_id= dj.id,song_id= s9.id, user_id = u1.id )
    # r10 = Request(Status=False, DJ_id= dj.id,song_id= s10.id, user_id = u1.id )
    # r11 = Request(Status=False, DJ_id= dj.id,song_id= s11.id, user_id = u2.id )
    # r12 = Request(Status=False, DJ_id= dj.id,song_id= s12.id, user_id = u2.id )
    # r13 = Request(Status=False, DJ_id= dj.id,song_id= s13.id, user_id = u2.id )
    # r14 = Request(Status=False, DJ_id= dj.id,song_id= s14.id, user_id = u2.id )
    # r15 = Request(Status=False, DJ_id= dj.id,song_id= s15.id, user_id = u2.id )
    # r16 = Request(Status=False, DJ_id= dj.id,song_id= s16.id, user_id = u2.id )
    # r17 = Request(Status=False, DJ_id= dj.id,song_id= s17.id, user_id = u2.id )
    # r18 = Request(Status=False, DJ_id= dj.id,song_id= s18.id, user_id = u2.id )
    # r19 = Request(Status=False, DJ_id= dj.id,song_id= s19.id, user_id = u2.id )
    # r20 = Request(Status=False, DJ_id= dj.id,song_id= s20.id, user_id = u2.id )

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
    # db.session.add(r1)
    # db.session.add(r2)
    # db.session.add(r3)
    # db.session.add(r4)
    # db.session.add(r5)
    # db.session.add(r6)
    # db.session.add(r7)
    # db.session.add(r8)
    # db.session.add(r9)
    # db.session.add(r10)
    # db.session.add(r11)
    # db.session.add(r12)
    # db.session.add(r13)
    # db.session.add(r14)
    # db.session.add(r15)
    # db.session.add(r16)
    # db.session.add(r17)
    # db.session.add(r18)
    # db.session.add(r19)
    # db.session.add(r20)
    db.session.commit()
    print("the party is ready to start")
    #for test purposes

    songs = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20]

    incoming_requests = []
    user = u1
    count=0

    for song in songs:

        if count==11:
            user=u2

        incoming_requests.append(user.create_request(song.id,dj.id))

        count+=1

    print(len(incoming_requests))

    for req in incoming_requests:
        dj.add_to_session(req)

    add = True

    for req in dj.session:
        add = not add

        dj.manage_session(add,req)
        song = Song.query.get(req.song_id)
        song_title= song.name
        print(f'{song_title}')

    dj.accepted_requests = dj.end_job()
    
    

if __name__ == "__main__":
    app = create_app()
    # with app.app_context():
    #     db.drop_all()
    app.app_context().push()
    print("good")
    tryout()


# if any change is done to the database you have to run these:
# flask db init (if new db)
# flask db migrate
# flask db upgrade

# if you want to go back to the previous version of the db:
# flask db downgrade