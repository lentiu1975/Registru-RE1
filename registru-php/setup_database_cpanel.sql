-- Script automat pentru crearea bazei de date in cPanel
-- NOTA: Acest script trebuie executat din phpMyAdmin cu userul ROOT al cPanel-ului

-- 1. Creează database
CREATE DATABASE IF NOT EXISTS `lentiuro_vamactasud` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Creează user (parola: VamaCtaSud2025!)
-- NOTA: În cPanel, userul va fi automat prefixat cu 'lentiuro_'
CREATE USER IF NOT EXISTS 'lentiuro_vamauser'@'localhost' IDENTIFIED BY 'VamaCtaSud2025!';

-- 3. Acordă privilegii
GRANT ALL PRIVILEGES ON `lentiuro_vamactasud`.* TO 'lentiuro_vamauser'@'localhost';
FLUSH PRIVILEGES;

-- 4. Selectează database-ul
USE `lentiuro_vamactasud`;

-- 5. Importă schema (din database.sql)
-- TABELE

-- Țări
CREATE TABLE IF NOT EXISTS `countries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(3) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tipuri containere
CREATE TABLE IF NOT EXISTS `container_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `description` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Porturi
CREATE TABLE IF NOT EXISTS `ports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `country_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `ports_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Nave
CREATE TABLE IF NOT EXISTS `ships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `imo_number` varchar(20) DEFAULT NULL,
  `flag_country_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `flag_country_id` (`flag_country_id`),
  CONSTRAINT `ships_ibfk_1` FOREIGN KEY (`flag_country_id`) REFERENCES `countries` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Manifeste
CREATE TABLE IF NOT EXISTS `manifests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `manifest_number` varchar(50) NOT NULL,
  `ship_id` int DEFAULT NULL,
  `arrival_date` date NOT NULL,
  `port_of_loading_id` int DEFAULT NULL,
  `port_of_discharge_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `manifest_number` (`manifest_number`),
  KEY `ship_id` (`ship_id`),
  KEY `port_of_loading_id` (`port_of_loading_id`),
  KEY `port_of_discharge_id` (`port_of_discharge_id`),
  CONSTRAINT `manifests_ibfk_1` FOREIGN KEY (`ship_id`) REFERENCES `ships` (`id`) ON DELETE SET NULL,
  CONSTRAINT `manifests_ibfk_2` FOREIGN KEY (`port_of_loading_id`) REFERENCES `ports` (`id`) ON DELETE SET NULL,
  CONSTRAINT `manifests_ibfk_3` FOREIGN KEY (`port_of_discharge_id`) REFERENCES `ports` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Intrări manifest (containere)
CREATE TABLE IF NOT EXISTS `manifest_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `manifest_id` int NOT NULL,
  `container_number` varchar(20) NOT NULL,
  `container_type_id` int DEFAULT NULL,
  `seal_number` varchar(50) DEFAULT NULL,
  `goods_description` text,
  `weight` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `manifest_id` (`manifest_id`),
  KEY `container_type_id` (`container_type_id`),
  KEY `idx_container_number` (`container_number`),
  CONSTRAINT `manifest_entries_ibfk_1` FOREIGN KEY (`manifest_id`) REFERENCES `manifests` (`id`) ON DELETE CASCADE,
  CONSTRAINT `manifest_entries_ibfk_2` FOREIGN KEY (`container_type_id`) REFERENCES `container_types` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Useri
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Log import
CREATE TABLE IF NOT EXISTS `import_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  `rows_imported` int DEFAULT '0',
  `errors` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `import_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- DATE INIȚIALE

-- User admin (username: admin, password: admin123)
INSERT INTO `users` (`username`, `password`, `email`, `role`)
VALUES ('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin@vamactasud.lentiu.ro', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- Tipuri containere comune
INSERT INTO `container_types` (`code`, `description`) VALUES
('20GP', '20ft General Purpose'),
('40GP', '40ft General Purpose'),
('40HC', '40ft High Cube'),
('20RF', '20ft Reefer'),
('40RF', '40ft Reefer'),
('20OT', '20ft Open Top'),
('40OT', '40ft Open Top'),
('20FR', '20ft Flat Rack'),
('40FR', '40ft Flat Rack')
ON DUPLICATE KEY UPDATE code=code;

-- Câteva țări importante
INSERT INTO `countries` (`code`, `name`) VALUES
('RO', 'România'),
('TR', 'Turcia'),
('GR', 'Grecia'),
('BG', 'Bulgaria'),
('IT', 'Italia'),
('DE', 'Germania'),
('CN', 'China'),
('US', 'SUA')
ON DUPLICATE KEY UPDATE code=code;

-- Porturi importante
INSERT INTO `ports` (`code`, `name`, `country_id`) VALUES
('ROCND', 'Constanta', (SELECT id FROM countries WHERE code='RO')),
('ROBAS', 'Basarabi', (SELECT id FROM countries WHERE code='RO')),
('TRIST', 'Istanbul', (SELECT id FROM countries WHERE code='TR')),
('GRPIR', 'Pireu', (SELECT id FROM countries WHERE code='GR'))
ON DUPLICATE KEY UPDATE code=code;
