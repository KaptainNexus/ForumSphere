INSERT INTO Users (email, first_name, last_name, password) VALUES
('alice@example.com', 'Alice', 'Smith', 'password123'),
('bob@example.com', 'Bob', 'Johnson', 'password456'),
('carol@example.com', 'Carol', 'Williams', 'password789');

INSERT INTO Images (timestamp, caption, user_id, image_link, pinned) VALUES
('2023-10-01 12:00:00', 'First Post Image', 1, 'https://example.com/image1.jpg', FALSE),
('2023-10-02 12:30:00', 'Second Post Image', 2, 'https://example.com/image2.jpg', TRUE);

INSERT INTO Tags (tag_name, tag_type) VALUES
('Beginner Tutorial', 'Beginner'),
('Advanced Security', 'Advanced');

INSERT INTO Posts (user_id, title, content, image_id, tag_id, difficulty) VALUES
(1, 'Hello World', 'This is the content of the first post.', 1, 1, 1),
(2, 'Advanced SQL', 'Content for advanced SQL techniques.', 2, 2, 5);

INSERT INTO Comments (post_id, user_id, content) VALUES
(1, 2, 'Great post, Alice!'),
(2, 1, 'This was very helpful, thanks Bob!');

INSERT INTO Likes (post_id, user_id) VALUES
(1, 3),
(2, 1);

INSERT INTO Follows (follower_id, followee_id) VALUES
(1, 2),
(2, 1);


INSERT INTO Friendship (user_id, friend_id) VALUES
(1, 2),
(2, 3);

INSERT INTO PostTags (post_id, tag_id) VALUES
(1, 1),
(2, 2);



