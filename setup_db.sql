-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS kbnda_dev_db;
CREATE USER IF NOT EXISTS 'kbnda_dev'@'localhost' IDENTIFIED BY 'kbnda_dev_pwd';
GRANT ALL PRIVILEGES ON `kbnda_dev_db`.* TO 'kbnda_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'kbnda_dev'@'localhost';
FLUSH PRIVILEGES;
