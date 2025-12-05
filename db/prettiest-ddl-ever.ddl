DROP DATABASE IF EXISTS testDB;
CREATE DATABASE testDB;
USE testDB;

CREATE TABLE designer (
    id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    dob date,
    PRIMARY KEY (id)
);

CREATE TABLE game (
    id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    slug varchar(255),
    year_published year,
    bgg_rating double,
    difficulty_rating double,
    description text,
    playing_time int(10),
    available tinyint(1),
    min_players int(10),
    max_players int(10),
    minimum_age int(10),
    thumbnail text,
    image text,
    PRIMARY KEY (id)
);

CREATE TABLE artist (
    id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    dob date,
    PRIMARY KEY (id)
);

CREATE TABLE genre (
    id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    description varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE `user` (
    id int(10) NOT NULL AUTO_INCREMENT,
    display_name varchar(55) NOT NULL UNIQUE,
    username varchar(255) NOT NULL UNIQUE,
    dob date,
    password varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE game_genres (
    game_id int(10) NOT NULL,
    genre_id int(10) NOT NULL,
    PRIMARY KEY (game_id, genre_id)
);

-- review now directly references game (many reviews per game, each review belongs to exactly one game)
CREATE TABLE review (
    id int(10) NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    text varchar(255),
    star_amount int(10) NOT NULL,
    user_id int(10) NOT NULL,
    game_id int(10) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE mechanic (
    id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

-- game_reviews removed: not needed for many-to-one

CREATE TABLE game_designers (
    game_id int(10) NOT NULL,
    designer_id int(10) NOT NULL,
    PRIMARY KEY (game_id, designer_id)
);

CREATE TABLE game_artists (
    game_id int(10) NOT NULL,
    artist_id int(10) NOT NULL,
    PRIMARY KEY (game_id, artist_id)
);

CREATE TABLE game_publishers (
    game_id int(10) NOT NULL,
    publisher_id int(10) NOT NULL,
    PRIMARY KEY (game_id, publisher_id)
);

CREATE TABLE game_mechanics (
    game_id int(10) NOT NULL,
    mechanic_id int(10) NOT NULL,
    PRIMARY KEY (game_id, mechanic_id)
);

CREATE TABLE `language` (
    id int(10) NOT NULL AUTO_INCREMENT,
    `language` varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE publisher (
    id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE video (
    id int(10) NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    category varchar(255) NOT NULL,
    link varchar(255) NOT NULL,
    game_id int(10) NOT NULL,
    language_id int(10) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE game_genres
    ADD CONSTRAINT FKgame_genre12575 FOREIGN KEY (genre_id) REFERENCES genre (id),
    ADD CONSTRAINT FKgame_genre659841 FOREIGN KEY (game_id) REFERENCES game (id);

ALTER TABLE review
    ADD CONSTRAINT FKreview880296 FOREIGN KEY (user_id) REFERENCES `user` (id),
    ADD CONSTRAINT FKreview_game FOREIGN KEY (game_id) REFERENCES game (id);

ALTER TABLE game_designers
    ADD CONSTRAINT FKgame_desig685981 FOREIGN KEY (game_id) REFERENCES game (id),
    ADD CONSTRAINT FKgame_desig253052 FOREIGN KEY (designer_id) REFERENCES designer (id);

ALTER TABLE game_artists
    ADD CONSTRAINT FKgame_artis11592 FOREIGN KEY (game_id) REFERENCES game (id),
    ADD CONSTRAINT FKgame_artis914658 FOREIGN KEY (artist_id) REFERENCES artist (id);

ALTER TABLE game_publishers
    ADD CONSTRAINT FKgame_publi1 FOREIGN KEY (game_id) REFERENCES game (id),
    ADD CONSTRAINT FKgame_publi2 FOREIGN KEY (publisher_id) REFERENCES publisher (id);

ALTER TABLE game_mechanics
    ADD CONSTRAINT FKgame_mech1 FOREIGN KEY (game_id) REFERENCES game (id),
    ADD CONSTRAINT FKgame_mech2 FOREIGN KEY (mechanic_id) REFERENCES mechanic (id);

ALTER TABLE video
    ADD CONSTRAINT FKvideo235072 FOREIGN KEY (game_id) REFERENCES game (id),
    ADD CONSTRAINT FKvideo738401 FOREIGN KEY (language_id) REFERENCES `language` (id);

CREATE TABLE audit_log (
    id BIGINT NOT NULL AUTO_INCREMENT,
    table_name VARCHAR(64) NOT NULL,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    row_pk VARCHAR(255) NOT NULL,
    changed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(255) NULL,
    old_data JSON NULL,
    new_data JSON NULL,
    PRIMARY KEY (id)
);

DELIMITER $$

CREATE TRIGGER trg_game_ai
AFTER INSERT ON game
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        table_name, operation, row_pk, changed_by, old_data, new_data
    )
    VALUES (
        'game',
        'INSERT',
        CAST(NEW.id AS CHAR),
        CURRENT_USER(),
        NULL,
        JSON_OBJECT(
            'id', NEW.id,
            'name', NEW.name,
            'slug', NEW.slug,
            'year_published', NEW.year_published,
            'bgg_rating', NEW.bgg_rating,
            'difficulty_rating', NEW.difficulty_rating,
            'description', NEW.description,
            'playing_time', NEW.playing_time,
            'available', NEW.available,
            'min_players', NEW.min_players,
            'max_players', NEW.max_players,
            'minimum_age', NEW.minimum_age,
            'thumbnail', NEW.thumbnail,
            'image', NEW.image
        )
    );
END$$

CREATE TRIGGER trg_game_au
AFTER UPDATE ON game
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        table_name, operation, row_pk, changed_by, old_data, new_data
    )
    VALUES (
        'game',
        'UPDATE',
        CAST(NEW.id AS CHAR),
        CURRENT_USER(),
        JSON_OBJECT(
            'id', OLD.id,
            'name', OLD.name,
            'slug', OLD.slug,
            'year_published', OLD.year_published,
            'bgg_rating', OLD.bgg_rating,
            'difficulty_rating', OLD.difficulty_rating,
            'description', OLD.description,
            'playing_time', OLD.playing_time,
            'available', OLD.available,
            'min_players', OLD.min_players,
            'max_players', OLD.max_players,
            'minimum_age', OLD.minimum_age,
            'thumbnail', OLD.thumbnail,
            'image', OLD.image
        ),
        JSON_OBJECT(
            'id', NEW.id,
            'name', NEW.name,
            'slug', NEW.slug,
            'year_published', NEW.year_published,
            'bgg_rating', NEW.bgg_rating,
            'difficulty_rating', NEW.difficulty_rating,
            'description', NEW.description,
            'playing_time', NEW.playing_time,
            'available', NEW.available,
            'min_players', NEW.min_players,
            'max_players', NEW.max_players,
            'minimum_age', NEW.minimum_age,
            'thumbnail', NEW.thumbnail,
            'image', NEW.image
        )
    );
END$$

CREATE TRIGGER trg_game_ad
AFTER DELETE ON game
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        table_name, operation, row_pk, changed_by, old_data, new_data
    )
    VALUES (
        'game',
        'DELETE',
        CAST(OLD.id AS CHAR),
        CURRENT_USER(),
        JSON_OBJECT(
            'id', OLD.id,
            'name', OLD.name,
            'slug', OLD.slug,
            'year_published', OLD.year_published,
            'bgg_rating', OLD.bgg_rating,
            'difficulty_rating', OLD.difficulty_rating,
            'description', OLD.description,
            'playing_time', OLD.playing_time,
            'available', OLD.available,
            'min_players', OLD.min_players,
            'max_players', OLD.max_players,
            'minimum_age', OLD.minimum_age,
            'thumbnail', OLD.thumbnail,
            'image', OLD.image
        ),
        NULL
    );
END$$

DELIMITER ;

