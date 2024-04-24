-- Start transaction
BEGIN;

-- Create alembic_version table
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('bb0b549de322');

-- Create dj table
CREATE TABLE dj (
    id SERIAL PRIMARY KEY, 
    username VARCHAR(64) NOT NULL, 
    phone VARCHAR(64), 
    email VARCHAR(120), 
    password VARCHAR(256), 
    accepted_requests INTEGER DEFAULT 0
);
INSERT INTO dj (username, phone, email, password, accepted_requests) VALUES
('Jay', NULL, NULL, NULL, 0);
-- Create song table
CREATE TABLE song (
    id SERIAL PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    artist VARCHAR NOT NULL, 
    genre VARCHAR
);
INSERT INTO song (name, artist, genre) VALUES
('Zero', 'Chris Brown', NULL),
('Soro', 'Adekunle GOLD', NULL),
('Water', 'Tyla', NULL),
('Melanin', 'Sauti Sol', NULL),
('Tuesday (feat. Drake)', 'iLoveMakonnen', NULL),
('Monalisa', 'LoJay', NULL),
('Dumebi', 'Rema', NULL),
('Ojuelegba', 'Wizkid', NULL),
('Me & U', 'Tems', NULL);

-- Create app_user table
CREATE TABLE app_user (
    id SERIAL PRIMARY KEY
);
INSERT INTO app_user (id) SELECT generate_series(1, 3);

-- Create event table
CREATE TABLE event (
    id SERIAL PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    place VARCHAR, 
    theme VARCHAR, 
    dj_id INTEGER NOT NULL REFERENCES dj(id)
);
INSERT INTO event (name, place, theme, dj_id) VALUES
('Party Next Door', NULL, NULL, 1);

-- Create request table
CREATE TABLE request (
    id SERIAL PRIMARY KEY, 
    timestamp TIMESTAMP NOT NULL, 
    in_stack BOOLEAN NOT NULL, 
    dj_id INTEGER NOT NULL REFERENCES dj(id), 
    user_id INTEGER NOT NULL REFERENCES app_user(id), 
    song_id INTEGER NOT NULL REFERENCES song(id), 
    event_id INTEGER NOT NULL REFERENCES event(id), 
    cancelled BOOLEAN NOT NULL
);
-- Add request inserts if necessary

-- Create indexes
CREATE INDEX ix_dj_username ON dj (username);
CREATE INDEX ix_song_name ON song (name);
CREATE INDEX ix_event_dj_id ON event (dj_id);
CREATE INDEX ix_request_dj_id ON request (dj_id);
CREATE INDEX ix_request_event_id ON request (event_id);
CREATE INDEX ix_request_song_id ON request (song_id);

-- Commit transaction
COMMIT;