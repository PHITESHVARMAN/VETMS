-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: vetms_db
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `command_logs`
--

DROP TABLE IF EXISTS `command_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `command_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `command_text` text DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `executed_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `command_logs`
--

LOCK TABLES `command_logs` WRITE;
/*!40000 ALTER TABLE `command_logs` DISABLE KEYS */;
INSERT INTO `command_logs` VALUES (1,'project completed successfully','Unknown','2026-02-05 17:41:10'),(2,'project completed successfully','Unknown','2026-02-05 17:41:57'),(3,'status completed','Unknown','2026-02-05 17:43:46'),(4,'show','Unknown','2026-02-05 17:45:13'),(5,'show tasks','Navigation','2026-02-05 17:45:23'),(6,'show task','Unknown','2026-02-05 17:45:50'),(7,'show','Unknown','2026-02-06 11:00:53'),(8,'show tas','Unknown','2026-02-06 11:01:28'),(9,'show tasks','Navigation','2026-02-06 11:01:44'),(10,'show tasks in ascending order by id','Navigation','2026-02-06 11:02:02'),(11,'show tasks in ascending order by id','Navigation','2026-02-06 11:02:03'),(12,'show tasks in ascending order by id','Navigation','2026-02-06 11:02:04'),(13,'status completed','Unknown','2026-02-06 11:28:38'),(14,'task','Unknown','2026-02-06 11:28:51'),(15,'status completed','Unknown','2026-02-06 11:29:05');
/*!40000 ALTER TABLE `command_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings`
--

DROP TABLE IF EXISTS `meetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meetings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `meeting_type` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `participants` varchar(255) DEFAULT NULL,
  `meeting_date` date NOT NULL,
  `meeting_time` time NOT NULL,
  `link` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `meetings_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings`
--

LOCK TABLES `meetings` WRITE;
/*!40000 ALTER TABLE `meetings` DISABLE KEYS */;
INSERT INTO `meetings` VALUES (1,6,'hitesh','Video Call (Zoom/Teams)','test','John','2026-02-26','01:30:00','');
/*!40000 ALTER TABLE `meetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `priority` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `assigned_user` varchar(100) DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` varchar(100) DEFAULT 'System',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Design Login Page','Hello Design Login Page','High','In Progress','Admin Team','2026-02-10','2026-02-05 15:11:22','System'),(2,'Database Backup',NULL,'Critical','Pending','DevOps','2026-02-08','2026-02-05 15:11:22','System'),(3,'Client Meeting',NULL,'Medium','Pending','Manager','2026-02-12','2026-02-05 15:11:22','System'),(4,'MySQL Bug Fix',NULL,'Critical','Pending','DevOps','2026-02-09','2026-02-05 15:11:22','System'),(5,'Data Update Documentation',NULL,'Medium','Pending','Manager','2026-02-11','2026-02-05 15:11:22','System'),(6,'Test Description','This is a test to see if the text saves correctly.','High','Pending','DevOps','2026-02-05','2026-02-05 16:14:30','System'),(7,'design voice module','Created via Voice','Medium','Pending','Admin Team','2026-02-05','2026-02-05 17:03:19','System'),(8,'project success','Created via Voice','Medium','Pending','Admin Team','2026-02-05','2026-02-05 17:15:35','System');
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_members`
--

DROP TABLE IF EXISTS `team_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `calendar_synced` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_members`
--

LOCK TABLES `team_members` WRITE;
/*!40000 ALTER TABLE `team_members` DISABLE KEYS */;
INSERT INTO `team_members` VALUES (1,'HITESHVARMAN P','USR001','hitesh@gmail.com','Super Admin','Active',1);
/*!40000 ALTER TABLE `team_members` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-06 17:02:33
