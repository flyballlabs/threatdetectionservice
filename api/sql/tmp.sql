CREATE DATABASE IF NOT EXISTS `tmp`;
grant all on tmp.* TO 'tmp'@'localhost' IDENTIFIED BY 'tmp';
grant all on tmp.* TO 'tmp'@'%' IDENTIFIED BY 'tmp';
flush privileges;
use tmp;

-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: tmp
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `agent`
--

DROP TABLE IF EXISTS `agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent` (
  `agent_id` int(11) NOT NULL AUTO_INCREMENT,
  `mac_address` varchar(45) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `company_id` varchar(45) DEFAULT NULL,
  `site` varchar(45) DEFAULT NULL,
  `mode` varchar(45) DEFAULT NULL,
  `cmd` varchar(45) DEFAULT NULL,
  `time_setting` json DEFAULT NULL,
  PRIMARY KEY (`agent_id`),
  UNIQUE KEY `mac_address` (`mac_address`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent`
--

LOCK TABLES `agent` WRITE;
/*!40000 ALTER TABLE `agent` DISABLE KEYS */;
INSERT INTO `agent` VALUES (1,'4A:1D:70:CD:54:A3','10.0.0.1','1','2','new_site','stream','stop','{\"interval\": {\"update\": \"08:00:00\", \"time_sync\": \"00:05:00\", \"discover_assets\": \"48:00:00\"}, \"start_stop\": {\"stop\": \"16:00:00\", \"start\": \"08:00:00\"}}'),(2,'D4:85:64:A3:9A:27','10.0.0.17','1','2','loving','live','stop','{\"interval\": {\"update\": \"06:00:00\", \"time_sync\": \"00:15:00\", \"discover_assets\": \"12:00:00\"}, \"start_stop\": {\"stop\": \"16:00:00\", \"start\": \"08:00:00\"}}'),(3,'00:05:04:03:02:01','10.0.0.254','1','2','site_3','replay','restart','{\"interval\": {\"update\": \"04:00:00\", \"time_sync\": \"00:30:00\", \"discover_assets\": \"24:00:00\"}, \"start_stop\": {\"stop\": \"18:00:00\", \"start\": \"06:00:00\"}}');
/*!40000 ALTER TABLE `agent` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'mack@goflyball.com','Mack','Hendricks','flyball','mack@goflyball.com','1','1','19475176566',NULL,'SU','{"alert_type":50,"notification_type":"email"}','NOT_A_PROD_KEY'),(2,'tmoore@goflyball.com','Tyler','Moore','flyball','tmoore@goflyball.com','1','1','12489092769',NULL,'ADMIN','{"alert_type":10,"notification_type":"sms"}','NOT_A_PROD_KEY'), (3,'tyler.moore58@gmail.com','Tyler','Moore','flyball','tyler.moore58@gmail.com','1','1','13131234567',NULL,'USER','{"alert_type":10,"notification_type":"email"}','NOT_A_PROD_KEY');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `company_id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(45) NOT NULL,
  `street` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `zip` varchar(45) DEFAULT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `authinfo` json DEFAULT NULL,
  `sites` json DEFAULT NULL,
  PRIMARY KEY (`company_id`),
  UNIQUE KEY `company_name` (`company_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'Flyball-Labs','1234-Fake-St','Detroit','MI','12345','012-345-6789','{\"ldap\": {\"port\": \"0000\", \"server\": \"0.0.0.0\"}, \"type\": \"basic\"}','[\"Site1\", \"Site2\", \"Site3\", \"Site4\"]'),(2,'Dopensource','1234-Fake-St','Detroit','MI','12345','012-345-6789','{\"ldap\": {\"port\": \"0000\", \"server\": \"0.0.0.0\"}, \"type\": \"basic\"}','[\"Site1\", \"Site2\", \"Site3\", \"Site4\"]'),(3,'Swagcity-Software','1234-Fake-Dr','Detroit','MI','01234','012-345-6789','{\"ldap\": {\"port\": \"0000\", \"server\": \"0.0.0.0\"}, \"type\": \"basic\"}','[\"Site1\", \"Site2\", \"Site3\", \"Site4\"]');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facial_image`
--

DROP TABLE IF EXISTS `facial_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `facial_image` (
  `facial_image_id` varchar(200) NOT NULL,
  `company_id` varchar(45) DEFAULT NULL,
  `image_name` varchar(100) DEFAULT NULL,
  `image_http_url` varchar(200) DEFAULT NULL,
  `engine_type` varchar(45) DEFAULT NULL,
  `face_id` varchar(100) DEFAULT NULL,
  `facelist_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`facial_image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facial_image`
--

LOCK TABLES `facial_image` WRITE;
/*!40000 ALTER TABLE `facial_image` DISABLE KEYS */;
INSERT INTO `facial_image` VALUES ('024bebeb443f47b09cd27232bdde8535','dpd','williamaikin1.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/williamaikin1.jpg','MSFT','494a2a16-353a-442d-ba07-5ac70d8a1dcd','dpd'),('20bd11dd14e242c388b58b246b0bbaff','dpd','williamaikin1.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/williamaikin1.jpg','MSFT','139e8a2f-b317-417b-a550-2af70445efcf','dpd'),('376272d698024cb0a6a245d2faf6a1f8','dpd','060214.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/060214.jpg','MSFT','b45140ef-d300-4079-97d2-8f1fbb149bef','dpd'),('3aa995bd4c6141e196087983cf66a5cd','dpd','amd-mug-patrick-stump-jpg.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/amd-mug-patrick-stump-jpg.jpg','MSFT','1b71f52e-7f6b-41fd-98fe-8cea805b2050','dpd'),('56bbfa77429f4a2a92fd77cf2a2feae5','dpd','justin_bieber_mugshot_0.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/justin_bieber_mugshot_0.jpg','MSFT','4ab0e4a3-42ca-4099-a99f-06305dde3b4f','dpd'),('56fcc93ab9fe461baed388ed7b942fef','dpd','070815-anthony-hill.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/070815-anthony-hill.jpg','MSFT','2d64ea87-dbf2-41bf-9b0a-da431296da41','dpd'),('590c41a448e349c99be6bb315cc215d9','dpd','121423.max-620x600.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/121423.max-620x600.jpg','MSFT','5755e424-83a6-4324-840c-ae20551d70ff','dpd'),('5dd48843b3954c7e8f1cfd48b7d26d3f','dpd','justin_bieber_mugshot_0.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/justin_bieber_mugshot_0.jpg','MSFT','a2337b54-1a01-4be5-aee6-d4f8dce3a777','dpd'),('5f01f1621ef34b218360674cc6f58050','dpd','070815-anthony-hill.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/070815-anthony-hill.jpg','MSFT','67a2e857-4a3f-4603-8fa6-32b8b95827bf','dpd'),('6ec528cd8a7944d39e66bfce54253c58','dpd','121423.max-620x600.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/121423.max-620x600.jpg','MSFT','6b50d578-cf0e-4c43-80e3-7356c603ef39','dpd'),('7ad3ab471b9e4af89c4367cff0e12c84','dpd','amd-mug-patrick-stump-jpg.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/amd-mug-patrick-stump-jpg.jpg','MSFT','57df2be9-d1fe-4483-8eae-77354ef227cd','dpd'),('7dba5feeaf4a413793399e4f77a215ec','dpd','070815-anthony-hill.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/070815-anthony-hill.jpg','MSFT','fb268818-1899-4249-8372-a76a433fa925','dpd'),('8449a40dc66a42d6a2701443e88ae901','dpd','121423.max-620x600.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/121423.max-620x600.jpg','MSFT','cc4e416f-039b-467f-999e-f3249d345180','dpd'),('8b54c1114ea74e9fa664e34416de1c60','dpd','060214.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/060214.jpg','MSFT','e37abd21-3179-4e47-be3b-0f2d6ec63167','dpd'),('8c8723b177024fbdb05585c6372e9a54','dpd','williamaikin1.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/williamaikin1.jpg','MSFT','5fde17f2-69f6-4679-a081-6060d8af27ab','dpd'),('937b7a0e4e5647d989ff6691be4b1ef0','dpd','amd-mug-patrick-stump-jpg.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/amd-mug-patrick-stump-jpg.jpg','MSFT','fea1d98e-180e-47d9-9aea-742e2cb81213','dpd'),('990fae0a535643e7874e828dc7146487','dpd','060214.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/060214.jpg','MSFT','2848643c-a45f-473a-b682-32cf0745547c','dpd'),('ad77d3b8b57d4508988dc1261e33fd9e','dpd','justin_bieber_mugshot_0.jpg','http://50.253.243.17:7777/api/facial/images/dpd/repo/justin_bieber_mugshot_0.jpg','MSFT','5888e9f6-8ecc-4be7-9977-07b143df970e','dpd');
/*!40000 ALTER TABLE `facial_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `firstname` varchar(45) DEFAULT NULL,
  `lastname` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `company_id` varchar(45) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `lastlogin` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'mack@goflyball.com','Mack','Hendricks','flyball','mack@goflyball.com','1',1,NULL),(2,'tmoore@goflyball.com','Tyler','Moore','flyball','tmoore@goflyball.com','1',1,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-06 13:29:31
