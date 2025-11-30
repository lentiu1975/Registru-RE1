-- Registru Import RE1 - Structură Bază de Date
-- Creat pentru: vama.lentiu.ro
-- Data: 2025-11-30

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Tabelul pentru utilizatori
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `last_login` TIMESTAMP NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserează utilizator implicit (parola: admin123)
INSERT INTO `users` (`username`, `password`) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');

-- Tabelul pentru nave
CREATE TABLE IF NOT EXISTS `ships` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `image` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelul pentru porturi
CREATE TABLE IF NOT EXISTS `ports` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `country` VARCHAR(100) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelul pentru manifeste
CREATE TABLE IF NOT EXISTS `manifests` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `manifest_number` VARCHAR(100) NOT NULL,
  `ship_id` INT DEFAULT NULL,
  `arrival_date` DATE DEFAULT NULL,
  `port_id` INT DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`ship_id`) REFERENCES `ships`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`port_id`) REFERENCES `ports`(`id`) ON DELETE SET NULL,
  INDEX `idx_manifest_number` (`manifest_number`),
  INDEX `idx_arrival_date` (`arrival_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelul pentru înregistrări manifest (containere)
CREATE TABLE IF NOT EXISTS `manifest_entries` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `manifest_id` INT NOT NULL,
  `container_number` VARCHAR(50) NOT NULL,
  `container_type` VARCHAR(20) DEFAULT NULL COMMENT 'Ex: 20G1, 40G1, 45G1',
  `seal_number` VARCHAR(100) DEFAULT NULL,
  `goods_description` TEXT DEFAULT NULL,
  `weight` DECIMAL(10,2) DEFAULT NULL COMMENT 'Greutate în kg',
  `shipper` VARCHAR(255) DEFAULT NULL,
  `consignee` VARCHAR(255) DEFAULT NULL,
  `marks_numbers` TEXT DEFAULT NULL,
  `country_of_origin` VARCHAR(100) DEFAULT NULL,
  `country_code` VARCHAR(10) DEFAULT NULL,
  `container_image` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`manifest_id`) REFERENCES `manifests`(`id`) ON DELETE CASCADE,
  INDEX `idx_container_number` (`container_number`),
  INDEX `idx_manifest_id` (`manifest_id`),
  INDEX `idx_country_code` (`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelul pentru tipuri de containere
CREATE TABLE IF NOT EXISTS `container_types` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `code` VARCHAR(20) NOT NULL UNIQUE COMMENT 'Ex: 20G1, 40G1, 45G1',
  `prefix` VARCHAR(10) NOT NULL COMMENT 'Ex: GCXU, TRHU, MEDU',
  `description` VARCHAR(255) DEFAULT NULL,
  `image` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserează tipuri de containere inițiale
INSERT INTO `container_types` (`code`, `prefix`, `description`) VALUES
('20G1', 'GCXU', 'Container general 20 picioare'),
('22G1', 'GCXU', 'Container general 22 picioare'),
('40G1', 'TRHU', 'Container general 40 picioare'),
('45G1', 'MEDU', 'Container general 45 picioare');

-- Tabelul pentru țări
CREATE TABLE IF NOT EXISTS `countries` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `code` VARCHAR(10) NOT NULL UNIQUE,
  `flag_image` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserează câteva țări comune
INSERT INTO `countries` (`name`, `code`) VALUES
('România', 'RO'),
('Germania', 'DE'),
('Franța', 'FR'),
('Italia', 'IT'),
('Spania', 'ES'),
('Turcia', 'TR'),
('China', 'CN'),
('Statele Unite', 'US'),
('Marea Britanie', 'GB');

-- Tabelul pentru log-uri import
CREATE TABLE IF NOT EXISTS `import_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `filename` VARCHAR(255) NOT NULL,
  `rows_imported` INT DEFAULT 0,
  `rows_failed` INT DEFAULT 0,
  `status` ENUM('success', 'partial', 'failed') DEFAULT 'success',
  `error_message` TEXT DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
