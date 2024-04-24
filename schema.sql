
CREATE DATABASE final_project;

CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    registration_day TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login_day TIMESTAMP NOT NULL DEFAULT NOW()
);