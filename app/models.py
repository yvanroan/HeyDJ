# https://stackoverflow.com/questions/23340812/python-sqlite-table-a-has-no-column-named-x


from typing import Optional
from datetime import datetime, timezone
import time
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db



class DJ(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    #optional above has to be removed when moving to prod
    accepted_requests: so.Mapped[int]= so.mapped_column(sa.Integer, default=0)
    incoming_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='dj')

    session = []
    MAX_REQUEST = 20
    cur_session_len=0
    is_shazamed = True
    played = 0

    print(f"The wild {username} DJ has appeared!")

    def __repr__(self):
        return '<DJ {name} has accepted {plays} song request>'.format(name=self.username,plays=self.accepted_requests)
    
    # def create_profile(name, email, password, phone):this cant be done here
        #these attributes' validity should be checked on the front end
    
    def add_to_session(self,request:'Request'):
        if self.cur_session_len > self.MAX_REQUEST:
            print("Max request for your queue/session has been reached. accept or deny more request to get more requests")
            return
        
        self.cur_session_len+=1

        self.session.append(request)
        # time.sleep(2)
        print("we have added the request to the session")

    def shazam(self, request: 'Request'):
        self.is_shazamed = not self.is_shazamed
        
        request.Status = self.is_shazamed

        print("We are shazaming, give us a sec..")

        # time.sleep(2)
        print("done shazaming :)")

        return self.is_shazamed

    def manage_session(self, accept:bool, request:'Request'):
        song = Song.query.get(request.song_id)
        song_title, song_artist = song.name, song.artist

        if accept:
            # start = time.time()
            #countdown starts
            # function to check if the song was played
            # if shazam_fxn(song_detail)
            if self.shazam(request):
                # time.sleep(2)
                print(f"Yeah, the song {song_title} by {song_artist} has been shazamed and is being played!") #if song is played
                self.played+=1
            else:
                # time.sleep(2)
                print(f"The song {song_title} by {song_artist} will stay in the session since it wasn't played") #if countdown elapsed or we couldn't find the song, which ever happen first
            
        else:
            idx = 0

            for req in self.session: 
                if req.id == request.id:
                    self.session.pop(idx)

                idx+=1
            # time.sleep(2)
            print(f'The request containing {song_title} by {song_artist} has been removed from the session')
        return
    
    def end_job(self):
        self.session.clear()
        # time.sleep(2)
        print(f"You had a great night with {self.played} request accpeted. Thank you for using the app!")
        return self.played
  
class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    outgoing_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='user')

    print(f"The night slayer {id} has join the party!")

    def __repr__(self):
        return '<User {}>'.format(self.id)
    
    def create_request(self, song_id,dj_id):
        # print("a request is being created")
        request = Request(Status=False, DJ_id= dj_id,song_id=song_id, user_id=self.id )
        # time.sleep(2)
        print("a request has been created")
        return request
    

class Song(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String)
    artist: so.Mapped[str] = so.mapped_column(sa.String)
    genre: so.Mapped[str] = so.mapped_column(sa.String)
    ongoing_request: so.WriteOnlyMapped['Request'] = so.relationship(back_populates='song')

    def __repr__(self):
        return '<Song: {name} by {artist}>'.format(name=self.name, artist=self.artist)

    
class Request(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    Status: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    DJ_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(DJ.id), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    song_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Song.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='outgoing_request')
    song: so.Mapped[Song] = so.relationship(back_populates='ongoing_request')
    dj: so.Mapped[DJ] = so.relationship(back_populates='incoming_request')

    def __repr__(self):
        return '<Request {}>'.format(self.id)