DROP DATABASE IF EXISTS gametable;
CREATE DATABASE gametable;
USE gametable;


CREATE TABLE designer (id int(10) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, dob date, PRIMARY KEY (id));
CREATE TABLE game (id int(10) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, slug varchar(255), year_published varchar(5), bgg_rating double, difficulty_rating double, description varchar(255), play_time int(10), available boolean, min_players int(10), max_players int(10), PRIMARY KEY (id));
CREATE TABLE artists (id int(10) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, dob date, PRIMARY KEY (id));
CREATE TABLE genre (id int(10) NOT NULL AUTO_INCREMENT, title varchar(30) NOT NULL, description varchar(255), PRIMARY KEY (id));
CREATE TABLE matchup (id int(10) NOT NULL AUTO_INCREMENT, game_id int(10) NOT NULL, start_time date, end_time date, created_at date, is_private bit(1) NOT NULL, created_by_user_id int(10), user_id_winner int(10) NOT NULL, user_id_1 int(10) NOT NULL, user_id_2 int(10) NOT NULL, PRIMARY KEY (id));
CREATE TABLE `user` (id int(10) NOT NULL AUTO_INCREMENT, display_name varchar(25) NOT NULL UNIQUE, username varchar(255) NOT NULL UNIQUE, password varchar(255) NOT NULL, dob date NOT NULL, email varchar(255) NOT NULL, PRIMARY KEY (id));
CREATE TABLE game_genres (game_id int(10) NOT NULL, genre_id int(10) NOT NULL, PRIMARY KEY (game_id, genre_id));
CREATE TABLE review (id int(10) NOT NULL AUTO_INCREMENT, title varchar(255) NOT NULL, text varchar(255), star_amount int(10) NOT NULL, user_id int(10) NOT NULL, PRIMARY KEY (id));
CREATE TABLE game_reviews (game_id int(10) NOT NULL, review_id int(10) NOT NULL, PRIMARY KEY (game_id, review_id));
CREATE TABLE matchup_comments (id int(10) NOT NULL AUTO_INCREMENT, matchup_id int(10) NOT NULL, text varchar(255), user_id int(10) NOT NULL, PRIMARY KEY (id));
CREATE TABLE spectator (id int(10) NOT NULL AUTO_INCREMENT, matchup_id int(10) NOT NULL, PRIMARY KEY (id));
CREATE TABLE spectator_users (spectator_id int(10) NOT NULL, user_id int(10) NOT NULL, PRIMARY KEY (spectator_id, user_id));
CREATE TABLE friendship (user_id_1 int(10) NOT NULL, user_id_2 int(10) NOT NULL, status tinyint(3) NOT NULL, created_at date, updated_at date);
CREATE TABLE message (user_id_1 int(10) NOT NULL, user_id_2 int(10) NOT NULL, text varchar(255) NOT NULL, timestamp timestamp NULL);
CREATE TABLE review_comments (review_id int(10) NOT NULL, timestamp timestamp NULL, text varchar(255), created_at timestamp NULL, updated_at timestamp NULL, user_id int(10) NOT NULL);
CREATE TABLE game_designers (game_id int(10) NOT NULL, designer_id int(10) NOT NULL, PRIMARY KEY (game_id, designer_id));
CREATE TABLE game_artists (game_id int(10) NOT NULL, artists_id int(10) NOT NULL, PRIMARY KEY (game_id, artists_id));
CREATE TABLE move (id int(10) NOT NULL AUTO_INCREMENT, ply int(10) NOT NULL, start_x_coordinate int(10) NOT NULL, start_y_coordinate int(10) NOT NULL, end_x_coordinate int(10), end_y_coordinate int(10), PRIMARY KEY (id));
CREATE TABLE matchup_move (matchup_id int(10) NOT NULL, move_id int(10) NOT NULL, PRIMARY KEY (matchup_id, move_id));
ALTER TABLE matchup ADD CONSTRAINT FKmatchup425277 FOREIGN KEY (game_id) REFERENCES game (id);
ALTER TABLE game_genres ADD CONSTRAINT FKgame_genre12575 FOREIGN KEY (genre_id) REFERENCES genre (id);
ALTER TABLE game_genres ADD CONSTRAINT FKgame_genre659841 FOREIGN KEY (game_id) REFERENCES game (id);
ALTER TABLE matchup ADD CONSTRAINT FKmatchup501864 FOREIGN KEY (user_id_winner) REFERENCES `user` (id);
ALTER TABLE matchup ADD CONSTRAINT FKmatchup660710 FOREIGN KEY (user_id_1) REFERENCES `user` (id);
ALTER TABLE matchup ADD CONSTRAINT FKmatchup660711 FOREIGN KEY (user_id_2) REFERENCES `user` (id);
ALTER TABLE game_reviews ADD CONSTRAINT FKgame_revie642759 FOREIGN KEY (game_id) REFERENCES game (id);
ALTER TABLE game_reviews ADD CONSTRAINT FKgame_revie516416 FOREIGN KEY (review_id) REFERENCES review (id);
ALTER TABLE review ADD CONSTRAINT FKreview880296 FOREIGN KEY (user_id) REFERENCES `user` (id);
ALTER TABLE matchup_comments ADD CONSTRAINT FKmatchup_co159819 FOREIGN KEY (matchup_id) REFERENCES matchup (id);
ALTER TABLE matchup_comments ADD CONSTRAINT FKmatchup_co681866 FOREIGN KEY (user_id) REFERENCES `user` (id);
ALTER TABLE spectator ADD CONSTRAINT FKspectator716181 FOREIGN KEY (matchup_id) REFERENCES matchup (id);
ALTER TABLE spectator_users ADD CONSTRAINT FKspectator_455085 FOREIGN KEY (spectator_id) REFERENCES spectator (id);
ALTER TABLE spectator_users ADD CONSTRAINT FKspectator_618930 FOREIGN KEY (user_id) REFERENCES `user` (id);
ALTER TABLE friendship ADD CONSTRAINT FKfriendship953283 FOREIGN KEY (user_id_1) REFERENCES `user` (id);
ALTER TABLE friendship ADD CONSTRAINT FKfriendship953282 FOREIGN KEY (user_id_2) REFERENCES `user` (id);
ALTER TABLE message ADD CONSTRAINT FKmessage723391 FOREIGN KEY (user_id_1) REFERENCES `user` (id);
ALTER TABLE message ADD CONSTRAINT FKmessage723392 FOREIGN KEY (user_id_2) REFERENCES `user` (id);
ALTER TABLE review_comments ADD CONSTRAINT FKreview_com177365 FOREIGN KEY (user_id) REFERENCES `user` (id);
ALTER TABLE review_comments ADD CONSTRAINT FKreview_com396043 FOREIGN KEY (review_id) REFERENCES review (id);
ALTER TABLE game_designers ADD CONSTRAINT FKgame_desig685981 FOREIGN KEY (game_id) REFERENCES game (id);
ALTER TABLE game_designers ADD CONSTRAINT FKgame_desig253052 FOREIGN KEY (designer_id) REFERENCES designer (id);
ALTER TABLE game_artists ADD CONSTRAINT FKgame_artis11592 FOREIGN KEY (game_id) REFERENCES game (id);
ALTER TABLE game_artists ADD CONSTRAINT FKgame_artis914658 FOREIGN KEY (artists_id) REFERENCES artists (id);
ALTER TABLE matchup_move ADD CONSTRAINT FKmatchup_mo278129 FOREIGN KEY (matchup_id) REFERENCES matchup (id);
ALTER TABLE matchup_move ADD CONSTRAINT FKmatchup_mo312622 FOREIGN KEY (move_id) REFERENCES move (id);


