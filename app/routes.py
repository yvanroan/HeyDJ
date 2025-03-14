#all the data coming from the front end will be sent here
#this is where we will be creating the instances and adding them to the database
# functions from each class will be used here to implement the actual flow of the app

#i had to copy the flask_cors folder from github to be able to use it here.

from flask_cors import CORS
from app import app, db, socketio
from app.models import App_user, DJ, Song, Request, Event
from flask import jsonify, request, render_template
import collections
from sqlalchemy import select, update, func, extract, text
import os
import requests
from dotenv import load_dotenv
from app.encode_decode import sound_breathing
from app.auth import login, signup
from flask_socketio import join_room,leave_room
import bcrypt
from datetime import datetime


CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login_page():
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

@app.route('/djentry')
def djentry():
    return render_template('djentry.html')

@app.route('/dj')
def dj():
    return render_template('dj.html')

@app.route('/exit')
def exit():
    return render_template('exit.html')

@app.route('/apiuser', methods=['POST'])
def get_data_user():
        
    data = request.get_json()
    event_id = data['id']
    user_id = data['user_id']

    event = db.session.execute(select(Event.id, Event.name, Event.dj_id).where(Event.id == event_id)).first()
    reqs = db.session.execute(select(Request.id, Request.timestamp, Request.dj_id, Request.song_id,Request.user_id, Request.tips).where(Request.in_stack == True).where(Request.user_id == user_id).order_by(Request.id.desc())).all()
    


    event_obj, req_obj = {}, collections.defaultdict(list)

    event_obj['id'] = event_id
    event_obj['name'] = event.name

    song_ids = set()

    for req in reqs:
        ask=0

        if req.song_id in song_ids:
            continue
        
        for r in reqs:
            if r.song_id == req.song_id:
                ask +=1
        # i removed the event_id filter above because you cant be in two event at once, so the event should be unique. you need to leave an event to join another one
        # or you'd have to get a new userid

        req_obj['timestamp'].append(str(req.timestamp))
        req_obj['ask'].append(ask)
        song_ids.add(req.song_id)

        cur_song = db.session.get(Song, req.song_id)
        song_artist, song_title = cur_song.artist, cur_song.name

        req_obj['song_name'].append(song_title)
        req_obj['song_artist'].append(song_artist)        
        req_obj['id'].append(req.id)
        req_obj['tips'].append(req.tips)
        
    print(req_obj)
    
    return jsonify({'Requests':req_obj, 'Event':event_obj})

@app.route('/apidj', methods=['POST'])
def get_data_dj():
        
    data = request.get_json()
    event_id = data['id']
    
     
    event = db.session.execute(select(Event.id, Event.name, Event.dj_id).where(Event.id == event_id)).first()
    dj = db.session.execute(select(DJ.id, DJ.username).where(DJ.id == event.dj_id)).first()
    reqs = db.session.execute(select(Request.id, Request.timestamp,Request.user_id, Request.dj_id, Request.song_id, Request.event_id, Request.tips).where(Request.in_stack == True).where(Request.event_id == event_id).order_by(Request.id.desc())).all()
      

    event_obj, dj_obj, req_obj = {}, {}, collections.defaultdict(list)

    song_ids = set()
    user_ids = set()
    event_obj['id'] = event_id
    event_obj['name'] = event.name


    dj_obj['id'] = dj.id
    dj_obj['name'] = dj.username

    for req in reqs:

        if req.song_id in song_ids:
            continue
        
        ask =  len([r for r in reqs if r.song_id == req.song_id and r.dj_id == dj.id])
        # i removed the event_id filter above because you cant be in two event at once, so the event should be unique. you need to leave an event to join another one
        # or you'd have to get a new userid
        #removed in_Stack=true because all the request are already in the stack

        req_obj['timestamp'].append(str(req.timestamp))
        req_obj['ask'].append(ask)
        song_ids.add(req.song_id)

        cur_song = db.session.get(Song, req.song_id)
        song_artist, song_title = cur_song.artist, cur_song.name

        req_obj['song_name'].append(song_title)
        req_obj['song_artist'].append(song_artist)        
        req_obj['id'].append(req.id)
        req_obj['tips'].append(req.tips)
        if req.user_id not in user_ids:
            req_obj['room'].append('interaction_'+str(req.dj_id)+'_'+str(req.user_id)+'_'+str(req.event_id))
            user_ids.add(req.user_id)
        

    print(req_obj)
    return jsonify({'Dj':dj_obj, 'Requests':req_obj, 'Event':event_obj})

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
        song = db.session.execute(select(Song.id).where(Song.name == ans['name']).where(Song.artist == ans['artist'])).first()
        
        user = App_user.query.get(data['user_id'])
        req =''

        if not song:
            new_song = Song(name = ans['name'], artist = ans['artist'])
            db.session.add(new_song)
            db.session.commit()
            req = user.create_request(new_song.id, data['dj_id'], data['event_id'], data['tips'])
        
        else:
            req = user.create_request(song.id, data['dj_id'], data['event_id'], data['tips'])
            


        if req !='':
            db.session.add(req)
            db.session.commit()

            room = data['room']
            print('room', room)

            socketio.emit('req_created', {'user_id':req.user_id, 'dj_id':req.dj_id, 'event_id':req.event_id, 'tips': req.tips}, to=room)

            
        else:
            print('the request is cooked')
            return {'msg':'api issue'}

    else:
        print('the song is not available at the moment')
        return {'msg':'the song is not available at the moment'}

    return {'good':'We good'}

