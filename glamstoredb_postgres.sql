-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-12-2025 a las 05:51:16
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: "glamstoredb"
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "auth_group"
--

CREATE TABLE "auth_group" (
  "id" integer NOT NULL,
  "name" character varying(150) NOT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "auth_group_permissions"
--

CREATE TABLE "auth_group_permissions" (
  "id" bigint NOT NULL,
  "group_id" integer NOT NULL,
  "permission_id" integer NOT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "auth_permission"
--

CREATE TABLE "auth_permission" (
  "id" integer NOT NULL,
  "name" character varying(255) NOT NULL,
  "content_type_id" integer NOT NULL,
  "codename" character varying(100) NOT NULL
);

--
-- Volcado de datos para la tabla "auth_permission"
--

INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add cliente', 7, 'add_cliente'),
(26, 'Can change cliente', 7, 'change_cliente'),
(27, 'Can delete cliente', 7, 'delete_cliente'),
(28, 'Can view cliente', 7, 'view_cliente'),
(29, 'Can add repartidor', 8, 'add_repartidor'),
(30, 'Can change repartidor', 8, 'change_repartidor'),
(31, 'Can delete repartidor', 8, 'delete_repartidor'),
(32, 'Can view repartidor', 8, 'view_repartidor'),
(33, 'Can add rol', 9, 'add_rol'),
(34, 'Can change rol', 9, 'change_rol'),
(35, 'Can delete rol', 9, 'delete_rol'),
(36, 'Can view rol', 9, 'view_rol'),
(37, 'Can add usuario', 10, 'add_usuario'),
(38, 'Can change usuario', 10, 'change_usuario'),
(39, 'Can delete usuario', 10, 'delete_usuario'),
(40, 'Can view usuario', 10, 'view_usuario'),
(41, 'Can add pedido', 11, 'add_pedido'),
(42, 'Can change pedido', 11, 'change_pedido'),
(43, 'Can delete pedido', 11, 'delete_pedido'),
(44, 'Can view pedido', 11, 'view_pedido'),
(45, 'Can add producto', 12, 'add_producto'),
(46, 'Can change producto', 12, 'change_producto'),
(47, 'Can delete producto', 12, 'delete_producto'),
(48, 'Can view producto', 12, 'view_producto'),
(49, 'Can add categoria', 13, 'add_categoria'),
(50, 'Can change categoria', 13, 'change_categoria'),
(51, 'Can delete categoria', 13, 'delete_categoria'),
(52, 'Can view categoria', 13, 'view_categoria'),
(53, 'Can add distribuidor', 14, 'add_distribuidor'),
(54, 'Can change distribuidor', 14, 'change_distribuidor'),
(55, 'Can delete distribuidor', 14, 'delete_distribuidor'),
(56, 'Can view distribuidor', 14, 'view_distribuidor'),
(57, 'Can add distribuidor producto', 15, 'add_distribuidorproducto'),
(58, 'Can change distribuidor producto', 15, 'change_distribuidorproducto'),
(59, 'Can delete distribuidor producto', 15, 'delete_distribuidorproducto'),
(60, 'Can view distribuidor producto', 15, 'view_distribuidorproducto'),
(61, 'Can add mensaje contacto', 16, 'add_mensajecontacto'),
(62, 'Can change mensaje contacto', 16, 'change_mensajecontacto'),
(63, 'Can delete mensaje contacto', 16, 'delete_mensajecontacto'),
(64, 'Can view mensaje contacto', 16, 'view_mensajecontacto'),
(65, 'Can add profile', 17, 'add_profile'),
(66, 'Can change profile', 17, 'change_profile'),
(67, 'Can delete profile', 17, 'delete_profile'),
(68, 'Can view profile', 17, 'view_profile'),
(69, 'Can add detalle pedido', 18, 'add_detallepedido'),
(70, 'Can change detalle pedido', 18, 'change_detallepedido'),
(71, 'Can delete detalle pedido', 18, 'delete_detallepedido'),
(72, 'Can view detalle pedido', 18, 'view_detallepedido'),
(73, 'Can add notificacion', 19, 'add_notificacion'),
(74, 'Can change notificacion', 19, 'change_notificacion'),
(75, 'Can delete notificacion', 19, 'delete_notificacion'),
(76, 'Can view notificacion', 19, 'view_notificacion'),
(77, 'Can add pedido producto', 20, 'add_pedidoproducto'),
(78, 'Can change pedido producto', 20, 'change_pedidoproducto'),
(79, 'Can delete pedido producto', 20, 'delete_pedidoproducto'),
(80, 'Can view pedido producto', 20, 'view_pedidoproducto'),
(81, 'Can add subcategoria', 21, 'add_subcategoria'),
(82, 'Can change subcategoria', 21, 'change_subcategoria'),
(83, 'Can delete subcategoria', 21, 'delete_subcategoria'),
(84, 'Can view subcategoria', 21, 'view_subcategoria'),
(85, 'Can add movimiento producto', 22, 'add_movimientoproducto'),
(86, 'Can change movimiento producto', 22, 'change_movimientoproducto'),
(87, 'Can delete movimiento producto', 22, 'delete_movimientoproducto'),
(88, 'Can view movimiento producto', 22, 'view_movimientoproducto'),
(89, 'Can add notificacion problema', 23, 'add_notificacionproblema'),
(90, 'Can change notificacion problema', 23, 'change_notificacionproblema'),
(91, 'Can delete notificacion problema', 23, 'delete_notificacionproblema'),
(92, 'Can view notificacion problema', 23, 'view_notificacionproblema'),
(93, 'Can add confirmacion entrega', 24, 'add_confirmacionentrega'),
(94, 'Can change confirmacion entrega', 24, 'change_confirmacionentrega'),
(95, 'Can delete confirmacion entrega', 24, 'delete_confirmacionentrega'),
(96, 'Can view confirmacion entrega', 24, 'view_confirmacionentrega'),
(97, 'Can add movimiento lote', 25, 'add_movimientolote'),
(98, 'Can change movimiento lote', 25, 'change_movimientolote'),
(99, 'Can delete movimiento lote', 25, 'delete_movimientolote'),
(100, 'Can view movimiento lote', 25, 'view_movimientolote'),
(101, 'Can add lote producto', 26, 'add_loteproducto'),
(102, 'Can change lote producto', 26, 'change_loteproducto'),
(103, 'Can delete lote producto', 26, 'delete_loteproducto'),
(104, 'Can view lote producto', 26, 'view_loteproducto'),
(105, 'Can add notificacion reporte', 27, 'add_notificacionreporte'),
(106, 'Can change notificacion reporte', 27, 'change_notificacionreporte'),
(107, 'Can delete notificacion reporte', 27, 'delete_notificacionreporte'),
(108, 'Can view notificacion reporte', 27, 'view_notificacionreporte'),
(109, 'Can add Configuración Global', 28, 'add_configuracionglobal'),
(110, 'Can change Configuración Global', 28, 'change_configuracionglobal'),
(111, 'Can delete Configuración Global', 28, 'delete_configuracionglobal'),
(112, 'Can view Configuración Global', 28, 'view_configuracionglobal');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "auth_user"
--

CREATE TABLE "auth_user" (
  "id" integer NOT NULL,
  "password" character varying(128) NOT NULL,
  "last_login" datetime(6) DEFAULT NULL,
  "is_superuser" smallint NOT NULL,
  "username" character varying(150) NOT NULL,
  "first_name" character varying(150) NOT NULL,
  "last_name" character varying(150) NOT NULL,
  "email" character varying(254) NOT NULL,
  "is_staff" smallint NOT NULL,
  "is_active" smallint NOT NULL,
  "date_joined" datetime(6) NOT NULL
);

--
-- Volcado de datos para la tabla "auth_user"
--

INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES
(1, 'pbkdf2_sha256$600000$fuC3u5YxeZidYXW7wwnSGP$Lh3N7ccFjYGXMD5lGEk8lxrNDuRwHtc154YBiL8DEpA=', NULL, 1, 'lauren samanta', '', '', 'laurensamanta0.r@gmail.com', 1, 1, '2025-11-05 18:55:12.012073'),
(2, 'pbkdf2_sha256$600000$ouGFhpOpJpoenXf23VgHHF$6dtSgXYWfcDhK1gicdsYrzd9uMo/ueUE/OYjjQLpzWE=', NULL, 1, 'lauren o', '', '', 'laurensamanta0.r@gmail.com', 1, 1, '2025-11-05 18:56:53.161260'),
(3, 'pbkdf2_sha256$600000$TBb8BeLASfOa3VDAO9RUU5$3otJZeKf3LWeuSdqoRWDocO44LH6ZZJqFhQ0bxMqUug=', NULL, 1, 'lauren s o', '', '', 'laurensamanta0.r@gmail.com', 1, 1, '2025-11-05 19:07:03.983906'),
(4, 'pbkdf2_sha256$600000$eVapBQU4k6hm38umXtc0CB$m89+Y+2flsr8jb+TYpiAR2wDw7z84tjnEZKren6AZwE=', NULL, 1, 'lauren sama', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:09:17.520694'),
(5, 'pbkdf2_sha256$600000$Dh5b5qMETiYRuBOvFB2w5o$v0ljQMznCEDfoXCVPvSTIsiyFOM3Jfhh7J2SqWCXa6M=', NULL, 1, 'lauren sam o', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:14:36.406095'),
(6, 'pbkdf2_sha256$600000$kT2F7owFSa9otjqSx96chS$p4I1CisHXfo76Etgfx+Ra3h5ia0YRKk+6p0uj8eh/Bo=', NULL, 1, 'laurem', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:15:27.186846'),
(7, 'pbkdf2_sha256$600000$sek4ueXhKoy4lTfFlEsuzu$77CuMjbdoE+VzvV2eTHOn2M/+vFw4ry8S5thj1JYP4g=', NULL, 1, 'leo', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:18:04.790263'),
(8, 'pbkdf2_sha256$600000$45DvRAXE6aMclDDz98v681$1xQbkF09WAxmt5dkYgkJHpKgi1I70DalqlRa+pv0+IQ=', NULL, 1, 'lauren primero', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:21:06.132387'),
(9, 'pbkdf2_sha256$600000$DVzXBqEhBpBp3CfHDhyszp$hlk/YfaN69RlOi94K6FCjAzsvdCeqziTAiXTf1JdYfA=', NULL, 1, 'nose', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:29:27.677923'),
(10, 'pbkdf2_sha256$600000$hQnXxaaYLbTIKTpPigfoJy$N85A3gM0JKZdeHdQbkat7YkbmYyZcWtfgKaAw0BQYUY=', NULL, 1, 'lau', '', '', 'lausamanta2024@gmail.com', 1, 1, '2025-11-05 19:34:55.465552'),
(11, 'pbkdf2_sha256$600000$9l5EUMdf7qOhelMDP9FloC$sCDpSFg4vzfC8emCWoE++alAUTH6xK55ReqOf9JsE3E=', NULL, 1, 'bobo', '', '', 'bob.glam@glamstore.com', 1, 1, '2025-11-05 21:33:48.277178'),
(12, 'pbkdf2_sha256$600000$RmyZRxoNvcQI7O2Vuaer74$W//91Xi+D1eo12O7SL4c4rSuQN6Bq3H7roUXP3Cj6Vk=', NULL, 1, 'bob', '', '', 'bob.glam@glamstore.com', 1, 1, '2025-11-05 21:38:39.869552');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "auth_user_groups"
--

CREATE TABLE "auth_user_groups" (
  "id" bigint NOT NULL,
  "user_id" integer NOT NULL,
  "group_id" integer NOT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "auth_user_user_permissions"
--

CREATE TABLE "auth_user_user_permissions" (
  "id" bigint NOT NULL,
  "user_id" integer NOT NULL,
  "permission_id" integer NOT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "categorias"
--

CREATE TABLE "categorias" (
  "idCategoria" integer NOT NULL,
  "nombreCategoria" character varying(20) NOT NULL,
  "descripcion" text DEFAULT NULL,
  "imagen" character varying(100) DEFAULT NULL
);

--
-- Volcado de datos para la tabla "categorias"
--

INSERT INTO "categorias" ("idCategoria", "nombreCategoria", "descripcion", "imagen") VALUES
(1, 'Rostro', 'Base, correctores, polvos compactos, rubores e iluminadores', 'categorias/rostro.avif'),
(2, 'Ojos', 'Sombras, delineadores, pesta?inas y cejas', 'categorias/ojos.jpg'),
(3, 'Labios', 'Labiales, brillos y delineadores de labios', 'categorias/la.jpg'),
(4, 'Uñas', 'Esmaltes, tratamientos y accesorios para uñas', 'categorias/uñas.webp'),
(5, 'Accesorios', 'Brochas, esponjas y herramientas de maquillaje', 'categorias/accessories_feb_main.jpg'),
(9, 'Cuidado Facial', 'cremas,serums', 'categorias/cuidado_facial_T4konPk.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "clientes"
--

CREATE TABLE "clientes" (
  "idCliente" integer NOT NULL,
  "cedula" character varying(20) NOT NULL,
  "nombre" character varying(100) DEFAULT NULL,
  "email" character varying(100) DEFAULT NULL,
  "direccion" character varying(200) DEFAULT NULL,
  "telefono" character varying(20) DEFAULT NULL
);

--
-- Volcado de datos para la tabla "clientes"
--

INSERT INTO "clientes" ("idCliente", "cedula", "nombre", "email", "direccion", "telefono") VALUES
(2, '10002', 'Laura Gómez', 'laura.gomez@gmail.com', 'Carrera 45 #12-34 Montería', '2147483647'),
(13, '7410852', 'william fontecha', 'carlos@gmail.com', '58bis, Rafael Uribe Uribe, Bogotá, Bogotá D.C. (9-49)', '3115176388'),
(15, '441515', 'lalaa ortega ', 'lala@gmail.com', 'carrera 19a 11, Teusaquillo, Bogotá, Bogotá D.C. - conjunto albarosa', '3024892804'),
(17, '441515', 'laura torres', 'lauratorres@gmail.com', 'carrera 19a 11a 67, Engativá, Bogotá, Bogotá D.C. (9-49)', '3024892804'),
(18, '458527', 'laura tibaque', 'lauratibaque@gmail.com', 'carrera 19a 11a 67, Comuna 4 - Cazucá, Soacha, Cundinamarca (9-49)', '3025458285'),
(20, '1234567', 'lauren ortiz', 'laurensamanta0.r@gmail.com', 'carrera 19a 11a 67, Barrios Unidos, Bogotá, Bogotá D.C. - 9-49', '3024892804'),
(22, '111111122222', 'michael   ', 'michael@gmail.com', 'calle123#12-14, Comuna 1 - Compartir, Soacha, Cundinamarca (soacha), Comuna 4 - Cazucá, Soacha, Cundinamarca (soacha), Antonio Nariño, Bogotá, Bogotá D.C. (barrio antonio nariño)', '3025858545'),
(23, '2025561653', 'alejandro rodriguez ', 'alejandro@gmail.com', 'calle123#4-5, Suba, Bogotá, Bogotá D.C. (suba ), Suba, Bogotá, Bogotá D.C. (suba )', '30254646254'),
(25, '2452785278', 'magda maria', 'lausamanta2024cha@gmail.com', 'Calle 19a #11a-67', '3024892804'),
(26, '111111122222', 'maria magdalena   so corro', 'lauren.20031028@gmail.com', 'calle123#4-5, Teusaquillo, Bogotá, Bogotá D.C. (teusaquillo)', '30254646254'),
(27, '1354531324', 'william fontecha', 'fontequin@gmail.com', 'calle #12, Barrios Unidos, Bogotá, Bogotá D.C. (9-49)', '3115176380'),
(28, '25431352', 'andrea   contreras ', 'andreacontrerlombana@gmail.com', 'carrera 19a 11a 67, Comuna 6 - San Humberto, Soacha, Cundinamarca (triunfo 4)', '3024892804'),
(29, '656135156', 'mao b2b', 'infob2bingenieria@gmail.com', 'carrera 19a 11a 67', '32123165656'),
(30, '13514564561', 'michael  ', 'michaeldaramirez117@gmail.com', 'carrera 19a 11a 67, Engativá, Engativá, Bogotá, Bogotá D.C. (engativa)', '32123165656');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "configuracion_global"
--

CREATE TABLE "configuracion_global" (
  "id" bigint NOT NULL,
  "margen_ganancia" decimal(5,2) DEFAULT 10.00,
  "fecha_actualizacion" datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
);

--
-- Volcado de datos para la tabla "configuracion_global"
--

INSERT INTO "configuracion_global" ("id", "margen_ganancia", "fecha_actualizacion") VALUES
(1, 9.00, '2025-12-10 20:25:01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "confirmaciones_entrega"
--

CREATE TABLE "confirmaciones_entrega" (
  "idConfirmacion" integer NOT NULL,
  "foto_entrega" character varying(100) DEFAULT NULL,
  "calificacion" integer NOT NULL,
  "comentario" longtext DEFAULT NULL,
  "fecha_confirmacion" datetime(6) NOT NULL,
  "pedido_id" integer NOT NULL,
  "repartidor_id" integer DEFAULT NULL
);

--
-- Volcado de datos para la tabla "confirmaciones_entrega"
--

INSERT INTO "confirmaciones_entrega" ("idConfirmacion", "foto_entrega", "calificacion", "comentario", "fecha_confirmacion", "pedido_id", "repartidor_id") VALUES
(1, 'confirmaciones_entrega/ojos.jpg', 3, 'si lo recibi gracias', '2025-11-26 17:30:02.430998', 52, 16),
(2, '', 5, 'exelente', '2025-11-26 17:39:58.936851', 48, 16),
(3, '', 5, 'bien', '2025-12-10 16:22:20.815213', 43, 15),
(4, '', 3, 'bien,amable', '2025-12-10 16:22:37.392926', 44, 15),
(5, '', 5, 'excelente', '2025-12-10 20:11:57.780570', 87, 17);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "core_notificacion"
--

CREATE TABLE "core_notificacion" (
  "id" bigint NOT NULL,
  "mensaje" longtext NOT NULL,
  "leida" smallint NOT NULL,
  "fecha" datetime(6) NOT NULL,
  "usuario_id" integer NOT NULL
);

--
-- Volcado de datos para la tabla "core_notificacion"
--

INSERT INTO "core_notificacion" ("id", "mensaje", "leida", "fecha", "usuario_id") VALUES
(1, 'Nuevo pedido desde soacha, Cundinamarca.', 0, '2025-11-07 07:54:00.290765', 1),
(2, 'Nuevo pedido desde soacha, Cundinamarca.', 0, '2025-11-07 07:59:13.501034', 1),
(3, 'Nuevo pedido #11 de Cliente1 desde Calle Principal #123.', 0, '2025-11-07 08:37:56.186601', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "core_profile"
--

CREATE TABLE "core_profile" (
  "id" bigint NOT NULL,
  "token_recuperacion" character varying(64) DEFAULT NULL,
  "user_id" integer NOT NULL
);

--
-- Volcado de datos para la tabla "core_profile"
--

INSERT INTO "core_profile" ("id", "token_recuperacion", "user_id") VALUES
(1, NULL, 1),
(2, NULL, 2),
(3, NULL, 3),
(4, NULL, 4),
(5, NULL, 5),
(6, NULL, 6),
(7, NULL, 7),
(8, NULL, 8),
(9, NULL, 9),
(10, NULL, 10),
(11, NULL, 11),
(12, NULL, 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "detallepedido"
--

CREATE TABLE "detallepedido" (
  "idDetalle" integer NOT NULL,
  "idPedido" integer NOT NULL,
  "idProducto" bigint DEFAULT NULL,
  "cantidad" integer  DEFAULT 1,
  "precio_unitario" decimal(10,2) NOT NULL,
  "subtotal" decimal(12,2) NOT NULL,
  "margen_ganancia" decimal(5,2) NOT NULL
);

--
-- Volcado de datos para la tabla "detallepedido"
--

INSERT INTO "detallepedido" ("idDetalle", "idPedido", "idProducto", "cantidad", "precio_unitario", "subtotal", "margen_ganancia") VALUES
(32, 20, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(33, 21, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(34, 22, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(35, 23, 7700000000042, 1, 15000.00, 15000.00, 10.00),
(36, 24, 7700000000032, 1, 14000.00, 14000.00, 10.00),
(37, 25, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(38, 26, 7700000000002, 1, 38000.00, 38000.00, 10.00),
(39, 27, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(40, 28, 7700000000032, 1, 14000.00, 14000.00, 10.00),
(46, 33, 7700000000003, 1, 29000.00, 29000.00, 10.00),
(47, 33, 7700000000004, 1, 34000.00, 34000.00, 10.00),
(48, 34, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(49, 35, 7700000000004, 1, 34000.00, 34000.00, 10.00),
(50, 36, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(51, 37, 7701234567890, 1, 55000.00, 55000.00, 10.00),
(52, 38, 7700000000023, 1, 18000.00, 18000.00, 10.00),
(53, 38, 7700000000021, 1, 22000.00, 22000.00, 10.00),
(54, 39, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(55, 39, 7700000000013, 1, 16000.00, 16000.00, 10.00),
(56, 40, 7700000000011, 1, 42000.00, 42000.00, 10.00),
(60, 43, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(61, 43, 7700000000002, 1, 38000.00, 38000.00, 10.00),
(62, 43, 7700000000003, 1, 29000.00, 29000.00, 10.00),
(63, 43, 7700000000004, 1, 34000.00, 34000.00, 10.00),
(64, 44, 7700000000012, 2, 18000.00, 36000.00, 10.00),
(65, 45, 7700000000012, 2, 18000.00, 36000.00, 10.00),
(66, 45, 7700000000013, 1, 16000.00, 16000.00, 10.00),
(67, 46, 7700000000024, 1, 15000.00, 15000.00, 10.00),
(68, 46, 7700000000025, 1, 30000.00, 30000.00, 10.00),
(69, 46, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(70, 47, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(71, 48, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(74, 52, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(75, 52, 7700000000002, 1, 38000.00, 38000.00, 10.00),
(76, 53, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(77, 53, 7700000000002, 1, 38000.00, 38000.00, 10.00),
(78, 54, 7700000000003, 1, 29000.00, 29000.00, 10.00),
(79, 55, 7700000000003, 1, 29000.00, 29000.00, 10.00),
(80, 55, 7700000000004, 1, 34000.00, 34000.00, 10.00),
(81, 56, 7700000000012, 1, 18000.00, 18000.00, 10.00),
(82, 56, 7700000000011, 1, 42000.00, 42000.00, 10.00),
(83, 57, 7700000000024, 1, 15000.00, 15000.00, 10.00),
(84, 57, 7700000000023, 1, 18000.00, 18000.00, 10.00),
(85, 58, 7700000000013, 1, 16000.00, 16000.00, 10.00),
(86, 58, 7700000000014, 1, 20000.00, 20000.00, 10.00),
(87, 59, 7700000000002, 1, 38000.00, 38000.00, 10.00),
(88, 59, 7700000000003, 2, 29000.00, 58000.00, 10.00),
(89, 60, 7700000000013, 1, 16000.00, 16000.00, 10.00),
(90, 60, 7700000000012, 2, 18000.00, 36000.00, 10.00),
(91, 61, 7701234567890, 2, 55000.00, 110000.00, 10.00),
(92, 61, 7700000000011, 2, 42000.00, 84000.00, 10.00),
(93, 62, 7700000000032, 1, 14000.00, 14000.00, 10.00),
(94, 62, 7700000000031, 1, 12000.00, 12000.00, 10.00),
(96, 64, 7700000000002, 2, 38000.00, 76000.00, 10.00),
(97, 64, 7700000000003, 1, 29000.00, 29000.00, 10.00),
(98, 64, 7700000000001, 1, 32000.00, 32000.00, 10.00),
(99, 65, 7700000000032, 1, 18200.00, 18200.00, 10.00),
(100, 65, 7700000000033, 2, 23400.00, 46800.00, 10.00),
(111, 74, 7700000000002, 1, 49400.00, 49400.00, 10.00),
(112, 74, 7700000000044, 1, 36400.00, 36400.00, 10.00),
(113, 74, 7700000000043, 2, 15600.00, 31200.00, 10.00),
(114, 75, 7700000000005, 1, 75400.00, 75400.00, 10.00),
(115, 75, 7700000000041, 1, 62400.00, 62400.00, 10.00),
(116, 75, 7700000000042, 2, 19500.00, 39000.00, 10.00),
(117, 76, 7700000000043, 2, 15600.00, 31200.00, 10.00),
(118, 76, 7700000000042, 2, 19500.00, 39000.00, 10.00),
(119, 76, 7700000000041, 2, 62400.00, 124800.00, 10.00),
(120, 77, 7700000000001, 1, 41600.00, 41600.00, 10.00),
(121, 77, 7700000000004, 1, 44200.00, 44200.00, 10.00),
(122, 77, 7700000000003, 1, 37700.00, 37700.00, 10.00),
(123, 77, 7700000000032, 1, 18200.00, 18200.00, 10.00),
(124, 77, 7700000000035, 2, 6500.00, 13000.00, 10.00),
(125, 78, 7700000000002, 1, 36800.00, 36800.00, 10.00),
(126, 78, 7700000000003, 2, 33350.00, 66700.00, 10.00),
(127, 78, 7700000000033, 1, 20700.00, 20700.00, 10.00),
(128, 79, 7700000000013, 2, 18400.00, 36800.00, 10.00),
(129, 80, 7700000000042, 2, 17250.00, 34500.00, 10.00),
(130, 81, 7700000000032, 1, 16100.00, 16100.00, 10.00),
(131, 81, 7700000000033, 1, 20700.00, 20700.00, 10.00),
(132, 82, 7700000000002, 1, 36800.00, 36800.00, 10.00),
(133, 82, 7700000000033, 1, 20700.00, 20700.00, 10.00),
(134, 83, 7700000000023, 1, 20700.00, 20700.00, 10.00),
(135, 83, 7700000000024, 1, 17250.00, 17250.00, 10.00),
(136, 84, 7700000000032, 2, 16100.00, 32200.00, 10.00),
(137, 84, 7700000000033, 2, 20700.00, 41400.00, 10.00),
(138, 85, 7700000000023, 2, 20700.00, 41400.00, 10.00),
(139, 85, 7700000000024, 2, 17250.00, 34500.00, 10.00),
(140, 86, 7700000000031, 2, 13800.00, 27600.00, 10.00),
(141, 87, 7700000000021, 2, 25300.00, 50600.00, 10.00),
(142, 88, 7700000000001, 1, 39100.00, 39100.00, 10.00),
(143, 88, 7709876543220, 1, 17250.00, 17250.00, 10.00),
(144, 89, 7700000000042, 2, 17250.00, 34500.00, 10.00),
(145, 90, 7700000000033, 1, 20700.00, 20700.00, 10.00),
(146, 90, 7700000000034, 1, 17250.00, 17250.00, 10.00),
(147, 91, 7700000000013, 1, 18400.00, 18400.00, 10.00),
(148, 91, 7700000000014, 1, 23000.00, 23000.00, 10.00),
(149, 92, 7700000000002, 1, 36800.00, 36800.00, 10.00),
(150, 92, 7700000000003, 1, 33350.00, 33350.00, 10.00),
(151, 93, 7701122334455, 1, 5750.00, 5750.00, 10.00),
(152, 93, 7700000000023, 2, 20700.00, 41400.00, 10.00),
(153, 94, 7700000000023, 1, 20700.00, 20700.00, 10.00),
(154, 94, 7700000000024, 1, 17250.00, 17250.00, 10.00),
(155, 94, 7700000000025, 1, 34500.00, 34500.00, 10.00),
(156, 95, 7700000000012, 1, 20700.00, 20700.00, 10.00),
(157, 95, 7700000000013, 1, 18400.00, 18400.00, 10.00),
(158, 96, 7700000000002, 1, 40350.00, 40350.00, 10.00),
(159, 96, 7700000000003, 1, 36600.00, 36600.00, 10.00),
(160, 97, 7700000000001, 1, 42900.00, 42900.00, 10.00),
(161, 97, 7700000000002, 1, 40350.00, 40350.00, 10.00),
(162, 98, 7700000000002, 1, 40350.00, 40350.00, 10.00),
(163, 98, 7700000000003, 1, 36600.00, 36600.00, 10.00),
(164, 98, 7700000000004, 1, 47950.00, 47950.00, 10.00),
(165, 98, 7700000000035, 1, 6300.00, 6300.00, 10.00),
(166, 99, 7700000000024, 1, 18900.00, 18900.00, 10.00),
(167, 99, 7700000000023, 1, 23550.00, 23550.00, 10.00),
(168, 99, 7700000000043, 2, 15150.00, 30300.00, 10.00),
(169, 100, 7700000000024, 1, 19650.00, 19650.00, 10.00),
(170, 100, 7700000000023, 1, 23550.00, 23550.00, 10.00),
(171, 100, 7700000000043, 2, 15700.00, 31400.00, 10.00),
(172, 101, 7700000000024, 1, 19650.00, 19650.00, 10.00),
(173, 101, 7700000000023, 1, 23550.00, 23550.00, 10.00),
(174, 102, 7700000000024, 1, 19650.00, 19650.00, 10.00),
(175, 102, 7700000000023, 1, 23550.00, 23550.00, 10.00),
(176, 103, 7700000000012, 1, 23350.00, 23350.00, 9.00),
(177, 103, 7700000000013, 1, 20750.00, 20750.00, 9.00),
(178, 103, 7700000000032, 3, 18150.00, 54450.00, 9.00),
(179, 104, 7700000000024, 1, 19450.00, 19450.00, 9.00),
(180, 104, 7700000000042, 1, 19450.00, 19450.00, 9.00),
(181, 105, 7709876543221, 2, 11050.00, 22100.00, 9.00),
(182, 105, 7700000000031, 1, 15550.00, 15550.00, 9.00),
(183, 106, 7700000000023, 2, 23350.00, 46700.00, 9.00),
(184, 106, 7700000000035, 1, 6500.00, 6500.00, 9.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "distribuidores"
--

CREATE TABLE "distribuidores" (
  "idDistribuidor" integer NOT NULL,
  "nombreDistribuidor" character varying(30) DEFAULT NULL,
  "contacto" character varying(20) DEFAULT NULL
);

--
-- Volcado de datos para la tabla "distribuidores"
--

INSERT INTO "distribuidores" ("idDistribuidor", "nombreDistribuidor", "contacto") VALUES
(1, 'Proveedor Central ', '214748364'),
(7, 'Proveedor Central tt', '214748364755');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "distribuidorproducto"
--

CREATE TABLE "distribuidorproducto" (
  "idDistribuidor" integer NOT NULL,
  "idProducto" integer NOT NULL
);

--
-- Volcado de datos para la tabla "distribuidorproducto"
--

INSERT INTO "distribuidorproducto" ("idDistribuidor", "idProducto") VALUES
(1, 1),
(1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "django_admin_log"
--

CREATE TABLE "django_admin_log" (
  "id" integer NOT NULL,
  "action_time" datetime(6) NOT NULL,
  "object_id" longtext DEFAULT NULL,
  "object_repr" character varying(200) NOT NULL,
  "action_flag" smallint(5)  NOT NULL CHECK ("action_flag" >= 0),
  "change_message" longtext NOT NULL,
  "content_type_id" integer DEFAULT NULL,
  "user_id" integer NOT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "django_content_type"
--

CREATE TABLE "django_content_type" (
  "id" integer NOT NULL,
  "app_label" character varying(100) NOT NULL,
  "model" character varying(100) NOT NULL
);

--
-- Volcado de datos para la tabla "django_content_type"
--

INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(13, 'core', 'categoria'),
(7, 'core', 'cliente'),
(28, 'core', 'configuracionglobal'),
(24, 'core', 'confirmacionentrega'),
(18, 'core', 'detallepedido'),
(14, 'core', 'distribuidor'),
(15, 'core', 'distribuidorproducto'),
(26, 'core', 'loteproducto'),
(16, 'core', 'mensajecontacto'),
(25, 'core', 'movimientolote'),
(22, 'core', 'movimientoproducto'),
(19, 'core', 'notificacion'),
(23, 'core', 'notificacionproblema'),
(27, 'core', 'notificacionreporte'),
(11, 'core', 'pedido'),
(20, 'core', 'pedidoproducto'),
(12, 'core', 'producto'),
(17, 'core', 'profile'),
(8, 'core', 'repartidor'),
(9, 'core', 'rol'),
(21, 'core', 'subcategoria'),
(10, 'core', 'usuario'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "django_migrations"
--

CREATE TABLE "django_migrations" (
  "id" bigint NOT NULL,
  "app" character varying(255) NOT NULL,
  "name" character varying(255) NOT NULL,
  "applied" datetime(6) NOT NULL
);

--
-- Volcado de datos para la tabla "django_migrations"
--

INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES
(1, 'contenttypes', '0001_initial', '2025-10-24 03:20:47.874567'),
(2, 'auth', '0001_initial', '2025-10-24 03:20:48.743453'),
(3, 'admin', '0001_initial', '2025-10-24 03:20:48.928893'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-10-24 03:20:48.939201'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-10-24 03:20:48.950214'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-10-24 03:20:49.030487'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-10-24 03:20:49.118988'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-10-24 03:20:49.142315'),
(9, 'auth', '0004_alter_user_username_opts', '2025-10-24 03:20:49.153530'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-10-24 03:20:49.215674'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-10-24 03:20:49.231239'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-10-24 03:20:49.235980'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-10-24 03:20:49.251292'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-10-24 03:20:49.266590'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-10-24 03:20:49.285854'),
(16, 'auth', '0011_update_proxy_permissions', '2025-10-24 03:20:49.301392'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-10-24 03:20:49.316915'),
(19, 'sessions', '0001_initial', '2025-10-24 03:20:49.667817'),
(51, 'core', '0001_initial', '2025-12-10 16:07:01.037089'),
(52, 'core', '0002_alter_producto_options', '2025-12-10 16:07:01.048003'),
(53, 'core', '0003_auto_fix_duplicate_columns', '2025-12-10 16:07:01.053292'),
(54, 'core', '0004_cliente_distribuidor_distribuidorproducto_repartidor_and_more', '2025-12-10 16:07:01.059349'),
(55, 'core', '0005_alter_categoria_options', '2025-12-10 16:07:01.065939'),
(56, 'core', '0006_categoria_imagen', '2025-12-10 16:07:01.068967'),
(57, 'core', '0007_movimientoproducto', '2025-12-10 16:07:01.078100'),
(58, 'core', '0008_movimientoproducto_precio_unitario', '2025-12-10 16:07:01.083614'),
(59, 'core', '0009_movimientoproducto_costo_unitario', '2025-12-10 16:07:01.084637'),
(60, 'core', '0010_notificacionproblema_delete_notificacion', '2025-12-10 16:07:01.093713'),
(61, 'core', '0011_notificacionproblema_fecha_respuesta_and_more', '2025-12-10 16:07:01.097965'),
(62, 'core', '0012_add_estado_fields_sql', '2025-12-10 16:07:01.103155'),
(63, 'core', '0013_alter_detallepedido_options_alter_pedido_options_and_more', '2025-12-10 16:07:01.109428'),
(64, 'core', '0014_repartidor_email', '2025-12-10 16:07:01.113760'),
(65, 'core', '0015_alter_repartidor_telefono', '2025-12-10 16:07:01.118243'),
(66, 'core', '0016_pedido_facturas_enviadas', '2025-12-10 16:07:01.122032'),
(67, 'core', '0017_remove_pedido_fecha_detallepedido_idpedido_and_more', '2025-12-10 16:07:01.126692'),
(68, 'core', '0018_add_missing_movimientos_columns', '2025-12-10 16:07:01.132834'),
(69, 'core', '0019_confirmacionentrega', '2025-12-10 16:07:01.145820'),
(70, 'core', '0020_loteproducto_movimientolote_and_more', '2025-12-10 16:07:01.150928'),
(71, 'core', '0021_notificacionreporte', '2025-12-10 16:07:01.159896'),
(72, 'core', '0022_alter_movimientoproducto_tipo_movimiento', '2025-12-10 16:07:01.165933'),
(73, 'core', '0023_alter_movimientoproducto_tipo_movimiento_and_more', '2025-12-10 16:07:01.172786'),
(74, 'core', '0024_producto_precio_venta', '2025-12-10 16:07:01.196217'),
(75, 'core', '0025_cliente_distribuidor_distribuidorproducto_repartidor_and_more', '2025-12-10 17:38:51.678733'),
(76, 'core', '0026_producto_margen_ganancia', '2025-12-10 17:39:15.327362'),
(77, 'core', '0027_configuracion_global', '2025-12-10 17:54:34.753445'),
(78, 'core', '0028_remove_producto_margen_ganancia', '2025-12-10 17:56:08.985958'),
(79, 'core', '0029_detallepedido_margen_ganancia', '2025-12-10 18:03:21.134440');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "django_session"
--

CREATE TABLE "django_session" (
  "session_key" character varying(40) NOT NULL,
  "session_data" longtext NOT NULL,
  "expire_date" datetime(6) NOT NULL
);

--
-- Volcado de datos para la tabla "django_session"
--

INSERT INTO "django_session" ("session_key", "session_data", "expire_date") VALUES
('1ofml2vngq04ufspkh6n7glaqcods9lc', 'e30:1vMcsc:40C7WG9FUlqYEsmirrNoX0z7ZD_ZoBYmUXs9W6aYP7M', '2025-12-06 01:57:38.565879'),
('9ldcrjet1dmnb530p42ldcj31zcb41rc', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJRyEkuLUvOUEDJF-TlAlbUAayMUyg:1vNh8C:eBbKVRmo2Nb8Wcd0qjWaQMOOVa8B_4EpfGXpFihlO58', '2025-12-09 00:42:08.666163'),
('b5diouliduym2ojwpchhvy9yi5j6s4a9', '.eJyFkk1uwjAQha8SzToU2xBKsitUShfcACHLOK6wmnha_6QLxN07QUBbWtrlPL95M5_tPaSQlLcobQMVZ_mldthtvYEK6lZ1IaI32UPTWZfBp8djS4ajbEP0qkFPp68em6QjBumN2qoQjbYNBqjWe7ikLlQw2TKFnUWX1S2-U6NWLtpG0SKCCqShMjkbh1FQFXPG2B0tSLJ-kWQ1pHuoJpPpWXTJ9Dgosxx61aKXEaOiHTmfnbpbjMP41WixrEeM09Rno3dK9sZp21njIgUA42MuxoKJezIcM6RGJ22vLlm8zOFUM0HRh_yabmXfEuFkT4_ZcIf_AhY3AHk5uwLk5fwHIPsVUNwCFH8Bsu-AbFoMgJscjPf0Eb4-7DlxvTl8AIaXvDo:1vTQwR:Wty0zBBvp9hIU5sUyEKXiN1lMpe5YWvzLHsWgkxkvFo', '2025-12-24 20:37:43.387356'),
('b72iptc762mpqkm89tk5wjf1hsjeekgw', 'e30:1vMcsb:0JHZJ70dRmUm8N1Ipu6CLAw1He5zQEj2Azce_8a7ibI', '2025-12-06 01:57:37.145277'),
('k5549xb69c0urw9cc19ek668uhh0z37y', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJRyEkuLUvOUEDJF-TlAlbUAayMUyg:1vPYvx:SOxFhCXoc1KI_MIVw1gpN1Ts4Z7wC4DUY1rEjLJUNvU', '2025-12-14 04:21:13.503847'),
('l5900uvny2bedhbazs6j6j4x1dan99zf', '.eJyrVkpOLCrKLMlXsqpWMjc3gAFDIyUrQx0UEWOgSG0tAER1C_A:1vLrXM:LxqIck_4vhkHBeBGiSXlT-_SFABF0LwAY-Tanau3tb0', '2025-12-03 23:24:32.718893'),
('tpaasu0iccukacp3q24jsj4gimlci6m5', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJRyEkuLUvOUEDJF-TlAlbUAayMUyg:1vJWWz:_eaifUz35kpwBBbdR2ByLo2ruRlLwPHY9wTo3GRj2vk', '2025-11-27 12:34:29.154577');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "facturas"
--

CREATE TABLE "facturas" (
  "idFactura" integer NOT NULL,
  "idPedido" integer DEFAULT NULL,
  "montoTotal" decimal(10,2) DEFAULT NULL,
  "fechaEmision" timestamp NOT NULL DEFAULT current_timestamp(),
  "estado" character varying(20) DEFAULT 'Pendiente',
  "idMetodoPago" integer DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "lotes_producto"
--

CREATE TABLE "lotes_producto" (
  "idLote" integer NOT NULL,
  "codigo_lote" character varying(100) NOT NULL,
  "fecha_entrada" datetime(6) NOT NULL,
  "fecha_vencimiento" date DEFAULT NULL,
  "cantidad_inicial" integer NOT NULL,
  "cantidad_disponible" integer NOT NULL,
  "costo_unitario" decimal(10,2) NOT NULL,
  "precio_venta" decimal(10,2) NOT NULL,
  "total_con_iva" decimal(10,2) DEFAULT NULL,
  "iva" decimal(10,2) DEFAULT NULL,
  "proveedor" character varying(200) DEFAULT NULL,
  "producto_id" bigint NOT NULL
);

--
-- Volcado de datos para la tabla "lotes_producto"
--

INSERT INTO "lotes_producto" ("idLote", "codigo_lote", "fecha_entrada", "fecha_vencimiento", "cantidad_inicial", "cantidad_disponible", "costo_unitario", "precio_venta", "total_con_iva", "iva", "proveedor", "producto_id") VALUES
(1, 'L2025-11', '2025-11-26 18:41:11.536084', '2027-11-01', 578, 464, 0.00, 0.00, NULL, NULL, NULL, 7700000000001),
(16, 'L2025-11', '2025-11-26 18:41:11.753123', '2027-11-01', 398, 382, 0.00, 0.00, NULL, NULL, NULL, 7700000000002),
(28, 'L2025-11', '2025-11-26 18:41:11.916369', '2027-11-01', 622, 608, 29000.00, 36250.00, NULL, NULL, NULL, 7700000000003),
(40, 'L2025-11', '2025-11-26 18:41:12.073029', '2027-11-01', 525, 518, 0.00, 0.00, NULL, NULL, NULL, 7700000000004),
(52, 'L2025-11', '2025-11-26 18:41:12.228059', '2027-11-01', 329, 326, 0.00, 0.00, NULL, NULL, NULL, 7700000000005),
(65, 'L2025-11', '2025-11-26 18:41:12.344721', '2027-11-01', 100, 96, 42000.00, 52500.00, NULL, NULL, NULL, 7700000000011),
(66, 'L2025-11', '2025-11-26 18:41:12.370556', '2027-11-01', 110, 94, 18000.00, 22500.00, NULL, NULL, NULL, 7700000000012),
(68, 'L2025-11', '2025-11-26 18:41:12.458944', '2026-11-01', 50, 40, 16000.00, 20000.00, NULL, NULL, NULL, 7700000000013),
(70, 'L2025-11', '2025-11-26 18:41:12.514643', '2027-11-01', 35, 32, 20000.00, 25000.00, NULL, NULL, NULL, 7700000000014),
(71, 'L2025-11', '2025-11-26 18:41:12.541690', '2027-11-01', 10, 6, 22000.00, 27500.00, NULL, NULL, NULL, 7700000000021),
(72, 'L2025-11', '2025-11-26 18:41:12.565520', '2025-12-01', 164, 14, 18000.00, 22500.00, 471240.00, 75240.00, 'Proveedor Central ', 7700000000023),
(80, 'L2025-11', '2025-11-26 18:41:12.684374', '2027-11-01', 10, 0, 14000.00, 17500.00, NULL, NULL, NULL, 7700000000032),
(81, 'L2025-11', '2025-11-26 18:41:12.724443', '2025-11-26', 21, 0, 18000.00, 22500.00, 449820.00, 71820.00, 'Proveedor Central ', 7700000000033),
(82, 'L2025-11', '2025-11-26 18:41:12.750655', '2028-01-01', 10, 7, 48000.00, 60000.00, 571200.00, 91200.00, NULL, 7700000000041),
(83, 'L2025-11', '2025-11-26 18:41:12.771411', '2028-01-01', 20, 10, 15000.00, 18750.00, NULL, NULL, NULL, 7700000000042),
(84, 'L2025-11', '2025-11-26 18:41:12.799524', '2028-01-01', 20, 12, 12000.00, 15000.00, NULL, NULL, NULL, 7700000000043),
(85, 'L2025-10', '2025-11-26 18:41:12.836769', '2027-11-05', 189, 186, 55000.00, 68750.00, NULL, NULL, NULL, 7701234567890),
(96, 'L2025-11', '2025-11-26 18:41:12.946106', '2025-11-26', 12, 0, 15000.00, 18750.00, 214200.00, 34200.00, 'Manual', 7709876543220),
(99, 'L2025-11', '2025-11-26 19:25:39.091678', '2025-11-26', 10, 0, 15000.00, 18750.00, 178500.00, 28500.00, 'Proveedor Central ', 7700000000024),
(100, 'L2025-12', '2025-11-26 19:27:00.228524', '2025-11-26', 10, 0, 18000.00, 22500.00, 214200.00, 34200.00, 'Proveedor Central tt', 7700000000033),
(101, 'L2025-11', '2025-11-30 00:35:24.670064', '2025-12-25', 10, 9, 12000.00, 15000.00, 142800.00, 22800.00, NULL, 7700000000031),
(102, 'L2025-12', '2025-11-30 00:49:06.984873', '2025-12-10', 10, 10, 30000.00, 37500.00, 357000.00, 57000.00, 'Proveedor Central tt', 7700000000025),
(103, 'L2025-15', '2025-11-30 00:49:44.627014', '2026-01-16', 100, 98, 5000.00, 6250.00, 595000.00, 95000.00, 'Proveedor Central ', 7700000000035),
(104, 'L2025-10', '2025-11-30 00:50:09.951812', '2025-12-01', 17, 17, 15000.00, 18750.00, 303450.00, 48450.00, 'Proveedor Central ', 7700000000034),
(105, 'L2025-15', '2025-11-30 00:52:22.165856', '2025-11-30', 10, 10, 28000.00, 35000.00, 333200.00, 53200.00, NULL, 7700000000044),
(106, 'L2025-10', '2025-11-30 00:59:52.375621', '2025-11-29', 10, 10, 18000.00, 22500.00, 214200.00, 34200.00, NULL, 7700000000033),
(107, 'L2025-15', '2025-11-30 01:01:51.419191', '2025-12-31', 122, 105, 15000.00, 18750.00, 2177700.00, 347700.00, 'Proveedor Central tt', 7700000000024),
(108, 'L2025-10', '2025-11-30 01:02:26.801969', '2025-11-28', 10, 0, 15000.00, 18750.00, 178500.00, 28500.00, 'Proveedor Central ', 7700000000024),
(109, 'L2025-12', '2025-11-30 01:02:52.132873', '2025-11-29', 30, 10, 15000.00, 18750.00, 535500.00, 85500.00, 'Proveedor Central tt', 7700000000024),
(110, 'L2025-12', '2025-11-30 01:06:03.539295', '2025-11-28', 10, 10, 5000.00, 6250.00, 59500.00, 9500.00, 'Proveedor Central ', 7701122334455),
(111, 'L2025-11', '2025-11-30 01:06:20.413548', '2025-11-19', 20, 20, 5000.00, 6250.00, 119000.00, 19000.00, 'Proveedor Central ', 7701122334455),
(112, 'L2025-10', '2025-11-30 01:07:04.467336', '2026-01-16', 50, 50, 5000.00, 6250.00, 297500.00, 47500.00, NULL, 7701122334455),
(113, 'L2025-15', '2025-11-30 01:07:39.269457', '2025-11-21', 20, 20, 25000.00, 31250.00, 595000.00, 95000.00, 'Proveedor Central ', 7700000000015),
(114, 'L2025-10', '2025-11-30 01:07:59.078804', '2026-01-09', 20, 20, 25000.00, 31250.00, 595000.00, 95000.00, 'Proveedor Central ', 7700000000015),
(115, 'L2025-12', '2025-11-30 01:09:08.148228', '2025-11-01', 15, 15, 18000.00, 22500.00, 321300.00, 51300.00, NULL, 7700000000023),
(116, 'L2025-10', '2025-11-30 01:09:26.177992', '2026-01-16', 20, 10, 18000.00, 22500.00, 428400.00, 68400.00, 'Proveedor Central ', 7700000000023),
(117, 'L2025-15', '2025-11-30 01:10:03.200834', '2025-12-27', 50, 50, 35000.00, 43750.00, 2082500.00, 332500.00, NULL, 7700000000045),
(118, 'L2025-10', '2025-11-30 01:10:29.760952', '2025-12-01', 10, 10, 15000.00, 18750.00, 178500.00, 28500.00, NULL, 7709876543210),
(119, 'L2025-15', '2025-12-10 18:15:12.621581', '2026-06-25', 10, 10, 15000.00, 18750.00, 178500.00, 28500.00, 'Proveedor Central ', 7709876543220),
(120, 'L2025-10', '2025-12-10 19:04:26.186382', '2026-09-25', 10, 8, 8500.00, 10625.00, 101150.00, 16150.00, 'Proveedor Central ', 7709876543221);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "mensajecontacto"
--

CREATE TABLE "mensajecontacto" (
  "id" bigint NOT NULL,
  "nombre" character varying(100) NOT NULL,
  "correo" character varying(254) NOT NULL,
  "mensaje" longtext NOT NULL,
  "fecha" datetime(6) NOT NULL,
  "leido" smallint NOT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "mensajes"
--

CREATE TABLE "mensajes" (
  "idMensaje" integer NOT NULL,
  "nombre" character varying(50) NOT NULL,
  "email" character varying(100) NOT NULL,
  "mensaje" longtext NOT NULL,
  "fecha" datetime(6) NOT NULL
);

--
-- Volcado de datos para la tabla "mensajes"
--

INSERT INTO "mensajes" ("idMensaje", "nombre", "email", "mensaje", "fecha") VALUES
(1, 'lauren', 'laurensamanta0.r@gmail.com', 'nose', '2025-11-29 22:14:32.990959'),
(2, 'lauren', 'laurensamanta0.r@gmail.com', 'nose', '2025-11-29 22:14:35.303937'),
(3, 'lauren', 'laurensamanta0.r@gmail.com', 'nose', '2025-11-29 22:24:18.893532'),
(4, 'lauren', 'lausamanta2024@gmail.com', 'nn', '2025-11-29 22:31:31.386470'),
(5, 'lauren', 'lausamanta2024@gmail.com', 'necesito informacion detallada de la tienda\r\n', '2025-11-30 00:27:08.661864');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "metodospago"
--

CREATE TABLE "metodospago" (
  "idMetodoPago" integer NOT NULL,
  "tipo" character varying(50) DEFAULT NULL,
  "descripcion" text DEFAULT NULL
);

--
-- Volcado de datos para la tabla "metodospago"
--

INSERT INTO "metodospago" ("idMetodoPago", "tipo", "descripcion") VALUES
(1, 'Nequi', 'Pago desde la app Nequi con n?mero de celular asociado.'),
(2, 'Daviplata', 'Pago directo por Daviplata.'),
(3, 'Transferencia Bancaria', 'Transferencia desde cuentas bancarias a las apps indicadas.'),
(4, 'Efectivo', 'Pago en efectivo al recibir el pedido.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "movimientos_lote"
--

CREATE TABLE "movimientos_lote" (
  "idMovimientoLote" integer NOT NULL,
  "cantidad" integer NOT NULL,
  "fecha" datetime(6) NOT NULL,
  "lote_id" integer NOT NULL,
  "movimiento_producto_id" integer NOT NULL
);

--
-- Volcado de datos para la tabla "movimientos_lote"
--

INSERT INTO "movimientos_lote" ("idMovimientoLote", "cantidad", "fecha", "lote_id", "movimiento_producto_id") VALUES
(1, 2, '2025-11-29 22:51:18.083753', 80, 231),
(2, 2, '2025-11-29 22:51:18.095479', 81, 232),
(3, 2, '2025-11-29 22:51:46.846582', 72, 233),
(4, 2, '2025-11-29 22:51:46.855373', 99, 234),
(5, 2, '2025-11-29 22:54:05.841957', 71, 236),
(6, 1, '2025-11-29 22:55:30.693562', 1, 237),
(7, 1, '2025-11-29 22:55:30.708279', 96, 238),
(8, 2, '2025-11-29 22:56:18.826936', 83, 239),
(9, 1, '2025-11-29 22:58:11.433094', 81, 240),
(10, 1, '2025-11-29 23:00:29.072204', 68, 242),
(11, 1, '2025-11-29 23:00:29.087483', 70, 243),
(12, 1, '2025-11-29 23:12:01.493423', 16, 244),
(13, 1, '2025-11-29 23:12:01.511134', 28, 245),
(14, 2, '2025-11-30 00:06:57.890147', 72, 247),
(15, 1, '2025-11-30 00:44:22.646161', 72, 263),
(16, 1, '2025-11-30 00:44:22.651805', 99, 264),
(17, 1, '2025-11-30 00:44:50.384024', 66, 266),
(18, 1, '2025-11-30 00:44:50.384024', 68, 267);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "movimientos_producto"
--

CREATE TABLE "movimientos_producto" (
  "idMovimiento" integer NOT NULL,
  "fecha" datetime(6) NOT NULL,
  "tipo_movimiento" character varying(50) NOT NULL,
  "cantidad" integer NOT NULL,
  "stock_anterior" integer NOT NULL,
  "stock_nuevo" integer NOT NULL,
  "descripcion" character varying(255) DEFAULT NULL,
  "idPedido" integer DEFAULT NULL,
  "producto_id" bigint NOT NULL,
  "precio_unitario" decimal(10,2) NOT NULL,
  "costo_unitario" decimal(10,2) NOT NULL,
  "lote" character varying(100) DEFAULT NULL,
  "fecha_vencimiento" date DEFAULT NULL,
  "total_con_iva" decimal(10,2) DEFAULT NULL,
  "iva" decimal(10,2) DEFAULT NULL,
  "lote_origen_id" integer DEFAULT NULL
);

--
-- Volcado de datos para la tabla "movimientos_producto"
--

INSERT INTO "movimientos_producto" ("idMovimiento", "fecha", "tipo_movimiento", "cantidad", "stock_anterior", "stock_nuevo", "descripcion", "idPedido", "producto_id", "precio_unitario", "costo_unitario", "lote", "fecha_vencimiento", "total_con_iva", "iva", "lote_origen_id") VALUES
(1, '2025-11-13 12:28:33.741663', 'AJUSTE_MANUAL_ENTRADA', 100, 0, 100, 'Ajuste manual desde el panel de edición', NULL, 7700000000002, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(2, '2025-11-13 12:28:50.373593', 'AJUSTE_MANUAL_ENTRADA', 95, 5, 100, 'Ajuste manual desde el panel de edición', NULL, 7700000000023, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(3, '2025-11-13 12:29:01.429167', 'AJUSTE_MANUAL_ENTRADA', 97, 3, 100, 'Ajuste manual desde el panel de edición', NULL, 7700000000005, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(4, '2025-11-13 12:29:17.450394', 'AJUSTE_MANUAL_ENTRADA', 100, 0, 100, 'Ajuste manual desde el panel de edición', NULL, 7700000000001, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(5, '2025-11-13 12:29:32.805905', 'AJUSTE_MANUAL_ENTRADA', 97, 3, 100, 'Ajuste manual desde el panel de edición', NULL, 7700000000004, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(6, '2025-11-13 12:34:16.259831', 'SALIDA_VENTA', 1, 100, 99, 'Venta en pedido #19', NULL, 7700000000001, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(7, '2025-11-13 12:34:16.270438', 'SALIDA_VENTA', 1, 100, 99, 'Venta en pedido #19', NULL, 7700000000002, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(8, '2025-11-13 12:34:16.276011', 'SALIDA_VENTA', 1, 2, 1, 'Venta en pedido #19', NULL, 7700000000003, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(9, '2025-11-13 12:38:58.681016', 'AJUSTE_MANUAL_ENTRADA', 10, 99, 109, 'entrada de distribuidor', NULL, 7700000000001, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(10, '2025-11-13 12:39:21.372703', 'AJUSTE_MANUAL_SALIDA', 1, 100, 99, 'prueba', NULL, 7700000000005, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 52),
(11, '2025-11-13 12:40:25.332975', 'AJUSTE_MANUAL_ENTRADA', 100, 109, 209, 'prueba', NULL, 7700000000001, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(12, '2025-11-13 12:40:37.399236', 'AJUSTE_MANUAL_SALIDA', 100, 209, 109, 'prueba', NULL, 7700000000001, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(13, '2025-11-13 12:56:24.602070', 'AJUSTE_MANUAL_ENTRADA', 10, 99, 109, 'prueba', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(14, '2025-11-13 12:56:34.874003', 'AJUSTE_MANUAL_ENTRADA', 5, 109, 114, 'prueba', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(15, '2025-11-13 12:57:48.109245', 'AJUSTE_MANUAL_SALIDA', 1, 114, 113, 'prueba', NULL, 7700000000005, 58000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 52),
(16, '2025-11-13 13:00:13.600803', 'AJUSTE_MANUAL_ENTRADA', 2, 100, 102, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(17, '2025-11-13 13:00:29.558824', 'AJUSTE_MANUAL_ENTRADA', 2, 102, 104, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(18, '2025-11-13 13:01:10.339158', 'AJUSTE_MANUAL_SALIDA', 2, 104, 102, 'prueba', NULL, 7700000000023, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(19, '2025-11-13 13:04:03.794447', 'AJUSTE_MANUAL_ENTRADA', 3, 102, 105, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(20, '2025-11-20 13:14:45.561114', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #20', 20, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(21, '2025-11-20 13:27:44.052706', 'SALIDA_VENTA', 1, 109, 108, 'Venta en pedido #21', 21, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(22, '2025-11-20 13:30:46.793123', 'SALIDA_VENTA', 1, 108, 107, 'Venta en pedido #22', 22, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(23, '2025-11-20 15:26:58.003613', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #23', 23, 7700000000042, 15000.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 83),
(24, '2025-11-20 15:28:42.041296', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #24', 24, 7700000000032, 14000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(25, '2025-11-20 15:53:40.103658', 'SALIDA_VENTA', 1, 107, 106, 'Venta en pedido #25', 25, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(26, '2025-11-20 16:13:31.403608', 'SALIDA_VENTA', 1, 99, 98, 'Venta en pedido #26', 26, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(27, '2025-11-20 18:59:45.574361', 'SALIDA_VENTA', 1, 106, 105, 'Venta en pedido #27', 27, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(28, '2025-11-20 19:03:10.921162', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #28', 28, 7700000000032, 14000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(30, '2025-11-20 19:05:52.159280', 'SALIDA_VENTA', 1, 105, 104, 'Venta en pedido #30', NULL, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(31, '2025-11-20 19:05:52.172165', 'SALIDA_VENTA', 1, 98, 97, 'Venta en pedido #30', NULL, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(32, '2025-11-20 19:16:22.798062', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #31', NULL, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(33, '2025-11-20 19:26:15.688884', 'SALIDA_VENTA', 1, 100, 99, 'Venta en pedido #32', NULL, 7700000000004, 34000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 40),
(34, '2025-11-20 19:54:27.680061', 'SALIDA_VENTA', 1, 1, 0, 'Venta en pedido #33', 33, 7700000000003, 29000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(35, '2025-11-20 19:54:27.680061', 'SALIDA_VENTA', 1, 99, 98, 'Venta en pedido #33', 33, 7700000000004, 34000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 40),
(36, '2025-11-20 20:05:09.793704', 'SALIDA_VENTA', 1, 3, 2, 'Venta en pedido #34', 34, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(37, '2025-11-20 20:12:06.100814', 'SALIDA_VENTA', 1, 98, 97, 'Venta en pedido #35', 35, 7700000000004, 34000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 40),
(38, '2025-11-20 20:20:36.869797', 'SALIDA_VENTA', 1, 2, 1, 'Venta en pedido #36', 36, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(39, '2025-11-20 22:14:43.399303', 'AJUSTE_MANUAL_ENTRADA', 10, 105, 115, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(40, '2025-11-20 22:14:56.045460', 'AJUSTE_MANUAL_ENTRADA', 10, 115, 125, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(41, '2025-11-21 00:32:13.268537', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #37', 37, 7701234567890, 55000.00, 0.00, 'L2025-10', '2027-11-05', NULL, NULL, 85),
(42, '2025-11-21 01:06:53.778433', 'SALIDA_VENTA', 1, 125, 124, 'Venta en pedido #38', 38, 7700000000023, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(43, '2025-11-21 01:06:53.781496', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #38', 38, 7700000000021, 22000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 71),
(44, '2025-11-21 01:08:27.631875', 'SALIDA_VENTA', 1, 1, 0, 'Venta en pedido #39', 39, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(45, '2025-11-21 01:08:27.639980', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #39', 39, 7700000000013, 16000.00, 0.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(46, '2025-11-21 01:13:13.395294', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #40', 40, 7700000000011, 42000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 65),
(47, '2025-11-21 01:19:04.299014', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #41', NULL, 7700000000013, 16000.00, 0.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(48, '2025-11-21 01:19:04.302065', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #41', NULL, 7700000000014, 20000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 70),
(49, '2025-11-21 01:21:28.466923', 'AJUSTE_MANUAL_ENTRADA', 100, 0, 100, 'prueba', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(50, '2025-11-21 01:21:53.614000', 'AJUSTE_MANUAL_ENTRADA', 10, 0, 10, 'prueba', NULL, 7700000000012, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(53, '2025-11-21 23:11:41.101027', 'AJUSTE_MANUAL_ENTRADA', 10, 3, 13, '111', NULL, 7700000000013, 16000.00, 16000.00, 'L2025-11', '2026-11-01', NULL, NULL, NULL),
(56, '2025-11-21 23:30:06.085382', 'AJUSTE_MANUAL_ENTRADA', 1, 113, 114, 'prueba', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(57, '2025-11-21 23:56:53.042792', 'AJUSTE_MANUAL_ENTRADA', 50, 104, 154, 'Reabastecimiento desde Excel - Rostro', NULL, 7700000000001, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(58, '2025-11-21 23:56:53.042792', 'AJUSTE_MANUAL_ENTRADA', 35, 97, 132, 'Reabastecimiento desde Excel - Rostro', NULL, 7700000000002, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(59, '2025-11-21 23:56:53.059442', 'AJUSTE_MANUAL_ENTRADA', 40, 100, 140, 'Reabastecimiento desde Excel - Rostro', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(60, '2025-11-21 23:56:53.074528', 'AJUSTE_MANUAL_ENTRADA', 45, 97, 142, 'Reabastecimiento desde Excel - Rostro', NULL, 7700000000004, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(61, '2025-11-21 23:56:53.085753', 'AJUSTE_MANUAL_ENTRADA', 30, 114, 144, 'Reabastecimiento desde Excel - Rostro', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(62, '2025-11-21 23:56:53.096264', 'AJUSTE_MANUAL_ENTRADA', 25, 4, 29, 'Reabastecimiento desde Excel - Rostro', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(63, '2025-11-21 23:59:34.790142', 'AJUSTE_MANUAL_ENTRADA', 40, 13, 53, 'Reabastecimiento desde Excel - Ojos', NULL, 7700000000013, 16000.00, 16000.00, 'L2025-11', '2026-11-01', NULL, NULL, NULL),
(64, '2025-11-21 23:59:34.806346', 'AJUSTE_MANUAL_ENTRADA', 35, 4, 39, 'Reabastecimiento desde Excel - Ojos', NULL, 7700000000014, 20000.00, 20000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(65, '2025-11-22 00:20:40.738720', 'AJUSTE_MANUAL_ENTRADA', 10, 124, 134, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(66, '2025-11-22 00:20:54.820926', 'AJUSTE_MANUAL_SALIDA', 11, 134, 123, 'prueba', NULL, 7700000000023, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(67, '2025-11-22 00:24:13.500283', 'AJUSTE_MANUAL_ENTRADA', 5, 154, 159, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000001, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(68, '2025-11-22 00:24:13.500283', 'AJUSTE_MANUAL_ENTRADA', 5, 132, 137, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000002, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(69, '2025-11-22 00:24:13.518238', 'AJUSTE_MANUAL_ENTRADA', 5, 140, 145, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(70, '2025-11-22 00:24:13.518238', 'AJUSTE_MANUAL_ENTRADA', 5, 142, 147, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000004, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(71, '2025-11-22 00:24:13.534368', 'AJUSTE_MANUAL_ENTRADA', 5, 144, 149, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(72, '2025-11-22 00:24:13.534368', 'AJUSTE_MANUAL_ENTRADA', 5, 29, 34, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(73, '2025-11-22 00:25:22.684095', 'AJUSTE_MANUAL_ENTRADA', 5, 159, 164, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000001, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(74, '2025-11-22 00:25:22.685092', 'AJUSTE_MANUAL_ENTRADA', 5, 137, 142, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000002, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(75, '2025-11-22 00:25:22.699481', 'AJUSTE_MANUAL_ENTRADA', 5, 145, 150, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(76, '2025-11-22 00:25:22.716467', 'AJUSTE_MANUAL_ENTRADA', 5, 147, 152, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000004, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(77, '2025-11-22 00:25:22.716467', 'AJUSTE_MANUAL_ENTRADA', 5, 149, 154, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(78, '2025-11-22 00:25:22.735871', 'AJUSTE_MANUAL_ENTRADA', 5, 34, 39, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(79, '2025-11-22 00:49:26.361237', 'SALIDA_VENTA', 1, 123, 122, 'Venta en pedido #42', NULL, 7700000000023, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(80, '2025-11-22 00:53:43.040008', 'SALIDA_VENTA', 1, 10, 9, 'Venta en pedido #43', 43, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(81, '2025-11-22 00:53:43.040008', 'SALIDA_VENTA', 1, 142, 141, 'Venta en pedido #43', 43, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(82, '2025-11-22 00:53:43.040008', 'SALIDA_VENTA', 1, 150, 149, 'Venta en pedido #43', 43, 7700000000003, 29000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(83, '2025-11-22 00:53:43.040008', 'SALIDA_VENTA', 1, 152, 151, 'Venta en pedido #43', 43, 7700000000004, 34000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 40),
(84, '2025-11-22 00:58:29.241807', 'SALIDA_VENTA', 2, 9, 7, 'Venta en pedido #44', 44, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(85, '2025-11-22 01:01:37.447823', 'AJUSTE_MANUAL_ENTRADA', 10, 3, 13, 'prueba', NULL, 7700000000032, 14000.00, 14000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(86, '2025-11-22 01:12:30.721732', 'SALIDA_VENTA', 2, 7, 5, 'Venta en pedido #45', 45, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(87, '2025-11-22 01:12:30.726137', 'SALIDA_VENTA', 1, 53, 52, 'Venta en pedido #45', 45, 7700000000013, 16000.00, 0.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(88, '2025-11-22 01:21:06.674728', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #46', 46, 7700000000024, 15000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(89, '2025-11-22 01:21:06.680291', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #46', 46, 7700000000025, 30000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(90, '2025-11-22 01:21:06.682890', 'SALIDA_VENTA', 1, 164, 163, 'Venta en pedido #46', 46, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(91, '2025-11-22 01:35:57.527914', 'SALIDA_VENTA', 1, 163, 162, 'Venta en pedido #47', 47, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(92, '2025-11-22 01:36:36.788043', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #48', 48, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(93, '2025-11-22 01:52:10.707185', 'SALIDA_VENTA', 1, 122, 121, 'Venta en pedido #49', NULL, 7700000000023, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(94, '2025-11-22 01:52:10.711768', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #49', NULL, 7700000000021, 22000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 71),
(95, '2025-11-22 02:52:36.233724', 'SALIDA_VENTA', 1, 162, 161, 'Venta en pedido #52', 52, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(96, '2025-11-22 02:52:36.239913', 'SALIDA_VENTA', 1, 141, 140, 'Venta en pedido #52', 52, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(97, '2025-11-22 02:56:08.765820', 'AJUSTE_MANUAL_ENTRADA', 10, 3, 13, 'prueba', NULL, 7700000000021, 22000.00, 22000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(98, '2025-11-24 08:16:01.669467', 'SALIDA_VENTA', 1, 161, 160, 'Venta en pedido #53', 53, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(99, '2025-11-24 08:16:01.669467', 'SALIDA_VENTA', 1, 140, 139, 'Venta en pedido #53', 53, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(100, '2025-11-24 08:27:11.397872', 'SALIDA_VENTA', 1, 149, 148, 'Venta en pedido #54', 54, 7700000000003, 29000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(101, '2025-11-24 08:32:20.544862', 'AJUSTE_MANUAL_ENTRADA', 10, 160, 170, 'prueba', NULL, 7700000000001, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(102, '2025-11-24 08:33:05.002504', 'AJUSTE_MANUAL_ENTRADA', 100, 4, 104, 'prueba', NULL, 7700000000011, 42000.00, 42000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(104, '2025-11-24 08:42:03.048175', 'SALIDA_VENTA', 1, 148, 147, 'Venta en pedido #55', 55, 7700000000003, 29000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(105, '2025-11-24 08:42:03.061125', 'SALIDA_VENTA', 1, 151, 150, 'Venta en pedido #55', 55, 7700000000004, 34000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 40),
(106, '2025-11-24 08:47:46.261052', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #56', 56, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(107, '2025-11-24 08:47:46.270376', 'SALIDA_VENTA', 1, 104, 103, 'Venta en pedido #56', 56, 7700000000011, 42000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 65),
(108, '2025-11-24 08:52:55.995817', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #57', 57, 7700000000024, 15000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(109, '2025-11-24 08:52:56.012791', 'SALIDA_VENTA', 1, 121, 120, 'Venta en pedido #57', 57, 7700000000023, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(110, '2025-11-24 08:59:34.693504', 'AJUSTE_MANUAL_ENTRADA', 100, 3, 103, 'prueba', NULL, 7700000000012, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(111, '2025-11-24 11:22:15.120089', 'AJUSTE_MANUAL_ENTRADA', 5, 170, 175, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central tt', NULL, 7700000000001, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(112, '2025-11-24 11:22:15.138184', 'AJUSTE_MANUAL_ENTRADA', 5, 139, 144, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central tt', NULL, 7700000000002, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(113, '2025-11-24 11:22:15.154524', 'AJUSTE_MANUAL_ENTRADA', 5, 147, 152, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central tt', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(114, '2025-11-24 11:22:15.169805', 'AJUSTE_MANUAL_ENTRADA', 5, 150, 155, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central tt', NULL, 7700000000004, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(115, '2025-11-24 11:22:15.183521', 'AJUSTE_MANUAL_ENTRADA', 5, 154, 159, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central tt', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(116, '2025-11-24 11:22:15.195781', 'AJUSTE_MANUAL_ENTRADA', 5, 39, 44, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central tt', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(117, '2025-11-24 11:38:41.759902', 'SALIDA_VENTA', 1, 52, 51, 'Venta en pedido #58', 58, 7700000000013, 16000.00, 0.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(118, '2025-11-24 11:38:41.764406', 'SALIDA_VENTA', 1, 39, 38, 'Venta en pedido #58', 58, 7700000000014, 20000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 70),
(119, '2025-11-24 19:45:28.043405', 'SALIDA_VENTA', 1, 144, 143, 'Venta en pedido #59', 59, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(120, '2025-11-24 19:45:28.044522', 'SALIDA_VENTA', 2, 152, 150, 'Venta en pedido #59', 59, 7700000000003, 29000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(121, '2025-11-24 19:46:43.704560', 'SALIDA_VENTA', 1, 51, 50, 'Venta en pedido #60', 60, 7700000000013, 16000.00, 0.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(122, '2025-11-24 19:46:43.715312', 'SALIDA_VENTA', 2, 103, 101, 'Venta en pedido #60', 60, 7700000000012, 18000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(123, '2025-11-24 20:07:39.848625', 'SALIDA_VENTA', 2, 44, 42, 'Venta en pedido #61', 61, 7701234567890, 55000.00, 0.00, 'L2025-10', '2027-11-05', NULL, NULL, 85),
(124, '2025-11-24 20:07:39.852046', 'SALIDA_VENTA', 2, 103, 101, 'Venta en pedido #61', 61, 7700000000011, 42000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 65),
(125, '2025-11-24 20:11:05.527152', 'SALIDA_VENTA', 1, 13, 12, 'Venta en pedido #62', 62, 7700000000032, 14000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(126, '2025-11-24 20:11:05.527152', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #62', 62, 7700000000031, 12000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(127, '2025-11-24 21:42:51.369365', 'SALIDA_VENTA', 2, 143, 141, 'Venta en pedido #64', 64, 7700000000002, 38000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(128, '2025-11-24 21:42:51.383839', 'SALIDA_VENTA', 1, 150, 149, 'Venta en pedido #64', 64, 7700000000003, 29000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(129, '2025-11-24 21:42:51.385395', 'SALIDA_VENTA', 1, 175, 174, 'Venta en pedido #64', 64, 7700000000001, 32000.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(130, '2025-11-24 22:07:17.543187', 'SALIDA_VENTA', 1, 12, 11, 'Venta en pedido #65', 65, 7700000000032, 18200.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(131, '2025-11-24 22:07:17.547090', 'SALIDA_VENTA', 2, 5, 3, 'Venta en pedido #65', 65, 7700000000033, 23400.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 81),
(132, '2025-11-25 00:38:59.249498', 'SALIDA_VENTA', 1, 141, 140, 'Venta en pedido #74', 74, 7700000000002, 49400.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(133, '2025-11-25 00:38:59.263462', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #74', 74, 7700000000044, 36400.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, NULL),
(134, '2025-11-25 00:38:59.266461', 'SALIDA_VENTA', 2, 4, 2, 'Venta en pedido #74', 74, 7700000000043, 15600.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 84),
(135, '2025-11-25 00:51:27.482416', 'SALIDA_VENTA', 1, 159, 158, 'Venta en pedido #75', 75, 7700000000005, 75400.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 52),
(136, '2025-11-25 00:51:27.482416', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #75', 75, 7700000000041, 62400.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 82),
(137, '2025-11-25 00:51:27.482416', 'SALIDA_VENTA', 2, 4, 2, 'Venta en pedido #75', 75, 7700000000042, 19500.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 83),
(138, '2025-11-25 00:58:41.658609', 'SALIDA_VENTA', 2, 2, 0, 'Venta en pedido #76', 76, 7700000000043, 15600.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 84),
(139, '2025-11-25 00:58:41.658609', 'SALIDA_VENTA', 2, 2, 0, 'Venta en pedido #76', 76, 7700000000042, 19500.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 83),
(140, '2025-11-25 00:58:41.675256', 'SALIDA_VENTA', 2, 4, 2, 'Venta en pedido #76', 76, 7700000000041, 62400.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 82),
(141, '2025-11-26 13:57:51.594471', 'SALIDA_VENTA', 1, 174, 173, 'Venta en pedido #77', 77, 7700000000001, 41600.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(142, '2025-11-26 13:57:51.594471', 'SALIDA_VENTA', 1, 155, 154, 'Venta en pedido #77', 77, 7700000000004, 44200.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 40),
(143, '2025-11-26 13:57:51.594471', 'SALIDA_VENTA', 1, 149, 148, 'Venta en pedido #77', 77, 7700000000003, 37700.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(144, '2025-11-26 13:57:51.594471', 'SALIDA_VENTA', 1, 11, 10, 'Venta en pedido #77', 77, 7700000000032, 18200.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(145, '2025-11-26 13:57:51.610162', 'SALIDA_VENTA', 2, 5, 3, 'Venta en pedido #77', 77, 7700000000035, 6500.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(146, '2025-11-26 14:02:26.921168', 'AJUSTE_MANUAL_ENTRADA', 20, 0, 20, 'prueba', NULL, 7700000000042, 15000.00, 15000.00, 'L2025-11', '2028-01-01', NULL, NULL, NULL),
(147, '2025-11-26 14:02:45.457416', 'AJUSTE_MANUAL_ENTRADA', 20, 0, 20, 'prueba', NULL, 7700000000043, 12000.00, 12000.00, 'L2025-11', '2028-01-01', NULL, NULL, NULL),
(148, '2025-11-26 14:20:47.334155', 'AJUSTE_MANUAL_ENTRADA', 5, 173, 178, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000001, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(149, '2025-11-26 14:20:47.352365', 'AJUSTE_MANUAL_ENTRADA', 5, 140, 145, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000002, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(150, '2025-11-26 14:20:47.367167', 'AJUSTE_MANUAL_ENTRADA', 5, 148, 153, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(151, '2025-11-26 14:20:47.383740', 'AJUSTE_MANUAL_ENTRADA', 5, 154, 159, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000004, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(152, '2025-11-26 14:20:47.383740', 'AJUSTE_MANUAL_ENTRADA', 5, 158, 163, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(153, '2025-11-26 14:20:47.400738', 'AJUSTE_MANUAL_ENTRADA', 5, 42, 47, 'Reabastecimiento desde Excel - Rostro - Proveedor: Proveedor Central ', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(154, '2025-11-26 15:15:42.618631', 'AJUSTE_MANUAL_ENTRADA', 47, 47, 94, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2026-11-01 00:00:00 | Total con IVA: $3,075,650 | IVA: $491,650', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(155, '2025-11-26 15:15:42.631062', 'AJUSTE_MANUAL_ENTRADA', 153, 153, 306, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-10-01 00:00:00 | Total con IVA: $5,285,370 | IVA: $842,370', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(156, '2025-11-26 15:15:42.640460', 'AJUSTE_MANUAL_ENTRADA', 80, 145, 225, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2026-09-01 00:00:00 | Total con IVA: $3,046,400 | IVA: $486,400', NULL, 7700000000002, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(157, '2025-11-26 15:15:42.656383', 'AJUSTE_MANUAL_ENTRADA', 120, 159, 279, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2027-08-01 00:00:00 | Total con IVA: $5,437,200 | IVA: $867,200', NULL, 7700000000004, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(158, '2025-11-26 15:15:42.665211', 'AJUSTE_MANUAL_ENTRADA', 95, 178, 273, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-RRG-06 | Vencimiento: 2026-07-01 00:00:00 | Total con IVA: $3,849,700 | IVA: $614,700', NULL, 7700000000001, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(159, '2025-11-26 15:16:33.204221', 'AJUSTE_MANUAL_ENTRADA', 47, 94, 141, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2026-11-01 00:00:00 | Total con IVA: $3,075,650 | IVA: $491,650', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(160, '2025-11-26 15:16:33.206228', 'AJUSTE_MANUAL_ENTRADA', 153, 306, 459, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-10-01 00:00:00 | Total con IVA: $5,285,370 | IVA: $842,370', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(161, '2025-11-26 15:16:33.222385', 'AJUSTE_MANUAL_ENTRADA', 80, 225, 305, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2026-09-01 00:00:00 | Total con IVA: $3,046,400 | IVA: $486,400', NULL, 7700000000002, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(162, '2025-11-26 15:16:33.239633', 'AJUSTE_MANUAL_ENTRADA', 120, 279, 399, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2027-08-01 00:00:00 | Total con IVA: $5,437,200 | IVA: $867,200', NULL, 7700000000004, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(163, '2025-11-26 15:16:33.251665', 'AJUSTE_MANUAL_ENTRADA', 95, 273, 368, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-RRG-06 | Vencimiento: 2026-07-01 00:00:00 | Total con IVA: $3,849,700 | IVA: $614,700', NULL, 7700000000001, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(164, '2025-11-26 15:19:45.102805', 'AJUSTE_MANUAL_ENTRADA', 163, 163, 326, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $11,263,140 | IVA: $1,797,140', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(165, '2025-11-26 15:19:45.121847', 'AJUSTE_MANUAL_ENTRADA', 47, 141, 188, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2026-11-01 00:00:00 | Total con IVA: $3,075,650 | IVA: $491,650', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(166, '2025-11-26 15:19:45.133888', 'AJUSTE_MANUAL_ENTRADA', 153, 459, 612, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-10-01 00:00:00 | Total con IVA: $5,285,370 | IVA: $842,370', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(167, '2025-11-26 15:19:45.142681', 'AJUSTE_MANUAL_ENTRADA', 80, 305, 385, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2026-09-01 00:00:00 | Total con IVA: $3,046,400 | IVA: $486,400', NULL, 7700000000002, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(168, '2025-11-26 15:19:45.151927', 'AJUSTE_MANUAL_ENTRADA', 120, 399, 519, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2027-08-01 00:00:00 | Total con IVA: $5,437,200 | IVA: $867,200', NULL, 7700000000004, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(169, '2025-11-26 15:19:45.151927', 'AJUSTE_MANUAL_ENTRADA', 95, 368, 463, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-RRG-06 | Vencimiento: 2026-07-01 00:00:00 | Total con IVA: $3,849,700 | IVA: $614,700', NULL, 7700000000001, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(170, '2025-11-26 15:24:07.546141', 'AJUSTE_MANUAL_ENTRADA', 1, 326, 327, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(171, '2025-11-26 15:24:07.553797', 'AJUSTE_MANUAL_ENTRADA', 1, 188, 189, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BLG-02 | Vencimiento: 2026-11-01 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(172, '2025-11-26 15:24:07.560472', 'AJUSTE_MANUAL_ENTRADA', 1, 612, 613, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-CLS-03 | Vencimiento: 2027-10-01 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(173, '2025-11-26 15:24:07.567679', 'AJUSTE_MANUAL_ENTRADA', 1, 385, 386, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-IPG-04 | Vencimiento: 2026-09-01 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(174, '2025-11-26 15:24:07.574406', 'AJUSTE_MANUAL_ENTRADA', 1, 519, 520, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-05 | Vencimiento: 2026-08-01 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(175, '2025-11-26 15:24:07.585613', 'AJUSTE_MANUAL_ENTRADA', 1, 463, 464, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-RRG-06 | Vencimiento: 2026-07-01 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(176, '2025-11-26 15:34:43.572150', 'AJUSTE_MANUAL_ENTRADA', 10, 120, 130, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(177, '2025-11-26 16:25:37.665788', 'AJUSTE_MANUAL_ENTRADA', 10, 0, 10, 'prueba', NULL, 7709876543220, 15000.00, 15000.00, 'L2025-11', '2025-11-27', 178500.00, 28500.00, NULL),
(178, '2025-11-26 16:42:31.791817', 'AJUSTE_MANUAL_SALIDA', 1, 10, 9, 'prueba', NULL, 7709876543220, 15000.00, 0.00, 'L2025-11', '2025-11-27', NULL, NULL, 96),
(179, '2025-11-26 16:43:32.715947', 'AJUSTE_MANUAL_ENTRADA', 2, 9, 11, 'prueba', NULL, 7709876543220, 15000.00, 15000.00, 'L2025-11', '2025-11-26', 35700.00, 5700.00, NULL),
(180, '2025-11-26 16:47:35.256048', 'AJUSTE_MANUAL_ENTRADA', 1, 327, 328, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(181, '2025-11-26 16:47:35.256953', 'AJUSTE_MANUAL_ENTRADA', 1, 189, 190, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2026-11-01 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L2025-10', '2027-11-05', NULL, NULL, NULL),
(182, '2025-11-26 16:47:35.274057', 'AJUSTE_MANUAL_ENTRADA', 1, 613, 614, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-10-01 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(183, '2025-11-26 16:47:35.274057', 'AJUSTE_MANUAL_ENTRADA', 1, 386, 387, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2026-09-01 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(184, '2025-11-26 16:47:35.290290', 'AJUSTE_MANUAL_ENTRADA', 1, 520, 521, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2026-08-01 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(185, '2025-11-26 16:47:35.310817', 'AJUSTE_MANUAL_ENTRADA', 1, 464, 465, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-RRG-06 | Vencimiento: 2026-07-01 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(186, '2025-11-26 17:02:04.729487', 'AJUSTE_MANUAL_ENTRADA', 10, 2, 12, 'prueba', NULL, 7700000000041, 48000.00, 48000.00, 'L2025-11', '2025-11-26', 571200.00, 91200.00, NULL),
(187, '2025-11-26 17:02:31.641555', 'AJUSTE_MANUAL_ENTRADA', 1, 328, 329, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 69020.00, 11020.00, NULL),
(188, '2025-11-26 17:02:31.658288', 'AJUSTE_MANUAL_ENTRADA', 1, 190, 191, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2026-11-01 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BLG-02', '2026-11-01', 65450.00, 10450.00, NULL),
(189, '2025-11-26 17:02:31.664987', 'AJUSTE_MANUAL_ENTRADA', 1, 614, 615, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-10-01 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L-CLS-03', '2027-10-01', 34510.00, 5510.00, NULL),
(190, '2025-11-26 17:02:31.672521', 'AJUSTE_MANUAL_ENTRADA', 1, 387, 388, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2026-09-01 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L-IPG-04', '2026-09-01', 38080.00, 6080.00, NULL),
(191, '2025-11-26 17:02:31.679446', 'AJUSTE_MANUAL_ENTRADA', 1, 521, 522, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2026-08-01 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L-PCMG-05', '2026-08-01', 45220.00, 7220.00, NULL),
(192, '2025-11-26 17:02:31.687042', 'AJUSTE_MANUAL_ENTRADA', 1, 465, 466, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-RRG-06 | Vencimiento: 2026-07-01 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L-RRG-06', '2026-07-01', 40460.00, 6460.00, NULL),
(193, '2025-11-26 18:14:24.560859', 'SALIDA_VENTA', 1, 388, 387, 'Venta en pedido #78', 78, 7700000000002, 36800.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(194, '2025-11-26 18:14:24.570696', 'SALIDA_VENTA', 2, 615, 613, 'Venta en pedido #78', 78, 7700000000003, 33350.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(195, '2025-11-26 18:14:24.576143', 'SALIDA_VENTA', 1, 3, 2, 'Venta en pedido #78', 78, 7700000000033, 20700.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 81),
(196, '2025-11-26 18:15:11.980906', 'SALIDA_VENTA', 2, 50, 48, 'Venta en pedido #79', 79, 7700000000013, 18400.00, 0.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(197, '2025-11-26 18:16:30.110636', 'SALIDA_VENTA', 2, 20, 18, 'Venta en pedido #80', 80, 7700000000042, 17250.00, 0.00, 'L2025-11', '2028-01-01', NULL, NULL, 83),
(198, '2025-11-26 18:20:12.905115', 'SALIDA_VENTA', 1, 10, 9, 'Venta en pedido #81', 81, 7700000000032, 16100.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(199, '2025-11-26 18:20:12.908655', 'SALIDA_VENTA', 1, 2, 1, 'Venta en pedido #81', 81, 7700000000033, 20700.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 81),
(200, '2025-11-26 18:25:08.968053', 'SALIDA_VENTA', 1, 387, 386, 'Venta en pedido #82', 82, 7700000000002, 36800.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(201, '2025-11-26 18:25:08.968053', 'SALIDA_VENTA', 1, 1, 0, 'Venta en pedido #82', 82, 7700000000033, 20700.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 81),
(202, '2025-11-26 18:29:41.553601', 'AJUSTE_MANUAL_ENTRADA', 1, 0, 1, 'prueba', NULL, 7700000000033, 18000.00, 18000.00, 'L2025-11', '2025-11-26', 21420.00, 3420.00, NULL),
(203, '2025-11-26 18:37:18.604822', 'SALIDA_VENTA', 1, 130, 129, 'Venta en pedido #83 - Sin lotes disponibles', 83, 7700000000023, 20700.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 72),
(204, '2025-11-26 18:37:18.622826', 'SALIDA_VENTA', 1, 3, 2, 'Venta en pedido #83 - Sin lotes disponibles', 83, 7700000000024, 17250.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, NULL),
(205, '2025-11-26 18:56:42.100283', 'AJUSTE_MANUAL_ENTRADA', 1, 129, 130, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-11-26', 21420.00, 3420.00, NULL),
(206, '2025-11-26 18:56:59.975376', 'AJUSTE_MANUAL_ENTRADA', 1, 130, 131, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-11-26', 21420.00, 3420.00, NULL),
(207, '2025-11-26 18:57:19.887720', 'AJUSTE_MANUAL_SALIDA', 1, 131, 130, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-11-26', NULL, NULL, 72),
(208, '2025-11-26 18:59:19.281629', 'AJUSTE_MANUAL_ENTRADA', 2, 11, 13, 'prueba', NULL, 7709876543220, 15000.00, 15000.00, 'L2025-11', '2025-11-26', 35700.00, 5700.00, NULL),
(209, '2025-11-26 19:07:54.886932', 'AJUSTE_MANUAL_ENTRADA', 1, 329, 330, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 69020.00, 11020.00, NULL),
(210, '2025-11-26 19:07:54.886932', 'AJUSTE_MANUAL_ENTRADA', 1, 191, 192, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BLG-02 | Vencimiento: 2027-12-02 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BLG-02', '2027-12-02', 65450.00, 10450.00, NULL),
(211, '2025-11-26 19:07:54.906066', 'AJUSTE_MANUAL_ENTRADA', 1, 613, 614, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-CLS-03 | Vencimiento: 2027-12-03 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L-CLS-03', '2027-12-03', 34510.00, 5510.00, NULL),
(212, '2025-11-26 19:07:54.913849', 'AJUSTE_MANUAL_ENTRADA', 1, 386, 387, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-IPG-04 | Vencimiento: 2027-12-04 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L-IPG-04', '2027-12-04', 38080.00, 6080.00, NULL),
(213, '2025-11-26 19:07:54.921568', 'AJUSTE_MANUAL_ENTRADA', 1, 522, 523, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-05 | Vencimiento: 2027-12-05 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L-PCMG-05', '2027-12-05', 45220.00, 7220.00, NULL),
(214, '2025-11-26 19:07:54.928118', 'AJUSTE_MANUAL_ENTRADA', 1, 466, 467, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-06 | Vencimiento: 2027-12-06 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L-PCMG-06', '2027-12-06', 40460.00, 6460.00, NULL),
(215, '2025-11-26 19:11:52.364745', 'AJUSTE_MANUAL_ENTRADA', 1, 330, 331, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 69020.00, 11020.00, NULL),
(216, '2025-11-26 19:11:52.366195', 'AJUSTE_MANUAL_ENTRADA', 1, 192, 193, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BLG-02 | Vencimiento: 2027-12-02 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BLG-02', '2027-12-02', 65450.00, 10450.00, NULL),
(217, '2025-11-26 19:11:52.383557', 'AJUSTE_MANUAL_ENTRADA', 1, 614, 615, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-CLS-03 | Vencimiento: 2027-12-03 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L-CLS-03', '2027-12-03', 34510.00, 5510.00, NULL),
(218, '2025-11-26 19:11:52.393258', 'AJUSTE_MANUAL_ENTRADA', 1, 387, 388, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-IPG-04 | Vencimiento: 2027-12-04 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L-IPG-04', '2027-12-04', 38080.00, 6080.00, NULL),
(219, '2025-11-26 19:11:52.402282', 'AJUSTE_MANUAL_ENTRADA', 1, 523, 524, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-05 | Vencimiento: 2027-12-05 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L-PCMG-05', '2027-12-05', 45220.00, 7220.00, NULL),
(220, '2025-11-26 19:11:52.411251', 'AJUSTE_MANUAL_ENTRADA', 1, 467, 468, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-06 | Vencimiento: 2027-12-06 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L-PCMG-06', '2027-12-06', 40460.00, 6460.00, NULL),
(221, '2025-11-26 19:14:44.746064', 'AJUSTE_MANUAL_ENTRADA', 1, 331, 332, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 69020.00, 11020.00, NULL),
(222, '2025-11-26 19:14:44.768131', 'AJUSTE_MANUAL_ENTRADA', 1, 193, 194, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BLG-02 | Vencimiento: 2027-12-02 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BLG-02', '2027-12-02', 65450.00, 10450.00, NULL),
(223, '2025-11-26 19:14:44.775401', 'AJUSTE_MANUAL_ENTRADA', 1, 615, 616, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-CLS-03 | Vencimiento: 2027-12-03 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L-CLS-03', '2027-12-03', 34510.00, 5510.00, NULL),
(224, '2025-11-26 19:14:44.784124', 'AJUSTE_MANUAL_ENTRADA', 1, 388, 389, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-IPG-04 | Vencimiento: 2027-12-04 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L-IPG-04', '2027-12-04', 38080.00, 6080.00, NULL),
(225, '2025-11-26 19:14:44.793217', 'AJUSTE_MANUAL_ENTRADA', 1, 524, 525, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-05 | Vencimiento: 2027-12-05 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L-PCMG-05', '2027-12-05', 45220.00, 7220.00, NULL),
(226, '2025-11-26 19:14:44.801312', 'AJUSTE_MANUAL_ENTRADA', 1, 468, 469, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-06 | Vencimiento: 2027-12-06 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L-PCMG-06', '2027-12-06', 40460.00, 6460.00, NULL),
(227, '2025-11-26 19:14:44.809310', 'AJUSTE_MANUAL_ENTRADA', 1, 13, 14, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-PCMG-07 | Vencimiento: 2027-12-07 00:00:00 | Total con IVA: $17,850 | IVA: $2,850', NULL, 7709876543220, 15000.00, 15000.00, 'L-PCMG-07', '2027-12-07', 17850.00, 2850.00, NULL),
(228, '2025-11-26 19:25:39.093686', 'AJUSTE_MANUAL_ENTRADA', 10, 2, 12, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-11', '2025-11-26', 178500.00, 28500.00, NULL),
(229, '2025-11-26 19:26:40.336584', 'AJUSTE_MANUAL_ENTRADA', 20, 1, 21, 'prueba', NULL, 7700000000033, 18000.00, 18000.00, 'L2025-11', '2025-11-26', 428400.00, 68400.00, NULL),
(230, '2025-11-26 19:27:00.230561', 'AJUSTE_MANUAL_ENTRADA', 10, 21, 31, 'prueba', NULL, 7700000000033, 18000.00, 18000.00, 'L2025-12', '2025-11-26', 214200.00, 34200.00, NULL),
(231, '2025-11-29 22:51:18.080350', 'SALIDA_VENTA', 2, 9, 7, 'Venta en pedido #84', 84, 7700000000032, 14000.00, 14000.00, 'L2025-11', '2027-11-01', NULL, NULL, 80),
(232, '2025-11-29 22:51:18.095479', 'SALIDA_VENTA', 2, 31, 29, 'Venta en pedido #84', 84, 7700000000033, 18000.00, 18000.00, 'L2025-11', '2025-11-26', NULL, NULL, 81),
(233, '2025-11-29 22:51:46.845577', 'SALIDA_VENTA', 2, 130, 128, 'Venta en pedido #85', 85, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-11-26', NULL, NULL, 72),
(234, '2025-11-29 22:51:46.853989', 'SALIDA_VENTA', 2, 12, 10, 'Venta en pedido #85', 85, 7700000000024, 15000.00, 15000.00, 'L2025-11', '2025-11-26', NULL, NULL, 99),
(235, '2025-11-29 22:52:36.594670', 'SALIDA_VENTA', 2, 4, 2, 'Venta en pedido #86 - Sin lotes disponibles', 86, 7700000000031, 13800.00, 0.00, NULL, NULL, NULL, NULL, NULL),
(236, '2025-11-29 22:54:05.840936', 'SALIDA_VENTA', 2, 13, 11, 'Venta en pedido #87', 87, 7700000000021, 22000.00, 22000.00, 'L2025-11', '2027-11-01', NULL, NULL, 71),
(237, '2025-11-29 22:55:30.693562', 'SALIDA_VENTA', 1, 469, 468, 'Venta en pedido #88', 88, 7700000000001, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 1),
(238, '2025-11-29 22:55:30.693562', 'SALIDA_VENTA', 1, 14, 13, 'Venta en pedido #88', 88, 7709876543220, 15000.00, 15000.00, 'L2025-11', '2025-11-26', NULL, NULL, 96),
(239, '2025-11-29 22:56:18.826936', 'SALIDA_VENTA', 2, 18, 16, 'Venta en pedido #89', 89, 7700000000042, 15000.00, 15000.00, 'L2025-11', '2028-01-01', NULL, NULL, 83),
(240, '2025-11-29 22:58:11.430031', 'SALIDA_VENTA', 1, 29, 28, 'Venta en pedido #90', 90, 7700000000033, 18000.00, 18000.00, 'L2025-11', '2025-11-26', NULL, NULL, 81),
(241, '2025-11-29 22:58:11.476696', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #90 - Sin lotes disponibles', 90, 7700000000034, 17250.00, 0.00, NULL, NULL, NULL, NULL, NULL),
(242, '2025-11-29 23:00:29.072204', 'SALIDA_VENTA', 1, 48, 47, 'Venta en pedido #91', 91, 7700000000013, 16000.00, 16000.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(243, '2025-11-29 23:00:29.072204', 'SALIDA_VENTA', 1, 38, 37, 'Venta en pedido #91', 91, 7700000000014, 20000.00, 20000.00, 'L2025-11', '2027-11-01', NULL, NULL, 70);
INSERT INTO "movimientos_producto" ("idMovimiento", "fecha", "tipo_movimiento", "cantidad", "stock_anterior", "stock_nuevo", "descripcion", "idPedido", "producto_id", "precio_unitario", "costo_unitario", "lote", "fecha_vencimiento", "total_con_iva", "iva", "lote_origen_id") VALUES
(244, '2025-11-29 23:12:01.493423', 'SALIDA_VENTA', 1, 389, 388, 'Venta en pedido #92', 92, 7700000000002, 0.00, 0.00, 'L2025-11', '2027-11-01', NULL, NULL, 16),
(245, '2025-11-29 23:12:01.511134', 'SALIDA_VENTA', 1, 616, 615, 'Venta en pedido #92', 92, 7700000000003, 29000.00, 29000.00, 'L2025-11', '2027-11-01', NULL, NULL, 28),
(246, '2025-11-30 00:06:57.879385', 'SALIDA_VENTA', 1, 5, 4, 'Venta en pedido #93 - Sin lotes disponibles', 93, 7701122334455, 5750.00, 0.00, NULL, NULL, NULL, NULL, NULL),
(247, '2025-11-30 00:06:57.888630', 'SALIDA_VENTA', 2, 128, 126, 'Venta en pedido #93', 93, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-11-26', NULL, NULL, 72),
(248, '2025-11-30 00:33:06.667869', 'AJUSTE_MANUAL_ENTRADA', 1, 332, 333, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 69020.00, 11020.00, NULL),
(249, '2025-11-30 00:33:06.678707', 'AJUSTE_MANUAL_ENTRADA', 1, 194, 195, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2027-12-02 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BLG-02', '2027-12-02', 65450.00, 10450.00, NULL),
(250, '2025-11-30 00:33:06.689874', 'AJUSTE_MANUAL_ENTRADA', 1, 615, 616, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-12-03 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L-CLS-03', '2027-12-03', 34510.00, 5510.00, NULL),
(251, '2025-11-30 00:33:06.698913', 'AJUSTE_MANUAL_ENTRADA', 1, 388, 389, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2027-12-04 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L-IPG-04', '2027-12-04', 38080.00, 6080.00, NULL),
(252, '2025-11-30 00:33:06.710075', 'AJUSTE_MANUAL_ENTRADA', 1, 525, 526, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2027-12-05 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L-PCMG-05', '2027-12-05', 45220.00, 7220.00, NULL),
(253, '2025-11-30 00:33:06.721234', 'AJUSTE_MANUAL_ENTRADA', 1, 468, 469, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-06 | Vencimiento: 2027-12-06 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L-PCMG-06', '2027-12-06', 40460.00, 6460.00, NULL),
(254, '2025-11-30 00:33:06.731344', 'AJUSTE_MANUAL_ENTRADA', 1, 13, 14, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-07 | Vencimiento: 2027-12-07 00:00:00 | Total con IVA: $17,850 | IVA: $2,850', NULL, 7709876543220, 15000.00, 15000.00, 'L-PCMG-07', '2027-12-07', 17850.00, 2850.00, NULL),
(255, '2025-11-30 00:34:25.525053', 'AJUSTE_MANUAL_ENTRADA', 1, 333, 334, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $69,020 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 69020.00, 11020.00, NULL),
(256, '2025-11-30 00:34:25.533227', 'AJUSTE_MANUAL_ENTRADA', 1, 195, 196, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-BLG-02 | Vencimiento: 2027-12-02 00:00:00 | Total con IVA: $65,450 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BLG-02', '2027-12-02', 65450.00, 10450.00, NULL),
(257, '2025-11-30 00:34:25.542386', 'AJUSTE_MANUAL_ENTRADA', 1, 616, 617, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-CLS-03 | Vencimiento: 2027-12-03 00:00:00 | Total con IVA: $34,510 | IVA: $5,510', NULL, 7700000000003, 29000.00, 29000.00, 'L-CLS-03', '2027-12-03', 34510.00, 5510.00, NULL),
(258, '2025-11-30 00:34:25.553619', 'AJUSTE_MANUAL_ENTRADA', 1, 389, 390, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-IPG-04 | Vencimiento: 2027-12-04 00:00:00 | Total con IVA: $38,080 | IVA: $6,080', NULL, 7700000000002, 32000.00, 32000.00, 'L-IPG-04', '2027-12-04', 38080.00, 6080.00, NULL),
(259, '2025-11-30 00:34:25.564047', 'AJUSTE_MANUAL_ENTRADA', 1, 526, 527, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-05 | Vencimiento: 2027-12-05 00:00:00 | Total con IVA: $45,220 | IVA: $7,220', NULL, 7700000000004, 38000.00, 38000.00, 'L-PCMG-05', '2027-12-05', 45220.00, 7220.00, NULL),
(260, '2025-11-30 00:34:25.571897', 'AJUSTE_MANUAL_ENTRADA', 1, 469, 470, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-06 | Vencimiento: 2027-12-06 00:00:00 | Total con IVA: $40,460 | IVA: $6,460', NULL, 7700000000001, 34000.00, 34000.00, 'L-PCMG-06', '2027-12-06', 40460.00, 6460.00, NULL),
(261, '2025-11-30 00:34:25.581297', 'AJUSTE_MANUAL_ENTRADA', 2, 14, 16, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central  | Lote: L-PCMG-07 | Vencimiento: 2027-12-07 00:00:00 | Total con IVA: $32,850 | IVA: $2,850', NULL, 7709876543220, 15000.00, 15000.00, 'L-PCMG-07', '2027-12-07', 32850.00, 2850.00, NULL),
(262, '2025-11-30 00:35:24.672179', 'AJUSTE_MANUAL_ENTRADA', 10, 2, 12, 'prueba', NULL, 7700000000031, 12000.00, 12000.00, 'L2025-11', '2025-12-25', 142800.00, 22800.00, NULL),
(263, '2025-11-30 00:44:22.643876', 'SALIDA_VENTA', 1, 126, 125, 'Venta en pedido #94', 94, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-11-26', NULL, NULL, 72),
(264, '2025-11-30 00:44:22.651805', 'SALIDA_VENTA', 1, 10, 9, 'Venta en pedido #94', 94, 7700000000024, 15000.00, 15000.00, 'L2025-11', '2025-11-26', NULL, NULL, 99),
(265, '2025-11-30 00:44:22.668360', 'SALIDA_VENTA', 1, 4, 3, 'Venta en pedido #94 - Sin lotes disponibles', 94, 7700000000025, 34500.00, 0.00, NULL, NULL, NULL, NULL, NULL),
(266, '2025-11-30 00:44:50.384024', 'SALIDA_VENTA', 1, 101, 100, 'Venta en pedido #95', 95, 7700000000012, 18000.00, 18000.00, 'L2025-11', '2027-11-01', NULL, NULL, 66),
(267, '2025-11-30 00:44:50.384024', 'SALIDA_VENTA', 1, 47, 46, 'Venta en pedido #95', 95, 7700000000013, 16000.00, 16000.00, 'L2025-11', '2026-11-01', NULL, NULL, 68),
(268, '2025-11-30 00:49:06.984873', 'AJUSTE_MANUAL_ENTRADA', 10, 3, 13, 'prueba', NULL, 7700000000025, 30000.00, 30000.00, 'L2025-12', '2025-12-10', 357000.00, 57000.00, NULL),
(269, '2025-11-30 00:49:44.630519', 'AJUSTE_MANUAL_ENTRADA', 100, 3, 103, 'prueba', NULL, 7700000000035, 5000.00, 5000.00, 'L2025-15', '2026-01-16', 595000.00, 95000.00, NULL),
(270, '2025-11-30 00:50:09.954105', 'AJUSTE_MANUAL_ENTRADA', 5, 4, 9, 'prueba', NULL, 7700000000034, 15000.00, 15000.00, 'L2025-10', '2025-11-30', 89250.00, 14250.00, NULL),
(271, '2025-11-30 00:51:48.912128', 'AJUSTE_MANUAL_ENTRADA', 12, 9, 21, 'prueba', NULL, 7700000000034, 15000.00, 15000.00, 'L2025-10', '2025-12-01', 214200.00, 34200.00, NULL),
(272, '2025-11-30 00:52:22.167870', 'AJUSTE_MANUAL_ENTRADA', 10, 4, 14, 'prueba', NULL, 7700000000044, 28000.00, 28000.00, 'L2025-15', '2025-11-30', 333200.00, 53200.00, NULL),
(273, '2025-11-30 00:58:55.672302', 'PERDIDA_VENCIMIENTO', 120, 125, 5, 'Pérdida por vencimiento - Lote L2025-11', NULL, 7700000000023, 0.00, 0.00, NULL, NULL, NULL, NULL, 72),
(274, '2025-11-30 00:58:55.698309', 'PERDIDA_VENCIMIENTO', 17, 28, 11, 'Pérdida por vencimiento - Lote L2025-11', NULL, 7700000000033, 0.00, 0.00, NULL, NULL, NULL, NULL, 81),
(275, '2025-11-30 00:58:55.713785', 'PERDIDA_VENCIMIENTO', 10, 16, 6, 'Pérdida por vencimiento - Lote L2025-11', NULL, 7709876543220, 0.00, 0.00, NULL, NULL, NULL, NULL, 96),
(276, '2025-11-30 00:58:55.728262', 'PERDIDA_VENCIMIENTO', 7, 9, 2, 'Pérdida por vencimiento - Lote L2025-11', NULL, 7700000000024, 0.00, 0.00, NULL, NULL, NULL, NULL, 99),
(277, '2025-11-30 00:58:55.742403', 'PERDIDA_VENCIMIENTO', 10, 11, 1, 'Pérdida por vencimiento - Lote L2025-12', NULL, 7700000000033, 0.00, 0.00, NULL, NULL, NULL, NULL, 100),
(278, '2025-11-30 00:59:52.375621', 'AJUSTE_MANUAL_ENTRADA', 10, 1, 11, 'prueba', NULL, 7700000000033, 18000.00, 18000.00, 'L2025-10', '2025-11-29', 214200.00, 34200.00, NULL),
(279, '2025-11-30 01:01:51.419191', 'AJUSTE_MANUAL_ENTRADA', 12, 2, 14, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-15', '2025-11-04', 214200.00, 34200.00, NULL),
(280, '2025-11-30 01:02:00.185279', 'PERDIDA_VENCIMIENTO', 12, 14, 2, 'Pérdida por vencimiento - Lote L2025-15', NULL, 7700000000024, 0.00, 0.00, NULL, NULL, NULL, NULL, 107),
(281, '2025-11-30 01:02:26.801969', 'AJUSTE_MANUAL_ENTRADA', 10, 2, 12, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-10', '2025-11-28', 178500.00, 28500.00, NULL),
(282, '2025-11-30 01:02:52.132873', 'AJUSTE_MANUAL_ENTRADA', 20, 12, 32, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-12', '2025-11-27', 357000.00, 57000.00, NULL),
(283, '2025-11-30 01:03:03.473635', 'PERDIDA_VENCIMIENTO', 10, 32, 22, 'Pérdida por vencimiento - Lote L2025-10', NULL, 7700000000024, 0.00, 0.00, NULL, NULL, NULL, NULL, 108),
(284, '2025-11-30 01:03:03.485196', 'PERDIDA_VENCIMIENTO', 20, 22, 2, 'Pérdida por vencimiento - Lote L2025-12', NULL, 7700000000024, 0.00, 0.00, NULL, NULL, NULL, NULL, 109),
(285, '2025-11-30 01:05:04.014937', 'AJUSTE_MANUAL_ENTRADA', 10, 2, 12, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-12', '2025-11-29', 178500.00, 28500.00, NULL),
(286, '2025-11-30 01:05:18.898509', 'AJUSTE_MANUAL_ENTRADA', 10, 12, 22, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-15', '2025-11-19', 178500.00, 28500.00, NULL),
(287, '2025-11-30 01:05:38.305304', 'AJUSTE_MANUAL_ENTRADA', 100, 22, 122, 'prueba', NULL, 7700000000024, 15000.00, 15000.00, 'L2025-15', '2025-12-31', 1785000.00, 285000.00, NULL),
(288, '2025-11-30 01:06:03.546333', 'AJUSTE_MANUAL_ENTRADA', 10, 4, 14, 'prueba', NULL, 7701122334455, 5000.00, 5000.00, 'L2025-12', '2025-11-28', 59500.00, 9500.00, NULL),
(289, '2025-11-30 01:06:20.413548', 'AJUSTE_MANUAL_ENTRADA', 20, 14, 34, 'prueba', NULL, 7701122334455, 5000.00, 5000.00, 'L2025-11', '2025-11-19', 119000.00, 19000.00, NULL),
(290, '2025-11-30 01:07:04.467336', 'AJUSTE_MANUAL_ENTRADA', 50, 34, 84, 'prueba', NULL, 7701122334455, 5000.00, 5000.00, 'L2025-10', '2026-01-16', 297500.00, 47500.00, NULL),
(291, '2025-11-30 01:07:39.276398', 'AJUSTE_MANUAL_ENTRADA', 20, 5, 25, 'prueba', NULL, 7700000000015, 25000.00, 25000.00, 'L2025-15', '2025-11-21', 595000.00, 95000.00, NULL),
(292, '2025-11-30 01:07:59.078804', 'AJUSTE_MANUAL_ENTRADA', 20, 25, 45, 'prueba', NULL, 7700000000015, 25000.00, 25000.00, 'L2025-10', '2026-01-09', 595000.00, 95000.00, NULL),
(293, '2025-11-30 01:08:50.531167', 'AJUSTE_MANUAL_ENTRADA', 20, 5, 25, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-11', '2025-12-01', 428400.00, 68400.00, NULL),
(294, '2025-11-30 01:09:08.148228', 'AJUSTE_MANUAL_ENTRADA', 15, 25, 40, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-12', '2025-11-01', 321300.00, 51300.00, NULL),
(295, '2025-11-30 01:09:26.177992', 'AJUSTE_MANUAL_ENTRADA', 20, 40, 60, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-10', '2026-01-16', 428400.00, 68400.00, NULL),
(296, '2025-11-30 01:10:03.200834', 'AJUSTE_MANUAL_ENTRADA', 50, 5, 55, 'prueba', NULL, 7700000000045, 35000.00, 35000.00, 'L2025-15', '2025-12-27', 2082500.00, 332500.00, NULL),
(297, '2025-11-30 01:10:29.760952', 'AJUSTE_MANUAL_ENTRADA', 10, 5, 15, 'prueba', NULL, 7709876543210, 15000.00, 15000.00, 'L2025-10', '2025-12-01', 178500.00, 28500.00, NULL),
(298, '2025-11-30 01:11:05.845641', 'AJUSTE_MANUAL_SALIDA', 10, 60, 50, 'prueba', NULL, 7700000000023, 18000.00, 18000.00, 'L2025-10', '2026-01-16', NULL, NULL, 116),
(299, '2025-12-10 16:21:10.712138', 'SALIDA_VENTA', 1, 390, 389, 'Pedido #96 - Venta (apartado) - Lote L2025-11', 96, 7700000000002, 40350.00, 0.00, 'L2025-11', '2027-11-01', 40350.00, 0.00, 16),
(300, '2025-12-10 16:21:10.728557', 'SALIDA_VENTA', 1, 617, 616, 'Pedido #96 - Venta (apartado) - Lote L2025-11', 96, 7700000000003, 36600.00, 29000.00, 'L2025-11', '2027-11-01', 36600.00, 5510.00, 28),
(301, '2025-12-10 16:24:19.169394', 'SALIDA_VENTA', 1, 470, 469, 'Pedido #97 - Venta (apartado) - Lote L2025-11', 97, 7700000000001, 42900.00, 0.00, 'L2025-11', '2027-11-01', 42900.00, 0.00, 1),
(302, '2025-12-10 16:24:19.180862', 'SALIDA_VENTA', 1, 389, 388, 'Pedido #97 - Venta (apartado) - Lote L2025-11', 97, 7700000000002, 40350.00, 0.00, 'L2025-11', '2027-11-01', 40350.00, 0.00, 16),
(303, '2025-12-10 17:46:24.758221', 'SALIDA_VENTA', 1, 388, 387, 'Pedido #98 - Venta (apartado) - Lote L2025-11', 98, 7700000000002, 40350.00, 0.00, 'L2025-11', '2027-11-01', 40350.00, 0.00, 16),
(304, '2025-12-10 17:46:24.774289', 'SALIDA_VENTA', 1, 616, 615, 'Pedido #98 - Venta (apartado) - Lote L2025-11', 98, 7700000000003, 36600.00, 29000.00, 'L2025-11', '2027-11-01', 36600.00, 5510.00, 28),
(305, '2025-12-10 17:46:24.790199', 'SALIDA_VENTA', 1, 527, 526, 'Pedido #98 - Venta (apartado) - Lote L2025-11', 98, 7700000000004, 47950.00, 0.00, 'L2025-11', '2027-11-01', 47950.00, 0.00, 40),
(306, '2025-12-10 17:46:24.806082', 'SALIDA_VENTA', 1, 103, 102, 'Pedido #98 - Venta (apartado) - Lote L2025-15', 98, 7700000000035, 6300.00, 5000.00, 'L2025-15', '2026-01-16', 6300.00, 950.00, 103),
(307, '2025-12-10 17:48:36.855992', 'SALIDA_VENTA', 1, 122, 121, 'Pedido #99 - Venta (apartado) - Lote L2025-15', 99, 7700000000024, 18900.00, 15000.00, 'L2025-15', '2025-12-31', 18900.00, 2850.00, 107),
(308, '2025-12-10 17:48:36.872557', 'SALIDA_VENTA', 1, 50, 49, 'Pedido #99 - Venta (apartado) - Lote L2025-11', 99, 7700000000023, 23550.00, 18000.00, 'L2025-11', '2025-12-01', 23550.00, 3420.00, 72),
(309, '2025-12-10 17:48:36.891182', 'SALIDA_VENTA', 2, 20, 18, 'Pedido #99 - Venta (apartado) - Lote L2025-11', 99, 7700000000043, 15150.00, 12000.00, 'L2025-11', '2028-01-01', 30300.00, 4560.00, 84),
(310, '2025-12-10 17:48:38.321756', 'SALIDA_VENTA', 1, 121, 120, 'Pedido #100 - Venta (apartado) - Lote L2025-15', 100, 7700000000024, 19650.00, 15000.00, 'L2025-15', '2025-12-31', 19650.00, 2850.00, 107),
(311, '2025-12-10 17:48:38.349434', 'SALIDA_VENTA', 1, 49, 48, 'Pedido #100 - Venta (apartado) - Lote L2025-11', 100, 7700000000023, 23550.00, 18000.00, 'L2025-11', '2025-12-01', 23550.00, 3420.00, 72),
(312, '2025-12-10 17:48:38.365852', 'SALIDA_VENTA', 2, 18, 16, 'Pedido #100 - Venta (apartado) - Lote L2025-11', 100, 7700000000043, 15700.00, 12000.00, 'L2025-11', '2028-01-01', 31400.00, 4560.00, 84),
(313, '2025-12-10 17:50:36.398665', 'SALIDA_VENTA', 1, 120, 119, 'Pedido #101 - Venta (apartado) - Lote L2025-15', 101, 7700000000024, 19650.00, 15000.00, 'L2025-15', '2025-12-31', 19650.00, 2850.00, 107),
(314, '2025-12-10 17:50:36.411385', 'SALIDA_VENTA', 1, 48, 47, 'Pedido #101 - Venta (apartado) - Lote L2025-11', 101, 7700000000023, 23550.00, 18000.00, 'L2025-11', '2025-12-01', 23550.00, 3420.00, 72),
(315, '2025-12-10 17:50:37.667753', 'SALIDA_VENTA', 1, 119, 118, 'Pedido #102 - Venta (apartado) - Lote L2025-15', 102, 7700000000024, 19650.00, 15000.00, 'L2025-15', '2025-12-31', 19650.00, 2850.00, 107),
(316, '2025-12-10 17:50:37.685938', 'SALIDA_VENTA', 1, 47, 46, 'Pedido #102 - Venta (apartado) - Lote L2025-11', 102, 7700000000023, 23550.00, 18000.00, 'L2025-11', '2025-12-01', 23550.00, 3420.00, 72),
(317, '2025-12-10 18:15:12.621581', 'AJUSTE_MANUAL_ENTRADA', 10, 6, 16, 'prueba', NULL, 7709876543220, 15000.00, 15000.00, 'L2025-15', '2026-06-25', 178500.00, 28500.00, NULL),
(318, '2025-12-10 18:16:30.059933', 'SALIDA_VENTA', 1, 100, 99, 'Pedido #103 - Venta (apartado) - Lote L2025-11', 103, 7700000000012, 23350.00, 18000.00, 'L2025-11', '2027-11-01', 23350.00, 3420.00, 66),
(319, '2025-12-10 18:16:30.073928', 'SALIDA_VENTA', 1, 46, 45, 'Pedido #103 - Venta (apartado) - Lote L2025-11', 103, 7700000000013, 20750.00, 16000.00, 'L2025-11', '2026-11-01', 20750.00, 3040.00, 68),
(320, '2025-12-10 18:16:30.102840', 'SALIDA_VENTA', 2, 7, 5, 'Pedido #103 - Venta (apartado) - Lote L2025-11', 103, 7700000000032, 18150.00, 14000.00, 'L2025-11', '2027-11-01', 36300.00, 5320.00, 80),
(321, '2025-12-10 18:32:29.560210', 'SALIDA_VENTA', 1, 118, 117, 'Pedido #104 - Venta (apartado) - Lote L2025-15', 104, 7700000000024, 19450.00, 15000.00, 'L2025-15', '2025-12-31', 19450.00, 2850.00, 107),
(322, '2025-12-10 18:32:29.576053', 'SALIDA_VENTA', 1, 16, 15, 'Pedido #104 - Venta (apartado) - Lote L2025-11', 104, 7700000000042, 19450.00, 15000.00, 'L2025-11', '2028-01-01', 19450.00, 2850.00, 83),
(323, '2025-12-10 19:04:26.186382', 'AJUSTE_MANUAL_ENTRADA', 10, 0, 10, 'prueba', NULL, 7709876543221, 8500.00, 8500.00, 'L2025-10', '2026-09-25', 101150.00, 16150.00, NULL),
(324, '2025-12-10 19:05:36.455918', 'SALIDA_VENTA', 2, 10, 8, 'Pedido #105 - Venta (apartado) - Lote L2025-10', 105, 7709876543221, 11050.00, 8500.00, 'L2025-10', '2026-09-25', 22100.00, 3230.00, 120),
(325, '2025-12-10 19:05:36.472517', 'SALIDA_VENTA', 1, 12, 11, 'Pedido #105 - Venta (apartado) - Lote L2025-11', 105, 7700000000031, 15550.00, 12000.00, 'L2025-11', '2025-12-25', 15550.00, 2280.00, 101),
(326, '2025-12-10 19:26:05.454377', 'SALIDA_VENTA', 2, 46, 44, 'Pedido #106 - Venta (apartado) - Lote L2025-11', 106, 7700000000023, 23350.00, 18000.00, 'L2025-11', '2025-12-01', 46700.00, 6840.00, 72),
(327, '2025-12-10 19:26:05.479639', 'SALIDA_VENTA', 1, 102, 101, 'Pedido #106 - Venta (apartado) - Lote L2025-15', 106, 7700000000035, 6500.00, 5000.00, 'L2025-15', '2026-01-16', 6500.00, 950.00, 103),
(328, '2025-12-10 20:37:43.353657', 'AJUSTE_MANUAL_ENTRADA', 2, 334, 336, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BCG-01 | Vencimiento: 2027-12-01 00:00:00 | Total con IVA: $116,000 | IVA: $11,020', NULL, 7700000000005, 58000.00, 58000.00, 'L-BCG-01', '2027-12-01', 116000.19, 11020.00, NULL),
(329, '2025-12-10 20:37:43.370178', 'AJUSTE_MANUAL_ENTRADA', 2, 196, 198, 'Reabastecimiento desde Excel - Rostro | Proveedor: Proveedor Central tt | Lote: L-BCG-02 | Vencimiento: 2027-12-02 00:00:00 | Total con IVA: $110,000 | IVA: $10,450', NULL, 7701234567890, 55000.00, 55000.00, 'L-BCG-02', '2027-12-02', 110000.19, 10450.00, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "notificaciones_problema"
--

CREATE TABLE "notificaciones_problema" (
  "idNotificacion" integer NOT NULL,
  "motivo" longtext NOT NULL,
  "foto" character varying(100) DEFAULT NULL,
  "fechaReporte" datetime(6) NOT NULL,
  "leida" smallint NOT NULL,
  "idPedido" integer NOT NULL,
  "fecha_respuesta" datetime(6) DEFAULT NULL,
  "respuesta_admin" longtext DEFAULT NULL
);

--
-- Volcado de datos para la tabla "notificaciones_problema"
--

INSERT INTO "notificaciones_problema" ("idNotificacion", "motivo", "foto", "fechaReporte", "leida", "idPedido", "fecha_respuesta", "respuesta_admin") VALUES
(5, 'no recibi mi pedido', 'problemas_entrega/pinta_cejaz.avif', '2025-11-24 08:30:31.920104', 1, 36, '2025-11-24 08:54:53.131555', 'lo sentimis muvho'),
(6, 'no recibi mi pedido', 'problemas_entrega/p.webp', '2025-11-24 13:03:29.320505', 1, 37, '2025-11-24 13:05:02.104185', 'lamentamos los inconvenientes nos contactaremos contigo por correo para hacer el reembolso de tu pedido'),
(7, 'no lo recibi', 'problemas_entrega/la.jpg', '2025-11-26 17:15:03.008365', 1, 52, '2025-11-26 17:17:40.491761', 'lamentamos las molestias nos comunicaremos con usted para el reembolso '),
(8, 'no lo recibi', 'problemas_entrega/la_1kIXdJ4.jpg', '2025-11-26 17:30:59.747639', 0, 48, NULL, NULL),
(9, 'nn', '', '2025-11-26 17:40:15.292725', 0, 47, NULL, NULL),
(10, 'nn', '', '2025-11-26 17:44:01.627105', 0, 47, NULL, NULL),
(11, 'nn', '', '2025-11-26 17:44:33.814749', 0, 47, NULL, NULL),
(12, 'nn', '', '2025-11-26 17:45:42.795141', 0, 47, NULL, NULL),
(13, 'nn', '', '2025-11-26 17:46:07.585639', 0, 47, NULL, NULL),
(14, 'nn', '', '2025-11-26 17:49:17.562019', 1, 47, '2025-12-10 19:24:51.009213', 'lo sentimos mucho nos comunicaremos con ut por correo'),
(15, 'no', '', '2025-11-26 17:51:49.777328', 1, 47, '2025-12-10 19:24:13.260363', 'lo sentimos nos cumunicaremos contigo por correo'),
(16, 'no recibi mi pedido', 'problemas_entrega/uñas.webp', '2025-11-30 00:24:35.943864', 1, 40, '2025-11-30 00:25:35.223652', 'lo sentimos mucho nos cominicaremos contigo despues');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "notificaciones_reporte"
--

CREATE TABLE "notificaciones_reporte" (
  "idNotificacion" integer NOT NULL,
  "titulo" character varying(255) NOT NULL,
  "contenido_html" longtext NOT NULL,
  "tipo" character varying(50) NOT NULL,
  "fechaCreacion" datetime(6) NOT NULL,
  "leida" smallint NOT NULL
);

--
-- Volcado de datos para la tabla "notificaciones_reporte"
--

INSERT INTO "notificaciones_reporte" ("idNotificacion", "titulo", "contenido_html", "tipo", "fechaCreacion", "leida") VALUES
(1, 'Reporte Dashboard - 29/11/2025', '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <style>\n                body { font-family: Arial, sans-serif; background-color: #fffafc; padding: 20px; }\n                .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }\n                h1 { color: #c2185b; border-bottom: 3px solid #f48fb1; padding-bottom: 10px; }\n                h2 { color: #ad1457; margin-top: 30px; margin-bottom: 15px; }\n                .stat-box { display: inline-block; background: #fce4ec; padding: 15px 25px; border-radius: 10px; margin: 8px; text-align: center; min-width: 120px; }\n                .stat-number { font-size: 1.8rem; font-weight: bold; color: #c2185b; }\n                .stat-label { color: #666; font-size: 0.85rem; }\n                table { width: 100%; border-collapse: collapse; margin: 15px 0; }\n                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #fce4ec; }\n                th { background: #fce4ec; color: #c2185b; }\n                .highlight { background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #fbc02d; }\n                .footer { text-align: center; color: #999; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fce4ec; }\n                .bar-container { margin: 8px 0; }\n                .bar-label { display: inline-block; width: 150px; font-size: 0.9rem; color: #333; }\n                .bar-wrapper { display: inline-block; width: calc(100% - 250px); background: #f5f5f5; border-radius: 5px; height: 25px; vertical-align: middle; }\n                .bar { height: 25px; border-radius: 5px; display: inline-block; }\n                .bar-value { display: inline-block; width: 80px; text-align: right; font-weight: bold; color: #c2185b; font-size: 0.9rem; }\n                .chart-vertical { display: flex; align-items: flex-end; justify-content: space-around; height: 200px; background: #fafafa; border-radius: 10px; padding: 20px 10px 10px 10px; margin: 15px 0; }\n                .chart-bar { display: flex; flex-direction: column; align-items: center; width: 12%; }\n                .chart-bar-fill { width: 100%; background: linear-gradient(180deg, #ec407a 0%, #f48fb1 100%); border-radius: 5px 5px 0 0; min-height: 5px; }\n                .chart-bar-label { font-size: 0.75rem; color: #666; margin-top: 8px; text-align: center; }\n                .chart-bar-value { font-size: 0.8rem; font-weight: bold; color: #c2185b; margin-bottom: 5px; }\n                .comparison-box { display: inline-block; background: white; padding: 15px 20px; border-radius: 10px; margin: 8px; border: 2px solid #f8bbd0; text-align: center; min-width: 180px; }\n                .comparison-title { font-size: 0.85rem; color: #666; margin-bottom: 5px; }\n                .comparison-value { font-size: 1.5rem; font-weight: bold; color: #c2185b; }\n                .comparison-change { font-size: 0.8rem; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block; }\n                .change-up { background: #e8f5e9; color: #2e7d32; }\n                .change-down { background: #ffebee; color: #c62828; }\n                .change-same { background: #f5f5f5; color: #666; }\n            </style>\n        </head>\n        <body>\n            <div class=\"container\">\n                <h1>Reporte Dashboard - Glam Store</h1>\n                <p style=\"color: #666;\">Generado el 29/11/2025 a las 22:24</p>\n                \n                <h2>Resumen General</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">28</div>\n                        <div class=\"stat-label\">Productos</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">12</div>\n                        <div class=\"stat-label\">Clientes</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">46</div>\n                        <div class=\"stat-label\">Pedidos Totales</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">$3,433,027</div>\n                        <div class=\"stat-label\">Ventas Totales</div>\n                    </div>\n                </div>\n                \n                <h2>Comparativa Semanal</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Nuevos Esta Semana</div>\n                        <div class=\"comparison-value\">6</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Activos Esta Semana</div>\n                        <div class=\"comparison-value\">7</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Esta Semana</div>\n                        <div class=\"comparison-value\">22</div>\n                        <div class=\"comparison-change\">\n                            $2,300,377 en ventas\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Este Mes</div>\n                        <div class=\"comparison-value\">46</div>\n                        <div class=\"comparison-change\">\n                            $3,433,027 en ventas\n                        </div>\n                    </div>\n                </div>\n                \n                <h2>Pedidos por Dia (Ultimos 7 dias)</h2>\n                <table>\n                    <tr>\n                        <th>Dia</th>\n                        <th>Pedidos</th>\n                        <th>Ventas</th>\n                        <th>Grafico</th>\n                    </tr>\n        \n                    <tr>\n                        <td style=\"font-weight: bold;\">Dom 23</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Lun 24</td>\n                        <td style=\"text-align: center;\">15</td>\n                        <td style=\"text-align: right;\">$1,686,262</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 100%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mar 25</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mie 26</td>\n                        <td style=\"text-align: center;\">7</td>\n                        <td style=\"text-align: right;\">$614,115</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 46%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Jue 27</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Vie 28</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Sab 29</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                </table>\n                \n                <h2>Ventas por Categoria</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Rostro</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 100%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$1,446,600</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Ojos</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 36%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$522,800</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Accesorios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 28%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$413,500</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Uñas</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 15%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$228,400</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Labios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 10%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$155,950</span>\n                </div>\n                \n                \n                <h2>Top 10 Productos Mas Vendidos</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">1. Delineador Liquido Precis</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 100%; background: #e91e63;\"></span>\n                    </span>\n                    <span class=\"bar-value\">13 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">2. Corrector Liquido Soft To</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #9c27b0;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">3. Iluminador Perla Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #673ab7;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">4. Rubor Rosado Glow</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #3f51b5;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">5. Esponja Blender Lavanda</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 53%; background: #2196f3;\"></span>\n                    </span>\n                    <span class=\"bar-value\">7 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">6. Pestañina Curvas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #00bcd4;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">7. Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #009688;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">8. Polvo Compacto Mate Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #4caf50;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">9. Tratamiento Fortalecedor</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #8bc34a;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">10. Sombra Cuarteto Rosa</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 30%; background: #cddc39;\"></span>\n                    </span>\n                    <span class=\"bar-value\">4 uds</span>\n                </div>\n            \n                \n                <h2>Inventario Bajo (Stock menor a 10)</h2>\n                <div style=\"background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;\">\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Kit Decoracion de Uñas</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 30%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">3 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Cremoso Fucsia Pop</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Rosa Pastel</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Organizador Acrilico Mini</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Sombra Liquida Glitter Po</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Glitter Champagne</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Espejo LED Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Pestañina Volumen Total G</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Mate Velvet Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 90%; background: #fbc02d;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #fbc02d;\">9 uds</span>\n                </div>\n            </div>\n                \n                <h2>Reabastecimientos Recientes (Ultima Semana)</h2>\n                <table>\n                    <tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Lote</th><th>Vencimiento</th></tr>\n        \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-12</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+20</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Delineador de Labios Coral Chic</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Bronceador trendy</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-07</td>\n                    <td>07/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Cushion Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BCG-01</td>\n                    <td>01/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Ultimos 15 Pedidos</h2>\n                <table>\n                    <tr><th>#</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr>\n        \n                <tr>\n                    <td>83</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$55,160</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:37</td>\n                </tr>\n            \n                <tr>\n                    <td>82</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$68,425</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:25</td>\n                </tr>\n            \n                <tr>\n                    <td>81</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:20</td>\n                </tr>\n            \n                <tr>\n                    <td>80</td>\n                    <td>william fontecha</td>\n                    <td style=\"font-weight: bold;\">$51,055</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:16</td>\n                </tr>\n            \n                <tr>\n                    <td>79</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:15</td>\n                </tr>\n            \n                <tr>\n                    <td>78</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$157,798</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:14</td>\n                </tr>\n            \n                <tr>\n                    <td>77</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$194,093</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 08:57</td>\n                </tr>\n            \n                <tr>\n                    <td>76</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$232,050</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:58</td>\n                </tr>\n            \n                <tr>\n                    <td>75</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$220,392</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:51</td>\n                </tr>\n            \n                <tr>\n                    <td>74</td>\n                    <td>magda maria</td>\n                    <td style=\"font-weight: bold;\">$139,230</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:38</td>\n                </tr>\n            \n                <tr>\n                    <td>65</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$77,350</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 17:07</td>\n                </tr>\n            \n                <tr>\n                    <td>64</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$173,030</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 16:42</td>\n                </tr>\n            \n                <tr>\n                    <td>62</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$40,940</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:11</td>\n                </tr>\n            \n                <tr>\n                    <td>61</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$240,860</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:07</td>\n                </tr>\n            \n                <tr>\n                    <td>60</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$61,880</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 14:46</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Repartidores y Entregas</h2>\n                <div class=\"highlight\" style=\"background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left-color: #4caf50;\">\n                    <div style=\"display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;\">\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">2</div>\n                            <div style=\"color: #666;\">Entregas Confirmadas (Mes)</div>\n                        </div>\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">4.0/5</div>\n                            <div style=\"color: #666;\">Calificacion Promedio</div>\n                        </div>\n                    </div>\n        \n                    <div style=\"margin-top: 15px; padding: 15px; background: white; border-radius: 10px; text-align: center;\">\n                        <div style=\"font-size: 1.2rem; color: #fbc02d; margin-bottom: 5px;\">ESTRELLA DEL MES</div>\n                        <div style=\"font-size: 1.5rem; font-weight: bold; color: #2e7d32;\">michael </div>\n                        <div style=\"color: #666;\">Promedio: 4.0/5 | 2 entregas</div>\n                    </div>\n            \n                </div>\n                \n                <div class=\"footer\">\n                    <p style=\"font-size: 0.9rem;\">Este reporte fue generado automaticamente desde el Dashboard de Glam Store</p>\n                    <p style=\"font-size: 0.8rem; color: #bbb;\">29/11/2025 22:24:51</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        ', 'DASHBOARD', '2025-11-29 22:24:51.921257', 0);
INSERT INTO "notificaciones_reporte" ("idNotificacion", "titulo", "contenido_html", "tipo", "fechaCreacion", "leida") VALUES
(2, 'Reporte Dashboard - 29/11/2025', '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <style>\n                body { font-family: Arial, sans-serif; background-color: #fffafc; padding: 20px; }\n                .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }\n                h1 { color: #c2185b; border-bottom: 3px solid #f48fb1; padding-bottom: 10px; }\n                h2 { color: #ad1457; margin-top: 30px; margin-bottom: 15px; }\n                .stat-box { display: inline-block; background: #fce4ec; padding: 15px 25px; border-radius: 10px; margin: 8px; text-align: center; min-width: 120px; }\n                .stat-number { font-size: 1.8rem; font-weight: bold; color: #c2185b; }\n                .stat-label { color: #666; font-size: 0.85rem; }\n                table { width: 100%; border-collapse: collapse; margin: 15px 0; }\n                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #fce4ec; }\n                th { background: #fce4ec; color: #c2185b; }\n                .highlight { background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #fbc02d; }\n                .footer { text-align: center; color: #999; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fce4ec; }\n                .bar-container { margin: 8px 0; }\n                .bar-label { display: inline-block; width: 150px; font-size: 0.9rem; color: #333; }\n                .bar-wrapper { display: inline-block; width: calc(100% - 250px); background: #f5f5f5; border-radius: 5px; height: 25px; vertical-align: middle; }\n                .bar { height: 25px; border-radius: 5px; display: inline-block; }\n                .bar-value { display: inline-block; width: 80px; text-align: right; font-weight: bold; color: #c2185b; font-size: 0.9rem; }\n                .chart-vertical { display: flex; align-items: flex-end; justify-content: space-around; height: 200px; background: #fafafa; border-radius: 10px; padding: 20px 10px 10px 10px; margin: 15px 0; }\n                .chart-bar { display: flex; flex-direction: column; align-items: center; width: 12%; }\n                .chart-bar-fill { width: 100%; background: linear-gradient(180deg, #ec407a 0%, #f48fb1 100%); border-radius: 5px 5px 0 0; min-height: 5px; }\n                .chart-bar-label { font-size: 0.75rem; color: #666; margin-top: 8px; text-align: center; }\n                .chart-bar-value { font-size: 0.8rem; font-weight: bold; color: #c2185b; margin-bottom: 5px; }\n                .comparison-box { display: inline-block; background: white; padding: 15px 20px; border-radius: 10px; margin: 8px; border: 2px solid #f8bbd0; text-align: center; min-width: 180px; }\n                .comparison-title { font-size: 0.85rem; color: #666; margin-bottom: 5px; }\n                .comparison-value { font-size: 1.5rem; font-weight: bold; color: #c2185b; }\n                .comparison-change { font-size: 0.8rem; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block; }\n                .change-up { background: #e8f5e9; color: #2e7d32; }\n                .change-down { background: #ffebee; color: #c62828; }\n                .change-same { background: #f5f5f5; color: #666; }\n            </style>\n        </head>\n        <body>\n            <div class=\"container\">\n                <h1>Reporte Dashboard - Glam Store</h1>\n                <p style=\"color: #666;\">Generado el 29/11/2025 a las 22:24</p>\n                \n                <h2>Resumen General</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">28</div>\n                        <div class=\"stat-label\">Productos</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">12</div>\n                        <div class=\"stat-label\">Clientes</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">46</div>\n                        <div class=\"stat-label\">Pedidos Totales</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">$3,433,027</div>\n                        <div class=\"stat-label\">Ventas Totales</div>\n                    </div>\n                </div>\n                \n                <h2>Comparativa Semanal</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Nuevos Esta Semana</div>\n                        <div class=\"comparison-value\">6</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Activos Esta Semana</div>\n                        <div class=\"comparison-value\">7</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Esta Semana</div>\n                        <div class=\"comparison-value\">22</div>\n                        <div class=\"comparison-change\">\n                            $2,300,377 en ventas\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Este Mes</div>\n                        <div class=\"comparison-value\">46</div>\n                        <div class=\"comparison-change\">\n                            $3,433,027 en ventas\n                        </div>\n                    </div>\n                </div>\n                \n                <h2>Pedidos por Dia (Ultimos 7 dias)</h2>\n                <table>\n                    <tr>\n                        <th>Dia</th>\n                        <th>Pedidos</th>\n                        <th>Ventas</th>\n                        <th>Grafico</th>\n                    </tr>\n        \n                    <tr>\n                        <td style=\"font-weight: bold;\">Dom 23</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Lun 24</td>\n                        <td style=\"text-align: center;\">15</td>\n                        <td style=\"text-align: right;\">$1,686,262</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 100%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mar 25</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mie 26</td>\n                        <td style=\"text-align: center;\">7</td>\n                        <td style=\"text-align: right;\">$614,115</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 46%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Jue 27</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Vie 28</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Sab 29</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                </table>\n                \n                <h2>Ventas por Categoria</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Rostro</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 100%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$1,446,600</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Ojos</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 36%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$522,800</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Accesorios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 28%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$413,500</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Uñas</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 15%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$228,400</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Labios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 10%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$155,950</span>\n                </div>\n                \n                \n                <h2>Top 10 Productos Mas Vendidos</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">1. Delineador Liquido Precis</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 100%; background: #e91e63;\"></span>\n                    </span>\n                    <span class=\"bar-value\">13 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">2. Rubor Rosado Glow</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #9c27b0;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">3. Corrector Liquido Soft To</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #673ab7;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">4. Iluminador Perla Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #3f51b5;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">5. Esponja Blender Lavanda</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 53%; background: #2196f3;\"></span>\n                    </span>\n                    <span class=\"bar-value\">7 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">6. Pestañina Curvas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #00bcd4;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">7. Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #009688;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">8. Tratamiento Fortalecedor</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #4caf50;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">9. Polvo Compacto Mate Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #8bc34a;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">10. Sombra Cuarteto Rosa</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 30%; background: #cddc39;\"></span>\n                    </span>\n                    <span class=\"bar-value\">4 uds</span>\n                </div>\n            \n                \n                <h2>Inventario Bajo (Stock menor a 10)</h2>\n                <div style=\"background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;\">\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Kit Decoracion de Uñas</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 30%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">3 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Cremoso Fucsia Pop</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Rosa Pastel</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Organizador Acrilico Mini</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Sombra Liquida Glitter Po</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Glitter Champagne</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Espejo LED Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Pestañina Volumen Total G</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Mate Velvet Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 90%; background: #fbc02d;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #fbc02d;\">9 uds</span>\n                </div>\n            </div>\n                \n                <h2>Reabastecimientos Recientes (Ultima Semana)</h2>\n                <table>\n                    <tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Lote</th><th>Vencimiento</th></tr>\n        \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-12</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+20</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Delineador de Labios Coral Chic</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Bronceador trendy</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-07</td>\n                    <td>07/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Cushion Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BCG-01</td>\n                    <td>01/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Ultimos 15 Pedidos</h2>\n                <table>\n                    <tr><th>#</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr>\n        \n                <tr>\n                    <td>83</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$55,160</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:37</td>\n                </tr>\n            \n                <tr>\n                    <td>82</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$68,425</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:25</td>\n                </tr>\n            \n                <tr>\n                    <td>81</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:20</td>\n                </tr>\n            \n                <tr>\n                    <td>80</td>\n                    <td>william fontecha</td>\n                    <td style=\"font-weight: bold;\">$51,055</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:16</td>\n                </tr>\n            \n                <tr>\n                    <td>79</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:15</td>\n                </tr>\n            \n                <tr>\n                    <td>78</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$157,798</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:14</td>\n                </tr>\n            \n                <tr>\n                    <td>77</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$194,093</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 08:57</td>\n                </tr>\n            \n                <tr>\n                    <td>76</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$232,050</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:58</td>\n                </tr>\n            \n                <tr>\n                    <td>75</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$220,392</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:51</td>\n                </tr>\n            \n                <tr>\n                    <td>74</td>\n                    <td>magda maria</td>\n                    <td style=\"font-weight: bold;\">$139,230</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:38</td>\n                </tr>\n            \n                <tr>\n                    <td>65</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$77,350</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 17:07</td>\n                </tr>\n            \n                <tr>\n                    <td>64</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$173,030</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 16:42</td>\n                </tr>\n            \n                <tr>\n                    <td>62</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$40,940</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:11</td>\n                </tr>\n            \n                <tr>\n                    <td>61</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$240,860</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:07</td>\n                </tr>\n            \n                <tr>\n                    <td>60</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$61,880</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 14:46</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Repartidores y Entregas</h2>\n                <div class=\"highlight\" style=\"background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left-color: #4caf50;\">\n                    <div style=\"display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;\">\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">2</div>\n                            <div style=\"color: #666;\">Entregas Confirmadas (Mes)</div>\n                        </div>\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">4.0/5</div>\n                            <div style=\"color: #666;\">Calificacion Promedio</div>\n                        </div>\n                    </div>\n        \n                    <div style=\"margin-top: 15px; padding: 15px; background: white; border-radius: 10px; text-align: center;\">\n                        <div style=\"font-size: 1.2rem; color: #fbc02d; margin-bottom: 5px;\">ESTRELLA DEL MES</div>\n                        <div style=\"font-size: 1.5rem; font-weight: bold; color: #2e7d32;\">michael </div>\n                        <div style=\"color: #666;\">Promedio: 4.0/5 | 2 entregas</div>\n                    </div>\n            \n                </div>\n                \n                <div class=\"footer\">\n                    <p style=\"font-size: 0.9rem;\">Este reporte fue generado automaticamente desde el Dashboard de Glam Store</p>\n                    <p style=\"font-size: 0.8rem; color: #bbb;\">29/11/2025 22:24:55</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        ', 'DASHBOARD', '2025-11-29 22:24:55.654180', 1);
INSERT INTO "notificaciones_reporte" ("idNotificacion", "titulo", "contenido_html", "tipo", "fechaCreacion", "leida") VALUES
(3, 'Reporte Dashboard - 29/11/2025', '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <style>\n                body { font-family: Arial, sans-serif; background-color: #fffafc; padding: 20px; }\n                .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }\n                h1 { color: #c2185b; border-bottom: 3px solid #f48fb1; padding-bottom: 10px; }\n                h2 { color: #ad1457; margin-top: 30px; margin-bottom: 15px; }\n                .stat-box { display: inline-block; background: #fce4ec; padding: 15px 25px; border-radius: 10px; margin: 8px; text-align: center; min-width: 120px; }\n                .stat-number { font-size: 1.8rem; font-weight: bold; color: #c2185b; }\n                .stat-label { color: #666; font-size: 0.85rem; }\n                table { width: 100%; border-collapse: collapse; margin: 15px 0; }\n                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #fce4ec; }\n                th { background: #fce4ec; color: #c2185b; }\n                .highlight { background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #fbc02d; }\n                .footer { text-align: center; color: #999; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fce4ec; }\n                .bar-container { margin: 8px 0; }\n                .bar-label { display: inline-block; width: 150px; font-size: 0.9rem; color: #333; }\n                .bar-wrapper { display: inline-block; width: calc(100% - 250px); background: #f5f5f5; border-radius: 5px; height: 25px; vertical-align: middle; }\n                .bar { height: 25px; border-radius: 5px; display: inline-block; }\n                .bar-value { display: inline-block; width: 80px; text-align: right; font-weight: bold; color: #c2185b; font-size: 0.9rem; }\n                .chart-vertical { display: flex; align-items: flex-end; justify-content: space-around; height: 200px; background: #fafafa; border-radius: 10px; padding: 20px 10px 10px 10px; margin: 15px 0; }\n                .chart-bar { display: flex; flex-direction: column; align-items: center; width: 12%; }\n                .chart-bar-fill { width: 100%; background: linear-gradient(180deg, #ec407a 0%, #f48fb1 100%); border-radius: 5px 5px 0 0; min-height: 5px; }\n                .chart-bar-label { font-size: 0.75rem; color: #666; margin-top: 8px; text-align: center; }\n                .chart-bar-value { font-size: 0.8rem; font-weight: bold; color: #c2185b; margin-bottom: 5px; }\n                .comparison-box { display: inline-block; background: white; padding: 15px 20px; border-radius: 10px; margin: 8px; border: 2px solid #f8bbd0; text-align: center; min-width: 180px; }\n                .comparison-title { font-size: 0.85rem; color: #666; margin-bottom: 5px; }\n                .comparison-value { font-size: 1.5rem; font-weight: bold; color: #c2185b; }\n                .comparison-change { font-size: 0.8rem; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block; }\n                .change-up { background: #e8f5e9; color: #2e7d32; }\n                .change-down { background: #ffebee; color: #c62828; }\n                .change-same { background: #f5f5f5; color: #666; }\n            </style>\n        </head>\n        <body>\n            <div class=\"container\">\n                <h1>Reporte Dashboard - Glam Store</h1>\n                <p style=\"color: #666;\">Generado el 29/11/2025 a las 22:32</p>\n                \n                <h2>Resumen General</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">28</div>\n                        <div class=\"stat-label\">Productos</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">12</div>\n                        <div class=\"stat-label\">Clientes</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">46</div>\n                        <div class=\"stat-label\">Pedidos Totales</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">$3,433,027</div>\n                        <div class=\"stat-label\">Ventas Totales</div>\n                    </div>\n                </div>\n                \n                <h2>Comparativa Semanal</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Nuevos Esta Semana</div>\n                        <div class=\"comparison-value\">6</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Activos Esta Semana</div>\n                        <div class=\"comparison-value\">7</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Esta Semana</div>\n                        <div class=\"comparison-value\">22</div>\n                        <div class=\"comparison-change\">\n                            $2,300,377 en ventas\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Este Mes</div>\n                        <div class=\"comparison-value\">46</div>\n                        <div class=\"comparison-change\">\n                            $3,433,027 en ventas\n                        </div>\n                    </div>\n                </div>\n                \n                <h2>Pedidos por Dia (Ultimos 7 dias)</h2>\n                <table>\n                    <tr>\n                        <th>Dia</th>\n                        <th>Pedidos</th>\n                        <th>Ventas</th>\n                        <th>Grafico</th>\n                    </tr>\n        \n                    <tr>\n                        <td style=\"font-weight: bold;\">Dom 23</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Lun 24</td>\n                        <td style=\"text-align: center;\">15</td>\n                        <td style=\"text-align: right;\">$1,686,262</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 100%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mar 25</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mie 26</td>\n                        <td style=\"text-align: center;\">7</td>\n                        <td style=\"text-align: right;\">$614,115</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 46%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Jue 27</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Vie 28</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Sab 29</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                </table>\n                \n                <h2>Ventas por Categoria</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Rostro</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 100%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$1,446,600</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Ojos</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 36%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$522,800</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Accesorios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 28%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$413,500</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Uñas</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 15%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$228,400</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Labios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 10%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$155,950</span>\n                </div>\n                \n                \n                <h2>Top 10 Productos Mas Vendidos</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">1. Delineador Liquido Precis</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 100%; background: #e91e63;\"></span>\n                    </span>\n                    <span class=\"bar-value\">13 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">2. Rubor Rosado Glow</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #9c27b0;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">3. Corrector Liquido Soft To</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #673ab7;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">4. Iluminador Perla Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #3f51b5;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">5. Esponja Blender Lavanda</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 53%; background: #2196f3;\"></span>\n                    </span>\n                    <span class=\"bar-value\">7 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">6. Pestañina Curvas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #00bcd4;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">7. Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #009688;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">8. Tratamiento Fortalecedor</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #4caf50;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">9. Polvo Compacto Mate Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #8bc34a;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">10. Pinza de Cejas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 30%; background: #cddc39;\"></span>\n                    </span>\n                    <span class=\"bar-value\">4 uds</span>\n                </div>\n            \n                \n                <h2>Inventario Bajo (Stock menor a 10)</h2>\n                <div style=\"background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;\">\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Kit Decoracion de Uñas</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 30%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">3 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Cremoso Fucsia Pop</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Rosa Pastel</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Organizador Acrilico Mini</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Sombra Liquida Glitter Po</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Glitter Champagne</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Espejo LED Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Pestañina Volumen Total G</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Mate Velvet Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 90%; background: #fbc02d;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #fbc02d;\">9 uds</span>\n                </div>\n            </div>\n                \n                <h2>Reabastecimientos Recientes (Ultima Semana)</h2>\n                <table>\n                    <tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Lote</th><th>Vencimiento</th></tr>\n        \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-12</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+20</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Delineador de Labios Coral Chic</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Bronceador trendy</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-07</td>\n                    <td>07/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Cushion Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BCG-01</td>\n                    <td>01/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Ultimos 15 Pedidos</h2>\n                <table>\n                    <tr><th>#</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr>\n        \n                <tr>\n                    <td>83</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$55,160</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:37</td>\n                </tr>\n            \n                <tr>\n                    <td>82</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$68,425</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:25</td>\n                </tr>\n            \n                <tr>\n                    <td>81</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:20</td>\n                </tr>\n            \n                <tr>\n                    <td>80</td>\n                    <td>william fontecha</td>\n                    <td style=\"font-weight: bold;\">$51,055</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:16</td>\n                </tr>\n            \n                <tr>\n                    <td>79</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:15</td>\n                </tr>\n            \n                <tr>\n                    <td>78</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$157,798</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:14</td>\n                </tr>\n            \n                <tr>\n                    <td>77</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$194,093</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 08:57</td>\n                </tr>\n            \n                <tr>\n                    <td>76</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$232,050</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:58</td>\n                </tr>\n            \n                <tr>\n                    <td>75</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$220,392</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:51</td>\n                </tr>\n            \n                <tr>\n                    <td>74</td>\n                    <td>magda maria</td>\n                    <td style=\"font-weight: bold;\">$139,230</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:38</td>\n                </tr>\n            \n                <tr>\n                    <td>65</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$77,350</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 17:07</td>\n                </tr>\n            \n                <tr>\n                    <td>64</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$173,030</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 16:42</td>\n                </tr>\n            \n                <tr>\n                    <td>62</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$40,940</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:11</td>\n                </tr>\n            \n                <tr>\n                    <td>61</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$240,860</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:07</td>\n                </tr>\n            \n                <tr>\n                    <td>60</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$61,880</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 14:46</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Repartidores y Entregas</h2>\n                <div class=\"highlight\" style=\"background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left-color: #4caf50;\">\n                    <div style=\"display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;\">\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">2</div>\n                            <div style=\"color: #666;\">Entregas Confirmadas (Mes)</div>\n                        </div>\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">4.0/5</div>\n                            <div style=\"color: #666;\">Calificacion Promedio</div>\n                        </div>\n                    </div>\n        \n                    <div style=\"margin-top: 15px; padding: 15px; background: white; border-radius: 10px; text-align: center;\">\n                        <div style=\"font-size: 1.2rem; color: #fbc02d; margin-bottom: 5px;\">ESTRELLA DEL MES</div>\n                        <div style=\"font-size: 1.5rem; font-weight: bold; color: #2e7d32;\">michael </div>\n                        <div style=\"color: #666;\">Promedio: 4.0/5 | 2 entregas</div>\n                    </div>\n            \n                </div>\n                \n                <div class=\"footer\">\n                    <p style=\"font-size: 0.9rem;\">Este reporte fue generado automaticamente desde el Dashboard de Glam Store</p>\n                    <p style=\"font-size: 0.8rem; color: #bbb;\">29/11/2025 22:32:03</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        ', 'DASHBOARD', '2025-11-29 22:32:03.129646', 0);
INSERT INTO "notificaciones_reporte" ("idNotificacion", "titulo", "contenido_html", "tipo", "fechaCreacion", "leida") VALUES
(4, 'Reporte Dashboard - 29/11/2025', '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <style>\n                body { font-family: Arial, sans-serif; background-color: #fffafc; padding: 20px; }\n                .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }\n                h1 { color: #c2185b; border-bottom: 3px solid #f48fb1; padding-bottom: 10px; }\n                h2 { color: #ad1457; margin-top: 30px; margin-bottom: 15px; }\n                .stat-box { display: inline-block; background: #fce4ec; padding: 15px 25px; border-radius: 10px; margin: 8px; text-align: center; min-width: 120px; }\n                .stat-number { font-size: 1.8rem; font-weight: bold; color: #c2185b; }\n                .stat-label { color: #666; font-size: 0.85rem; }\n                table { width: 100%; border-collapse: collapse; margin: 15px 0; }\n                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #fce4ec; }\n                th { background: #fce4ec; color: #c2185b; }\n                .highlight { background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #fbc02d; }\n                .footer { text-align: center; color: #999; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fce4ec; }\n                .bar-container { margin: 8px 0; }\n                .bar-label { display: inline-block; width: 150px; font-size: 0.9rem; color: #333; }\n                .bar-wrapper { display: inline-block; width: calc(100% - 250px); background: #f5f5f5; border-radius: 5px; height: 25px; vertical-align: middle; }\n                .bar { height: 25px; border-radius: 5px; display: inline-block; }\n                .bar-value { display: inline-block; width: 80px; text-align: right; font-weight: bold; color: #c2185b; font-size: 0.9rem; }\n                .chart-vertical { display: flex; align-items: flex-end; justify-content: space-around; height: 200px; background: #fafafa; border-radius: 10px; padding: 20px 10px 10px 10px; margin: 15px 0; }\n                .chart-bar { display: flex; flex-direction: column; align-items: center; width: 12%; }\n                .chart-bar-fill { width: 100%; background: linear-gradient(180deg, #ec407a 0%, #f48fb1 100%); border-radius: 5px 5px 0 0; min-height: 5px; }\n                .chart-bar-label { font-size: 0.75rem; color: #666; margin-top: 8px; text-align: center; }\n                .chart-bar-value { font-size: 0.8rem; font-weight: bold; color: #c2185b; margin-bottom: 5px; }\n                .comparison-box { display: inline-block; background: white; padding: 15px 20px; border-radius: 10px; margin: 8px; border: 2px solid #f8bbd0; text-align: center; min-width: 180px; }\n                .comparison-title { font-size: 0.85rem; color: #666; margin-bottom: 5px; }\n                .comparison-value { font-size: 1.5rem; font-weight: bold; color: #c2185b; }\n                .comparison-change { font-size: 0.8rem; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block; }\n                .change-up { background: #e8f5e9; color: #2e7d32; }\n                .change-down { background: #ffebee; color: #c62828; }\n                .change-same { background: #f5f5f5; color: #666; }\n            </style>\n        </head>\n        <body>\n            <div class=\"container\">\n                <h1>Reporte Dashboard - Glam Store</h1>\n                <p style=\"color: #666;\">Generado el 29/11/2025 a las 22:32</p>\n                \n                <h2>Resumen General</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">28</div>\n                        <div class=\"stat-label\">Productos</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">12</div>\n                        <div class=\"stat-label\">Clientes</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">46</div>\n                        <div class=\"stat-label\">Pedidos Totales</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">$3,433,027</div>\n                        <div class=\"stat-label\">Ventas Totales</div>\n                    </div>\n                </div>\n                \n                <h2>Comparativa Semanal</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Nuevos Esta Semana</div>\n                        <div class=\"comparison-value\">6</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Activos Esta Semana</div>\n                        <div class=\"comparison-value\">7</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Esta Semana</div>\n                        <div class=\"comparison-value\">22</div>\n                        <div class=\"comparison-change\">\n                            $2,300,377 en ventas\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Este Mes</div>\n                        <div class=\"comparison-value\">46</div>\n                        <div class=\"comparison-change\">\n                            $3,433,027 en ventas\n                        </div>\n                    </div>\n                </div>\n                \n                <h2>Pedidos por Dia (Ultimos 7 dias)</h2>\n                <table>\n                    <tr>\n                        <th>Dia</th>\n                        <th>Pedidos</th>\n                        <th>Ventas</th>\n                        <th>Grafico</th>\n                    </tr>\n        \n                    <tr>\n                        <td style=\"font-weight: bold;\">Dom 23</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Lun 24</td>\n                        <td style=\"text-align: center;\">15</td>\n                        <td style=\"text-align: right;\">$1,686,262</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 100%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mar 25</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mie 26</td>\n                        <td style=\"text-align: center;\">7</td>\n                        <td style=\"text-align: right;\">$614,115</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 46%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Jue 27</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Vie 28</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Sab 29</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                </table>\n                \n                <h2>Ventas por Categoria</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Rostro</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 100%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$1,446,600</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Ojos</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 36%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$522,800</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Accesorios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 28%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$413,500</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Uñas</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 15%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$228,400</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Labios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 10%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$155,950</span>\n                </div>\n                \n                \n                <h2>Top 10 Productos Mas Vendidos</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">1. Delineador Liquido Precis</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 100%; background: #e91e63;\"></span>\n                    </span>\n                    <span class=\"bar-value\">13 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">2. Rubor Rosado Glow</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #9c27b0;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">3. Corrector Liquido Soft To</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #673ab7;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">4. Iluminador Perla Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #3f51b5;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">5. Esponja Blender Lavanda</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 53%; background: #2196f3;\"></span>\n                    </span>\n                    <span class=\"bar-value\">7 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">6. Pestañina Curvas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #00bcd4;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">7. Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #009688;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">8. Tratamiento Fortalecedor</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #4caf50;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">9. Polvo Compacto Mate Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #8bc34a;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">10. Pinza de Cejas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 30%; background: #cddc39;\"></span>\n                    </span>\n                    <span class=\"bar-value\">4 uds</span>\n                </div>\n            \n                \n                <h2>Inventario Bajo (Stock menor a 10)</h2>\n                <div style=\"background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;\">\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Kit Decoracion de Uñas</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 30%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">3 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Cremoso Fucsia Pop</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Rosa Pastel</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Organizador Acrilico Mini</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Sombra Liquida Glitter Po</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Glitter Champagne</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Espejo LED Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Pestañina Volumen Total G</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Mate Velvet Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 90%; background: #fbc02d;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #fbc02d;\">9 uds</span>\n                </div>\n            </div>\n                \n                <h2>Reabastecimientos Recientes (Ultima Semana)</h2>\n                <table>\n                    <tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Lote</th><th>Vencimiento</th></tr>\n        \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-12</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+20</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Delineador de Labios Coral Chic</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Bronceador trendy</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-07</td>\n                    <td>07/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Cushion Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BCG-01</td>\n                    <td>01/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Ultimos 15 Pedidos</h2>\n                <table>\n                    <tr><th>#</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr>\n        \n                <tr>\n                    <td>83</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$55,160</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:37</td>\n                </tr>\n            \n                <tr>\n                    <td>82</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$68,425</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:25</td>\n                </tr>\n            \n                <tr>\n                    <td>81</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:20</td>\n                </tr>\n            \n                <tr>\n                    <td>80</td>\n                    <td>william fontecha</td>\n                    <td style=\"font-weight: bold;\">$51,055</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:16</td>\n                </tr>\n            \n                <tr>\n                    <td>79</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:15</td>\n                </tr>\n            \n                <tr>\n                    <td>78</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$157,798</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:14</td>\n                </tr>\n            \n                <tr>\n                    <td>77</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$194,093</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 08:57</td>\n                </tr>\n            \n                <tr>\n                    <td>76</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$232,050</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:58</td>\n                </tr>\n            \n                <tr>\n                    <td>75</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$220,392</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:51</td>\n                </tr>\n            \n                <tr>\n                    <td>74</td>\n                    <td>magda maria</td>\n                    <td style=\"font-weight: bold;\">$139,230</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:38</td>\n                </tr>\n            \n                <tr>\n                    <td>65</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$77,350</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 17:07</td>\n                </tr>\n            \n                <tr>\n                    <td>64</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$173,030</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 16:42</td>\n                </tr>\n            \n                <tr>\n                    <td>62</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$40,940</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:11</td>\n                </tr>\n            \n                <tr>\n                    <td>61</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$240,860</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:07</td>\n                </tr>\n            \n                <tr>\n                    <td>60</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$61,880</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 14:46</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Repartidores y Entregas</h2>\n                <div class=\"highlight\" style=\"background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left-color: #4caf50;\">\n                    <div style=\"display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;\">\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">2</div>\n                            <div style=\"color: #666;\">Entregas Confirmadas (Mes)</div>\n                        </div>\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">4.0/5</div>\n                            <div style=\"color: #666;\">Calificacion Promedio</div>\n                        </div>\n                    </div>\n        \n                    <div style=\"margin-top: 15px; padding: 15px; background: white; border-radius: 10px; text-align: center;\">\n                        <div style=\"font-size: 1.2rem; color: #fbc02d; margin-bottom: 5px;\">ESTRELLA DEL MES</div>\n                        <div style=\"font-size: 1.5rem; font-weight: bold; color: #2e7d32;\">michael </div>\n                        <div style=\"color: #666;\">Promedio: 4.0/5 | 2 entregas</div>\n                    </div>\n            \n                </div>\n                \n                <div class=\"footer\">\n                    <p style=\"font-size: 0.9rem;\">Este reporte fue generado automaticamente desde el Dashboard de Glam Store</p>\n                    <p style=\"font-size: 0.8rem; color: #bbb;\">29/11/2025 22:32:07</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        ', 'DASHBOARD', '2025-11-29 22:32:07.411021', 0);
INSERT INTO "notificaciones_reporte" ("idNotificacion", "titulo", "contenido_html", "tipo", "fechaCreacion", "leida") VALUES
(5, 'Reporte Dashboard - 29/11/2025', '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <style>\n                body { font-family: Arial, sans-serif; background-color: #fffafc; padding: 20px; }\n                .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }\n                h1 { color: #c2185b; border-bottom: 3px solid #f48fb1; padding-bottom: 10px; }\n                h2 { color: #ad1457; margin-top: 30px; margin-bottom: 15px; }\n                .stat-box { display: inline-block; background: #fce4ec; padding: 15px 25px; border-radius: 10px; margin: 8px; text-align: center; min-width: 120px; }\n                .stat-number { font-size: 1.8rem; font-weight: bold; color: #c2185b; }\n                .stat-label { color: #666; font-size: 0.85rem; }\n                table { width: 100%; border-collapse: collapse; margin: 15px 0; }\n                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #fce4ec; }\n                th { background: #fce4ec; color: #c2185b; }\n                .highlight { background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #fbc02d; }\n                .footer { text-align: center; color: #999; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fce4ec; }\n                .bar-container { margin: 8px 0; }\n                .bar-label { display: inline-block; width: 150px; font-size: 0.9rem; color: #333; }\n                .bar-wrapper { display: inline-block; width: calc(100% - 250px); background: #f5f5f5; border-radius: 5px; height: 25px; vertical-align: middle; }\n                .bar { height: 25px; border-radius: 5px; display: inline-block; }\n                .bar-value { display: inline-block; width: 80px; text-align: right; font-weight: bold; color: #c2185b; font-size: 0.9rem; }\n                .chart-vertical { display: flex; align-items: flex-end; justify-content: space-around; height: 200px; background: #fafafa; border-radius: 10px; padding: 20px 10px 10px 10px; margin: 15px 0; }\n                .chart-bar { display: flex; flex-direction: column; align-items: center; width: 12%; }\n                .chart-bar-fill { width: 100%; background: linear-gradient(180deg, #ec407a 0%, #f48fb1 100%); border-radius: 5px 5px 0 0; min-height: 5px; }\n                .chart-bar-label { font-size: 0.75rem; color: #666; margin-top: 8px; text-align: center; }\n                .chart-bar-value { font-size: 0.8rem; font-weight: bold; color: #c2185b; margin-bottom: 5px; }\n                .comparison-box { display: inline-block; background: white; padding: 15px 20px; border-radius: 10px; margin: 8px; border: 2px solid #f8bbd0; text-align: center; min-width: 180px; }\n                .comparison-title { font-size: 0.85rem; color: #666; margin-bottom: 5px; }\n                .comparison-value { font-size: 1.5rem; font-weight: bold; color: #c2185b; }\n                .comparison-change { font-size: 0.8rem; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block; }\n                .change-up { background: #e8f5e9; color: #2e7d32; }\n                .change-down { background: #ffebee; color: #c62828; }\n                .change-same { background: #f5f5f5; color: #666; }\n            </style>\n        </head>\n        <body>\n            <div class=\"container\">\n                <h1>Reporte Dashboard - Glam Store</h1>\n                <p style=\"color: #666;\">Generado el 29/11/2025 a las 22:32</p>\n                \n                <h2>Resumen General</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">28</div>\n                        <div class=\"stat-label\">Productos</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">12</div>\n                        <div class=\"stat-label\">Clientes</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">46</div>\n                        <div class=\"stat-label\">Pedidos Totales</div>\n                    </div>\n                    <div class=\"stat-box\">\n                        <div class=\"stat-number\">$3,433,027</div>\n                        <div class=\"stat-label\">Ventas Totales</div>\n                    </div>\n                </div>\n                \n                <h2>Comparativa Semanal</h2>\n                <div style=\"text-align: center;\">\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Nuevos Esta Semana</div>\n                        <div class=\"comparison-value\">6</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Clientes Activos Esta Semana</div>\n                        <div class=\"comparison-value\">7</div>\n                        <div class=\"comparison-change change-up\">\n                            vs 5 semana pasada\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Esta Semana</div>\n                        <div class=\"comparison-value\">22</div>\n                        <div class=\"comparison-change\">\n                            $2,300,377 en ventas\n                        </div>\n                    </div>\n                    <div class=\"comparison-box\">\n                        <div class=\"comparison-title\">Pedidos Este Mes</div>\n                        <div class=\"comparison-value\">46</div>\n                        <div class=\"comparison-change\">\n                            $3,433,027 en ventas\n                        </div>\n                    </div>\n                </div>\n                \n                <h2>Pedidos por Dia (Ultimos 7 dias)</h2>\n                <table>\n                    <tr>\n                        <th>Dia</th>\n                        <th>Pedidos</th>\n                        <th>Ventas</th>\n                        <th>Grafico</th>\n                    </tr>\n        \n                    <tr>\n                        <td style=\"font-weight: bold;\">Dom 23</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Lun 24</td>\n                        <td style=\"text-align: center;\">15</td>\n                        <td style=\"text-align: right;\">$1,686,262</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 100%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mar 25</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Mie 26</td>\n                        <td style=\"text-align: center;\">7</td>\n                        <td style=\"text-align: right;\">$614,115</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 46%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Jue 27</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Vie 28</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                    <tr>\n                        <td style=\"font-weight: bold;\">Sab 29</td>\n                        <td style=\"text-align: center;\">0</td>\n                        <td style=\"text-align: right;\">$0</td>\n                        <td style=\"width: 40%;\">\n                            <div style=\"background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;\">\n                                <div style=\"background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: 0%; border-radius: 5px;\"></div>\n                            </div>\n                        </td>\n                    </tr>\n            \n                </table>\n                \n                <h2>Ventas por Categoria</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Rostro</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 100%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$1,446,600</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Ojos</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 36%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$522,800</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Accesorios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 28%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$413,500</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Uñas</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 15%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$228,400</span>\n                </div>\n                \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\">Labios</span>\n                    <span class=\"bar-wrapper\">\n                        <span class=\"bar\" style=\"width: 10%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);\"></span>\n                    </span>\n                    <span class=\"bar-value\">$155,950</span>\n                </div>\n                \n                \n                <h2>Top 10 Productos Mas Vendidos</h2>\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">1. Delineador Liquido Precis</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 100%; background: #e91e63;\"></span>\n                    </span>\n                    <span class=\"bar-value\">13 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">2. Rubor Rosado Glow</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #9c27b0;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">3. Corrector Liquido Soft To</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #673ab7;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">4. Iluminador Perla Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 76%; background: #3f51b5;\"></span>\n                    </span>\n                    <span class=\"bar-value\">10 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">5. Esponja Blender Lavanda</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 53%; background: #2196f3;\"></span>\n                    </span>\n                    <span class=\"bar-value\">7 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">6. Pestañina Curvas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #00bcd4;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">7. Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 46%; background: #009688;\"></span>\n                    </span>\n                    <span class=\"bar-value\">6 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">8. Tratamiento Fortalecedor</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #4caf50;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">9. Polvo Compacto Mate Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 38%; background: #8bc34a;\"></span>\n                    </span>\n                    <span class=\"bar-value\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">10. Pinza de Cejas Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 300px);\">\n                        <span class=\"bar\" style=\"width: 30%; background: #cddc39;\"></span>\n                    </span>\n                    <span class=\"bar-value\">4 uds</span>\n                </div>\n            \n                \n                <h2>Inventario Bajo (Stock menor a 10)</h2>\n                <div style=\"background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;\">\n        \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Kit Decoracion de Uñas</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 30%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">3 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Cremoso Fucsia Pop</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Rosa Pastel</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Organizador Acrilico Mini</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 40%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">4 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Sombra Liquida Glitter Po</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Esmalte Glitter Champagne</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Espejo LED Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Pestañina Volumen Total G</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Labial Mate Velvet Glam</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 50%; background: #f57c00;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #f57c00;\">5 uds</span>\n                </div>\n            \n                <div class=\"bar-container\">\n                    <span class=\"bar-label\" style=\"width: 200px;\">Top Coat Brillo Extremo</span>\n                    <span class=\"bar-wrapper\" style=\"width: calc(100% - 280px); background: #ffcdd2;\">\n                        <span class=\"bar\" style=\"width: 90%; background: #fbc02d;\"></span>\n                    </span>\n                    <span class=\"bar-value\" style=\"color: #fbc02d;\">9 uds</span>\n                </div>\n            </div>\n                \n                <h2>Reabastecimientos Recientes (Ultima Semana)</h2>\n                <table>\n                    <tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Lote</th><th>Vencimiento</th></tr>\n        \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-12</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Tratamiento Fortalecedor</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+20</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Delineador de Labios Coral Chic</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+10</td>\n                    <td>L2025-11</td>\n                    <td>26/11/2025</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Bronceador trendy</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-07</td>\n                    <td>07/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Cushion Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BCG-01</td>\n                    <td>01/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Rubor Rosado Glow</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-06</td>\n                    <td>06/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Polvo Compacto Mate Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-PCMG-05</td>\n                    <td>05/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Iluminador Perla Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-IPG-04</td>\n                    <td>04/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Corrector Liquido Soft Touch</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-CLS-03</td>\n                    <td>03/12/2027</td>\n                </tr>\n            \n                <tr>\n                    <td>26/11/2025</td>\n                    <td>Base Liquida HD Glam</td>\n                    <td style=\"color: #2e7d32; font-weight: bold;\">+1</td>\n                    <td>L-BLG-02</td>\n                    <td>02/12/2027</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Ultimos 15 Pedidos</h2>\n                <table>\n                    <tr><th>#</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr>\n        \n                <tr>\n                    <td>83</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$55,160</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:37</td>\n                </tr>\n            \n                <tr>\n                    <td>82</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$68,425</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:25</td>\n                </tr>\n            \n                <tr>\n                    <td>81</td>\n                    <td>andrea </td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:20</td>\n                </tr>\n            \n                <tr>\n                    <td>80</td>\n                    <td>william fontecha</td>\n                    <td style=\"font-weight: bold;\">$51,055</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:16</td>\n                </tr>\n            \n                <tr>\n                    <td>79</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$43,792</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:15</td>\n                </tr>\n            \n                <tr>\n                    <td>78</td>\n                    <td>lauren ortiz contrer  as</td>\n                    <td style=\"font-weight: bold;\">$157,798</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 13:14</td>\n                </tr>\n            \n                <tr>\n                    <td>77</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$194,093</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>26/11/2025 08:57</td>\n                </tr>\n            \n                <tr>\n                    <td>76</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$232,050</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:58</td>\n                </tr>\n            \n                <tr>\n                    <td>75</td>\n                    <td>maria magdalena  </td>\n                    <td style=\"font-weight: bold;\">$220,392</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:51</td>\n                </tr>\n            \n                <tr>\n                    <td>74</td>\n                    <td>magda maria</td>\n                    <td style=\"font-weight: bold;\">$139,230</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 19:38</td>\n                </tr>\n            \n                <tr>\n                    <td>65</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$77,350</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 17:07</td>\n                </tr>\n            \n                <tr>\n                    <td>64</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$173,030</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 16:42</td>\n                </tr>\n            \n                <tr>\n                    <td>62</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$40,940</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:11</td>\n                </tr>\n            \n                <tr>\n                    <td>61</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$240,860</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 15:07</td>\n                </tr>\n            \n                <tr>\n                    <td>60</td>\n                    <td>alejandro rodriguez </td>\n                    <td style=\"font-weight: bold;\">$61,880</td>\n                    <td style=\"color: #1976d2;\">Confirmado</td>\n                    <td>24/11/2025 14:46</td>\n                </tr>\n            \n                </table>\n                \n                <h2>Repartidores y Entregas</h2>\n                <div class=\"highlight\" style=\"background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left-color: #4caf50;\">\n                    <div style=\"display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;\">\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">2</div>\n                            <div style=\"color: #666;\">Entregas Confirmadas (Mes)</div>\n                        </div>\n                        <div style=\"padding: 10px;\">\n                            <div style=\"font-size: 2rem; font-weight: bold; color: #2e7d32;\">4.0/5</div>\n                            <div style=\"color: #666;\">Calificacion Promedio</div>\n                        </div>\n                    </div>\n        \n                    <div style=\"margin-top: 15px; padding: 15px; background: white; border-radius: 10px; text-align: center;\">\n                        <div style=\"font-size: 1.2rem; color: #fbc02d; margin-bottom: 5px;\">ESTRELLA DEL MES</div>\n                        <div style=\"font-size: 1.5rem; font-weight: bold; color: #2e7d32;\">michael </div>\n                        <div style=\"color: #666;\">Promedio: 4.0/5 | 2 entregas</div>\n                    </div>\n            \n                </div>\n                \n                <div class=\"footer\">\n                    <p style=\"font-size: 0.9rem;\">Este reporte fue generado automaticamente desde el Dashboard de Glam Store</p>\n                    <p style=\"font-size: 0.8rem; color: #bbb;\">29/11/2025 22:32:18</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        ', 'DASHBOARD', '2025-11-29 22:32:18.953755', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "pedidoproducto"
--

CREATE TABLE "pedidoproducto" (
  "idPedido" integer NOT NULL,
  "idProducto" bigint NOT NULL,
  "cantidad" integer DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "pedidos"
--

CREATE TABLE "pedidos" (
  "idPedido" integer NOT NULL,
  "idCliente" integer DEFAULT NULL,
  "fechaCreacion" timestamp NOT NULL DEFAULT current_timestamp(),
  "fechaEntrega" date DEFAULT NULL,
  "estado" character varying(20) DEFAULT 'Pendiente',
  "total" decimal(12,2) DEFAULT NULL,
  "requiere_verificacion_pago" smallint DEFAULT 0,
  "idRepartidor" integer DEFAULT NULL,
  "direccionEntrega" character varying(30) DEFAULT NULL,
  "estado_pago" character varying(20) NOT NULL DEFAULT 'Pago Completo',
  "estado_pedido" character varying(20) NOT NULL DEFAULT 'Confirmado',
  "fechaVencimiento" date DEFAULT NULL,
  "facturasEnviadas" integer NOT NULL DEFAULT 0
);

--
-- Volcado de datos para la tabla "pedidos"
--

INSERT INTO "pedidos" ("idPedido", "idCliente", "fechaCreacion", "fechaEntrega", "estado", "total", "requiere_verificacion_pago", "idRepartidor", "direccionEntrega", "estado_pago", "estado_pedido", "fechaVencimiento", "facturasEnviadas") VALUES
(20, 13, '2025-11-20 13:14:00', NULL, 'Pago Parcial', 21420.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(21, 13, '2025-11-20 13:27:44', NULL, 'Pago Parcial', 38080.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(22, 13, '2025-11-20 13:30:46', NULL, 'Pago Parcial', 38080.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(23, 13, '2025-11-20 15:26:57', NULL, 'Pago Parcial', 17850.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(24, 13, '2025-11-20 15:28:42', NULL, 'Pago Parcial', 16660.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(25, 13, '2025-11-20 15:53:40', NULL, 'Pago Parcial', 38080.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(26, 13, '2025-11-20 16:13:31', NULL, 'Pago Parcial', 45220.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(27, 13, '2025-11-20 18:59:45', NULL, 'Pago Parcial', 38080.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(28, 13, '2025-11-20 19:03:10', NULL, 'Pago Parcial', 16660.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(33, 15, '2025-11-20 19:54:00', NULL, 'Pago Parcial', 74970.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(34, 15, '2025-11-20 20:05:09', NULL, 'Pago Parcial', 21420.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(35, 15, '2025-11-20 20:12:06', NULL, 'Pago Parcial', 40460.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(36, 15, '2025-11-20 20:20:36', NULL, 'Pago Parcial', 21420.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(37, 17, '2025-11-21 00:32:13', NULL, 'Pago Parcial', 65450.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(38, 17, '2025-11-21 01:06:53', NULL, 'En Camino', 57600.00, 0, 19, NULL, 'Pago Completo', 'Entregado', '2025-11-25', 1),
(39, 18, '2025-11-21 01:08:27', NULL, 'Pago Parcial', 40460.00, 0, 15, NULL, 'Pago Parcial', 'Entregado', '2025-11-25', 1),
(40, 18, '2025-11-21 01:13:13', NULL, 'Problema en Entrega', 49980.00, 0, 15, NULL, 'Pago Completo', 'Completado', '2025-11-25', 1),
(43, 20, '2025-11-22 00:53:43', NULL, 'Entregado', 141610.00, 0, 15, NULL, 'Pago Completo', 'Completado', '2025-11-26', 1),
(44, 20, '2025-11-22 00:58:29', NULL, 'Entregado', 42840.00, 0, 15, NULL, 'Pago Completo', 'Completado', '2025-11-26', 1),
(45, 20, '2025-11-22 01:12:30', NULL, 'Pago Parcial', 61880.00, 0, 15, NULL, 'Pago Parcial', 'Entregado', '2025-11-26', 1),
(46, 20, '2025-11-22 01:21:06', NULL, 'Pago Parcial', 91630.00, 0, 16, NULL, 'Pago Parcial', 'Entregado', '2025-11-26', 1),
(47, 20, '2025-11-22 01:35:57', NULL, 'Problema en Entrega', 38080.00, 0, 16, NULL, 'Pago Completo', 'Completado', '2025-11-26', 1),
(48, 20, '2025-11-22 01:36:36', NULL, 'Entregado', 21420.00, 0, 16, NULL, 'Pago Parcial', 'Completado', '2025-11-26', 1),
(52, 20, '2025-11-22 02:52:36', NULL, 'Entregado', 93300.00, 0, 16, NULL, 'Pago Completo', 'Completado', '2025-11-26', 1),
(53, 22, '2025-11-24 08:16:01', NULL, 'Pago Parcial', 93300.00, 0, 16, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(54, 22, '2025-11-24 08:27:11', NULL, 'Pago Completo', 44510.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(55, 22, '2025-11-24 08:42:02', NULL, 'Pago Parcial', 84970.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(56, 22, '2025-11-24 08:47:46', NULL, 'Confirmado', 71400.00, 0, 17, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 1),
(57, 22, '2025-11-24 08:52:55', NULL, 'Confirmado', 39270.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 0),
(58, 23, '2025-11-24 11:38:41', NULL, 'Confirmado', 42840.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 0),
(59, 23, '2025-11-24 19:45:27', NULL, 'Confirmado', 124240.00, 0, 18, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(60, 23, '2025-11-24 19:46:43', NULL, 'Confirmado', 61880.00, 0, 18, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 1),
(61, 23, '2025-11-24 20:07:39', NULL, 'Confirmado', 240860.00, 0, 18, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(62, 23, '2025-11-24 20:11:05', NULL, 'Confirmado', 40940.00, 0, 18, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(64, 23, '2025-11-24 21:42:51', NULL, 'Confirmado', 173030.00, 0, 18, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 1),
(65, 23, '2025-11-24 22:07:17', NULL, 'Confirmado', 77350.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 1),
(74, 25, '2025-11-25 00:38:59', NULL, 'Confirmado', 139230.00, 0, 19, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 2),
(75, 26, '2025-11-25 00:51:27', NULL, 'Confirmado', 220392.00, 0, 19, NULL, 'Pago Completo', 'Entregado', '2025-11-27', 2),
(76, 26, '2025-11-25 00:58:41', NULL, 'Confirmado', 232050.00, 0, 15, NULL, 'Pago Parcial', 'Entregado', '2025-11-27', 5),
(77, 26, '2025-11-26 13:57:51', NULL, 'Confirmado', 194093.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 1),
(78, 20, '2025-11-26 18:14:24', NULL, 'Confirmado', 157798.00, 0, 15, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 0),
(79, 20, '2025-11-26 18:15:11', NULL, 'Confirmado', 43792.00, 0, 15, NULL, 'Pago Parcial', 'Entregado', '2025-12-01', 0),
(80, 27, '2025-11-26 18:16:30', NULL, 'Confirmado', 51055.00, 0, 15, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 1),
(81, 28, '2025-11-26 18:20:12', NULL, 'Confirmado', 43792.00, 0, 17, NULL, 'Pago Parcial', 'Entregado', '2025-11-29', 1),
(82, 28, '2025-11-26 18:25:08', NULL, 'Confirmado', 68425.00, 0, 15, NULL, 'Pago Parcial', 'Entregado', '2025-12-01', 0),
(83, 28, '2025-11-26 18:37:18', NULL, 'Confirmado', 55160.00, 0, 15, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 0),
(84, 20, '2025-11-29 22:51:18', NULL, 'Confirmado', 97584.00, 0, 15, NULL, 'Pago Completo', 'Entregado', '2025-12-03', 0),
(85, 20, '2025-11-29 22:51:46', NULL, 'Confirmado', 100321.00, 0, 15, NULL, 'Pago Completo', 'Entregado', '2025-12-03', 0),
(86, 20, '2025-11-29 22:52:36', NULL, 'Confirmado', 42844.00, 0, 15, NULL, 'Pago Completo', 'Entregado', '2025-12-03', 0),
(87, 20, '2025-11-29 22:54:05', NULL, 'Entregado', 70214.00, 0, 17, NULL, 'Pago Completo', 'Completado', '2025-12-01', 0),
(88, 28, '2025-11-29 22:55:30', NULL, 'Confirmado', 77056.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-12-02', 0),
(89, 28, '2025-11-29 22:56:18', NULL, 'Confirmado', 51055.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-12-02', 0),
(90, 28, '2025-11-29 22:58:11', NULL, 'Confirmado', 55160.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-12-02', 0),
(91, 26, '2025-11-29 23:00:29', NULL, 'Confirmado', 59266.00, 0, 17, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 0),
(92, 26, '2025-11-29 23:12:01', NULL, 'Confirmado', 93478.00, 0, 18, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 0),
(93, 29, '2025-11-30 00:06:57', NULL, 'Confirmado', 56108.00, 0, 17, NULL, 'Pago Parcial', 'Entregado', '2025-12-02', 0),
(94, 30, '2025-11-30 00:44:22', NULL, 'Confirmado', 96215.00, 0, 18, NULL, 'Pago Completo', 'Entregado', '2025-12-01', 0),
(95, 30, '2025-11-30 00:44:50', NULL, 'Confirmado', 46529.00, 0, 18, NULL, 'Pago Parcial', 'Entregado', '2025-12-01', 0),
(96, 15, '2025-12-10 21:21:10', NULL, 'En Preparación', 76950.00, 0, 18, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(97, 20, '2025-12-10 21:24:19', NULL, 'En Preparación', 83250.00, 0, 18, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(98, 20, '2025-12-10 22:46:24', NULL, 'En Preparación', 131200.00, 0, 15, NULL, 'Pago Completo', 'En Camino', '2025-12-15', 1),
(99, 20, '2025-12-10 22:48:36', NULL, 'En Preparación', 72750.00, 0, 17, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(100, 20, '2025-12-10 22:48:38', NULL, 'En Preparación', 74600.00, 0, 17, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(101, 20, '2025-12-10 22:50:36', NULL, 'En Preparación', 43200.00, 0, 17, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(102, 20, '2025-12-10 22:50:37', NULL, 'En Preparación', 43200.00, 0, 18, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(103, 20, '2025-12-10 23:16:30', NULL, 'En Preparación', 98550.00, 0, 18, NULL, 'Pago Completo', 'En Camino', '2025-12-12', 1),
(104, 20, '2025-12-10 23:32:29', NULL, 'En Preparación', 38900.00, 0, 15, NULL, 'Pago Parcial', 'En Camino', '2025-12-12', 1),
(105, 20, '2025-12-11 00:05:36', NULL, 'En Preparación', 37650.00, 0, 18, NULL, 'Pago Parcial', 'En Camino', '2025-12-12', 1),
(106, 20, '2025-12-11 00:26:05', NULL, 'En Preparación', 53200.00, 0, 18, NULL, 'Pago Parcial', 'En Camino', '2025-12-12', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "perfil"
--

CREATE TABLE "perfil" (
  "idProfile" integer NOT NULL,
  "usuario" integer NOT NULL,
  "imagen" character varying(255) DEFAULT NULL,
  "descripcion" longtext DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "productos"
--

CREATE TABLE "productos" (
  "idProducto" bigint NOT NULL,
  "nombreProducto" character varying(50) NOT NULL,
  "precio" decimal(10,2) NOT NULL,
  "descripcion" text DEFAULT NULL,
  "lote" character varying(20) DEFAULT NULL,
  "cantidadDisponible" integer DEFAULT 0,
  "fechaIngreso" timestamp NOT NULL DEFAULT current_timestamp(),
  "fechaVencimiento" date DEFAULT NULL,
  "idCategoria" integer DEFAULT NULL,
  "imagen" character varying(255) DEFAULT NULL,
  "idSubcategoria" integer DEFAULT NULL,
  "stock" integer DEFAULT 0,
  "precio_venta" decimal(10,2) NOT NULL,
  "margen_ganancia" decimal(5,2) DEFAULT 10.00
);

--
-- Volcado de datos para la tabla "productos"
--

INSERT INTO "productos" ("idProducto", "nombreProducto", "precio", "descripcion", "lote", "cantidadDisponible", "fechaIngreso", "fechaVencimiento", "idCategoria", "imagen", "idSubcategoria", "stock", "precio_venta", "margen_ganancia") VALUES
(7700000000001, 'Rubor Rosado Glow', 34000.00, 'Rubor en polvo con acabado satinado y pigmento suave.', 'L2025-11', 50, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/rubor.jpg', 4, 469, 44100.00, 10.00),
(7700000000002, 'Iluminador Perla Glam', 32000.00, 'Ilumina tus mejillas con un brillo nacarado y elegante.', 'L2025-11', 35, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/ilumi_p.webp', 5, 387, 41500.00, 10.00),
(7700000000003, 'Corrector Liquido Soft Touch', 29000.00, 'Cobertura media con textura ligera y acabado natural.', 'L2025-11', 40, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/corrector.avif', 2, 615, 37600.00, 10.00),
(7700000000004, 'Polvo Compacto Mate Glam', 38000.00, 'Controla el brillo con un acabado mate y aterciopelado.', 'L2025-11', 45, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/base_polvo.webp', 3, 526, 49300.00, 10.00),
(7700000000005, 'Base Cushion Glow', 58000.00, 'Base ligera con esponja cushion y efecto luminoso.', 'L2025-11', 30, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/base.png', 1, 336, 75250.00, 11.00),
(7700000000011, 'Sombra Cuarteto Rosa', 42000.00, 'Paleta de 4 tonos rosados con acabado satinado.', 'L2025-11', 50, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/s.jpg', 6, 101, 54500.00, 10.00),
(7700000000012, 'Delineador Liquido Precisio', 18000.00, 'Punta fina para trazos definidos y resistentes al agua.', 'L2025-11', 60, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/delini.webp', 7, 99, 23350.00, 10.00),
(7700000000013, 'Pestañina Curvas Glam', 16000.00, 'Define y curva tus pesta?as con f?rmula ligera.', 'L2025-11', 40, '2025-11-07 07:01:16', '2026-11-01', 2, 'productos/pestanina.webp', 8, 45, 20750.00, 10.00),
(7700000000014, 'Gel para Cejas Natural Brow', 20000.00, 'Fija y da forma a tus cejas con acabado natural.', 'L2025-11', 35, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/pinta_cejaz.avif', 9, 37, 25950.00, 10.00),
(7700000000015, 'Sombra Liquida Glitter Pop', 25000.00, 'Brillo liquido para parpados con efecto multidimensional.', 'L2025-11', 30, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/l.webp', 6, 45, 32450.00, 10.00),
(7700000000021, 'Brillo Labial Cristal', 22000.00, 'Gloss transparente con efecto volumen y aroma a vainilla.', 'L2025-11', 50, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/ll.webp', 11, 11, 28550.00, 10.00),
(7700000000023, 'Balsamo Hidratante Berry Kis', 18000.00, 'Hidratacion profunda con aroma a frutos rojos.', 'L2025-11', -60, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/balsamo.webp', 12, 44, 23350.00, 10.00),
(7700000000024, 'Delineador de Labios Coral Chic', 15000.00, 'Define y realza con precisi?n y suavidad.', 'L2025-11', -14, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/dd.webp', 13, 117, 19450.00, 10.00),
(7700000000025, 'Labial Cremoso Fucsia Pop', 30000.00, 'Color vibrante con textura cremosa y humectante.', 'L2025-11', 45, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/la.webp', 10, 13, 38900.00, 10.00),
(7700000000031, 'Esmalte Rosa Pastel', 12000.00, 'Color suave, f?rmula vegana y secado r?pido.', 'L2025-11', 50, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/esm.webp', 14, 11, 15550.00, 10.00),
(7700000000032, 'Top Coat Brillo Extremo', 14000.00, 'Protecci?n y brillo espejo para tus u?as.', 'L2025-11', 40, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/top.jpg', 15, 5, 18150.00, 10.00),
(7700000000033, 'Tratamiento Fortalecedor', 18000.00, 'Fortalece u?as quebradizas con queratina y calcio.', 'L2025-11', 3, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/tr.webp', 15, 11, 23350.00, 10.00),
(7700000000034, 'Esmalte Glitter Champagne', 15000.00, 'Brillo dorado para un acabado festivo y glamuroso.', 'L2025-11', 35, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/ess.webp', 14, 21, 19450.00, 10.00),
(7700000000035, 'Kit Decoracion de Uñas', 5000.00, 'Piedras, stickers y pinceles para dise?os creativos.', 'L2025-11', 20, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/ki.webp', 16, 101, 6500.00, 10.00),
(7700000000041, 'Set de Brochas Rosa Gold', 48000.00, '10 brochas suaves para rostro y ojos en estuche glam.', 'L2025-11', 25, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/br.webp', 17, 12, 62250.00, 10.00),
(7700000000042, 'Esponja Blender Lavanda', 15000.00, 'Esponja suave para base y corrector, acabado uniforme.', 'L2025-11', 40, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/esp.webp', 18, 15, 19450.00, 10.00),
(7700000000043, 'Pinza de Cejas Glam', 12000.00, 'Precision y diseño ergonomico en acabado metalico rosado.', 'L2025-11', 50, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/pinzas.webp', 9, 16, 15550.00, 10.00),
(7700000000044, 'Organizador Acrilico Mini', 28000.00, 'Guarda tus productos con estilo y orden.', 'L2025-11', 30, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/o.webp', 19, 14, 36300.00, 10.00),
(7700000000045, 'Espejo LED Glam', 35000.00, 'Espejo compacto con luz LED y aumento x5.', 'L2025-11', 20, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/es.jpg', NULL, 55, 45400.00, 10.00),
(7701122334455, 'Labial Mate Velvet Glam', 5000.00, 'Color intenso, textura aterciopelada, larga duraci?n', 'L2025-11', 40, '2025-11-05 15:45:00', '2027-05-05', 3, 'productos/red_velved.jpg', 10, 84, 6500.00, 10.00),
(7701234567890, 'Base Liquida HD Glam', 55000.00, 'Cobertura alta, acabado natural, ideal para piel mixta', 'L2025-10', 25, '2025-11-05 15:45:00', '2027-11-05', 1, 'productos/otra_b.webp', 1, 198, 71350.00, 10.00),
(7709876543210, 'Pestañina Volumen Total Gla', 15000.00, 'Volumen extremo, resistente al agua, f?rmula vegana', 'L2025-11', 30, '2025-11-05 15:45:00', '2026-11-05', 2, 'productos/p.webp', 8, 15, 19450.00, 10.00),
(7709876543220, 'Bronceador trendy', 15000.00, 'Bronceador de trendy', NULL, -10, '2025-11-26 16:24:35', NULL, 1, 'productos/bronceador.jpg', 27, 16, 19450.00, 10.00),
(7709876543221, 'Serum Centella Asiática', 8500.00, 'Serum Centella Asiática Antiedad Calmante Control Poros Tipo De Piel Todo Tipo', NULL, 0, '2025-12-10 19:03:58', NULL, 9, 'productos/Serum_Centella_Asiática_Antiedad_Calmante_Control_Poros_Tipo_De_Piel_Todo_Tipo_h3J3iRp.png', 28, 8, 11050.00, 10.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "repartidores"
--

CREATE TABLE "repartidores" (
  "idRepartidor" integer NOT NULL,
  "nombreRepartidor" character varying(50) DEFAULT NULL,
  "telefono" character varying(20) DEFAULT NULL,
  "estado_turno" character varying(20) DEFAULT 'Disponible',
  "email" character varying(100) DEFAULT NULL
);

--
-- Volcado de datos para la tabla "repartidores"
--

INSERT INTO "repartidores" ("idRepartidor", "nombreRepartidor", "telefono", "estado_turno", "email") VALUES
(15, 'lauren', '3024892804', 'En Ruta', 'laurensamanta0.r@gmail.com'),
(16, 'michael ', '3024892804', 'Disponible', 'michaeldaramirez117@gmail.com'),
(17, 'lauren oo', '+573024892804', 'En Ruta', 'lausamanta2024cha@gmail.com'),
(18, 'lauren sam', '3024892804', 'En Ruta', 'lauren.20031028@gmail.com'),
(19, 'william', '315156165984', 'Disponible', 'fontequin@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "roles"
--

CREATE TABLE "roles" (
  "id_rol" integer NOT NULL,
  "nombre_rol" character varying(20) NOT NULL
);

--
-- Volcado de datos para la tabla "roles"
--

INSERT INTO "roles" ("id_rol", "nombre_rol") VALUES
(1, 'Administrador'),
(2, 'Cliente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "subcategorias"
--

CREATE TABLE "subcategorias" (
  "idSubcategoria" integer NOT NULL,
  "nombreSubcategoria" character varying(50) NOT NULL,
  "idCategoria" integer NOT NULL
);

--
-- Volcado de datos para la tabla "subcategorias"
--

INSERT INTO "subcategorias" ("idSubcategoria", "nombreSubcategoria", "idCategoria") VALUES
(1, 'Base', 1),
(2, 'Correctores', 1),
(3, 'Polvos compactos', 1),
(4, 'Rubores', 1),
(5, 'Iluminadores', 1),
(6, 'Sombras', 2),
(7, 'Delineadores', 2),
(8, 'Pestañas', 2),
(9, 'Cejas', 2),
(10, 'Labiales', 3),
(11, 'Brillos', 3),
(12, 'B?lsamos', 3),
(13, 'Delineadores de labios', 3),
(14, 'Esmaltes', 4),
(15, 'Tratamientos', 4),
(16, 'Decoraci?n', 4),
(17, 'Brochas', 5),
(18, 'Esponjas', 5),
(19, 'Organizadores', 5),
(25, 'espejo', 1),
(27, 'Bronceadores', 1),
(28, 'Serums', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla "usuarios"
--

CREATE TABLE "usuarios" (
  "idUsuario" integer NOT NULL,
  "email" character varying(30) NOT NULL,
  "password" character varying(255) DEFAULT NULL,
  "id_rol" integer NOT NULL,
  "idCliente" integer DEFAULT NULL,
  "fechaCreacion" timestamp NOT NULL DEFAULT current_timestamp(),
  "nombre" character varying(50) DEFAULT NULL,
  "telefono" character varying(20) DEFAULT NULL,
  "direccion" character varying(50) DEFAULT NULL,
  "reset_token" character varying(255) DEFAULT NULL,
  "reset_token_expires" datetime DEFAULT NULL,
  "ultimoAcceso" datetime DEFAULT NULL
);

--
-- Volcado de datos para la tabla "usuarios"
--

INSERT INTO "usuarios" ("idUsuario", "email", "password", "id_rol", "idCliente", "fechaCreacion", "nombre", "telefono", "direccion", "reset_token", "reset_token_expires", "ultimoAcceso") VALUES
(10, 'glamstore0303777@gmail.com', 'pbkdf2_sha256$600000$PpT7bTOmCUOctDntYMUC5K$iLQW1DP7WSCXJQpyNInqAt56x5nvhbHoZD8fGC2kSv8=', 1, NULL, '2025-11-11 05:42:06', 'Glamstore Admin ', '3000000000', 'Calle Glam 123', 'eINBqu8nBwCywbMgLbygwTZxGkmq81a3', '2025-12-10 21:06:41', '2025-12-10 20:35:51'),
(12, 'cliente3@gmail.com', 'pbkdf2_sha256$600000$8TudOY3FCiujKwuPYT4umM$NbSsig85Vt7P+5S15Y9nc/d926fI/jZA33WRDanzi3U=', 2, NULL, '2025-11-13 12:31:42', 'lauren', NULL, NULL, NULL, NULL, NULL),
(13, 'carlos@gmail.com', 'pbkdf2_sha256$600000$8mg0LPZXcRLCP6QcLKJMt5$kr7LUCH3bhJPNvCwRGJuvc6RS4pkkeIkKe1VAP0WLRk=', 2, 13, '2025-11-20 15:29:27', 'william fontecha', NULL, NULL, NULL, NULL, NULL),
(15, 'lala@gmail.com', 'pbkdf2_sha256$600000$7Y5ziRSkMs2SgM2s4IsVTU$7ZGOqbaaiOZHsjC5ADJxvB2oNFpdqNFtyer3CrOCsHY=', 2, 15, '2025-11-20 20:00:54', 'lala', NULL, NULL, NULL, NULL, NULL),
(16, 'lauratorres@gmail.com', 'pbkdf2_sha256$600000$eKBznW1t5RuW3ZvGjZC272$bGZtIpV1xV2d4l9gb1I/xtV7hSmEQccz8RtWMJRfSsY=', 2, 17, '2025-11-21 00:31:04', 'Laura Torres', NULL, NULL, NULL, NULL, NULL),
(17, 'lauratibaque@gmail.com', 'pbkdf2_sha256$600000$EW31JEdw1CAM0cSH6HrGGZ$Hw70/NF/XmEC+L9Xm09yk8zshMutit2l9iLeVG2/wfc=', 2, 18, '2025-11-21 01:09:23', 'laura tibaque', NULL, NULL, NULL, NULL, NULL),
(18, 'laurensamanta0.r@gmail.com', 'pbkdf2_sha256$600000$rXISs5aJsAVneqcIUur5PV$142Pz/E/o7i6bh5hOUjFFkpQMhbgrjFzxd4l1HXW5o8=', 2, 20, '2025-11-22 00:54:06', 'Lauren Samanta Ortiz ', NULL, NULL, NULL, NULL, '2025-12-10 20:21:23'),
(19, 'jeimycontreras11@gmail.com', 'pbkdf2_sha256$600000$sG1heKNYr9XL6z9WpFCfFJ$ZMphBsfGupL0S58xJHh0FNH0YqU9++MNsi6CyBUGl00=', 2, NULL, '2025-11-22 01:51:09', 'jeimy contreras', NULL, NULL, NULL, NULL, NULL),
(20, 'michael@gmail.com', 'pbkdf2_sha256$600000$OcTE5rXFLSMYvikPwl5PK7$34sWZ+wh8y3HeSf3mEHXcxyRudjPlfuLMbtRX1x0yP8=', 2, 22, '2025-11-24 08:27:50', 'michael', NULL, NULL, NULL, NULL, NULL),
(21, 'admin123@glamstore.com', 'pbkdf2_sha256$600000$H6vyXqLqUoINBizXnvyy0c$a0I72ZuNVaMkLAqYPysxkr+IVE7kercJAzzECxFChYs=', 1, NULL, '2025-11-24 13:40:20', 'Lauren Samanta Ortiz ', NULL, NULL, NULL, NULL, '2025-12-10 19:17:58'),
(22, 'alejandro@gmail.com', 'pbkdf2_sha256$600000$jIQApXMzVsRBNRzOiyu37G$GOX1jX5vNWHYTuWQE93jz1odB8uG+AL/RYRQvo3qUMk=', 2, 23, '2025-11-24 11:39:59', 'alejandro', NULL, NULL, NULL, NULL, NULL),
(23, 'lausamanta2024cha@gmail.com', 'pbkdf2_sha256$600000$SbH8Xv3ygscunBND2Xpfiy$HBSa3J1cJb6j9hhUT4zQge5qXs3UBYgNxIWkxbsRoEk=', 2, 25, '2025-11-25 00:40:58', 'magda maria', NULL, NULL, NULL, NULL, NULL),
(24, 'lauren.20031028@gmail.com', 'pbkdf2_sha256$600000$0BxMzoPQJOENk4LUDgqAYd$Yzjlza/jvRWSvkr/XT7C/3soNIMuX9dVy1fqy3OIRzg=', 2, 26, '2025-11-25 00:52:39', 'maria magdalena   socorro', NULL, NULL, NULL, NULL, NULL),
(25, 'andreacontrerlombana@gmail.com', 'pbkdf2_sha256$600000$JaVIAVDxyeDpSTGChaWi43$UUvqtjic8ql8eevQmZZsR0vs4AB2wqmWhdubP80ITu8=', 2, 28, '2025-11-26 18:26:07', 'andrea   contreras', NULL, NULL, NULL, NULL, NULL),
(27, 'infob2bingenieria@gmail.com', 'pbkdf2_sha256$600000$joFeUjGRIwb0ZA7B7tLFUu$G2Oc/3PIQ8OtvaQCTBy1jRRygjVaVLndeqFlyZBvlsE=', 2, 29, '2025-11-30 00:08:17', 'mao b2b', NULL, NULL, NULL, NULL, NULL),
(29, 'haro79874476@gmail.com', 'pbkdf2_sha256$600000$TPZczkhUlC9xyyxiZ1nx69$aMgqbgUyL9pFjsOMRIry2gG21IU1tvSlWIZicWcSFFY=', 1, NULL, '2025-11-30 05:17:14', 'harol', NULL, NULL, NULL, NULL, '2025-12-10 19:18:39'),
(30, 'michaeldaramirez117@gmail.com', 'pbkdf2_sha256$600000$W9cQskZJZLVF4XSyypFrFT$6GmRdyyuaGLuSx80o4PYH+v1SMRK89s114ipQUVKFPA=', 2, 30, '2025-11-30 00:18:08', 'michael', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista "vista_facturas_detalladas"
-- (Véase abajo para la vista actual)
--
CREATE TABLE "vista_facturas_detalladas" (
"idFactura" integer
,"fechaEmision" timestamp
,"estado_factura" character varying(20)
,"montoTotal" decimal(10,2)
,"idPedido" integer
,"cliente" character varying(100)
,"correo_cliente" character varying(100)
,"metodo_pago" character varying(50)
,"descripcion" text
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista "vista_historial_cliente"
-- (Véase abajo para la vista actual)
--
CREATE TABLE "vista_historial_cliente" (
"idCliente" integer
,"cliente" integer
,"email" integer
,"idPedido" integer
,"fechaCreacion" integer
,"fechaEntrega" integer
,"estado" integer
,"total" integer
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista "vista_pedidos_distribuidores"
-- (Véase abajo para la vista actual)
--
CREATE TABLE "vista_pedidos_distribuidores" (
"idDistribuidor" integer
,"distribuidor" integer
,"idPedido" integer
,"fechaCreacion" integer
,"fechaEntrega" integer
,"estado_pedido" integer
,"idCliente" integer
,"cliente" integer
,"direccion_cliente" integer
,"idProducto" integer
,"producto" integer
,"cantidad" integer
,"precio" integer
,"subtotal" integer
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista "vista_pedidos_repartidor"
-- (Véase abajo para la vista actual)
--
CREATE TABLE "vista_pedidos_repartidor" (
"idRepartidor" integer
,"repartidor" integer
,"telefono_repartidor" integer
,"idPedido" integer
,"cliente" integer
,"telefono_cliente" integer
,"direccion_entrega" integer
,"estado_pedido" integer
,"monto_total" integer
,"fechaEntrega" integer
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista "vista_productos_categoria"
-- (Véase abajo para la vista actual)
--
CREATE TABLE "vista_productos_categoria" (
"idProducto" integer
,"nombreProducto" integer
,"precio" integer
,"descripcion" integer
,"cantidadDisponible" integer
,"categoria" integer
,"descripcionCategoria" integer
,"fechaIngreso" integer
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista "vista_productos_distribuidor"
-- (Véase abajo para la vista actual)
--
CREATE TABLE "vista_productos_distribuidor" (
"idDistribuidor" integer
,"distribuidor" integer
,"idProducto" integer
,"producto" integer
,"precio" integer
,"stock" integer
);

-- --------------------------------------------------------

--
-- Estructura para la vista "vista_facturas_detalladas"
--
DROP TABLE IF EXISTS "vista_facturas_detalladas";

CREATE ALGORITHM=UNDEFINED DEFINER="root"@"localhost" SQL SECURITY DEFINER VIEW "vista_facturas_detalladas"  AS SELECT "f"."idFactura" AS "idFactura", "f"."fechaEmision" AS "fechaEmision", "f"."estado" AS "estado_factura", "f"."montoTotal" AS "montoTotal", "p"."idPedido" AS "idPedido", "c"."nombre" AS "cliente", "c"."email" AS "correo_cliente", "m"."tipo" AS "metodo_pago", "m"."descripcion" AS "descripcion" FROM ((("facturas" "f" join "pedidos" "p" on("f"."idPedido" = "p"."idPedido")) join "clientes" "c" on("p"."idCliente" = "c"."idCliente")) left join "metodospago" "m" on("f"."idMetodoPago" = "m"."idMetodoPago")) ;

-- --------------------------------------------------------

--
-- Estructura para la vista "vista_historial_cliente"
--
DROP TABLE IF EXISTS "vista_historial_cliente";

CREATE ALGORITHM=UNDEFINED DEFINER="root"@"localhost" SQL SECURITY DEFINER VIEW "vista_historial_cliente"  AS SELECT 1 AS "idCliente", 1 AS "cliente", 1 AS "email", 1 AS "idPedido", 1 AS "fechaCreacion", 1 AS "fechaEntrega", 1 AS "estado", 1 AS "total" ;

-- --------------------------------------------------------

--
-- Estructura para la vista "vista_pedidos_distribuidores"
--
DROP TABLE IF EXISTS "vista_pedidos_distribuidores";

CREATE ALGORITHM=UNDEFINED DEFINER="root"@"localhost" SQL SECURITY DEFINER VIEW "vista_pedidos_distribuidores"  AS SELECT 1 AS "idDistribuidor", 1 AS "distribuidor", 1 AS "idPedido", 1 AS "fechaCreacion", 1 AS "fechaEntrega", 1 AS "estado_pedido", 1 AS "idCliente", 1 AS "cliente", 1 AS "direccion_cliente", 1 AS "idProducto", 1 AS "producto", 1 AS "cantidad", 1 AS "precio", 1 AS "subtotal" ;

-- --------------------------------------------------------

--
-- Estructura para la vista "vista_pedidos_repartidor"
--
DROP TABLE IF EXISTS "vista_pedidos_repartidor";

CREATE ALGORITHM=UNDEFINED DEFINER="root"@"localhost" SQL SECURITY DEFINER VIEW "vista_pedidos_repartidor"  AS SELECT 1 AS "idRepartidor", 1 AS "repartidor", 1 AS "telefono_repartidor", 1 AS "idPedido", 1 AS "cliente", 1 AS "telefono_cliente", 1 AS "direccion_entrega", 1 AS "estado_pedido", 1 AS "monto_total", 1 AS "fechaEntrega" ;

-- --------------------------------------------------------

--
-- Estructura para la vista "vista_productos_categoria"
--
DROP TABLE IF EXISTS "vista_productos_categoria";

CREATE ALGORITHM=UNDEFINED DEFINER="root"@"localhost" SQL SECURITY DEFINER VIEW "vista_productos_categoria"  AS SELECT 1 AS "idProducto", 1 AS "nombreProducto", 1 AS "precio", 1 AS "descripcion", 1 AS "cantidadDisponible", 1 AS "categoria", 1 AS "descripcionCategoria", 1 AS "fechaIngreso" ;

-- --------------------------------------------------------

--
-- Estructura para la vista "vista_productos_distribuidor"
--
DROP TABLE IF EXISTS "vista_productos_distribuidor";

CREATE ALGORITHM=UNDEFINED DEFINER="root"@"localhost" SQL SECURITY DEFINER VIEW "vista_productos_distribuidor"  AS SELECT 1 AS "idDistribuidor", 1 AS "distribuidor", 1 AS "idProducto", 1 AS "producto", 1 AS "precio", 1 AS "stock" ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla "auth_group"
--
ALTER TABLE "auth_group"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "name" ("name");

--
-- Indices de la tabla "auth_group_permissions"
--
ALTER TABLE "auth_group_permissions"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ("group_id","permission_id"),
  ADD KEY "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" ("permission_id");

--
-- Indices de la tabla "auth_permission"
--
ALTER TABLE "auth_permission"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "auth_permission_content_type_id_codename_01ab375a_uniq" ("content_type_id","codename");

--
-- Indices de la tabla "auth_user"
--
ALTER TABLE "auth_user"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "username" ("username");

--
-- Indices de la tabla "auth_user_groups"
--
ALTER TABLE "auth_user_groups"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "auth_user_groups_user_id_group_id_94350c0c_uniq" ("user_id","group_id"),
  ADD KEY "auth_user_groups_group_id_97559544_fk_auth_group_id" ("group_id");

--
-- Indices de la tabla "auth_user_user_permissions"
--
ALTER TABLE "auth_user_user_permissions"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ("user_id","permission_id"),
  ADD KEY "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" ("permission_id");

--
-- Indices de la tabla "categorias"
--
ALTER TABLE "categorias"
  ADD PRIMARY KEY ("idCategoria");

--
-- Indices de la tabla "clientes"
--
ALTER TABLE "clientes"
  ADD PRIMARY KEY ("idCliente"),
  ADD UNIQUE KEY "email" ("email");

--
-- Indices de la tabla "configuracion_global"
--
ALTER TABLE "configuracion_global"
  ADD PRIMARY KEY ("id");

--
-- Indices de la tabla "confirmaciones_entrega"
--
ALTER TABLE "confirmaciones_entrega"
  ADD PRIMARY KEY ("idConfirmacion"),
  ADD UNIQUE KEY "pedido_id" ("pedido_id"),
  ADD KEY "confirmaciones_entre_repartidor_id_b27e4e23_fk_repartido" ("repartidor_id");

--
-- Indices de la tabla "core_notificacion"
--
ALTER TABLE "core_notificacion"
  ADD PRIMARY KEY ("id"),
  ADD KEY "core_notificacion_usuario_id_f14c4107_fk_auth_user_id" ("usuario_id");

--
-- Indices de la tabla "core_profile"
--
ALTER TABLE "core_profile"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "user_id" ("user_id");

--
-- Indices de la tabla "detallepedido"
--
ALTER TABLE "detallepedido"
  ADD PRIMARY KEY ("idDetalle"),
  ADD KEY "idPedido" ("idPedido"),
  ADD KEY "detallepedido_ibfk_2" ("idProducto");

--
-- Indices de la tabla "distribuidores"
--
ALTER TABLE "distribuidores"
  ADD PRIMARY KEY ("idDistribuidor");

--
-- Indices de la tabla "distribuidorproducto"
--
ALTER TABLE "distribuidorproducto"
  ADD PRIMARY KEY ("idDistribuidor","idProducto"),
  ADD KEY "idProducto" ("idProducto");

--
-- Indices de la tabla "django_admin_log"
--
ALTER TABLE "django_admin_log"
  ADD PRIMARY KEY ("id"),
  ADD KEY "django_admin_log_content_type_id_c4bce8eb_fk_django_co" ("content_type_id"),
  ADD KEY "django_admin_log_user_id_c564eba6_fk_auth_user_id" ("user_id");

--
-- Indices de la tabla "django_content_type"
--
ALTER TABLE "django_content_type"
  ADD PRIMARY KEY ("id"),
  ADD UNIQUE KEY "django_content_type_app_label_model_76bd3d3b_uniq" ("app_label","model");

--
-- Indices de la tabla "django_migrations"
--
ALTER TABLE "django_migrations"
  ADD PRIMARY KEY ("id");

--
-- Indices de la tabla "django_session"
--
ALTER TABLE "django_session"
  ADD PRIMARY KEY ("session_key"),
  ADD KEY "django_session_expire_date_a5c62663" ("expire_date");

--
-- Indices de la tabla "facturas"
--
ALTER TABLE "facturas"
  ADD PRIMARY KEY ("idFactura"),
  ADD KEY "idPedido" ("idPedido"),
  ADD KEY "idMetodoPago" ("idMetodoPago");

--
-- Indices de la tabla "lotes_producto"
--
ALTER TABLE "lotes_producto"
  ADD PRIMARY KEY ("idLote"),
  ADD UNIQUE KEY "lotes_producto_producto_id_codigo_lote_3a023c6e_uniq" ("producto_id","codigo_lote");

--
-- Indices de la tabla "mensajecontacto"
--
ALTER TABLE "mensajecontacto"
  ADD PRIMARY KEY ("id");

--
-- Indices de la tabla "mensajes"
--
ALTER TABLE "mensajes"
  ADD PRIMARY KEY ("idMensaje");

--
-- Indices de la tabla "metodospago"
--
ALTER TABLE "metodospago"
  ADD PRIMARY KEY ("idMetodoPago");

--
-- Indices de la tabla "movimientos_lote"
--
ALTER TABLE "movimientos_lote"
  ADD PRIMARY KEY ("idMovimientoLote"),
  ADD KEY "movimientos_lote_lote_id_29458a65_fk_lotes_producto_idLote" ("lote_id"),
  ADD KEY "movimientos_lote_movimiento_producto__65a07369_fk_movimient" ("movimiento_producto_id");

--
-- Indices de la tabla "movimientos_producto"
--
ALTER TABLE "movimientos_producto"
  ADD PRIMARY KEY ("idMovimiento"),
  ADD KEY "movimientos_producto_idPedido_f819b66b_fk_pedidos_idPedido" ("idPedido"),
  ADD KEY "movimientos_producto_producto_id_a133645f_fk_productos" ("producto_id"),
  ADD KEY "movimientos_producto_lote_origen_id_242d3d70_fk_lotes_pro" ("lote_origen_id");

--
-- Indices de la tabla "notificaciones_problema"
--
ALTER TABLE "notificaciones_problema"
  ADD PRIMARY KEY ("idNotificacion"),
  ADD KEY "notificaciones_problema_idPedido_2316d01a_fk_pedidos_idPedido" ("idPedido");

--
-- Indices de la tabla "notificaciones_reporte"
--
ALTER TABLE "notificaciones_reporte"
  ADD PRIMARY KEY ("idNotificacion");

--
-- Indices de la tabla "pedidoproducto"
--
ALTER TABLE "pedidoproducto"
  ADD PRIMARY KEY ("idPedido","idProducto"),
  ADD KEY "idProducto" ("idProducto");

--
-- Indices de la tabla "pedidos"
--
ALTER TABLE "pedidos"
  ADD PRIMARY KEY ("idPedido"),
  ADD KEY "idCliente" ("idCliente"),
  ADD KEY "idRepartidor" ("idRepartidor"),
  ADD KEY "idx_fecha_vencimiento" ("fechaVencimiento");

--
-- Indices de la tabla "perfil"
--
ALTER TABLE "perfil"
  ADD PRIMARY KEY ("idProfile");

--
-- Indices de la tabla "productos"
--
ALTER TABLE "productos"
  ADD PRIMARY KEY ("idProducto"),
  ADD KEY "fk_productos_categorias" ("idCategoria"),
  ADD KEY "fk_subcategoria_producto" ("idSubcategoria");

--
-- Indices de la tabla "repartidores"
--
ALTER TABLE "repartidores"
  ADD PRIMARY KEY ("idRepartidor");

--
-- Indices de la tabla "roles"
--
ALTER TABLE "roles"
  ADD PRIMARY KEY ("id_rol");

--
-- Indices de la tabla "subcategorias"
--
ALTER TABLE "subcategorias"
  ADD PRIMARY KEY ("idSubcategoria"),
  ADD KEY "idCategoria" ("idCategoria");

--
-- Indices de la tabla "usuarios"
--
ALTER TABLE "usuarios"
  ADD PRIMARY KEY ("idUsuario"),
  ADD UNIQUE KEY "email" ("email"),
  ADD KEY "id_rol" ("id_rol"),
  ADD KEY "idCliente" ("idCliente");

--
-- SERIAL de las tablas volcadas
--

--
-- SERIAL de la tabla "auth_group"
--
ALTER TABLE "auth_group"
  MODIFY "id" integer NOT NULL SERIAL;

--
-- SERIAL de la tabla "auth_group_permissions"
--
ALTER TABLE "auth_group_permissions"
  MODIFY "id" bigint NOT NULL SERIAL;

--
-- SERIAL de la tabla "auth_permission"
--
ALTER TABLE "auth_permission"
  MODIFY "id" integer NOT NULL SERIAL, SERIAL=113;

--
-- SERIAL de la tabla "auth_user"
--
ALTER TABLE "auth_user"
  MODIFY "id" integer NOT NULL SERIAL, SERIAL=13;

--
-- SERIAL de la tabla "auth_user_groups"
--
ALTER TABLE "auth_user_groups"
  MODIFY "id" bigint NOT NULL SERIAL;

--
-- SERIAL de la tabla "auth_user_user_permissions"
--
ALTER TABLE "auth_user_user_permissions"
  MODIFY "id" bigint NOT NULL SERIAL;

--
-- SERIAL de la tabla "categorias"
--
ALTER TABLE "categorias"
  MODIFY "idCategoria" integer NOT NULL SERIAL, SERIAL=10;

--
-- SERIAL de la tabla "clientes"
--
ALTER TABLE "clientes"
  MODIFY "idCliente" integer NOT NULL SERIAL, SERIAL=31;

--
-- SERIAL de la tabla "configuracion_global"
--
ALTER TABLE "configuracion_global"
  MODIFY "id" bigint NOT NULL SERIAL, SERIAL=2;

--
-- SERIAL de la tabla "confirmaciones_entrega"
--
ALTER TABLE "confirmaciones_entrega"
  MODIFY "idConfirmacion" integer NOT NULL SERIAL, SERIAL=6;

--
-- SERIAL de la tabla "core_notificacion"
--
ALTER TABLE "core_notificacion"
  MODIFY "id" bigint NOT NULL SERIAL, SERIAL=4;

--
-- SERIAL de la tabla "core_profile"
--
ALTER TABLE "core_profile"
  MODIFY "id" bigint NOT NULL SERIAL, SERIAL=13;

--
-- SERIAL de la tabla "detallepedido"
--
ALTER TABLE "detallepedido"
  MODIFY "idDetalle" integer NOT NULL SERIAL, SERIAL=185;

--
-- SERIAL de la tabla "distribuidores"
--
ALTER TABLE "distribuidores"
  MODIFY "idDistribuidor" integer NOT NULL SERIAL, SERIAL=8;

--
-- SERIAL de la tabla "django_admin_log"
--
ALTER TABLE "django_admin_log"
  MODIFY "id" integer NOT NULL SERIAL;

--
-- SERIAL de la tabla "django_content_type"
--
ALTER TABLE "django_content_type"
  MODIFY "id" integer NOT NULL SERIAL, SERIAL=29;

--
-- SERIAL de la tabla "django_migrations"
--
ALTER TABLE "django_migrations"
  MODIFY "id" bigint NOT NULL SERIAL, SERIAL=80;

--
-- SERIAL de la tabla "facturas"
--
ALTER TABLE "facturas"
  MODIFY "idFactura" integer NOT NULL SERIAL, SERIAL=7;

--
-- SERIAL de la tabla "lotes_producto"
--
ALTER TABLE "lotes_producto"
  MODIFY "idLote" integer NOT NULL SERIAL, SERIAL=121;

--
-- SERIAL de la tabla "mensajecontacto"
--
ALTER TABLE "mensajecontacto"
  MODIFY "id" bigint NOT NULL SERIAL;

--
-- SERIAL de la tabla "mensajes"
--
ALTER TABLE "mensajes"
  MODIFY "idMensaje" integer NOT NULL SERIAL, SERIAL=6;

--
-- SERIAL de la tabla "metodospago"
--
ALTER TABLE "metodospago"
  MODIFY "idMetodoPago" integer NOT NULL SERIAL, SERIAL=5;

--
-- SERIAL de la tabla "movimientos_lote"
--
ALTER TABLE "movimientos_lote"
  MODIFY "idMovimientoLote" integer NOT NULL SERIAL, SERIAL=19;

--
-- SERIAL de la tabla "movimientos_producto"
--
ALTER TABLE "movimientos_producto"
  MODIFY "idMovimiento" integer NOT NULL SERIAL, SERIAL=330;

--
-- SERIAL de la tabla "notificaciones_problema"
--
ALTER TABLE "notificaciones_problema"
  MODIFY "idNotificacion" integer NOT NULL SERIAL, SERIAL=17;

--
-- SERIAL de la tabla "notificaciones_reporte"
--
ALTER TABLE "notificaciones_reporte"
  MODIFY "idNotificacion" integer NOT NULL SERIAL, SERIAL=6;

--
-- SERIAL de la tabla "pedidos"
--
ALTER TABLE "pedidos"
  MODIFY "idPedido" integer NOT NULL SERIAL, SERIAL=107;

--
-- SERIAL de la tabla "perfil"
--
ALTER TABLE "perfil"
  MODIFY "idProfile" integer NOT NULL SERIAL;

--
-- SERIAL de la tabla "productos"
--
ALTER TABLE "productos"
  MODIFY "idProducto" bigint NOT NULL SERIAL, SERIAL=7709876543222;

--
-- SERIAL de la tabla "repartidores"
--
ALTER TABLE "repartidores"
  MODIFY "idRepartidor" integer NOT NULL SERIAL, SERIAL=20;

--
-- SERIAL de la tabla "roles"
--
ALTER TABLE "roles"
  MODIFY "id_rol" integer NOT NULL SERIAL, SERIAL=3;

--
-- SERIAL de la tabla "subcategorias"
--
ALTER TABLE "subcategorias"
  MODIFY "idSubcategoria" integer NOT NULL SERIAL, SERIAL=29;

--
-- SERIAL de la tabla "usuarios"
--
ALTER TABLE "usuarios"
  MODIFY "idUsuario" integer NOT NULL SERIAL, SERIAL=31;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla "auth_group_permissions"
--
ALTER TABLE "auth_group_permissions"
  ADD CONSTRAINT "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id"),
  ADD CONSTRAINT "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id");

--
-- Filtros para la tabla "auth_permission"
--
ALTER TABLE "auth_permission"
  ADD CONSTRAINT "auth_permission_content_type_id_2f476e4b_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id");

--
-- Filtros para la tabla "auth_user_groups"
--
ALTER TABLE "auth_user_groups"
  ADD CONSTRAINT "auth_user_groups_group_id_97559544_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id"),
  ADD CONSTRAINT "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id");

--
-- Filtros para la tabla "auth_user_user_permissions"
--
ALTER TABLE "auth_user_user_permissions"
  ADD CONSTRAINT "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id"),
  ADD CONSTRAINT "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id");

--
-- Filtros para la tabla "confirmaciones_entrega"
--
ALTER TABLE "confirmaciones_entrega"
  ADD CONSTRAINT "confirmaciones_entre_repartidor_id_b27e4e23_fk_repartido" FOREIGN KEY ("repartidor_id") REFERENCES "repartidores" ("idRepartidor"),
  ADD CONSTRAINT "confirmaciones_entrega_pedido_id_cd3a377b_fk_pedidos_idPedido" FOREIGN KEY ("pedido_id") REFERENCES "pedidos" ("idPedido");

--
-- Filtros para la tabla "core_notificacion"
--
ALTER TABLE "core_notificacion"
  ADD CONSTRAINT "core_notificacion_usuario_id_f14c4107_fk_auth_user_id" FOREIGN KEY ("usuario_id") REFERENCES "auth_user" ("id");

--
-- Filtros para la tabla "detallepedido"
--
ALTER TABLE "detallepedido"
  ADD CONSTRAINT "detallepedido_ibfk_1" FOREIGN KEY ("idPedido") REFERENCES "pedidos" ("idPedido") ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT "detallepedido_ibfk_2" FOREIGN KEY ("idProducto") REFERENCES "productos" ("idProducto");

--
-- Filtros para la tabla "distribuidorproducto"
--
ALTER TABLE "distribuidorproducto"
  ADD CONSTRAINT "distribuidorproducto_ibfk_1" FOREIGN KEY ("idDistribuidor") REFERENCES "distribuidores" ("idDistribuidor");

--
-- Filtros para la tabla "django_admin_log"
--
ALTER TABLE "django_admin_log"
  ADD CONSTRAINT "django_admin_log_content_type_id_c4bce8eb_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id"),
  ADD CONSTRAINT "django_admin_log_user_id_c564eba6_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id");

--
-- Filtros para la tabla "facturas"
--
ALTER TABLE "facturas"
  ADD CONSTRAINT "facturas_ibfk_1" FOREIGN KEY ("idPedido") REFERENCES "pedidos" ("idPedido"),
  ADD CONSTRAINT "facturas_ibfk_2" FOREIGN KEY ("idMetodoPago") REFERENCES "metodospago" ("idMetodoPago");

--
-- Filtros para la tabla "lotes_producto"
--
ALTER TABLE "lotes_producto"
  ADD CONSTRAINT "lotes_producto_producto_id_c48f6919_fk_productos_idProducto" FOREIGN KEY ("producto_id") REFERENCES "productos" ("idProducto");

--
-- Filtros para la tabla "movimientos_lote"
--
ALTER TABLE "movimientos_lote"
  ADD CONSTRAINT "movimientos_lote_lote_id_29458a65_fk_lotes_producto_idLote" FOREIGN KEY ("lote_id") REFERENCES "lotes_producto" ("idLote"),
  ADD CONSTRAINT "movimientos_lote_movimiento_producto__65a07369_fk_movimient" FOREIGN KEY ("movimiento_producto_id") REFERENCES "movimientos_producto" ("idMovimiento");

--
-- Filtros para la tabla "movimientos_producto"
--
ALTER TABLE "movimientos_producto"
  ADD CONSTRAINT "movimientos_producto_idPedido_f819b66b_fk_pedidos_idPedido" FOREIGN KEY ("idPedido") REFERENCES "pedidos" ("idPedido"),
  ADD CONSTRAINT "movimientos_producto_lote_origen_id_242d3d70_fk_lotes_pro" FOREIGN KEY ("lote_origen_id") REFERENCES "lotes_producto" ("idLote"),
  ADD CONSTRAINT "movimientos_producto_producto_id_a133645f_fk_productos" FOREIGN KEY ("producto_id") REFERENCES "productos" ("idProducto");

--
-- Filtros para la tabla "notificaciones_problema"
--
ALTER TABLE "notificaciones_problema"
  ADD CONSTRAINT "notificaciones_problema_idPedido_2316d01a_fk_pedidos_idPedido" FOREIGN KEY ("idPedido") REFERENCES "pedidos" ("idPedido");

--
-- Filtros para la tabla "pedidoproducto"
--
ALTER TABLE "pedidoproducto"
  ADD CONSTRAINT "pedidoproducto_ibfk_1" FOREIGN KEY ("idPedido") REFERENCES "pedidos" ("idPedido"),
  ADD CONSTRAINT "pedidoproducto_ibfk_2" FOREIGN KEY ("idProducto") REFERENCES "productos" ("idProducto");

--
-- Filtros para la tabla "pedidos"
--
ALTER TABLE "pedidos"
  ADD CONSTRAINT "pedidos_ibfk_1" FOREIGN KEY ("idCliente") REFERENCES "clientes" ("idCliente"),
  ADD CONSTRAINT "pedidos_ibfk_2" FOREIGN KEY ("idRepartidor") REFERENCES "repartidores" ("idRepartidor");

--
-- Filtros para la tabla "productos"
--
ALTER TABLE "productos"
  ADD CONSTRAINT "fk_categoria_producto" FOREIGN KEY ("idCategoria") REFERENCES "categorias" ("idCategoria") ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT "fk_productos_categorias" FOREIGN KEY ("idCategoria") REFERENCES "categorias" ("idCategoria") ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT "fk_subcategoria_producto" FOREIGN KEY ("idSubcategoria") REFERENCES "subcategorias" ("idSubcategoria");

--
-- Filtros para la tabla "subcategorias"
--
ALTER TABLE "subcategorias"
  ADD CONSTRAINT "subcategorias_ibfk_1" FOREIGN KEY ("idCategoria") REFERENCES "categorias" ("idCategoria");

--
-- Filtros para la tabla "usuarios"
--
ALTER TABLE "usuarios"
  ADD CONSTRAINT "usuarios_ibfk_1" FOREIGN KEY ("id_rol") REFERENCES "roles" ("id_rol"),
  ADD CONSTRAINT "usuarios_ibfk_2" FOREIGN KEY ("idCliente") REFERENCES "clientes" ("idCliente");
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
