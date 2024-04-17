INSERT INTO Users (email, first_name, last_name, password) 
VALUES 
    ('user1@example.com', 'John', 'Doe', 'password1'),
    ('user2@example.com', 'Jane', 'Smith', 'password2'),
    ('user3@example.com', 'Michael', 'Johnson', 'password3');

INSERT INTO Images (timestamp, caption, user_id, image_link, pinned) 
VALUES 
    ('2024-04-16 12:00:00', 'Beautiful sunset', 1, 'https://example.com/image1.jpg', TRUE),
    ('2024-04-15 15:30:00', 'Cute puppy', 2, 'https://example.com/image2.jpg', FALSE),
    ('2024-04-14 09:45:00', 'Delicious food', 3, 'https://example.com/image3.jpg', TRUE);

INSERT INTO Posts (user_id, title, content, image_id, tag_id, difficulty) 
VALUES 
    (1, 'Introduction to SQL', 'This is a beginner-friendly guide to SQL.', NULL, 1, 1),
    (2, 'Advanced Python Techniques', 'Explore advanced Python programming techniques.', NULL, 4, 3),
    (3, 'Web3 Development Basics', 'Learn the fundamentals of Web3 development.', NULL, 6, 2);

INSERT INTO Comments (post_id, user_id, content) 
VALUES 
    (1, 2, 'Great tutorial!'),
    (2, 3, 'I learned a lot from this.'),
    (3, 1, 'Looking forward to more content like this.');

INSERT INTO Likes (post_id, user_id) 
VALUES 
    (1, 2),
    (2, 3),
    (3, 1);

INSERT INTO Follows (follower_id, followee_id) 
VALUES 
    (1, 2),
    (2, 3),
    (3, 1);

INSERT INTO Tags (tag_name, tag_type) 
VALUES 
    ('SQL', 'Beginner'),
    ('Python', 'Advanced'),
    ('Web3', 'Intermediate');

INSERT INTO Friendship (user_id, friend_id) 
VALUES 
    (1, 2),
    (2, 3),
    (3, 1);

INSERT INTO PostTags (post_id, tag_id) 
VALUES 
    (1, 1),
    (2, 2),
    (3, 3);