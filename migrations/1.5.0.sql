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
