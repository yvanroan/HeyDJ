# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x



from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from dataclasses import dataclass
import bcrypt

@dataclass
class DJ(db.Model):

    __tablename__ = 'dj'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))#make sure to hash the password when in prod( look up bcrypt)
    #optional above has to be removed when moving to prod
    accepted_requests: so.Mapped[Optional[int]]= so.mapped_column(sa.Integer, default=0)
    events : so.WriteOnlyMapped['Event'] = so.relationship(back_populates='dj')
    incoming_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='dj')

    session = []
    MAX_REQUEST = 20
    cur_session_len=0
    is_shazamed = True
    played = 0

    # print(f"The wild {username} DJ has appeared!")
    
    def __repr__(self):
        return '<A wild DJ {name} has accepted {plays} song request>'.format(name=self.username,plays=self.accepted_requests)
    
    # def create_profile(name, email, password, phone):this cant be done here
        #these attributes' validity should be checked on the front end
    
    def create_password(password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


    def add_to_stack(self,request:'Request'):
        if self.cur_session_len > self.MAX_REQUEST:
            print("Max request for your queue/session has been reached. accept or deny more request to get more requests")
            return
        
        self.cur_session_len+=1

        self.session.append(request)
        print("we have added the request to the session")

    def shazam(self, request: 'Request'):
        self.is_shazamed = not self.is_shazamed
        
        request.Status = self.is_shazamed

        print("We are shazaming, give us a sec..")

        print("done shazaming :)")

        return self.is_shazamed

    def manage_session(self, accept:bool, request:'Request'):
        song = Song.query.get(request.song_id)
        song_title, song_artist = song.name, song.artist

        if accept:
            #countdown starts
            # function to check if the song was played
            # if shazam_fxn(song_detail)
            if self.shazam(request):
                print(f"Yeah, the song {song_title} by {song_artist} has been shazamed and is being played!") #if song is played
                self.played+=1
            else:
                print(f"The song {song_title} by {song_artist} will stay in the session since it wasn't played") #if countdown elapsed or we couldn't find the song, which ever happen first
            
        else:
            idx = 0

            for req in self.session: 
                if req.id == request.id:
                    self.session.pop(idx)

                idx+=1
            print(f'The request containing {song_title} by {song_artist} has been removed from the session')
        return
    
    def end_job(self):
        self.session.clear()
        print(f"You had a great night with {self.played} request accpeted. Thank you for using the app!")
        return self.played
  
@dataclass
class App_user(db.Model):

    __tablename__ = 'app_user'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    outgoing_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='app_user')

    # print(f"The night slayer {id} has join the party!")

    def __repr__(self):
        return '<User {}>'.format(self.id)
    
    def create_request(self, song_id,djid, event_id,tips):
        print("a request is being created")
        
        cur_dj = db.session.get(DJ,djid).username
        cur_song = db.session.get(Song, song_id)

        if not cur_dj:
            print("can't find that dj in the db")

        if not cur_song:
            print("can't find that song in the db")

        request = Request(in_stack=True, dj_id= djid,song_id=song_id, user_id=self.id, event_id= event_id, cancelled=False, tips=tips)
        
        return request
    
@dataclass
class Song(db.Model):
    __tablename__ = 'song'
    id: so.Mapped[int] = so.mapped_column(primary_key=True) 
    name: so.Mapped[str] = so.mapped_column(sa.String, index=True)
    artist: so.Mapped[str] = so.mapped_column(sa.String)
    genre: so.Mapped[Optional[str]] = so.mapped_column(sa.String)
    ongoing_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='song')

    def __repr__(self):
        return '<Song: {name} by {artist}>'.format(name=self.name, artist=self.artist)

class Event(db.Model):
    __tablename__ = 'event'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String)
    place: so.Mapped[Optional[str]] = so.mapped_column(sa.String)
    theme: so.Mapped[Optional[str]] = so.mapped_column(sa.String)
    dj_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(DJ.id), index=True)
    dj: so.Mapped[DJ] = so.relationship(back_populates='events')
    event_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='event')

@dataclass  
class Request(db.Model):
    __tablename__ = 'request'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    in_stack: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    dj_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(DJ.id), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(App_user.id))
    song_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Song.id), index=True)
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Event.id), index=True)
    cancelled: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    tips: so.Mapped[float] = so.mapped_column(sa.Float)
    app_user: so.Mapped[App_user] = so.relationship(back_populates='outgoing_request')
    song: so.Mapped[Song] = so.relationship(back_populates='ongoing_request')
    dj: so.Mapped[DJ] = so.relationship(back_populates='incoming_request')
    event: so.Mapped[Event] = so.relationship(back_populates='event_request')
    
    # change Status to in_stack
    #you need to add another parameter here, cancelled which tells us if a request was cancel or not.
    # because status only account for the prescence of the request in the queue or not.
    # and think of changing status to "completed" instead, it make more sense
    def __repr__(self):
        return '<Request {}>'.format(self.DJ_id)
    

    