@app.route('/api/request_delta', methods=['POST'])
def update_request():
    data = request.get_json()

    ref_request = db.session.execute(
        select(Request.song_id, Request.event_id, Request.dj_id)
        .where(Request.id == data['id'])
    ).first()

    db.session.execute(
        update(Request)
        .where(Request.song_id == ref_request.song_id)
        .where(Request.event_id == ref_request.event_id)
        .where(Request.dj_id == ref_request.dj_id)
        .where(Request.in_stack == True)  # Only update active requests
        .values(
            in_stack=False,
            cancelled=data['cancel']
        )
    )
    req = db.session.execute(select(Request.dj_id, Request.user_id,Request.event_id).where(Request.id == data['id'])).first()

    db.session.commit()

    room = data['room']

    socketio.emit('req_updated',{'user_id':req.user_id, 'dj_id':req.dj_id, 'event_id':req.event_id},to=room)

    return "updated req"

@app.route('/api/end', methods=['POST'])
def end_session():
    data = request.get_json()
    rooms = data['room']
    access= data['access']
    req=''

    for req_id in data['req_id']:

        db.session.execute(update(Request).where(Request.id == req_id).values(in_stack= False))
        db.session.execute(update(Request).where(Request.id == req_id).values(cancelled = True))


    db.session.commit()
    

    if access !='IamDJ':
        req = Request.query(data['req_id'][0])
        socketio.emit('exit',{'user_id':req.user_id},room=rooms)
        leave_room(rooms)

    else:
        for room in set(rooms):
            socketio.emit('exit_user',room=room)
            leave_room(room)
    


    print('party ended')
    return {'done':'we ended the session'}

@app.route('/api/user', methods=['POST'])
def create_user():    
    # Create a new Item instance
    user = App_user()
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
    result = signup(data['mail'], data['pass'])
    
    if result:
        hashed = DJ.create_password(data['pass'])
        dj = DJ(username=data['name'], phone=data['phone'], email=data['mail'], password=hashed) 
        db.session.add(dj)
        db.session.commit()

        return {'id':dj.id}
    
    return {}

@app.route('/apidj/check', methods=['POST'])
def confirm_dj():

    data = request.get_json()
    ans = login(data['mail'], data['pass'])
    print('ans', ans)
    if ans:
        dj = db.session.execute(select(DJ.id, DJ.password).where(DJ.email == data['mail'])).first()
        
    
        return {'id':dj.id, 'exist': True, 'valid_password':bcrypt.checkpw(data['pass'].encode('utf-8'), dj.password.encode('utf-8'))} if dj.id else {'exist':'the password is in firebase but not in the db'}
    
    return {'exist':False}


def search_songs(title, singer):

    url = os.environ.get('FM_URL') 
    url+='=track.search'
    track = '&track=' + title
    artist = '&artist=' + singer
    API_KEY= os.environ.get('FM_API_key')
    rest = '&api_key='+ API_KEY + '&format=json'

    link = url + track + artist + rest


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

    file = request.files['audio']
    url = os.environ.get('RAPID_URL')

    querystring = {"timezone":"America/Chicago","locale":"en-US"}

    API_KEY= os.environ.get('RAPID_API_KEY')
    
    payload = sound_breathing(file)
 

    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }
    try:
        response = requests.post(url, data=payload, headers=headers, params=querystring)

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
    if data['access']=='user':
        socketio.emit('new_room', {'room_id': room})

@app.route('/dj/dashboard')
def dj_dashboard():
    return render_template('djdashboard.html')


@app.route('/api/dj/stats/<dj_id>', methods=['GET'])
def get_dj_stats(dj_id):
    # Get current month stats
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Top played songs
    top_played = db.session.execute(
        select(Song.name, Song.artist, func.count(Request.id).label('play_count'))
        .join(Request, Song.id == Request.song_id)
        .where(Request.dj_id == dj_id)
        .where(Request.in_stack == False)
        .where(Request.cancelled == False)
        .group_by(Song.id)
        .order_by(text('play_count DESC'))
        .limit(5)
    ).all()

    # Top cancelled songs
    top_cancelled = db.session.execute(
        select(Song.name, Song.artist, func.count(Request.id).label('cancel_count'))
        .join(Request, Song.id == Request.song_id)
        .where(Request.dj_id == dj_id)
        .where(Request.cancelled == True)
        .group_by(Song.id)
        .order_by(text('cancel_count DESC'))
        .limit(5)
    ).all()

    # Tips stats
    current_month_tips = db.session.execute(
        select(func.sum(Request.tips))
        .where(Request.dj_id == dj_id)
        .where(extract('month', Request.timestamp) == current_month)
        .where(extract('year', Request.timestamp) == current_year)
    ).scalar() or 0

    total_tips = db.session.execute(
        select(func.sum(Request.tips))
        .where(Request.dj_id == dj_id)
    ).scalar() or 0

    dj_details = db.session.execute(select(DJ.username).where(DJ.id == dj_id)).first()

    return jsonify({
        'dj_details': {
            'name': dj_details.username
        },
        'top_played': [
            {'title': song.name, 'artist': song.artist, 'count': song.play_count}
            for song in top_played
        ],
        'top_cancelled': [
            {'title': song.name, 'artist': song.artist, 'count': song.cancel_count}
            for song in top_cancelled
        ],
        'tips': {
            'current_month': float(current_month_tips),
            'all_time': float(total_tips)
        }
    })