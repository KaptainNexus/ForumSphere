-- Insert data into the User table
INSERT INTO "users" (username, email, password, registration_day, last_login_day)
VALUES
('john_doe', 'john.doe@example.com', 'hashed_password', NOW(), NOW()),
('jane_smith', 'jane.smith@example.com', 'hashed_password', NOW(), NOW());

-- Insert data into the Image table
INSERT INTO Image (timestamp, caption, user_id, image_link, pinned)
VALUES
(NOW(), 'A beautiful sunset', 1, 'http://example.com/sunset.jpg', FALSE),
(NOW(), 'Delicious homemade pizza', 2, 'http://example.com/pizza.jpg', TRUE);
-- Insert data into the User table
INSERT INTO "users" (username, email, password, registration_day, last_login_day)
VALUES
('john_doe', 'john.doe@example.com', 'hashed_password', NOW(), NOW()),
('jane_smith', 'jane.smith@example.com', 'hashed_password', NOW(), NOW());

-- Insert data into the Image table
INSERT INTO Image (timestamp, caption, user_id, image_link, pinned)
VALUES
(NOW(), 'A beautiful sunset', 1, 'http://example.com/sunset.jpg', FALSE),
(NOW(), 'Delicious homemade pizza', 2, 'http://example.com/pizza.jpg', TRUE);

-- Insert data into the Post table
INSERT INTO Post (user_id, title, content, post_data, last_modified_data, image_id, difficulty_level)
VALUES
(1, 'Sunset Photography Tips', 'Here are some tips for taking stunning sunset photos...', NOW(), NOW(), 1, 'easy'),
(2, 'Cooking 101', 'Learn to cook delicious meals with simple ingredients...', NOW(), NOW(), 2, 'medium');

-- Insert data into the Comment table
INSERT INTO Comment (post_id, user_id, content, comment_data)
VALUES
(1, 2, 'Great tips! Thanks for sharing.', NOW()),
(2, 1, 'I would love to try this recipe!', NOW());

-- Insert data into the Reaction table
INSERT INTO Reaction (reaction_id, user_id, image_id, like_type)
VALUES
(1, 1, 2, TRUE),
(2, 2, 1, FALSE);

-- Insert data into the Friendship table
INSERT INTO Friendship (user_id_one, user_id_two)
VALUES
(1, 2);  -- Assuming user_id 1 is less than user_id 2 based on the check constraint

-- Insert data into the Post table
INSERT INTO Post (user_id, title, content, post_data, last_modified_data, image_id, difficulty_level)
VALUES
(1, 'Sunset Photography Tips', 'Here are some tips for taking stunning sunset photos...', NOW(), NOW(), 1, 'easy'),
(2, 'Cooking 101', 'Learn to cook delicious meals with simple ingredients...', NOW(), NOW(), 2, 'medium');

-- Insert data into the Comment table
INSERT INTO Comment (post_id, user_id, content, comment_data)
VALUES
(1, 2, 'Great tips! Thanks for sharing.', NOW()),
(2, 1, 'I would love to try this recipe!', NOW());

-- Insert data into the Reaction table
INSERT INTO Reaction (reaction_id, user_id, image_id, like_type)
VALUES
(1, 1, 2, 'like'),
(2, 2, 1, 'heart');

-- Insert data into the Friendship table
INSERT INTO Friendship (user_id_one, user_id_two)
VALUES
(1, 2);  -- Assuming user_id 1 is less than user_id 2 based on the check constraint

-- Insert data into the Friendship table
INSERT INTO Friendship (user_id_one, user_id_two)
VALUES
(1, 2);  -- Assuming user_id 1 is less than user_id 2 based on the check constraint