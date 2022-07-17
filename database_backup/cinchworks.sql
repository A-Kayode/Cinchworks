-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 17, 2022 at 02:51 PM
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
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL,
  `b_vendor` int(11) NOT NULL,
  `b_customer` int(11) NOT NULL,
  `b_venservice` int(11) NOT NULL,
  `booking_date` datetime NOT NULL,
  `service_location` enum('vendor_address','customer_address') NOT NULL,
  `confirmation_status` enum('active','pending','cancelled','completed','rejected') NOT NULL,
  `calender_date` date NOT NULL,
  `calender_time` time NOT NULL,
  `calender_endtime` time NOT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`booking_id`, `b_vendor`, `b_customer`, `b_venservice`, `booking_date`, `service_location`, `confirmation_status`, `calender_date`, `calender_time`, `calender_endtime`, `notes`) VALUES
(1, 1, 1, 5, '2022-07-12 16:01:07', 'customer_address', 'active', '2022-07-15', '10:30:00', '13:15:00', 'The impression must be perfect');

-- --------------------------------------------------------

--
-- Table structure for table `calender`
--

CREATE TABLE `calender` (
  `calen_id` int(11) NOT NULL,
  `c_offday` int(11) DEFAULT NULL,
  `c_booking` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `cus_id` int(11) NOT NULL,
  `cus_fname` varchar(255) NOT NULL,
  `cus_lname` varchar(255) NOT NULL,
  `cus_phone1` varchar(40) DEFAULT NULL,
  `cus_phone2` varchar(40) DEFAULT NULL,
  `cus_email` varchar(255) NOT NULL,
  `cus_address` varchar(255) DEFAULT NULL,
  `cus_city` varchar(150) DEFAULT NULL,
  `cus_lga` int(11) DEFAULT NULL,
  `cus_state` int(11) DEFAULT NULL,
  `cus_username` varchar(255) NOT NULL,
  `cus_password` varchar(255) NOT NULL,
  `cus_profilepic` varchar(255) DEFAULT NULL,
  `cus_regdate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`cus_id`, `cus_fname`, `cus_lname`, `cus_phone1`, `cus_phone2`, `cus_email`, `cus_address`, `cus_city`, `cus_lga`, `cus_state`, `cus_username`, `cus_password`, `cus_profilepic`, `cus_regdate`) VALUES
(1, 'Friday', 'Iwangumi', '08154289637', '08052936648', 'friiwan@yahoo.com', '5, Ogunsiji Close, Allen Avenue', 'Ikeja', 513, 24, 'freakyfriday', 'pbkdf2:sha256:260000$uuIB0LQ4q83lO5ZE$dc5be7165bdfdad4f678b583bf60feddc7a6ed8aed1e950c26b87f46974005ee', '8523440126080357.0.jpg', '2022-07-17 13:50:25'),
(3, 'Lucky', 'Monday', NULL, NULL, 'monlucky@yahoo.com', NULL, NULL, NULL, NULL, 'luckyday', 'pbkdf2:sha256:260000$MZTTA8hz7kjEGEPM$37b6f959fb275fd2ec9f8d7e5af36a8755af11f53a4275770ce38ae942df1648', NULL, '2022-07-13 13:46:39');

-- --------------------------------------------------------

--
-- Table structure for table `lga`
--

CREATE TABLE `lga` (
  `lga_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  `lga_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lga`
--

INSERT INTO `lga` (`lga_id`, `state_id`, `lga_name`) VALUES
(1, 1, 'Aba North'),
(2, 1, 'Aba South'),
(3, 1, 'Arochukwu'),
(4, 1, 'Bende'),
(5, 1, 'Ikwuano'),
(6, 1, 'Isiala-Ngwa North'),
(7, 1, 'Isiala-Ngwa South'),
(8, 1, 'Isikwuato'),
(9, 1, 'Nneochi'),
(10, 1, 'Obi-Ngwa'),
(11, 1, 'Ohafia'),
(12, 1, 'Osisioma'),
(13, 1, 'Ugwunagbo'),
(14, 1, 'Ukwa East'),
(15, 1, 'Ukwa West'),
(16, 1, 'Umuahia North'),
(17, 1, 'Umuahia South'),
(18, 2, 'Demsa'),
(19, 2, 'Fufore'),
(20, 2, 'Genye'),
(21, 2, 'Girei'),
(22, 2, 'Gombi'),
(23, 2, 'guyuk'),
(24, 2, 'Hong'),
(25, 2, 'Jada'),
(26, 2, 'Jimeta'),
(27, 2, 'Lamurde'),
(28, 2, 'Madagali'),
(29, 2, 'Maiha'),
(30, 2, 'Mayo Belwa'),
(31, 2, 'Michika'),
(32, 2, 'Mubi North'),
(33, 2, 'Mubi South'),
(34, 2, 'Numan'),
(35, 2, 'Shelleng'),
(36, 2, 'Song'),
(37, 2, 'Toungo'),
(38, 2, 'Yola'),
(39, 3, 'Abak'),
(40, 3, 'Eastern-Obolo'),
(41, 3, 'Eket'),
(42, 3, 'Ekpe-Atani'),
(43, 3, 'Essien-Udim'),
(44, 3, 'Esit Ekit'),
(45, 3, 'Etim-Ekpo'),
(46, 3, 'Etinam'),
(47, 3, 'Ibeno'),
(48, 3, 'Ibesikp-Asitan'),
(49, 3, 'Ibiono-Ibom'),
(50, 3, 'Ika'),
(51, 3, 'Ikono'),
(52, 3, 'Ikot-Abasi'),
(53, 3, 'Ikot-Ekpene'),
(54, 3, 'Ini'),
(55, 3, 'Itu'),
(56, 3, 'Mbo'),
(57, 3, 'Mkpae-Enin'),
(58, 3, 'Nsit-Ibom'),
(59, 3, 'Nsit-Ubium'),
(60, 3, 'Obot-Akara'),
(61, 3, 'Okobo'),
(62, 3, 'Onna'),
(63, 3, 'Oron'),
(64, 3, 'Oro-Anam'),
(65, 3, 'Udung-Uko'),
(66, 3, 'Ukanefun'),
(67, 3, 'Uru Offong Oruko'),
(68, 3, 'Uruan'),
(69, 3, 'Uquo Ibene'),
(70, 3, 'Uyo'),
(71, 4, 'Aguata'),
(72, 4, 'Anambra'),
(73, 4, 'Anambra West'),
(74, 4, 'Anocha'),
(75, 4, 'Awka- North'),
(76, 4, 'Awka-South'),
(77, 4, 'Ayamelum'),
(78, 4, 'Dunukofia'),
(79, 4, 'Ekwusigo'),
(80, 4, 'Idemili-North'),
(81, 4, 'Idemili-South'),
(82, 4, 'Ihiala'),
(83, 4, 'Njikoka'),
(84, 4, 'Nnewi-North'),
(85, 4, 'Nnewi-South'),
(86, 4, 'Ogbaru'),
(87, 4, 'Onisha North'),
(88, 4, 'Onitsha South'),
(89, 4, 'Orumba North'),
(90, 4, 'Orumba South'),
(91, 4, 'Oyi'),
(92, 5, 'Alkaleri'),
(93, 5, 'Bauchi'),
(94, 5, 'Bogoro'),
(95, 5, 'Damban'),
(96, 5, 'Darazo'),
(97, 5, 'Dass'),
(98, 5, 'Gamawa'),
(99, 5, 'Ganjuwa'),
(100, 5, 'Giade'),
(101, 5, 'Itas/Gadau'),
(102, 5, 'Jama\'are'),
(103, 5, 'Katagum'),
(104, 5, 'Kirfi'),
(105, 5, 'Misau'),
(106, 5, 'Ningi'),
(107, 5, 'Shira'),
(108, 5, 'Tafawa-Balewa'),
(109, 5, 'Toro'),
(110, 5, 'Warji'),
(111, 5, 'Zaki'),
(112, 6, 'Brass'),
(113, 6, 'Ekerernor'),
(114, 6, 'Kolokuma/Opokuma'),
(115, 6, 'Nembe'),
(116, 6, 'Ogbia'),
(117, 6, 'Sagbama'),
(118, 6, 'Southern-Ijaw'),
(119, 6, 'Yenegoa'),
(120, 6, 'Kembe'),
(121, 7, 'Ado'),
(122, 7, 'Agatu'),
(123, 7, 'Apa'),
(124, 7, 'Buruku'),
(125, 7, 'Gboko'),
(126, 7, 'Guma'),
(127, 7, 'Gwer-East'),
(128, 7, 'Gwer-West'),
(129, 7, 'Katsina-Ala'),
(130, 7, 'Konshisha'),
(131, 7, 'Kwande'),
(132, 7, 'Logo'),
(133, 7, 'Makurdi'),
(134, 7, 'Obi'),
(135, 7, 'Ogbadibo'),
(136, 7, 'Ohimini'),
(137, 7, 'Oju'),
(138, 7, 'Okpokwu'),
(139, 7, 'Otukpo'),
(140, 7, 'Tarkar'),
(141, 7, 'Vandeikya'),
(142, 7, 'Ukum'),
(143, 7, 'Ushongo'),
(144, 8, 'Abadan'),
(145, 8, 'Askira-Uba'),
(146, 8, 'Bama'),
(147, 8, 'Bayo'),
(148, 8, 'Biu'),
(149, 8, 'Chibok'),
(150, 8, 'Damboa'),
(151, 8, 'Dikwa'),
(152, 8, 'Gubio'),
(153, 8, 'Guzamala'),
(154, 8, 'Gwoza'),
(155, 8, 'Hawul'),
(156, 8, 'Jere'),
(157, 8, 'Kaga'),
(158, 8, 'Kala/Balge'),
(159, 8, 'Kukawa'),
(160, 8, 'Konduga'),
(161, 8, 'Kwaya-Kusar'),
(162, 8, 'Mafa'),
(163, 8, 'Magumeri'),
(164, 8, 'Maiduguri'),
(165, 8, 'Marte'),
(166, 8, 'Mobbar'),
(167, 8, 'Monguno'),
(168, 8, 'Ngala'),
(169, 8, 'Nganzai'),
(170, 8, 'Shani'),
(171, 9, 'Abi'),
(172, 9, 'Akamkpa'),
(173, 9, 'Akpabuyo'),
(174, 9, 'Bakassi'),
(175, 9, 'Bekwara'),
(176, 9, 'Biasi'),
(177, 9, 'Boki'),
(178, 9, 'Calabar-Municipal'),
(179, 9, 'Calabar-South'),
(180, 9, 'Etunk'),
(181, 9, 'Ikom'),
(182, 9, 'Obantiku'),
(183, 9, 'Ogoja'),
(184, 9, 'Ugep North'),
(185, 9, 'Yakurr'),
(186, 9, 'Yala'),
(187, 10, 'Aniocha North'),
(188, 10, 'Aniocha South'),
(189, 10, 'Bomadi'),
(190, 10, 'Burutu'),
(191, 10, 'Ethiope East'),
(192, 10, 'Ethiope West'),
(193, 10, 'Ika North East'),
(194, 10, 'Ika South'),
(195, 10, 'Isoko North'),
(196, 10, 'Isoko South'),
(197, 10, 'Ndokwa East'),
(198, 10, 'Ndokwa West'),
(199, 10, 'Okpe'),
(200, 10, 'Oshimili North'),
(201, 10, 'Oshimili South'),
(202, 10, 'Patani'),
(203, 10, 'Sapele'),
(204, 10, 'Udu'),
(205, 10, 'Ughilli North'),
(206, 10, 'Ughilli South'),
(207, 10, 'Ukwuani'),
(208, 10, 'Uvwie'),
(209, 10, 'Warri Central'),
(210, 10, 'Warri North'),
(211, 10, 'Warri South'),
(212, 11, 'Abakaliki'),
(213, 11, 'Ofikpo North'),
(214, 11, 'Ofikpo South'),
(215, 11, 'Ebonyi'),
(216, 11, 'Ezza North'),
(217, 11, 'Ezza South'),
(218, 11, 'ikwo'),
(219, 11, 'Ishielu'),
(220, 11, 'Ivo'),
(221, 11, 'Izzi'),
(222, 11, 'Ohaukwu'),
(223, 11, 'Ohaozara'),
(224, 11, 'Onicha'),
(225, 12, 'Akoko Edo'),
(226, 12, 'Egor'),
(227, 12, 'Esan Central'),
(228, 12, 'Esan North East'),
(229, 12, 'Esan South East'),
(230, 12, 'Esan West'),
(231, 12, 'Etsako-Central'),
(232, 12, 'Etsako-West'),
(233, 12, 'Igueben'),
(234, 12, 'Ikpoba-Okha'),
(235, 12, 'Oredo'),
(236, 12, 'Orhionmwon'),
(237, 12, 'Ovia North East'),
(238, 12, 'Ovia South West'),
(239, 12, 'owan east'),
(240, 12, 'Owan West'),
(241, 12, 'Umunniwonde'),
(242, 13, 'Ado Ekiti'),
(243, 13, 'Aiyedire'),
(244, 13, 'Efon'),
(245, 13, 'Ekiti-East'),
(246, 13, 'Ekiti-South West'),
(247, 13, 'Ekiti West'),
(248, 13, 'Emure'),
(249, 13, 'Ido Osi'),
(250, 13, 'Ijero'),
(251, 13, 'Ikere'),
(252, 13, 'Ikole'),
(253, 13, 'Ilejemeta'),
(254, 13, 'Irepodun/Ifelodun'),
(255, 13, 'Ise Orun'),
(256, 13, 'Moba'),
(257, 13, 'Oye'),
(258, 14, 'Aninri'),
(259, 14, 'Awgu'),
(260, 14, 'Enugu East'),
(261, 14, 'Enugu North'),
(262, 14, 'Enugu South'),
(263, 14, 'Ezeagu'),
(264, 14, 'Igbo Etiti'),
(265, 14, 'Igbo Eze North'),
(266, 14, 'Igbo Eze South'),
(267, 14, 'Isi Uzo'),
(268, 14, 'Nkanu East'),
(269, 14, 'Nkanu West'),
(270, 14, 'Nsukka'),
(271, 14, 'Oji-River'),
(272, 14, 'Udenu'),
(273, 14, 'Udi'),
(274, 14, 'Uzo Uwani'),
(275, 15, 'Akko'),
(276, 15, 'Balanga'),
(277, 15, 'Billiri'),
(278, 15, 'Dukku'),
(279, 15, 'Funakaye'),
(280, 15, 'Gombe'),
(281, 15, 'Kaltungo'),
(282, 15, 'Kwami'),
(283, 15, 'Nafada/Bajoga'),
(284, 15, 'Shomgom'),
(285, 15, 'Yamltu/Deba'),
(286, 16, 'Ahiazu-Mbaise'),
(287, 16, 'Ehime-Mbano'),
(288, 16, 'Ezinihtte'),
(289, 16, 'Ideato North'),
(290, 16, 'Ideato South'),
(291, 16, 'Ihitte/Uboma'),
(292, 16, 'Ikeduru'),
(293, 16, 'Isiala-Mbano'),
(294, 16, 'Isu'),
(295, 16, 'Mbaitoli'),
(296, 16, 'Ngor-Okpala'),
(297, 16, 'Njaba'),
(298, 16, 'Nkwerre'),
(299, 16, 'Nwangele'),
(300, 16, 'obowo'),
(301, 16, 'Oguta'),
(302, 16, 'Ohaji-Eggema'),
(303, 16, 'Okigwe'),
(304, 16, 'Onuimo'),
(305, 16, 'Orlu'),
(306, 16, 'Orsu'),
(307, 16, 'Oru East'),
(308, 16, 'Oru West'),
(309, 16, 'Owerri Municipal'),
(310, 16, 'Owerri North'),
(311, 16, 'Owerri West'),
(312, 17, 'Auyu'),
(313, 17, 'Babura'),
(314, 17, 'Birnin Kudu'),
(315, 17, 'Birniwa'),
(316, 17, 'Bosuwa'),
(317, 17, 'Buji'),
(318, 17, 'Dutse'),
(319, 17, 'Gagarawa'),
(320, 17, 'Garki'),
(321, 17, 'Gumel'),
(322, 17, 'Guri'),
(323, 17, 'Gwaram'),
(324, 17, 'Gwiwa'),
(325, 17, 'Hadejia'),
(326, 17, 'Jahun'),
(327, 17, 'Kafin Hausa'),
(328, 17, 'Kaugama'),
(329, 17, 'Kazaure'),
(330, 17, 'Kirikasanuma'),
(331, 17, 'Kiyawa'),
(332, 17, 'Maigatari'),
(333, 17, 'Malam Maduri'),
(334, 17, 'Miga'),
(335, 17, 'Ringim'),
(336, 17, 'Roni'),
(337, 17, 'Sule Tankarkar'),
(338, 17, 'Taura'),
(339, 17, 'Yankwashi'),
(340, 18, 'Birnin-Gwari'),
(341, 18, 'Chikun'),
(342, 18, 'Giwa'),
(343, 18, 'Gwagwada'),
(344, 18, 'Igabi'),
(345, 18, 'Ikara'),
(346, 18, 'Jaba'),
(347, 18, 'Jema\'a'),
(348, 18, 'Kachia'),
(349, 18, 'Kaduna North'),
(350, 18, 'Kagarko'),
(351, 18, 'Kajuru'),
(352, 18, 'Kaura'),
(353, 18, 'Kauru'),
(354, 18, 'Koka/Kawo'),
(355, 18, 'Kubah'),
(356, 18, 'Kudan'),
(357, 18, 'Lere'),
(358, 18, 'Makarfi'),
(359, 18, 'Sabon Gari'),
(360, 18, 'Sanga'),
(361, 18, 'Sabo'),
(362, 18, 'Tudun-Wada/Makera'),
(363, 18, 'Zango-Kataf'),
(364, 18, 'Zaria'),
(365, 19, 'Ajingi'),
(366, 19, ' Albasu'),
(367, 19, 'Bagwai'),
(368, 19, 'Bebeji'),
(369, 19, 'Bichi'),
(370, 19, 'Bunkure'),
(371, 19, 'Dala'),
(372, 19, 'Dambatta'),
(373, 19, 'Dawakin Kudu'),
(374, 19, 'Dawakin Tofa'),
(375, 19, 'Doguwa'),
(376, 19, 'Fagge'),
(377, 19, 'Gabasawa'),
(378, 19, 'Garko'),
(379, 19, 'Garun-Mallam'),
(380, 19, 'Gaya'),
(381, 19, 'Gezawa'),
(382, 19, 'Gwale'),
(383, 19, 'Gwarzo'),
(384, 19, 'Kabo'),
(385, 19, 'Kano Municipal'),
(386, 19, 'Karaye'),
(387, 19, 'Kibiya'),
(388, 19, 'Kiru'),
(389, 19, 'Kumbotso'),
(390, 19, 'Kunchi'),
(391, 19, 'Kura'),
(392, 19, 'Madobi'),
(393, 19, 'Makoda'),
(394, 19, 'Minjibir'),
(395, 19, 'Nasarawa'),
(396, 19, 'Rano'),
(397, 19, 'Rimin Gado'),
(398, 19, 'Rogo'),
(399, 19, 'Shanono'),
(400, 19, 'Sumaila'),
(401, 19, 'Takai'),
(402, 19, 'Tarauni'),
(403, 19, 'Tofa'),
(404, 19, 'Tsanyawa'),
(405, 19, 'Tudun Wada'),
(406, 19, 'Ngogo'),
(407, 19, 'Warawa'),
(408, 19, 'Wudil'),
(409, 20, 'Bakori'),
(410, 20, 'Batagarawa'),
(411, 20, 'Batsari'),
(412, 20, 'Baure'),
(413, 20, 'Bindawa'),
(414, 20, 'Charanchi'),
(415, 20, 'Danja'),
(416, 20, 'Danjume'),
(417, 20, 'Dan-Musa'),
(418, 20, 'Daura'),
(419, 20, 'Dutsi'),
(420, 20, 'Dutsinma'),
(421, 20, 'Faskari'),
(422, 20, 'Funtua'),
(423, 20, 'Ingara'),
(424, 20, 'Jibia'),
(425, 20, 'Kafur'),
(426, 20, 'Kaita'),
(427, 20, 'Kankara'),
(428, 20, 'Kankia'),
(429, 20, 'Katsina'),
(430, 20, 'Kurfi'),
(431, 20, 'Kusada'),
(432, 20, 'Mai Adua'),
(433, 20, 'Malumfashi'),
(434, 20, 'Mani'),
(435, 20, 'Mashi'),
(436, 20, 'Matazu'),
(437, 20, 'Musawa'),
(438, 20, 'Rimi'),
(439, 20, 'Sabuwa'),
(440, 20, 'Safana'),
(441, 20, 'Sandamu'),
(442, 20, 'Zango'),
(443, 21, 'Aleira'),
(444, 21, 'Arewa'),
(445, 21, 'Argungu'),
(446, 21, 'Augie'),
(447, 21, 'Bagudo'),
(448, 21, 'Birnin-Kebbi'),
(449, 21, 'Bumza'),
(450, 21, 'Dandi'),
(451, 21, 'Danko'),
(452, 21, 'Fakai'),
(453, 21, 'Gwandu'),
(454, 21, 'Jega'),
(455, 21, 'Kalgo'),
(456, 21, 'Koko-Besse'),
(457, 21, 'Maiyama'),
(458, 21, 'Ngaski'),
(459, 21, 'Sakaba'),
(460, 21, 'Shanga'),
(461, 21, 'Suru'),
(462, 21, 'Wasagu'),
(463, 21, 'Yauri'),
(464, 21, 'Zuru'),
(465, 22, 'Adavi'),
(466, 22, 'Ajaokuta'),
(467, 22, 'Ankpa'),
(468, 22, 'Bassa'),
(469, 22, 'Dekina'),
(470, 22, 'Ibaji'),
(471, 22, 'Idah'),
(472, 22, 'Igalamela'),
(473, 22, 'Ijumu'),
(474, 22, 'Kabba/Bunu'),
(475, 22, 'Kogi'),
(476, 22, 'Lokoja'),
(477, 22, 'Mopa-Muro-Mopi'),
(478, 22, 'Ofu'),
(479, 22, 'Ogori/Magongo'),
(480, 22, 'Okehi'),
(481, 22, 'Okene'),
(482, 22, 'Olamaboro'),
(483, 22, 'Omala'),
(484, 22, 'Oyi'),
(485, 22, 'Yagba-East'),
(486, 22, 'Yagba-West'),
(487, 23, 'Asa'),
(488, 23, 'Baruten'),
(489, 23, 'Edu'),
(490, 23, 'Ekiti'),
(491, 23, 'Ifelodun'),
(492, 23, 'Ilorin East'),
(493, 23, 'Ilorin South'),
(494, 23, 'Ilorin West'),
(495, 23, 'Irepodun'),
(496, 23, 'Isin'),
(497, 23, 'Kaiama'),
(498, 23, 'Moro'),
(499, 23, 'Offa'),
(500, 23, 'Oke-Ero'),
(501, 23, 'Oyun'),
(502, 23, 'Pategi'),
(503, 24, 'Agege'),
(504, 24, 'Ajeromi-Ifelodun'),
(505, 24, 'Alimosho'),
(506, 24, 'Amuwo-Odofin'),
(507, 24, 'Apapa'),
(508, 24, 'Bagagry'),
(509, 24, 'Epe'),
(510, 24, 'Eti-Osa'),
(511, 24, 'Ibeju-Lekki'),
(512, 24, 'Ifako-Ijaiye'),
(513, 24, 'Ikeja'),
(514, 24, 'Ikorodu'),
(515, 24, 'Kosofe'),
(516, 24, 'Lagos-Island'),
(517, 24, 'Lagos-Mainland'),
(518, 24, 'Mushin'),
(519, 24, 'Ojo'),
(520, 24, 'Oshodi-Isolo'),
(521, 24, 'Shomolu'),
(522, 24, 'Suru-Lere'),
(523, 25, 'Akwanga'),
(524, 25, 'Awe'),
(525, 25, 'Doma'),
(526, 25, 'Karu'),
(527, 25, 'Keana'),
(528, 25, 'Keffi'),
(529, 25, 'Kokona'),
(530, 25, 'Lafia'),
(531, 25, 'Nassarawa'),
(532, 25, 'Nassarawa Eggor'),
(533, 25, 'Obi'),
(534, 25, 'Toto'),
(535, 25, 'Wamba'),
(536, 26, 'Agaie'),
(537, 26, 'Agwara'),
(538, 26, 'Bida'),
(539, 26, 'Borgu'),
(540, 26, 'Bosso'),
(541, 26, 'Chanchaga'),
(542, 26, 'Edati'),
(543, 26, 'Gbako'),
(544, 26, 'Gurara'),
(545, 26, 'Katcha'),
(546, 26, 'Kontagora'),
(547, 26, 'Lapai'),
(548, 26, 'Lavum'),
(549, 26, 'Magama'),
(550, 26, 'Mariga'),
(551, 26, 'Mashegu'),
(552, 26, 'Mokwa'),
(553, 26, 'Muya'),
(554, 26, 'Paikoro'),
(555, 26, 'Rafi'),
(556, 26, 'Rajau'),
(557, 26, 'Shiroro'),
(558, 26, 'Suleja'),
(559, 26, 'Tafa'),
(560, 26, 'Wushishi'),
(561, 27, 'Abeokuta -North'),
(562, 27, 'Abeokuta -South'),
(563, 27, 'Ado-Odu/Ota'),
(564, 27, 'Yewa-North'),
(565, 27, 'Yewa-South'),
(566, 27, 'Ewekoro'),
(567, 27, 'Ifo'),
(568, 27, 'Ijebu East'),
(569, 27, 'Ijebu North'),
(570, 27, 'Ijebu North-East'),
(571, 27, 'Ijebu-Ode'),
(572, 27, 'Ikenne'),
(573, 27, 'Imeko-Afon'),
(574, 27, 'Ipokia'),
(575, 27, 'Obafemi -Owode'),
(576, 27, 'Odeda'),
(577, 27, 'Odogbolu'),
(578, 27, 'Ogun-Water Side'),
(579, 27, 'Remo-North'),
(580, 27, 'Shagamu'),
(581, 28, 'Akoko-North-East'),
(582, 28, 'Akoko-North-West'),
(583, 28, 'Akoko-South-West'),
(584, 28, 'Akoko-South-East'),
(585, 28, 'Akure- South'),
(586, 28, 'Akure-North'),
(587, 28, 'Ese-Odo'),
(588, 28, 'Idanre'),
(589, 28, 'Ifedore'),
(590, 28, 'Ilaje'),
(591, 28, 'Ile-Oluji-Okeigbo'),
(592, 28, 'Irele'),
(593, 28, 'Odigbo'),
(594, 28, 'Okitipupa'),
(595, 28, 'Ondo-West'),
(596, 28, 'Ondo East'),
(597, 28, 'Ose'),
(598, 28, 'Owo'),
(599, 29, 'Atakumosa'),
(600, 29, 'Atakumosa East'),
(601, 29, 'Ayeda-Ade'),
(602, 29, 'Ayedire'),
(603, 29, 'Boluwaduro'),
(604, 29, 'Boripe'),
(605, 29, 'Ede'),
(606, 29, 'Ede North'),
(607, 29, 'Egbedore'),
(608, 29, 'Ejigbo'),
(609, 29, 'Ife'),
(610, 29, 'Ife East'),
(611, 29, 'Ife North'),
(612, 29, 'Ife South'),
(613, 29, 'Ifedayo'),
(614, 29, 'Ifelodun'),
(615, 29, 'Ila'),
(616, 29, 'Ilesha'),
(617, 29, 'Ilesha-West'),
(618, 29, 'Irepodun'),
(619, 29, 'Irewole'),
(620, 29, 'Isokun'),
(621, 29, 'Iwo'),
(622, 29, 'Obokun'),
(623, 29, 'Odo-Otin'),
(624, 29, 'Ola Oluwa'),
(625, 29, 'Olorunda'),
(626, 29, 'Ori-Ade'),
(627, 29, 'Orolu'),
(628, 29, 'Osogbo'),
(629, 30, 'Afijio'),
(630, 30, 'Akinyele'),
(631, 30, 'Atiba'),
(632, 30, 'Atisbo'),
(633, 30, 'Egbeda'),
(634, 30, 'Ibadan-Central'),
(635, 30, 'Ibadan-North-East'),
(636, 30, 'Ibadan-North-West'),
(637, 30, 'Ibadan-South-East'),
(638, 30, 'Ibadan-South West'),
(639, 30, 'Ibarapa-Central'),
(640, 30, 'Ibarapa-East'),
(641, 30, 'Ibarapa-North'),
(642, 30, 'Ido'),
(643, 30, 'Ifedayo'),
(644, 30, 'Ifeloju'),
(645, 30, 'Irepo'),
(646, 30, 'Iseyin'),
(647, 30, 'Itesiwaju'),
(648, 30, 'Iwajowa'),
(649, 30, 'Kajola'),
(650, 30, 'Lagelu'),
(651, 30, 'Odo-Oluwa'),
(652, 30, 'Ogbomoso-North'),
(653, 30, 'Ogbomosho-South'),
(654, 30, 'Olorunsogo'),
(655, 30, 'Oluyole'),
(656, 30, 'Ona-Ara'),
(657, 30, 'Orelope'),
(658, 30, 'Ori-Ire'),
(659, 30, 'Oyo East'),
(660, 30, 'Oyo West'),
(661, 30, 'saki east'),
(662, 30, 'Saki West'),
(663, 30, 'Surulere'),
(664, 31, 'Barkin Ladi'),
(665, 31, 'Bassa'),
(666, 31, 'Bokkos'),
(667, 31, 'Jos-East'),
(668, 31, 'Jos-South'),
(669, 31, 'Jos-North'),
(670, 31, 'Kanam'),
(671, 31, 'Kanke'),
(672, 31, 'Langtang North'),
(673, 31, 'Langtang South'),
(674, 31, 'Mangu'),
(675, 31, 'Mikang'),
(676, 31, 'Pankshin'),
(677, 31, 'Quan\'pan'),
(678, 31, 'Riyom'),
(679, 31, 'Shendam'),
(680, 31, 'Wase'),
(681, 32, 'Abua/Odual'),
(682, 32, 'Ahoada East'),
(683, 32, 'Ahoada West'),
(684, 32, 'Akukutoru'),
(685, 32, 'Andoni'),
(686, 32, 'Asari-Toro'),
(687, 32, 'Bonny'),
(688, 32, 'Degema'),
(689, 32, 'Eleme'),
(690, 32, 'Emuoha'),
(691, 32, 'Etche'),
(692, 32, 'Gokana'),
(693, 32, 'Ikwerre'),
(694, 32, 'Khana'),
(695, 32, 'Obio/Akpor'),
(696, 32, 'Ogba/Egbama/Ndoni'),
(697, 32, 'Ogu/Bolo'),
(698, 32, 'Okrika'),
(699, 32, 'Omuma'),
(700, 32, 'Opobo/Nkoro'),
(701, 32, 'Oyigbo'),
(702, 32, 'Port-Harcourt'),
(703, 32, 'Tai'),
(704, 33, 'Binji'),
(705, 33, 'Bodinga'),
(706, 33, 'Dange-Shuni'),
(707, 33, 'Gada'),
(708, 33, 'Goronyo'),
(709, 33, 'Gudu'),
(710, 33, 'Gwadabawa'),
(711, 33, 'Illela'),
(712, 33, 'Isa'),
(713, 33, 'Kebbe'),
(714, 33, 'Kware'),
(715, 33, 'Raba'),
(716, 33, 'Sabon-Birni'),
(717, 33, 'Shagari'),
(718, 33, 'Silame'),
(719, 33, 'Sokoto North'),
(720, 33, 'Sokoto South'),
(721, 33, 'Tambuwal'),
(722, 33, 'Tanzaga'),
(723, 33, 'Tureta'),
(724, 33, 'Wamakko'),
(725, 33, 'Wurno'),
(726, 33, 'Yabo'),
(727, 34, 'Ardo Kola'),
(728, 34, 'Bali'),
(729, 34, 'Donga'),
(730, 34, 'Gashaka'),
(731, 34, 'Gassol'),
(732, 34, 'Ibi'),
(733, 34, 'Jalingo'),
(734, 34, 'Karim-Lamido'),
(735, 34, 'Kurmi'),
(736, 34, 'Lau'),
(737, 34, 'Sardauna'),
(738, 34, 'Takuni'),
(739, 34, 'Ussa'),
(740, 34, 'Wukari'),
(741, 34, 'Yarro'),
(742, 34, 'Zing'),
(743, 35, 'Bade'),
(744, 35, 'Bursali'),
(745, 35, 'Damaturu'),
(746, 35, 'Fuka'),
(747, 35, 'Fune'),
(748, 35, 'Geidam'),
(749, 35, 'Gogaram'),
(750, 35, 'Gujba'),
(751, 35, 'Gulani'),
(752, 35, 'Jakusko'),
(753, 35, 'Karasuwa'),
(754, 35, 'Machina'),
(755, 35, 'Nangere'),
(756, 35, 'Nguru'),
(757, 35, 'Potiskum'),
(758, 35, 'Tarmua'),
(759, 35, 'Yunisari'),
(760, 35, 'Yusufari'),
(761, 36, 'Anka'),
(762, 36, 'Bakure'),
(763, 36, 'Bukkuyum'),
(764, 36, 'Bungudo'),
(765, 36, 'Gumi'),
(766, 36, 'Gusau'),
(767, 36, 'Isa'),
(768, 36, 'Kaura-Namoda'),
(769, 36, 'Kiyawa'),
(770, 36, 'Maradun'),
(771, 36, 'Marau'),
(772, 36, 'Shinkafa'),
(773, 36, 'Talata-Mafara'),
(774, 36, 'Tsafe'),
(775, 36, 'Zurmi'),
(776, 9, 'Obudu'),
(777, 37, 'Abaji'),
(778, 37, 'Bwari'),
(779, 37, 'Gwagwalada'),
(780, 37, 'Kuje'),
(781, 37, 'Kwali'),
(782, 37, 'Municipal'),
(783, 12, 'Etsako-East'),
(784, 16, 'Ahiazu-Mbaise'),
(785, 38, 'Foreign'),
(786, 18, 'Kaduna South'),
(787, 16, 'Aboh-Mbaise'),
(788, 9, 'Odukpani');

-- --------------------------------------------------------

--
-- Table structure for table `offday`
--

CREATE TABLE `offday` (
  `off_id` int(11) NOT NULL,
  `off_ven` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL,
  `r_customer` int(11) NOT NULL,
  `r_vendor` int(11) NOT NULL,
  `review_date` date DEFAULT NULL,
  `review_score` int(11) NOT NULL,
  `review_desc` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `service_name` varchar(150) NOT NULL,
  `ser_category` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `service_name`, `ser_category`) VALUES
(1, 'Painting', 1),
(2, 'Sculpture', 1),
(3, 'Magomago', 1),
(5, 'Impression', 1),
(6, 'Chocolate Making', 2);

-- --------------------------------------------------------

--
-- Table structure for table `service_category`
--

CREATE TABLE `service_category` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `service_category`
--

INSERT INTO `service_category` (`category_id`, `category_name`) VALUES
(1, 'Art'),
(2, 'Food and Drinks');

-- --------------------------------------------------------

--
-- Table structure for table `state`
--

CREATE TABLE `state` (
  `state_id` int(11) NOT NULL,
  `state_name` varchar(75) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `state`
--

INSERT INTO `state` (`state_id`, `state_name`) VALUES
(1, 'Abia'),
(2, 'Adamawa'),
(3, 'Akwa Ibom'),
(4, 'Anambra'),
(5, 'Bauchi'),
(6, 'Bayelsa'),
(7, 'Benue'),
(8, 'Borno'),
(9, 'Cross River'),
(10, 'Delta'),
(11, 'Ebonyi'),
(12, 'Edo'),
(13, 'Ekiti'),
(14, 'Enugu'),
(15, 'Gombe'),
(16, 'Imo'),
(17, 'Jigawa'),
(18, 'Kaduna'),
(19, 'Kano'),
(20, 'Katsina'),
(21, 'Kebbi'),
(22, 'Kogi'),
(23, 'Kwara'),
(24, 'Lagos'),
(25, 'Nassarawa'),
(26, 'Niger'),
(27, 'Ogun'),
(28, 'Ondo'),
(29, 'Osun'),
(30, 'Oyo'),
(31, 'Plateau'),
(32, 'Rivers'),
(33, 'Sokoto'),
(34, 'Taraba'),
(35, 'Yobe'),
(36, 'Zamfara'),
(37, 'Abuje (FCT)'),
(38, 'Foreign');

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `ven_id` int(11) NOT NULL,
  `ven_fname` varchar(255) NOT NULL,
  `ven_lname` varchar(255) NOT NULL,
  `ven_busname` varchar(255) DEFAULT NULL,
  `ven_phone1` varchar(40) DEFAULT NULL,
  `ven_phone2` varchar(40) DEFAULT NULL,
  `ven_email` varchar(255) NOT NULL,
  `ven_address` varchar(255) DEFAULT NULL,
  `ven_city` varchar(150) DEFAULT NULL,
  `ven_lga` int(11) DEFAULT NULL,
  `ven_state` int(11) DEFAULT NULL,
  `ven_username` varchar(255) NOT NULL,
  `ven_password` varchar(255) NOT NULL,
  `ven_shortdesc` varchar(255) DEFAULT NULL,
  `ven_openingtime` time DEFAULT NULL,
  `ven_closingtime` time DEFAULT NULL,
  `ven_bannerpic` varchar(255) DEFAULT NULL,
  `ven_profilepic` varchar(255) DEFAULT NULL,
  `ven_regdate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vendor`
--

INSERT INTO `vendor` (`ven_id`, `ven_fname`, `ven_lname`, `ven_busname`, `ven_phone1`, `ven_phone2`, `ven_email`, `ven_address`, `ven_city`, `ven_lga`, `ven_state`, `ven_username`, `ven_password`, `ven_shortdesc`, `ven_openingtime`, `ven_closingtime`, `ven_bannerpic`, `ven_profilepic`, `ven_regdate`) VALUES
(1, 'Damilola', 'Crazycongo', 'Dami Sells Stuff', '08175963248', '', 'cogocray@gmail.com', '25, Ilupeju drive, Ilupeju', 'Ikeja', NULL, 24, 'damicray', 'pbkdf2:sha256:260000$YExGCkkUSq3TzGBB$673d4f50abd4ecb95dfda394a1c9c18cc56fed362cd99877847eadc4e414cbaf', 'Well Sell Stuff That you might need.', '09:00:00', '05:00:00', NULL, NULL, '2022-07-11 13:46:07'),
(2, 'Willy', 'Wonka', 'Wonka Foods', '07052954189', 'None', 'willwonka@yahoo.com', '58, Nigerian street, Ojodu, Berger', 'Berger', 517, 24, 'willywonka', 'pbkdf2:sha256:260000$SsIC7PpjC1zLpiqt$e97842575b5f00120d555d8a2bc186de22834e17f6ef314980ca3faa6c8411f3', 'We make and sell delicious food and chocolates', '08:00:00', '04:00:00', '4613172034963542.0.jpg', '8958985686155323.0.jpg', '2022-07-17 13:32:47');

-- --------------------------------------------------------

--
-- Table structure for table `vendor_services`
--

CREATE TABLE `vendor_services` (
  `ven_service_id` int(11) NOT NULL,
  `vendor_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `short_desc` varchar(255) NOT NULL,
  `long_desc` text DEFAULT NULL,
  `service_price` float NOT NULL,
  `average_duration` varchar(50) DEFAULT NULL,
  `min_duration` varchar(50) DEFAULT NULL,
  `max_duration` varchar(50) DEFAULT NULL,
  `avgdur_text` varchar(100) DEFAULT NULL,
  `mindur_text` varchar(100) DEFAULT NULL,
  `maxdur_text` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vendor_services`
--

INSERT INTO `vendor_services` (`ven_service_id`, `vendor_id`, `service_id`, `short_desc`, `long_desc`, `service_price`, `average_duration`, `min_duration`, `max_duration`, `avgdur_text`, `mindur_text`, `maxdur_text`) VALUES
(1, 1, 2, 'We sculpt stuff', 'We will sculp your dick to your liking', 50000, '02:30', NULL, NULL, '', '', ''),
(2, 1, 1, 'We paint stuff for you', 'We are the true painters', 1500, '23:20', NULL, NULL, '', '', ''),
(3, 1, 3, 'We do magomago', 'Magomagomagomago', 500, '03:30', NULL, NULL, '', '', ''),
(5, 1, 5, 'We make impressions of things', 'The impression that is created at the crux of the battle of sambody.', 2500, '2 hours 45 minutes', '2 hours ', '3 hours 30 minutes', '', '', ''),
(6, 1, 2, 'We sculpt nice things', 'Nice things are good to look at', 5000, '05:00', '03:00', '07:30', '5 hours ', '3 hours ', '7 hours 30 minutes'),
(7, 2, 6, 'We make delicious chocolates for your enjoyment', 'The chocolates are made from the freshest of cocoas and the best confectionary experts.', 7500, '03:00', '03:00', '05:00', '3 hours ', '3 hours ', '5 hours ');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `b_vendor` (`b_vendor`),
  ADD KEY `b_customer` (`b_customer`),
  ADD KEY `b_venservice` (`b_venservice`);

--
-- Indexes for table `calender`
--
ALTER TABLE `calender`
  ADD PRIMARY KEY (`calen_id`),
  ADD KEY `c_offday` (`c_offday`),
  ADD KEY `c_booking` (`c_booking`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`cus_id`),
  ADD UNIQUE KEY `cus_username` (`cus_username`),
  ADD KEY `cus_state` (`cus_state`),
  ADD KEY `customer_ibfk_2` (`cus_lga`);

--
-- Indexes for table `lga`
--
ALTER TABLE `lga`
  ADD PRIMARY KEY (`lga_id`),
  ADD KEY `lga_ibfk_1` (`state_id`);

--
-- Indexes for table `offday`
--
ALTER TABLE `offday`
  ADD PRIMARY KEY (`off_id`),
  ADD KEY `off_ven` (`off_ven`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `reviews_ibfk_2` (`r_vendor`),
  ADD KEY `reviews_ibfk_1` (`r_customer`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`),
  ADD UNIQUE KEY `service_name` (`service_name`),
  ADD KEY `ser_category` (`ser_category`);

--
-- Indexes for table `service_category`
--
ALTER TABLE `service_category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `state`
--
ALTER TABLE `state`
  ADD PRIMARY KEY (`state_id`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`ven_id`),
  ADD UNIQUE KEY `ven_email` (`ven_email`),
  ADD UNIQUE KEY `ven_username` (`ven_username`),
  ADD UNIQUE KEY `ven_busname` (`ven_busname`),
  ADD UNIQUE KEY `ven_phone1` (`ven_phone1`),
  ADD UNIQUE KEY `ven_phone2` (`ven_phone2`),
  ADD KEY `ven_state` (`ven_state`),
  ADD KEY `vendor_ibfk_2` (`ven_lga`);

--
-- Indexes for table `vendor_services`
--
ALTER TABLE `vendor_services`
  ADD PRIMARY KEY (`ven_service_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `vendor_services_ibfk_1` (`vendor_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `calender`
--
ALTER TABLE `calender`
  MODIFY `calen_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `cus_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `lga`
--
ALTER TABLE `lga`
  MODIFY `lga_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=789;

--
-- AUTO_INCREMENT for table `offday`
--
ALTER TABLE `offday`
  MODIFY `off_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `service_category`
--
ALTER TABLE `service_category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `state`
--
ALTER TABLE `state`
  MODIFY `state_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `vendor`
--
ALTER TABLE `vendor`
  MODIFY `ven_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vendor_services`
--
ALTER TABLE `vendor_services`
  MODIFY `ven_service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`b_vendor`) REFERENCES `vendor` (`ven_id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`b_customer`) REFERENCES `customer` (`cus_id`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`b_venservice`) REFERENCES `vendor_services` (`ven_service_id`);

--
-- Constraints for table `calender`
--
ALTER TABLE `calender`
  ADD CONSTRAINT `calender_ibfk_1` FOREIGN KEY (`c_offday`) REFERENCES `offday` (`off_id`),
  ADD CONSTRAINT `calender_ibfk_2` FOREIGN KEY (`c_booking`) REFERENCES `booking` (`booking_id`);

--
-- Constraints for table `customer`
--
ALTER TABLE `customer`
  ADD CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`cus_state`) REFERENCES `state` (`state_id`),
  ADD CONSTRAINT `customer_ibfk_2` FOREIGN KEY (`cus_lga`) REFERENCES `lga` (`lga_id`);

--
-- Constraints for table `lga`
--
ALTER TABLE `lga`
  ADD CONSTRAINT `lga_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `state` (`state_id`);

--
-- Constraints for table `offday`
--
ALTER TABLE `offday`
  ADD CONSTRAINT `offday_ibfk_1` FOREIGN KEY (`off_ven`) REFERENCES `vendor` (`ven_id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`r_customer`) REFERENCES `customer` (`cus_id`),
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`r_vendor`) REFERENCES `vendor` (`ven_id`);

--
-- Constraints for table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`ser_category`) REFERENCES `service_category` (`category_id`);

--
-- Constraints for table `vendor`
--
ALTER TABLE `vendor`
  ADD CONSTRAINT `vendor_ibfk_1` FOREIGN KEY (`ven_state`) REFERENCES `state` (`state_id`),
  ADD CONSTRAINT `vendor_ibfk_2` FOREIGN KEY (`ven_lga`) REFERENCES `lga` (`lga_id`);

--
-- Constraints for table `vendor_services`
--
ALTER TABLE `vendor_services`
  ADD CONSTRAINT `vendor_services_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`ven_id`),
  ADD CONSTRAINT `vendor_services_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
