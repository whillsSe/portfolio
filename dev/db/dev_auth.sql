GRANT SELECT, INSERT, UPDATE ON *.* TO `dev_auth`@`%` IDENTIFIED BY PASSWORD '*BC75FCA529D5095BE4399F28595058357D534EBA';

GRANT SELECT, INSERT, UPDATE, REFERENCES ON `tascal`.`users` TO `dev_auth`@`%`;

GRANT SELECT, INSERT, UPDATE ON `tascal`.`refresh_tokens` TO `dev_auth`@`%`;

GRANT SELECT, INSERT, UPDATE ON `tascal`.`authentication` TO `dev_auth`@`%`;