-- event
ALTER TABLE matchup ADD COLUMN is_expired TINYINT(1) DEFAULT 0;
CREATE EVENT expire_stale_matchups
ON SCHEDULE EVERY 1 DAY
DO
  UPDATE matchup
  SET is_expired = 1
  WHERE end_time IS NULL AND start_time < CURDATE() - INTERVAL 30 DAY;
  
  
-- trigger 
DELIMITER $$

CREATE TRIGGER hash_password_before_insert
BEFORE INSERT ON user
FOR EACH ROW
BEGIN
   SET NEW.password = SHA2(NEW.password, 256);
END;
$$

DELIMITER ;


-- procedure can be called with:
-- CALL create_matchup(12, 5, 9, 5, b'0', CURRENT_DATE());
DELIMITER $$
CREATE PROCEDURE create_matchup(
  IN p_game_id INT,
  IN p_user_id_1 INT,
  IN p_user_id_2 INT,
  IN p_created_by_user_id INT,
  IN p_is_private BIT,
  IN p_start_time DATE
)
BEGIN
  -- Validate game and users exist
  IF NOT EXISTS (SELECT 1 FROM game WHERE id = p_game_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Game not found';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM `user` WHERE id = p_user_id_1) OR
     NOT EXISTS (SELECT 1 FROM `user` WHERE id = p_user_id_2) OR
     NOT EXISTS (SELECT 1 FROM `user` WHERE id = p_created_by_user_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'One or more users not found';
  END IF;

  INSERT INTO matchup (game_id, start_time, end_time, created_at, is_private, ply, created_by_user_id, user_id_winner, user_id_1, user_id_2)
  VALUES (p_game_id, p_start_time, NULL, CURRENT_DATE(), p_is_private, NULL, p_created_by_user_id, 0, p_user_id_1, p_user_id_2);

  SELECT LAST_INSERT_ID() AS matchup_id;
END$$
DELIMITER ;

-- stored function GetAverageRating ()

DELIMITER $$
CREATE FUNCTION GetAverageRating(gameId INT)
RETURNS DOUBLE
DETERMINISTIC
BEGIN
    DECLARE avg_rating DOUBLE;

    SELECT AVG(r.star_amount)
    INTO avg_rating
    FROM game_reviews gr
    JOIN review r ON gr.review_id = r.id
    WHERE gr.game_id = gameId;

    RETURN IFNULL(avg_rating, 0);
END$$
DELIMITER ;

-- example for index with user display_name
CREATE INDEX idx_user_display_name ON user(display_name);
