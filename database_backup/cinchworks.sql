-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 05, 2022 at 01:02 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinchworks`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `cus_id` int(11) NOT NULL,
  `cus_fname` varchar(255) NOT NULL,
  `cus_lname` varchar(255) NOT NULL,
  `cus_phone1` varchar(40) DEFAULT NULL,
  `cus_phone2` varchar(40) DEFAULT NULL,
  `cus_email` varchar(255) NOT NULL,
  `cus_address` varchar(255) DEFAULT NULL,
  `cus_city` varchar(150) DEFAULT NULL,
  `cus_state` int(11) DEFAULT NULL,
  `cus_username` varchar(255) NOT NULL,
  `cus_password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`cus_id`, `cus_fname`, `cus_lname`, `cus_phone1`, `cus_phone2`, `cus_email`, `cus_address`, `cus_city`, `cus_state`, `cus_username`, `cus_password`) VALUES
(1, 'Eren', 'Nightengale', NULL, NULL, 'nighteren@vordworld.com', NULL, NULL, NULL, 'sireren', '123654'),
(2, 'Dongo', 'Youga', NULL, NULL, 'youbouga@dongo.com', NULL, NULL, NULL, 'dongoya', '78945');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`cus_id`),
  ADD UNIQUE KEY `cus_username` (`cus_username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `cus_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
