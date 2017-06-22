BEGIN;

-- migrate admin 0002_logentry_remove_auto_add
INSERT INTO `django_migrations` (`app`, `name`, `applied`) VALUES ('admin', '0002_logentry_remove_auto_add', '2017-06-22 00:00:00.000000');

-- migrate auth 0007_alter_validators_add_error_messages
INSERT INTO `django_migrations` (`app`, `name`, `applied`) VALUES ('auth', '0007_alter_validators_add_error_messages', '2017-06-22 00:00:00.000000');

-- migrate registration 0004_supervisedregistrationprofile
--
-- Create model SupervisedRegistrationProfile
--
CREATE TABLE `registration_supervisedregistrationprofile` (`registrationprofile_ptr_id` integer NOT NULL PRIMARY KEY);
ALTER TABLE `registration_supervisedregistrationprofile` ADD CONSTRAINT `D1dc58cae9bed3b42fe3afa704e85f11` FOREIGN KEY (`registrationprofile_ptr_id`) REFERENCES `registration_registrationprofile` (`id`);

INSERT INTO `django_migrations` (`app`, `name`, `applied`) VALUES ('registration', '0004_supervisedregistrationprofile', '2017-06-22 00:00:00.000000');

COMMIT;
