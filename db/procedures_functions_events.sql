-- this script has 1 event, 1 procedure and 1 function

DELIMITER $$
CREATE PROCEDURE add_game_review(
    IN p_user_id INT,
    IN p_game_id INT,
    IN p_title VARCHAR(255),
    IN p_text VARCHAR(255),
    IN p_stars INT
)
BEGIN
    IF p_stars NOT BETWEEN 1 AND 10 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Star rating must be between 1 and 10';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM user WHERE id = p_user_id) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'User does not exist';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM game WHERE id = p_game_id) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Game does not exist';
    END IF;

    INSERT INTO review (title, text, star_amount, user_id, game_id)
    VALUES (p_title, p_text, p_stars, p_user_id, p_game_id);

    SELECT LAST_INSERT_ID() AS new_review_id;
END$$
DELIMITER ;

-- event updates game.bgg_rating everyday day
DELIMITER $$
CREATE EVENT update_bgg_ratings
ON SCHEDULE EVERY 1 DAY
STARTS '2025-12-07 16:22:00'
DO
BEGIN
    UPDATE game g
    SET g.bgg_rating = (
        SELECT AVG(r.star_amount)
        FROM review r
        WHERE r.game_id = g.id
    )
    WHERE g.id IS NOT NULL;
END $$
DELIMITER ;

-- function GetGameReviewCount(game id)
DELIMITER $$
CREATE FUNCTION GetGameReviewCount(p_game_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN (SELECT COUNT(*) FROM review WHERE game_id = p_game_id);
END $$
DELIMITER ;