-- Enable foreign key constraints if not enabled
PRAGMA foreign_keys = ON;

-- Drop the new__core_story table if it exists
DROP TABLE IF EXISTS new__core_story;

-- Create new__core_story table with proper constraints
CREATE TABLE IF NOT EXISTS new__core_story (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,  -- Ensure author_id is NOT NULL
    media_url TEXT,
    media_type TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    valid_user_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES auth_user(id)  -- Assuming author_id is a foreign key
);

-- Copy existing data to the new__core_story table, ensuring author_id is not NULL
INSERT INTO new__core_story (author_id, media_url, media_type, created_at)
SELECT author_id, media_url, media_type, created_at FROM core_story
WHERE author_id IS NOT NULL;  -- Filter out rows where author_id is NULL

-- Drop the original core_story table if it exists
DROP TABLE IF EXISTS core_story;

-- Rename the new__core_story table to core_story
ALTER TABLE new__core_story RENAME TO core_story;

-- Verify the table structure of core_story after renaming
PRAGMA table_info(core_story);

-- Verify the data in core_story after migration
SELECT * FROM core_story;
