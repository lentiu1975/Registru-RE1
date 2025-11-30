-- Fix password pentru user admin
-- Password: admin123

UPDATE users SET password = '$2y$12$NVBspn5rHq7oK51hGsLzcekUoP7wT5H56xRHFaadTeHu/ZbkiYjea' WHERE username = 'admin';
