-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 15-05-2022 a las 05:33:21
-- Versión del servidor: 5.7.36
-- Versión de PHP: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `muni`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movements`
--

DROP TABLE IF EXISTS `movements`;
CREATE TABLE IF NOT EXISTS `movements` (
  `ID_Mov` bigint(110) NOT NULL AUTO_INCREMENT,
  `RouteName` varchar(250) NOT NULL,
  `FuOrder` varchar(250) NOT NULL,
  `CLid` bigint(110) NOT NULL,
  `Ean` varchar(250) NOT NULL,
  `Description` varchar(250) NOT NULL,
  `Quantity` bigint(110) NOT NULL,
  `Process` varchar(250) NOT NULL,
  `Responsible` varchar(250) NOT NULL,
  `Site` varchar(250) NOT NULL,
  `DateTime` datetime NOT NULL,
  PRIMARY KEY (`ID_Mov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `ID_Order` bigint(110) NOT NULL AUTO_INCREMENT,
  `RouteName` varchar(250) NOT NULL,
  `FUName` varchar(250) NOT NULL,
  `Service_Zone` varchar(250) NOT NULL,
  `FK_order` bigint(110) NOT NULL,
  `Packer` varchar(250) DEFAULT NULL,
  `FuOrder` varchar(250) DEFAULT NULL,
  `Ean` varchar(250) NOT NULL,
  `OperationGroup` varchar(250) NOT NULL,
  `ProductName` varchar(250) NOT NULL,
  `Type` varchar(250) NOT NULL,
  `DeliveryDay` date NOT NULL,
  `OriginalQuantity` bigint(110) NOT NULL,
  `Vendedor` varchar(250) NOT NULL,
  `CLid` bigint(110) NOT NULL,
  `Stop` bigint(110) NOT NULL,
  `CurrentQuantity` bigint(110) NOT NULL,
  `PendingQuantity` bigint(110) NOT NULL,
  `Status` varchar(250) NOT NULL,
  `Site` varchar(250) NOT NULL,
  PRIMARY KEY (`ID_Order`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `receiving`
--

DROP TABLE IF EXISTS `receiving`;
CREATE TABLE IF NOT EXISTS `receiving` (
  `ID_Receiving` bigint(110) NOT NULL AUTO_INCREMENT,
  `PurchaseOrder` varchar(250) DEFAULT 'N/A',
  `Type` varchar(250) NOT NULL,
  `Ean` varchar(250) DEFAULT NULL,
  `EanMuni` varchar(250) DEFAULT NULL,
  `ConversionUnit` bigint(110) DEFAULT NULL,
  `Quantity` bigint(110) NOT NULL,
  `Description` varchar(250) DEFAULT NULL,
  `Responsible` varchar(250) NOT NULL,
  `Site` varchar(250) NOT NULL,
  `DateTime` datetime NOT NULL,
  PRIMARY KEY (`ID_Receiving`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `ID_User` bigint(110) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(250) NOT NULL,
  `LastName` varchar(250) NOT NULL,
  `User` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Access` varchar(250) NOT NULL,
  `Site` varchar(250) NOT NULL,
  PRIMARY KEY (`ID_User`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
