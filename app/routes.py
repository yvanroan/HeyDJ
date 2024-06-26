#all the data coming from the front end will be sent here
#this is where we will be creating the instances and adding them to the database
# functions from each class will be used here to implement the actual flow of the app

#i had to copy the flask_cors folder from github to be able to use it here.

from flask_cors import CORS
from app import app, db
from app.models import App_user, DJ, Song, Request, Event
from flask import jsonify, request, render_template
import collections
from sqlalchemy import select, update
import os
import requests
from dotenv import load_dotenv
from app.encode_decode import sound_breathing
from app.auth import login, signup
from flask_socketio import SocketIO, join_room,leave_room



CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')


load_dotenv()

@app.route('/')
@app.route('/login')
def start():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/userentry')
def userentry():
    return render_template('userentry.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/homelandooo')
def homelandooo():
    return render_template('homepage.html')

@app.route('/djentry')
def djentry():
    return render_template('djentry.html')

@app.route('/dj')
def dj():
    return render_template('dj.html')

@app.route('/exit')
def exit():
    return render_template('exit.html')



@app.route('/api', methods=['POST'])
def get_data():

    data = request.get_json()
    event_id = data['id']

    
    print("ys")
    # add_song()
    event = db.session.execute(select(Event.id, Event.name, Event.dj_id).where(Event.id == event_id)).first()
    users = db.session.execute(select(App_user.id)).all()
    songs = db.session.execute(select(Song.id, Song.artist, Song.name)).all()
    dj = db.session.execute(select(DJ.id, DJ.username).where(DJ.id == event.dj_id) ).first()
    reqs = db.session.execute(select(Request.id, Request.timestamp,Request.user_id, Request.dj_id, Request.song_id).where(Request.in_stack == True).order_by(Request.id.desc())).all()
       

    event_obj, user_obj, dj_obj, song_obj, req_obj = {}, collections.defaultdict(list), {}, collections.defaultdict(list), collections.defaultdict(list)
    
    event_obj['id'] = event.id
    event_obj['name'] = event.name

    dj_obj['id'] = dj.id
    dj_obj['name'] = dj.username

    for user in users:
        user_obj['id'].append(user.id)

    for song in songs[:10]:
        song_obj['id'].append(song.id)
        song_obj['artist'].append(song.artist)
        song_obj['title'].append(song.name)

    for req in reqs:
        if 'dj_id' in req_obj and 'song_id' in req_obj and req.song_id in req_obj['song_id'] and req.dj_id in req_obj['dj_id']:
            continue
        
        ask =  len(db.session.execute(select(Request.id).where(Request.event_id == event_id).where(Request.song_id == req.song_id).where(Request.dj_id == req.dj_id).where(Request.in_stack == True)).all())

        req_obj['timestamp'].append(str(req.timestamp))
        req_obj['dj_id'].append(req.dj_id)
        req_obj['song_id'].append(req.song_id)
        req_obj['ask'].append(ask)

        cur_song = db.session.get(Song, req.song_id)
        song_artist, song_title = cur_song.artist, cur_song.name

        req_obj['song_name'].append(song_title)
        req_obj['song_artist'].append(song_artist)        
        req_obj['id'].append(req.id)
    
    return jsonify({'Users':user_obj, 'Djs':dj_obj,'Songs':song_obj, 'Requests':req_obj, 'Event':event_obj})

@app.route('/apiuser', methods=['POST'])
def get_data_user():
        
    data = request.get_json()
    event_id = data['id']
    user_id = data['user_id']

    
    print("ys")
    # add_song()
    event = db.session.execute(select(Event.id, Event.name, Event.dj_id).where(Event.id == event_id)).first()
    songs = db.session.execute(select(Song.id, Song.artist, Song.name)).all()
    dj = db.session.execute(select(DJ.id, DJ.username).where(DJ.id == event.dj_id)).first()
    reqs = db.session.execute(select(Request.id, Request.timestamp, Request.dj_id, Request.song_id,Request.user_id).where(Request.in_stack == True).where(Request.user_id == user_id).order_by(Request.id.desc())).all()
    

    event_obj, dj_obj, song_obj, req_obj = {}, {}, collections.defaultdict(list), collections.defaultdict(list)
    
    event_obj['id'] = event.id
    event_obj['name'] = event.name

    dj_obj['id'] = dj.id
    dj_obj['name'] = dj.username

    for song in songs[:10]:
        song_obj['id'].append(song.id)
        song_obj['artist'].append(song.artist)
        song_obj['title'].append(song.name)

    song_ids = []

    for req in reqs:

        
        if req.song_id in song_ids:
            print(req.song_id,"get_data_user")
            continue
        
        ask =  len(db.session.execute(select(Request.id).where(Request.song_id == req.song_id).where(Request.user_id == user_id).where(Request.in_stack == True)).all())
        # i removed the event_id filter above because you cant be in two event at once, so the event should be unique. you need to leave an event to join another one
        # or you'd have to get a new userid

        req_obj['timestamp'].append(str(req.timestamp))
        req_obj['ask'].append(ask)
        song_ids.append(req.song_id)

        cur_song = db.session.get(Song, req.song_id)
        song_artist, song_title = cur_song.artist, cur_song.name

        req_obj['song_name'].append(song_title)
        req_obj['song_artist'].append(song_artist)        
        req_obj['id'].append(req.id)

    print(req_obj)
    
    return jsonify({'Djs':dj_obj,'Songs':song_obj, 'Requests':req_obj, 'Event':event_obj})


