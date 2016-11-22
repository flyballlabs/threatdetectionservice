-- Quick and dirty way to create a database and setup a local and remote user

CREATE DATABASE IF NOT EXISTS `tmp`;
grant all on tmp.* TO 'tmp'@'localhost' IDENTIFIED BY 'tmp';
grant all on tmp.* TO 'tmp'@'%' IDENTIFIED BY 'tmp';
flush privileges;
use tmp;

-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: tmp
-- ------------------------------------------------------
-- Server version	5.1.73-log

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
  `status` varchar(45) DEFAULT NULL,
  `lastlogin` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

-- DEFAULT CHARSET=latin1
--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'mack@goflyball.com','Mack','Hendricks','flyball','mack@goflyball.com','1','1',NULL),(2,'tmoore@goflyball.com','Tyler','Moore','flyball','tmoore@goflyball.com','1','1',NULL);
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
  `address` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `zip` varchar(45) DEFAULT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `authinfo` json DEFAULT NULL,
  `sites` json DEFAULT NULL,
  PRIMARY KEY (`company_id`),
  UNIQUE KEY (`company_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'Flyball Labs','1234 Fake St','Detroit','MI','12345','012-345-6789','{"type":"basic","ldap":{"server":"0.0.0.0","port":"0000"}}','["Site1","Site2","Site3","Site4"]'),(2,'Dopensource','1234 Fake St','Detroit','MI','12345','012-345-6789','{"type":"basic","ldap":{"server":"0.0.0.0","port":"0000"}}','["Site1","Site2","Site3","Site4"]');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

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
  UNIQUE KEY (`mac_address`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent`
--

LOCK TABLES `agent` WRITE;
/*!40000 ALTER TABLE `agent` DISABLE KEYS */;
INSERT INTO `agent` VALUES (1,'4A:1D:70:CD:54:A3','10.0.0.1','1','1','glazer','replay','start','{"start_stop":{"start":"08:00:00","stop":"16:00:00"},"interval":{"time_sync":"00:05:00","update":"04:00:00","discover_assets":"24:00:00"}}'),(2,'D4:85:64:A3:9A:27','10.0.0.17','1','2','loving','live','stop','{"start_stop":{"start":"08:00:00","stop":"16:00:00"},"interval":{"time_sync":"00:15:00","update":"06:00:00","discover_assets":"12:00:00"}}');
/*!40000 ALTER TABLE `agent` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-15 16:12:24
