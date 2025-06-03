CREATE TABLE Event (
    Event_Type integer PRIMARY KEY,
    description text NOT NULL
);

CREATE TABLE GeneralUser (
    ID_user integer PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL,
    email text NOT NULL,
    description text NOT NULL,
    permission_level integer NOT NULL,
    fake_username text
);

CREATE TABLE Ai (
    ID_user integer PRIMARY KEY,
    model_name text NOT NULL,
    prompt text NOT NULL,
    max_comment_length integer,
    comments_context_size integer,
    temp real,
    min_p real,
    FOREIGN KEY(ID_user) REFERENCES GeneralUser (ID_user)
);

CREATE TABLE Post (
    ID_post integer PRIMARY KEY,
    text text NOT NULL,
    time timestamp NOT NULL,
    like_count integer NOT NULL DEFAULT 0,
    is_reply boolean NOT NULL DEFAULT false,
    is_trending boolean NOT NULL DEFAULT false,
    ID_user integer,
    FOREIGN KEY(ID_user) REFERENCES GeneralUser (ID_user)
);

CREATE TABLE Logged (
    ID_logged integer PRIMARY KEY,
    time timestamp NOT NULL,
    IPv4 inet NOT NULL,
    page text,
    ID_user integer NOT NULL,
    Event_Type integer NOT NULL,
    FOREIGN KEY(Event_Type) REFERENCES Event (Event_Type),
    FOREIGN KEY(ID_user) REFERENCES GeneralUser (ID_user)
);

CREATE TABLE Following (
    following integer,
    follower integer,
    PRIMARY KEY(following, follower),
    FOREIGN KEY(following) REFERENCES GeneralUser (ID_user),
    FOREIGN KEY(follower) REFERENCES GeneralUser (ID_user)
);

CREATE TABLE Reacted_To (
    ID_user integer,
    ID_post integer,
    liked boolean NOT NULL DEFAULT false,
    PRIMARY KEY(ID_user, ID_post),
    FOREIGN KEY(ID_user) REFERENCES GeneralUser (ID_user),
    FOREIGN KEY(ID_post) REFERENCES Post (ID_post)
);
