--
-- Save story's words in separated field
--

ALTER TABLE ponyFiction_story ADD COLUMN words INTEGER NOT NULL DEFAULT 0;

CREATE TEMPORARY TABLE tmp_story_words (
  story_id    INT NOT NULL,
  words_count INT NOT NULL DEFAULT 0
)
  ENGINE = MEMORY
  AS
    SELECT
      story_id,
      SUM(words) AS words_count
    FROM ponyFiction_chapter
    GROUP BY story_id;

UPDATE ponyFiction_story
  LEFT JOIN tmp_story_words
    ON tmp_story_words.story_id = ponyFiction_story.id
SET ponyFiction_story.words = IFNULL(
    tmp_story_words.words_count,
    DEFAULT(ponyFiction_story.words)
);

DROP TEMPORARY TABLE tmp_story_words;

--
-- Create table for static pages
--
CREATE TABLE ponyFiction_staticpage (
  id      INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  name    VARCHAR(128)           NOT NULL,
  title   VARCHAR(255)           NOT NULL,
  content LONGTEXT               NOT NULL,
  updated DATETIME               NOT NULL
);
CREATE INDEX ponyFiction_staticpage_b068931c ON ponyFiction_staticpage (name);

--
-- Add column for category's label color
--
ALTER TABLE ponyFiction_category ADD COLUMN color VARCHAR(7) NOT NULL;

UPDATE ponyFiction_category
  SET color = CASE name
    WHEN 'Приключения' THEN '#3F74CE'
    WHEN 'Кроссовер' THEN '#EDA21F'
    WHEN 'Романтика' THEN '#CEC12A'
    WHEN 'Драма' THEN '#45C950'
    WHEN 'Ангст' THEN '#45C9AB'
    WHEN 'Флафф' THEN '#CA6565'
    WHEN 'Юмор' THEN '#D84A9D'
    WHEN 'Зарисовка' THEN '#8738D8'
    WHEN 'Экшн' THEN '#B5835A'
    WHEN 'Ужасы' THEN '#808080'
    WHEN 'Эротика' THEN '#CA0707'
    WHEN 'Повседневность' THEN '#8760B0'
    ELSE '#cccccc'
  END;

--
-- Remove NOT NULL constraint causing manage.py createsuperuser to fail
--
ALTER TABLE ponyFiction_author MODIFY COLUMN last_login DATETIME NULL DEFAULT NULL;
