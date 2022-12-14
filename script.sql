DROP DATABASE IF EXISTS `o1233239_dataset`;
CREATE DATABASE `o1233239_dataset`;

DROP TABLE IF EXISTS `Image`;
CREATE TABLE `Image` (
  `IdUser` bigint(20) UNSIGNED NOT NULL,
  `Path` varchar(255) NOT NULL
);

DROP TABLE IF EXISTS `People`;
CREATE TABLE `People` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `FIO` varchar(50) NOT NULL,
  `Encodings` text NOT NULL,
  `Date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TRIGGER IF EXISTS `DELETE IMAGE`;
CREATE TRIGGER `DELETE IMAGE` BEFORE DELETE ON `People` FOR EACH ROW BEGIN
    DELETE
        FROM `Image`
            WHERE `IdUser` = old.`ID`;
    END

ALTER TABLE `Image`
  ADD PRIMARY KEY (`IdUser`,`Path`);

ALTER TABLE `People`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `People`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `Image`
  ADD CONSTRAINT `UserImage` FOREIGN KEY (`IdUser`) REFERENCES `People` (`ID`);
COMMIT;
