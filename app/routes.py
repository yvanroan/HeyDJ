#all the data coming from the front end will be sent here
#this is where we will be creating the instances and adding them to the database
# functions from each class will be used here to implement the actual flow of the app

#i had to copy the flask_cors folder from github to be able to use it here.

from flask_cors import CORS, cross_origin
from app import app, db
from app.models import User, DJ, Song, Request
from flask import jsonify, request, abort
import collections


CORS(app, supports_credentials=True)
@app.route('/api', methods=['GET'])

def get_data():
    print("yes")
    # add_song()

    users = User.query.all()
    djs = DJ.query.all()
    songs = Song.query.all()
    reqs = Request.query.all()

    print("ok")
    

    user_obj,dj_obj, song_obj, req_obj = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    for user in users:
        user_obj['id'].append(user.id)

    for dj in djs:
        dj_obj['id'].append(dj.id)
        dj_obj['name'].append(dj.username)

    for song in songs[:10]:
        song_obj['id'].append(song.id)
        song_obj['artist'].append(song.artist)
        song_obj['title'].append(song.name)

    for req in reqs:
        req_obj['id'].append(req.id)
        req_obj['timestamp'].append(req.timestamp)
        req_obj['user'].append(req.user)
        req_obj['Dj'].append(req.dj)
        req_obj['song'].append(req.song)
        req_obj['Status'].append(req.Status)

    return jsonify({'Users':user_obj,'Djs':dj_obj,'Songs':song_obj,'Requests':req_obj})

def add_song():
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

@app.route('/api/request', methods=['POST'])
def create_request():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    req = user.create_request(data['song_id'],data['dj_id'])
    db.session.add(req)
    db.session.commit()
    return get_data()


@app.route('/api/request/<int:req_id>', methods=['POST'])
def update_request(req_id):
    data = request.get_json() #this should be data sent from the front end 
    # to update our db
    req = Request.query.get(req_id)
    if not req:
        abort(404, description="Request not found")
    if 'Status' in data:
        req.Status = data['Status']
        db.session.commit()
        return get_data()
    else:
        abort(400, description="Request found but status is required for update")


@app.route('/api/user', methods=['POST'])
def create_user():    
    # Create a new Item instance
    user = User()
    db.session.add(user)
    db.session.commit()
    return get_data()



# if __name__ == "__main__":
#     app.run(debug=True)

