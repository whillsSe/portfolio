GRANT SELECT, INSERT, UPDATE ON *.* TO `dev_api`@`%` IDENTIFIED BY PASSWORD '*BC75FCA529D5095BE4399F28595058357D534EBA';

GRANT SELECT, INSERT ON `tascal`.`tags` TO `dev_api`@`%`;

GRANT SELECT, INSERT, UPDATE, REFERENCES ON `tascal`.`tasks` TO `dev_api`@`%`;

GRANT SELECT, UPDATE (`profilename`), REFERENCES ON `tascal`.`users` TO `dev_api`@`%`;

GRANT SELECT, INSERT, UPDATE, DELETE ON `tascal`.`task_tag` TO `dev_api`@`%`;