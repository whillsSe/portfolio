# `tascalapi`@`%` に対する権限

GRANT SELECT, INSERT, UPDATE ON *.* TO `tascalapi`@`%` IDENTIFIED BY PASSWORD 'threadTascalApiPassW0rd';

GRANT SELECT, INSERT ON `tascal`.`tags` TO `tascalapi`@`%`;

GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON `tascal`.`tasks` TO `tascalapi`@`%`;

GRANT SELECT, INSERT, UPDATE, DELETE ON `tascal`.`task_tag` TO `tascalapi`@`%`;

GRANT SELECT, UPDATE (`profilename`), REFERENCES ON `tascal`.`users` TO `tascalapi`@`%`;


# `tascalauth`@`%` に対する権限

GRANT SELECT, INSERT, UPDATE ON *.* TO `tascalauth`@`%` IDENTIFIED BY PASSWORD 'threadTascalAuthPassW0rd';

GRANT SELECT, INSERT, UPDATE, REFERENCES ON `tascal`.`users` TO `tascalauth`@`%`;

GRANT SELECT, INSERT, UPDATE ON `tascal`.`refresh_tokens` TO `tascalauth`@`%`;

GRANT SELECT, INSERT, UPDATE ON `tascal`.`authentication` TO `tascalauth`@`%`;