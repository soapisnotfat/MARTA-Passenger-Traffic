-- phpMyAdmin SQL Dump
-- version 2.11.11.3
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 10, 2017 at 03:22 PM
-- Server version: 5.1.73
-- PHP Version: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `cs4400_Group_91`
--

-- --------------------------------------------------------

--
-- Table structure for table `Breezecard`
--

DROP TABLE IF EXISTS `Breezecard`;
CREATE TABLE IF NOT EXISTS `Breezecard` (
  `BreezecardNum` char(16) NOT NULL DEFAULT '',
  `Value` decimal(6,2) NOT NULL,
  `BelongsTo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`BreezecardNum`),
  KEY `BelongsTo` (`BelongsTo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Breezecard`
--


-- --------------------------------------------------------

--
-- Table structure for table `BusStationIntersection`
--

DROP TABLE IF EXISTS `BusStationIntersection`;
CREATE TABLE IF NOT EXISTS `BusStationIntersection` (
  `StopID` varchar(50) NOT NULL DEFAULT '',
  `Intersection` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`StopID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `BusStationIntersection`
--


-- --------------------------------------------------------

--
-- Table structure for table `Conflict`
--

DROP TABLE IF EXISTS `Conflict`;
CREATE TABLE IF NOT EXISTS `Conflict` (
  `Username` varchar(50) NOT NULL DEFAULT '',
  `BreezecardNum` char(16) NOT NULL DEFAULT '',
  `DateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Username`,`BreezecardNum`),
  KEY `BreezecardNum` (`BreezecardNum`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Conflict`
--


-- --------------------------------------------------------

--
-- Table structure for table `Passenger`
--

DROP TABLE IF EXISTS `Passenger`;
CREATE TABLE IF NOT EXISTS `Passenger` (
  `Username` varchar(50) NOT NULL DEFAULT '',
  `Email` varchar(50) NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Passenger`
--


-- --------------------------------------------------------

--
-- Table structure for table `Station`
--

DROP TABLE IF EXISTS `Station`;
CREATE TABLE IF NOT EXISTS `Station` (
  `StopID` varchar(50) NOT NULL DEFAULT '',
  `Name` varchar(50) NOT NULL,
  `EnterFare` decimal(4,2) NOT NULL,
  `ClosedStatus` tinyint(1) NOT NULL,
  `IsTrain` tinyint(1) NOT NULL,
  PRIMARY KEY (`StopID`),
  UNIQUE KEY `Name` (`Name`,`IsTrain`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Station`
--


-- --------------------------------------------------------

--
-- Table structure for table `Trip`
--

DROP TABLE IF EXISTS `Trip`;
CREATE TABLE IF NOT EXISTS `Trip` (
  `Tripfare` decimal(4,2) NOT NULL,
  `StartTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `BreezecardNum` char(16) NOT NULL DEFAULT '',
  `StartsAt` varchar(50) NOT NULL,
  `EndsAt` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`StartTime`,`BreezecardNum`),
  KEY `BreezecardNum` (`BreezecardNum`),
  KEY `StartsAt` (`StartsAt`),
  KEY `EndsAt` (`EndsAt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Trip`
--


-- --------------------------------------------------------

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `Username` varchar(50) NOT NULL DEFAULT '',
  `Password` varchar(50) NOT NULL,
  `IsAdmin` tinyint(1) NOT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `User`
--


--
-- Constraints for dumped tables
--

--
-- Constraints for table `Breezecard`
--
ALTER TABLE `Breezecard`
  ADD CONSTRAINT `Breezecard_ibfk_1` FOREIGN KEY (`BelongsTo`) REFERENCES `Passenger` (`Username`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `BusStationIntersection`
--
ALTER TABLE `BusStationIntersection`
  ADD CONSTRAINT `BusStationIntersection_ibfk_1` FOREIGN KEY (`StopID`) REFERENCES `Station` (`StopID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Conflict`
--
ALTER TABLE `Conflict`
  ADD CONSTRAINT `Conflict_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `Passenger` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Conflict_ibfk_2` FOREIGN KEY (`BreezecardNum`) REFERENCES `Breezecard` (`BreezecardNum`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Passenger`
--
ALTER TABLE `Passenger`
  ADD CONSTRAINT `Passenger_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `User` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Trip`
--
ALTER TABLE `Trip`
  ADD CONSTRAINT `Trip_ibfk_1` FOREIGN KEY (`BreezecardNum`) REFERENCES `Breezecard` (`BreezecardNum`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Trip_ibfk_2` FOREIGN KEY (`StartsAt`) REFERENCES `Station` (`StopID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `Trip_ibfk_3` FOREIGN KEY (`EndsAt`) REFERENCES `Station` (`StopID`) ON UPDATE CASCADE;