@app.route('/apidj', methods=['POST'])
def get_data_dj():
        
    data = request.get_json()
    event_id = data['id']

    event = db.session.execute(select(Event.id, Event.name, Event.dj_id).where(Event.id == event_id)).first()
    dj = db.session.execute(select(DJ.id, DJ.username).where(DJ.id == event.dj_id)).first()
    reqs = db.session.execute(select(Request.id, Request.timestamp,Request.user_id, Request.dj_id, Request.song_id).where(Request.in_stack == True).where(Request.event_id == event_id).where(Request.dj_id == event.dj_id).order_by(Request.id.desc())).all()
       

    event_obj, dj_obj, req_obj = {}, {}, collections.defaultdict(list)
    
    event_obj['id'] = event.id
    event_obj['name'] = event.name

    dj_obj['id'] = dj.id
    dj_obj['name'] = dj.username

    song_ids = []

    for req in reqs:
        
        if req.song_id in song_ids:
            continue
        
        ask =  len(db.session.execute(select(Request.id).where(Request.song_id == req.song_id).where(Request.dj_id == dj.id).where(Request.in_stack == True)).all())
        # i removed the event_id filter above because you cant be in two event at once, so the event should be unique. you need to leave an event to join another one
        # or you'd have to get a new userid

        req_obj['timestamp'].append(str(req.timestamp))
        req_obj['ask'].append(ask)
        song_ids.append(req.song_id)

        cur_song = db.session.get(Song, req.song_id)
        song_artist, song_title = cur_song.artist, cur_song.name

        req_obj['song_name'].append(song_title)
        req_obj['song_artist'].append(song_artist)        
        req_obj['id'].append(req.id)
        req_obj['room'].append('interaction_'+str(req.dj_id)+'_'+str(req.user_id))
        

    # print(req_obj)
    return jsonify({'Dj':dj_obj, 'Requests':req_obj, 'Event':event_obj})

def seeding():

    dj=DJ(username='Jay')

    u1 = App_user()
    u2 = App_user()
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

@app.route('/api/dj', methods=['POST'])
def get_maindj():
    data = request.get_json()
    ev = Event.query.get(data['id'])


    return jsonify({'id': ev.dj_id})

@app.route('/api/request', methods=['POST'])
def create_request():

    data = request.get_json()

    ans = search_songs(data['song_title'], data['song_artist'])

    if 'name' in ans:
        print('in')
        songs = db.session.execute(select(Song.id).where(Song.name == ans['name']).where(Song.artist == ans['artist'])).first()
        
        user = App_user.query.get(data['user_id'])
        req =''

        if not songs:
            print('ok')
            song = Song(name = ans['name'], artist = ans['artist'])
            db.session.add(song)
            db.session.commit()
            req = user.create_request(song.id, data['dj_id'], data['event_id'])
        
        else:
            print('ok1')
            print(songs.id,data['dj_id'], data['event_id'])
            req = user.create_request(songs.id, data['dj_id'], data['event_id'])
            


        if req !='':
            db.session.add(req)
            db.session.commit()
            print('yessir')

            room = data['room']
            print(room)

            socketio.emit('req_created', {'user_id':req.user_id, 'dj_id':req.dj_id, 'event_id':req.event_id}, to=room)

            
        else:
            print('the request is cooked')
            return {'msg':'api issue'}

    else:
        print('nah')
        return {'msg':'the song is not available at the moment'}

    return {'good':'We good'}

@app.route('/api/request_delta', methods=['POST'])
def update_request():
    data = request.get_json()


    
    db.session.execute(update(Request).where(Request.id == data['id']).values(in_stack= False))
    req = db.session.execute(select(Request.dj_id, Request.user_id,Request.event_id).where(Request.id == data['id'])).first()
    print('updated')
    if (data['cancel']):
        db.session.execute(update(Request).where(Request.id == data['id']).values(cancelled = True))

    db.session.commit()

    room = data['room']

    socketio.emit('req_updated',{'user_id':req.user_id, 'dj_id':req.dj_id, 'event_id':req.event_id},to=room)
    # print("yes")
    return "updated req"

