# `dev_api`@`%` に対する権限

GRANT SELECT, INSERT, UPDATE ON *.* TO `dev_api`@`%` IDENTIFIED BY PASSWORD '*BC75FCA529D5095BE4399F28595058357D534EBA';

GRANT SELECT, INSERT ON `tascal`.`tags` TO `dev_api`@`%`;

GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON `tascal`.`tasks` TO `dev_api`@`%`;

GRANT SELECT, INSERT, UPDATE, DELETE ON `tascal`.`task_tag` TO `dev_api`@`%`;

GRANT SELECT, UPDATE (`profilename`), REFERENCES ON `tascal`.`users` TO `dev_api`@`%`;


# `dev_auth`@`%` に対する権限

GRANT SELECT, INSERT, UPDATE ON *.* TO `dev_auth`@`%` IDENTIFIED BY PASSWORD '*BC75FCA529D5095BE4399F28595058357D534EBA';

GRANT SELECT, INSERT, UPDATE, REFERENCES ON `tascal`.`users` TO `dev_auth`@`%`;

GRANT SELECT, INSERT, UPDATE ON `tascal`.`refresh_tokens` TO `dev_auth`@`%`;

GRANT SELECT, INSERT, UPDATE ON `tascal`.`authentication` TO `dev_auth`@`%`;