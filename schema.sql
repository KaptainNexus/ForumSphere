

User
CREATE TABLE Users
(
    user_id    SERIAL PRIMARY KEY,
    email      VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name  VARCHAR(255) NOT NULL,
    password   VARCHAR(255) NOT NULL
);

CREATE TABLE Images (
    image_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    caption VARCHAR(255),
    user_id INTEGER NOT NULL,
    image_link VARCHAR(255) NOT NULL,
    pinned BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_user
        FOREIGN KEY Users(user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE Posts
(
    post_id    SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES Users(user_id),
    title      VARCHAR(255) NOT NULL,
    content    TEXT NOT NULL,
    last_modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_id INTEGER REFERENCES Images(image_id), 
    tag_id INTEGER REFERENCES Tags(tag_id),
    difficulty INTEGER NOT NULL
);

CREATE TABLE Comments
(
    comment_id SERIAL PRIMARY KEY,
    post_id    INTEGER REFERENCES Posts(post_id),
    user_id    INTEGER REFERENCES Users(user_id),
    content    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Likes
(
    like_id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES Posts(post_id),
    user_id INTEGER REFERENCES Users(user_id)
);

CREATE TABLE Follows
(
    follow_id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES Users(user_id),
    followee_id INTEGER REFERENCES Users(user_id)
);

CREATE TYPE tag AS ENUM ('Beginner', 'Intermediate', 'Advanced', 'Expert', 'Gaming', 'Fintech', 'WEB3', 'Managment/Communications', 'Systems',
'Cyber Security', 'Data Sci/AI/ML', 'Blockchain','Metaverse', 'Cloud Computing', 'Networks', 'Operating Systems', 'Hardware/Firmware');

CREATE TABLE Tags
(
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL,
    tag_type tag
);

CREATE TABLE Friendship
(
    friendship_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    friend_id INTEGER REFERENCES Users(user_id)
);

CREATE TABLE PostTags
(
    post_id INTEGER REFERENCES Posts(post_id),
    tag_id INTEGER REFERENCES Tags(tag_id),
    PRIMARY KEY (post_id, tag_id)
);

-- Figure out what the differnce between post_data and last_modified_at is
-- How to add the tags to the post table, might not need to Tags table and 
-- just the tag type that we can use in the post table not sure
