
CREATE DATABASE sandbox_project;

-- Create the ENUM type for difficulty_level
CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard');

CREATE TABLE IF NOT EXISTS "User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    registration_day TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login_day TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS Post (
    post_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    title VARCHAR(255),
    content VARCHAR(255),
    post_data TIMESTAMP,
    last_modified_data TIMESTAMP  NOT NULL DEFAULT NOW(),
    image_id INTEGER,
    difficulty_level difficulty_level NOT NULL
);
CREATE TABLE IF NOT EXISTS Comment (
    comment_id SERIAL PRIMARY KEY,
    post_id INTEGER,
    user_id INTEGER,
    content VARCHAR(255),
    comment_data TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS Image (
    image_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    caption VARCHAR(255),
    user_id INTEGER,
    image_link VARCHAR(255),
    pinned BOOLEAN
);
CREATE TABLE IF NOT EXISTS Reaction (
    reaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    image_id INTEGER,
    like_type BOOLEAN
);
CREATE TABLE IF NOT EXISTS Friendship (
    user_id_one INTEGER NOT NULL,
    user_id_two INTEGER NOT NULL,
    CONSTRAINT pk_friendship PRIMARY KEY (user_id_one, user_id_two),
    CONSTRAINT fk_user_one
        FOREIGN KEY (user_id_one)
        REFERENCES "User" (user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_user_two
        FOREIGN KEY (user_id_two)
        REFERENCES "User" (user_id)
        ON DELETE CASCADE,
    CONSTRAINT check_user_id_order CHECK (user_id_one < user_id_two)
);

-- Add foreign key constraints to Post table
ALTER TABLE Post ADD CONSTRAINT FK_Post_User FOREIGN KEY (user_id) REFERENCES "User"(user_id);
ALTER TABLE Post ADD CONSTRAINT FK_Post_Image FOREIGN KEY (image_id) REFERENCES Image(image_id);

-- Add foreign key constraints to Comment table
ALTER TABLE Comment ADD CONSTRAINT FK_Comment_Post FOREIGN KEY (post_id) REFERENCES Post(post_id);
ALTER TABLE Comment ADD CONSTRAINT FK_Comment_User FOREIGN KEY (user_id) REFERENCES "User"(user_id);

-- Add foreign key constraints to Image table
ALTER TABLE Image ADD CONSTRAINT FK_Image_User FOREIGN KEY (user_id) REFERENCES "User"(user_id);

-- Add foreign key constraints to Reaction table
ALTER TABLE Reaction ADD CONSTRAINT FK_Reaction_User FOREIGN KEY (user_id) REFERENCES "User"(user_id);
ALTER TABLE Reaction ADD CONSTRAINT FK_Reaction_Image FOREIGN KEY (image_id) REFERENCES Image(image_id);

-- Add foreign key constraints to Friendship table
ALTER TABLE Friendship ADD CONSTRAINT FK_Friendship_User_One FOREIGN KEY (user_id_one) REFERENCES "User"(user_id);
ALTER TABLE Friendship ADD CONSTRAINT FK_Friendship_User_Two FOREIGN KEY (user_id_two) REFERENCES "User"(user_id);
