-- Insert migration record for core_artist if needed
INSERT INTO django_migrations (app, name, applied)
VALUES ('core', '0001_initial', datetime('now'));

-- Optionally mark all migrations for 'core' as applied
-- UPDATE django_migrations SET applied = datetime('now') WHERE app = 'core';

-- Verify migration status for 'core'
SELECT * FROM django_migrations WHERE app = 'core';