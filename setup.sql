-- Make sure to insert data into the User table first
INSERT INTO "User" (username, email, password, registration_day, last_login_day) VALUES
('john_doe', 'john.doe@example.com', 'hashed_password', NOW(), NOW()),
('jane_smith', 'jane.smith@example.com', 'hashed_password', NOW(), NOW()),
('alice_jones', 'alice.jones@example.com', 'hashed_password', NOW(), NOW()),
('bob_brown', 'bob.brown@example.com', 'hashed_password', NOW(), NOW()),
('carol_white', 'carol.white@example.com', 'hashed_password', NOW(), NOW()),
('david_clark', 'david.clark@example.com', 'hashed_password', NOW(), NOW()),
('eva_black', 'eva.black@example.com', 'hashed_password', NOW(), NOW()),
('frank_hall', 'frank.hall@example.com', 'hashed_password', NOW(), NOW()),
('grace_lee', 'grace.lee@example.com', 'hashed_password', NOW(), NOW()),
('harry_king', 'harry.king@example.com', 'hashed_password', NOW(), NOW());

-- After users are inserted, now insert images
INSERT INTO Image (timestamp, caption, user_id, image_link, pinned) VALUES
(NOW(), 'A beautiful sunset', 1, 'http://example.com/sunset.jpg', FALSE),
(NOW(), 'Delicious homemade pizza', 2, 'http://example.com/pizza.jpg', TRUE),
(NOW(), 'Scenic Mountain View', 3, 'http://example.com/mountain.jpg', FALSE),
(NOW(), 'City at Night', 4, 'http://example.com/city.jpg', TRUE),
(NOW(), 'Winter Wonderland', 5, 'http://example.com/winter.jpg', TRUE),
(NOW(), 'Spring Blossoms', 6, 'http://example.com/spring.jpg', FALSE),
(NOW(), 'Summer Beach Fun', 7, 'http://example.com/beach.jpg', TRUE),
(NOW(), 'Autumn Leaves', 8, 'http://example.com/autumn.jpg', FALSE),
(NOW(), 'Night Sky Stars', 9, 'http://example.com/stars.jpg', TRUE),
(NOW(), 'Early Morning Dew', 10, 'http://example.com/dew.jpg', FALSE);


-- Insert data into the Comment table
INSERT INTO Comment (post_id, user_id, content, comment_data) VALUES
(1, 2, 'This sunset tip was really useful!', NOW()),
(2, 1, 'Cant wait to try this pizza recipe!', NOW()),
(3, 4, 'Great advice on the hiking gear.', NOW()),
(4, 3, 'Love the city photos!', NOW()),
(5, 6, 'Really helpful for my winter trips.', NOW()),
(6, 5, 'The flowers look amazing.', NOW()),
(7, 8, 'Beach photography is my favorite.', NOW()),
(8, 7, 'Autumn leaves are the best to capture.', NOW()),
(9, 10, 'These stargazing tips are stellar!', NOW()),
(10, 9, 'Morning dew photos look magical.', NOW()),
(1, 3, 'I also tried these tips; they are great!', NOW()),
(2, 4, 'This will be my weekend project!', NOW()),
(3, 5, 'Just bought my new hiking boots!', NOW()),
(4, 6, 'Urban photography is quite challenging.', NOW()),
(5, 7, 'Can these techniques work for rain photography too?', NOW());


-- Insert data into the Reaction table
INSERT INTO Reaction (reaction_id, user_id, image_id, like_type) VALUES
(1, 1, 2, TRUE),
(2, 2, 1, FALSE),
(3, 3, 4, TRUE),
(4, 4, 3, FALSE),
(5, 5, 6, TRUE),
(6, 6, 5, FALSE),
(7, 7, 8, TRUE),
(8, 8, 7, FALSE),
(9, 9, 10, TRUE),
(10, 10, 9, FALSE),
(11, 1, 3, TRUE),
(12, 2, 4, FALSE),
(13, 3, 5, TRUE),
(14, 4, 6, FALSE),
(15, 5, 7, TRUE);

-- Insert data into the Friendship table
INSERT INTO Friendship (user_id_one, user_id_two) VALUES
(1, 2),
(1, 3),
(1, 4),
(2, 3),
(2, 5),
(3, 6),
(4, 5),
(4, 6),
(5, 7),
(6, 8),
(7, 8),
(7, 9),
(8, 10),
(9, 10),
(2, 4);

INSERT INTO Post (user_id, title, content, post_data, last_modified_data, image_id, difficulty_level) VALUES
(1, 'Sunset Photography Tips', 'Learn how to capture stunning sunsets.', NOW(), NOW(), 1, 'easy'),
(2, 'Ultimate Pizza Making', 'Your guide to making delicious pizza at home.', NOW(), NOW(), 2, 'medium'),
(3, 'Mountain Hiking Essentials', 'Must-have gear for your next mountain hike.', NOW(), NOW(), 3, 'hard'),
(4, 'Urban Night Photography', 'Techniques for capturing vibrant city nights.', NOW(), NOW(), 4, 'medium'),
(5, 'Winter Photography Guide', 'Tips for shooting in cold weather.', NOW(), NOW(), 5, 'hard'),
(6, 'Spring Flowers to Capture', 'Best spring flowers for photographers.', NOW(), NOW(), 6, 'easy'),
(7, 'Beach Photography Tips', 'Capture the perfect beach day.', NOW(), NOW(), 7, 'easy'),
(8, 'Autumn Colors', 'How to photograph autumn leaves.', NOW(), NOW(), 8, 'medium'),
(9, 'Stargazing Photography', 'Guide to capturing the night sky.', NOW(), NOW(), 9, 'hard'),
(10, 'Morning Dew', 'Techniques for macro photography of dew.', NOW(), NOW(), 10, 'easy');
