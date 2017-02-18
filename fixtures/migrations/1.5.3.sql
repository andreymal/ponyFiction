--
-- Migrate new registrations
--
ALTER TABLE stories.registration_registrationprofile ADD activated BOOLEAN DEFAULT FALSE NOT NULL;
UPDATE registration_registrationprofile SET activated = TRUE WHERE activation_key = 'ALREADY_ACTIVATED';