@app.route('/api/end', methods=['POST'])
def end_session():
    data = request.get_json()
    room = data['room']
    req=''

    for req_id in data['req_id']:

        db.session.execute(update(Request).where(Request.id == req_id).values(in_stack= False))
        db.session.execute(update(Request).where(Request.id == req_id).values(cancelled = True))


    db.session.commit()
    

    if room !='IamDJ':
        req = Request.query(data['req_id'][0])
        socketio.emit('exit',{'user_id':req.user_id},room=room)
        leave_room(room)

    print('party ended')
    # print("yes")
    return {'done':'we ended the session'}

@app.route('/api/user', methods=['POST'])
def create_user():    
    # Create a new Item instance
    user = App_user()
    print(user,user.id,"ouiii")
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id})

@app.route('/api/event', methods=['POST'])
def create_event():    
    # Create a new Item instance
    data = request.get_json()
    event = Event(name= data['name'], dj_id = data['dj'])
    db.session.add(event)
    db.session.commit()
    return {'id':event.id, 'name':event.name, 'dj_id': event.dj_id}

@app.route('/api/check_event_and_dj', methods=['POST'])
def check_event_and_dj():
    data=request.get_json()
    event_id=data['ev_id']
    dj_id = data['dj_id']

    event = db.session.execute(select(Event.id,Event.dj_id).where(Event.id == event_id)).all()

    

    if len(event)==1:
        if(dj_id !=event[0].dj_id):
            return {'exist':True, 'msg': 'You are not the dj of this event, create a new one!'}
        return {'exist':True}

    return {'exist':False}

@app.route('/apidj/create', methods=['POST'])
def create_dj():
    data = request.get_json()
    # print(data)
    result = signup(data['mail'], data['pass'])
    
    if result:
        hashed = DJ.create_password(data['pass'])
        dj = DJ(username=data['name'], phone=data['phone'], email=data['mail'], password=hashed) 
        db.session.add(dj)
        db.session.commit()

        return {'id':dj.id}
    
    return {}

import bcrypt

@app.route('/apidj/check', methods=['POST'])
def confirm_dj():

    data = request.get_json()
    ans = login(data['mail'], data['pass'])
    if ans:
        dj = db.session.execute(select(DJ.id, DJ.password).where(DJ.email == data['mail'])).first()
        print(dj.password)
        # print(dj.id)
    
        return {'id':dj.id, 'exist': True, 'valid_password':bcrypt.checkpw(data['pass'].encode('utf-8'), dj.password.encode('utf-8'))} if dj.id else {'exist':'the password is in firebase but not in the db'}
    
    return {'exist':False}


def search_songs(title, singer):

    url = os.environ.get('FM_URL') 
    print(url)
    url+='=track.search'
    track = '&track=' + title
    artist = '&artist=' + singer
    API_KEY= os.environ.get('FM_API_key')
    rest = '&api_key='+ API_KEY + '&format=json'

    link = url + track + artist + rest

    print(link)
    # return ''

    try:
        response = requests.get(link)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        all_dat = response.json()  # Parse JSON data
        
        dat = all_dat['results']['trackmatches']['track']
        info = {}

        if len(dat)>0:
            dat = dat[0]
            info['name'] = dat['name']
            info['artist'] = dat['artist']
            return info # Do something with the data
        
        return {'msg':'Please double Check if the details provided are correct. If they are, this tune is not available at the moment.'}
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


@app.route('/apidj/upload-audio', methods=['POST'])
def listen_song():

    print('got in')

    file = request.files['audio']
    url = os.environ.get('RAPID_URL')

    querystring = {"timezone":"America/Chicago","locale":"en-US"}

    API_KEY= os.environ.get('RAPID_API_KEY')
    
    payload = sound_breathing(file)
    # print(payload)
 

    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }
    try:
        response = requests.post(url, data=payload, headers=headers, params=querystring)
        # print(response.json())

        all_dat = response.json()
        info = {}
        if len(all_dat)>0:
            if 'track' in all_dat:
                info['title'] = all_dat['track']['title']
                info['artist'] = all_dat['track']['subtitle']
            else:
                info['title'] = "Didn't recognize the song, try again!"
                info['artist'] = all_dat['timezone']

            
        
        return info
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('req_updated')
def handle_req_updated(message):
    print('Request updated')

@socketio.on('req_created')
def handle_req_created(message):
    print('Request created')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')



@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    print(room,"joined")
    print(data)
    if data['access']=='user':
        socketio.emit('new_room', {'room_id': room})


# @socketio.on('ping')
# def ping_clients():
#     # print('pinging')
#     while True:
#         socketio.sleep(25)  # Sleeps are managed by Flask-SocketIO
#         # print('start ping')
#         socketio.emit('ping', {'data': 'Keeping connection alive'})


# @socketio.on('pong')
# def handle_pong(payload):
#     print('Pong received:', payload)
