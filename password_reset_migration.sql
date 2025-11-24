-- password_reset_migration.sql
ALTER TABLE `usuarios`
ADD COLUMN `reset_token` VARCHAR(255) NULL DEFAULT NULL,
ADD COLUMN `reset_token_expires` DATETIME NULL DEFAULT NULL;