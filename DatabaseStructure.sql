-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 14, 2017 at 03:17 PM
-- Server version: 10.1.24-MariaDB
-- PHP Version: 7.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Metazombies`
--
CREATE DATABASE IF NOT EXISTS `Metazombies` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `Metazombies`;

-- --------------------------------------------------------

--
-- Table structure for table `ClaimHistory`
--

CREATE TABLE `ClaimHistory` (
  `tranID` bigint(20) NOT NULL,
  `claimID` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `userID` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Claims`
--

CREATE TABLE `Claims` (
  `ID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `claimValue` int(11) NOT NULL,
  `timeStart` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `timeValid` int(11) NOT NULL,
  `usesRemaining` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Newsfeed`
--

CREATE TABLE `Newsfeed` (
  `ID` int(11) NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Updates`
--

CREATE TABLE `Updates` (
  `ID` int(11) NOT NULL,
  `command` longtext COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `userID` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `studentNumber` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cellNumber` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SectionName` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `humanScore` int(11) NOT NULL DEFAULT '0',
  `zombieScore` int(11) NOT NULL DEFAULT '0',
  `hearts` int(11) NOT NULL DEFAULT '1',
  `nextHeart` int(11) NOT NULL DEFAULT '10800',
  `admin` tinyint(1) NOT NULL DEFAULT '0',
  `passwordhash` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ClaimHistory`
--
ALTER TABLE `ClaimHistory`
  ADD PRIMARY KEY (`tranID`),
  ADD KEY `ClaimHistory_fk0` (`claimID`),
  ADD KEY `ClaimHistory_fk1` (`userID`);

--
-- Indexes for table `Claims`
--
ALTER TABLE `Claims`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Indexes for table `Newsfeed`
--
ALTER TABLE `Newsfeed`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Indexes for table `Updates`
--
ALTER TABLE `Updates`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `studentNumber` (`studentNumber`),
  ADD UNIQUE KEY `cellNumber` (`cellNumber`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ClaimHistory`
--
ALTER TABLE `ClaimHistory`
  MODIFY `tranID` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Newsfeed`
--
ALTER TABLE `Newsfeed`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Updates`
--
ALTER TABLE `Updates`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `ClaimHistory`
--
ALTER TABLE `ClaimHistory`
  ADD CONSTRAINT `ClaimHistory_fk0` FOREIGN KEY (`claimID`) REFERENCES `Claims` (`ID`),
  ADD CONSTRAINT `ClaimHistory_fk1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
