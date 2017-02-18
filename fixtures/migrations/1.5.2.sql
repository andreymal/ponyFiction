--
-- Create table for news
--
CREATE TABLE IF NOT EXISTS ponyFiction_newsitem (
  id      INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  title   VARCHAR(255)           NOT NULL,
  text    LONGTEXT               NOT NULL,
  visible TINYINT(1) DEFAULT 0   NOT NULL,
  updated DATETIME               NOT NULL
);
CREATE INDEX ponyFiction_newsitem_f852084e ON ponyFiction_newsitem (title);
