-- Migrare COMPLETA din Django la PHP MySQL

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Containere (3195) - DELETE OLD DATA
DELETE FROM manifest_entries;
DELETE FROM manifests;

INSERT IGNORE INTO manifests (manifest_number, ship_name, ship_flag, arrival_date) VALUES ('153', 'MAX SCHULTE', 'PA', '2025-11-26');
