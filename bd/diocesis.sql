-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-11-2023 a las 19:22:13
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `diocesis`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividades`
--

CREATE TABLE `actividades` (
  `id_actividad` int(11) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `descripcion` longtext NOT NULL,
  `objetivos` longtext NOT NULL,
  `fecha` date NOT NULL,
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividades`
--

INSERT INTO `actividades` (`id_actividad`, `titulo`, `descripcion`, `objetivos`, `fecha`, `id_user`) VALUES
(1, 'Actividad 1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras sagittis consequat hendrerit. Suspendisse dignissim bibendum leo sit amet convallis. Morbi lobortis orci et scelerisque elementum. Aenean euismod tortor ligula, at facilisis libero interdum quis. Curabitur nec ex et tellus rutrum ullamcorper. Sed rutrum lobortis mauris, id vestibulum leo lacinia id. Nunc porta euismod tortor.', '- Maecenas cursus est ligula, ut tincidunt ipsum auctor eu. Donec bibendum magna ac justo pulvinar, quis \r\n- facilisis est viverra. Vestibulum mattis odio nec nulla tincidunt, vestibulum convallis augue interdum. \r\n-Curabitur tempus congue ligula, id aliquet leo rutrum a. Morbi ornare in nisi et ultrices. In feugiat, sapien at iaculis ultricies, arcu elit porttitor quam, at maximus lorem turpis laoreet mauris. ', '2023-12-31', 2),
(2, 'Actividad 2', 'n hac habitasse platea dictumst. Nulla vulputate imperdiet quam nec tempus. ', 'Maecenas molestie, tortor in consectetur ultricies, arcu mi maximus libero, et dignissim ipsum sapien sed mi. Duis non auctor nisl. Cras posuere, est eu ornare egestas, sem elit ullamcorper neque, sit amet gravida ligula ligula at lorem.', '2024-02-02', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividadxcolegio`
--

CREATE TABLE `actividadxcolegio` (
  `id_axc` int(11) NOT NULL,
  `escuela_id` int(11) NOT NULL,
  `id_actividad` int(11) NOT NULL,
  `fecha_adherido` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividadxcolegio`
--

INSERT INTO `actividadxcolegio` (`id_axc`, `escuela_id`, `id_actividad`, `fecha_adherido`) VALUES
(1, 1, 1, '2023-10-16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `nmb_admin` varchar(40) NOT NULL,
  `id_user` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `admin`
--

INSERT INTO `admin` (`id_admin`, `nmb_admin`, `id_user`) VALUES
(1, 'Padre test', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `escuelas`
--

CREATE TABLE `escuelas` (
  `escuela_id` int(11) NOT NULL,
  `nmb_esc` varchar(40) NOT NULL,
  `celu_esc` varchar(20) NOT NULL,
  `email_esc` varchar(25) NOT NULL,
  `direc_esc` varchar(40) NOT NULL,
  `id_user` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `escuelas`
--

INSERT INTO `escuelas` (`escuela_id`, `nmb_esc`, `celu_esc`, `email_esc`, `direc_esc`, `id_user`) VALUES
(1, 'Escuela N 2134 test', '555566', 'test@gmail.com', 'Av. Irrazabal', 3),
(2, 'Escuela N 2134 test', '12344455', 'test@gmail.com', 'Av. Mallorquin', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resoluciones`
--

CREATE TABLE `resoluciones` (
  `id_res` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `titulo` varchar(80) NOT NULL,
  `des` varchar(150) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `resoluciones`
--

INSERT INTO `resoluciones` (`id_res`, `id_user`, `filename`, `titulo`, `des`, `date`) VALUES
(3, 2, 'Tarea8_Cristologia.pdf', 'Test Resolucion N12424', 'Resolucion tal cosa, test. Resolucion tal cosa, test. Resolucion tal cosa, test. Resolucion tal cosa, test', '2023-11-06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_usuarios`
--

CREATE TABLE `tipos_usuarios` (
  `id_tipo_user` int(11) NOT NULL,
  `desc_user` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos_usuarios`
--

INSERT INTO `tipos_usuarios` (`id_tipo_user`, `desc_user`) VALUES
(1, 'Colegio'),
(2, 'Admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_user` int(11) NOT NULL,
  `user` varchar(20) NOT NULL,
  `password` longtext NOT NULL,
  `id_tipo_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_user`, `user`, `password`, `id_tipo_user`) VALUES
(2, 'test', 'pbkdf2:sha256:600000$Ki4UMQFfPyxPDae6$12d3e58f73ba869486b377886fc566454cdde56ba4b662eb3cd200f39710f9f0', 2),
(3, 'test2', 'pbkdf2:sha256:600000$UU9CWTHSKp4K4uw5$da2f13e37172fa400349e9fb72380ef9283c898df6d9120c620a7c7f945de5f4', 1),
(4, 'test3', 'pbkdf2:sha256:600000$hGq49xSYrAeMcBpQ$1451905c30df92bc2d408c55879782fb32637c51764c5d4587b3cd1457e08f76', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD PRIMARY KEY (`id_actividad`);

--
-- Indices de la tabla `actividadxcolegio`
--
ALTER TABLE `actividadxcolegio`
  ADD PRIMARY KEY (`id_axc`);

--
-- Indices de la tabla `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indices de la tabla `escuelas`
--
ALTER TABLE `escuelas`
  ADD PRIMARY KEY (`escuela_id`);

--
-- Indices de la tabla `resoluciones`
--
ALTER TABLE `resoluciones`
  ADD PRIMARY KEY (`id_res`);

--
-- Indices de la tabla `tipos_usuarios`
--
ALTER TABLE `tipos_usuarios`
  ADD PRIMARY KEY (`id_tipo_user`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividades`
--
ALTER TABLE `actividades`
  MODIFY `id_actividad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `actividadxcolegio`
--
ALTER TABLE `actividadxcolegio`
  MODIFY `id_axc` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `escuelas`
--
ALTER TABLE `escuelas`
  MODIFY `escuela_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `resoluciones`
--
ALTER TABLE `resoluciones`
  MODIFY `id_res` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipos_usuarios`
--
ALTER TABLE `tipos_usuarios`
  MODIFY `id_tipo_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
