BEGIN;
-- migrate auth 0008_alter_user_username_max_length
INSERT INTO `django_migrations` (`app`, `name`, `applied`) VALUES ('auth', '0008_alter_user_username_max_length', '2017-06-22 00:00:00.000000');

COMMIT;
