-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-10-2022 a las 17:52:11
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `inventario_it`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
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
(25, 'Can add departamentos', 7, 'add_departamentos'),
(26, 'Can change departamentos', 7, 'change_departamentos'),
(27, 'Can delete departamentos', 7, 'delete_departamentos'),
(28, 'Can view departamentos', 7, 'view_departamentos'),
(29, 'Can add departamentos empresas', 8, 'add_departamentosempresas'),
(30, 'Can change departamentos empresas', 8, 'change_departamentosempresas'),
(31, 'Can delete departamentos empresas', 8, 'delete_departamentosempresas'),
(32, 'Can view departamentos empresas', 8, 'view_departamentosempresas'),
(33, 'Can add empresas', 9, 'add_empresas'),
(34, 'Can change empresas', 9, 'change_empresas'),
(35, 'Can delete empresas', 9, 'delete_empresas'),
(36, 'Can view empresas', 9, 'view_empresas'),
(37, 'Can add marcas', 10, 'add_marcas'),
(38, 'Can change marcas', 10, 'change_marcas'),
(39, 'Can delete marcas', 10, 'delete_marcas'),
(40, 'Can view marcas', 10, 'view_marcas'),
(41, 'Can add tipos_equipos', 11, 'add_tipos_equipos'),
(42, 'Can change tipos_equipos', 11, 'change_tipos_equipos'),
(43, 'Can delete tipos_equipos', 11, 'delete_tipos_equipos'),
(44, 'Can view tipos_equipos', 11, 'view_tipos_equipos'),
(45, 'Can add ubicaciones', 12, 'add_ubicaciones'),
(46, 'Can change ubicaciones', 12, 'change_ubicaciones'),
(47, 'Can delete ubicaciones', 12, 'delete_ubicaciones'),
(48, 'Can view ubicaciones', 12, 'view_ubicaciones'),
(49, 'Can add usuarios', 13, 'add_usuarios'),
(50, 'Can change usuarios', 13, 'change_usuarios'),
(51, 'Can delete usuarios', 13, 'delete_usuarios'),
(52, 'Can view usuarios', 13, 'view_usuarios'),
(53, 'Can add tipos_equipos_marcas', 14, 'add_tipos_equipos_marcas'),
(54, 'Can change tipos_equipos_marcas', 14, 'change_tipos_equipos_marcas'),
(55, 'Can delete tipos_equipos_marcas', 14, 'delete_tipos_equipos_marcas'),
(56, 'Can view tipos_equipos_marcas', 14, 'view_tipos_equipos_marcas'),
(57, 'Can add modelos', 15, 'add_modelos'),
(58, 'Can change modelos', 15, 'change_modelos'),
(59, 'Can delete modelos', 15, 'delete_modelos'),
(60, 'Can view modelos', 15, 'view_modelos'),
(61, 'Can add informacion', 16, 'add_informacion'),
(62, 'Can change informacion', 16, 'change_informacion'),
(63, 'Can delete informacion', 16, 'delete_informacion'),
(64, 'Can view informacion', 16, 'view_informacion'),
(65, 'Can add impresoras', 17, 'add_impresoras'),
(66, 'Can change impresoras', 17, 'change_impresoras'),
(67, 'Can delete impresoras', 17, 'delete_impresoras'),
(68, 'Can view impresoras', 17, 'view_impresoras'),
(69, 'Can add dispositivos', 18, 'add_dispositivos'),
(70, 'Can change dispositivos', 18, 'change_dispositivos'),
(71, 'Can delete dispositivos', 18, 'delete_dispositivos'),
(72, 'Can view dispositivos', 18, 'view_dispositivos'),
(73, 'Can add equipos', 19, 'add_equipos'),
(74, 'Can change equipos', 19, 'change_equipos'),
(75, 'Can delete equipos', 19, 'delete_equipos'),
(76, 'Can view equipos', 19, 'view_equipos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'it', 'departamentos'),
(8, 'it', 'departamentosempresas'),
(18, 'it', 'dispositivos'),
(9, 'it', 'empresas'),
(19, 'it', 'equipos'),
(17, 'it', 'impresoras'),
(16, 'it', 'informacion'),
(10, 'it', 'marcas'),
(15, 'it', 'modelos'),
(11, 'it', 'tipos_equipos'),
(14, 'it', 'tipos_equipos_marcas'),
(12, 'it', 'ubicaciones'),
(13, 'it', 'usuarios'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-10-27 15:01:53.507884'),
(2, 'auth', '0001_initial', '2022-10-27 15:02:03.321974'),
(3, 'admin', '0001_initial', '2022-10-27 15:02:05.658632'),
(4, 'admin', '0002_logentry_remove_auto_add', '2022-10-27 15:02:05.915842'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2022-10-27 15:02:06.099306'),
(6, 'contenttypes', '0002_remove_content_type_name', '2022-10-27 15:02:06.774485'),
(7, 'auth', '0002_alter_permission_name_max_length', '2022-10-27 15:02:07.654122'),
(8, 'auth', '0003_alter_user_email_max_length', '2022-10-27 15:02:07.799582'),
(9, 'auth', '0004_alter_user_username_opts', '2022-10-27 15:02:07.853600'),
(10, 'auth', '0005_alter_user_last_login_null', '2022-10-27 15:02:08.899632'),
(11, 'auth', '0006_require_contenttypes_0002', '2022-10-27 15:02:08.936661'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2022-10-27 15:02:08.998569'),
(13, 'auth', '0008_alter_user_username_max_length', '2022-10-27 15:02:09.127338'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2022-10-27 15:02:09.323153'),
(15, 'auth', '0010_alter_group_name_max_length', '2022-10-27 15:02:09.472140'),
(16, 'auth', '0011_update_proxy_permissions', '2022-10-27 15:02:09.544984'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2022-10-27 15:02:09.655169'),
(18, 'it', '0001_initial', '2022-10-27 15:02:29.663960'),
(19, 'sessions', '0001_initial', '2022-10-27 15:02:30.180468'),
(20, 'it', '0002_tipos_equipos_marcas', '2022-10-27 15:22:12.057483');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_departamentos`
--

CREATE TABLE `it_departamentos` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `it_departamentos`
--

INSERT INTO `it_departamentos` (`id`, `nombre`) VALUES
(1, 'IT'),
(2, 'RRHH'),
(3, 'Procura'),
(4, 'Finanzas'),
(5, 'Administracion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_departamentosempresas`
--

CREATE TABLE `it_departamentosempresas` (
  `id` bigint(20) NOT NULL,
  `departamentosforeignkey_id` bigint(20) NOT NULL,
  `empresasforeignkey_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `it_departamentosempresas`
--

INSERT INTO `it_departamentosempresas` (`id`, `departamentosforeignkey_id`, `empresasforeignkey_id`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 1, 2),
(5, 4, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_dispositivos`
--

CREATE TABLE `it_dispositivos` (
  `id` bigint(20) NOT NULL,
  `serial` varchar(45) NOT NULL,
  `informacionforeignkey_id` bigint(20) DEFAULT NULL,
  `modelosforeignkey_id` bigint(20) DEFAULT NULL,
  `usuariosforeignkey_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_empresas`
--

CREATE TABLE `it_empresas` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `it_empresas`
--

INSERT INTO `it_empresas` (`id`, `nombre`) VALUES
(1, 'Yaracal'),
(2, 'JAC'),
(3, 'Auto Partes Lara');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_equipos`
--

CREATE TABLE `it_equipos` (
  `id_id` bigint(20) NOT NULL,
  `tipo_equipo` varchar(45) NOT NULL,
  `serial` varchar(45) NOT NULL,
  `serial_unidad` varchar(45) NOT NULL,
  `serial_cargador` varchar(45) NOT NULL,
  `csb` varchar(45) NOT NULL,
  `dd` varchar(45) NOT NULL,
  `ram` varchar(45) NOT NULL,
  `tipo_ram` varchar(45) NOT NULL,
  `antivirus` varchar(45) NOT NULL,
  `so` varchar(45) NOT NULL,
  `usuario_so` varchar(45) NOT NULL,
  `empresasforeignkey_id` bigint(20) DEFAULT NULL,
  `modelosforeignkey_id` bigint(20) NOT NULL,
  `usuariosforeignkey_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_impresoras`
--

CREATE TABLE `it_impresoras` (
  `id` bigint(20) NOT NULL,
  `codigo_inventario` varchar(45) NOT NULL,
  `serial` varchar(45) NOT NULL,
  `csb` varchar(45) NOT NULL,
  `cbc` varchar(45) NOT NULL,
  `tipo_impresion` varchar(45) NOT NULL,
  `tipo_conexion` varchar(45) NOT NULL,
  `ip` varchar(45) NOT NULL,
  `propiedad` varchar(45) NOT NULL,
  `informacionforeignkey_id` bigint(20) DEFAULT NULL,
  `modelosforeignkey_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_informacion`
--

CREATE TABLE `it_informacion` (
  `id` bigint(20) NOT NULL,
  `estatus` varchar(45) NOT NULL,
  `asignacion` varchar(45) NOT NULL,
  `observacion` longtext NOT NULL,
  `ubicacionesforeignkey_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_marcas`
--

CREATE TABLE `it_marcas` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_modelos`
--

CREATE TABLE `it_modelos` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `tipos_equipos_marcas_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_tipos_equipos`
--

CREATE TABLE `it_tipos_equipos` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_tipos_equipos_marcas`
--

CREATE TABLE `it_tipos_equipos_marcas` (
  `id` bigint(20) NOT NULL,
  `marcasforeignkey_id` bigint(20) DEFAULT NULL,
  `tipos_equiposforeignkey_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_ubicaciones`
--

CREATE TABLE `it_ubicaciones` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `it_usuarios`
--

CREATE TABLE `it_usuarios` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `cargo` varchar(45) NOT NULL,
  `departamentosEmpresasforeignfey_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `it_departamentos`
--
ALTER TABLE `it_departamentos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `it_departamentosempresas`
--
ALTER TABLE `it_departamentosempresas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_departamentosempr_empresasforeignkey_i_5edad373_fk_it_empres` (`empresasforeignkey_id`),
  ADD KEY `it_departamentosempr_departamentosforeign_c6ebd2f8_fk_it_depart` (`departamentosforeignkey_id`);

--
-- Indices de la tabla `it_dispositivos`
--
ALTER TABLE `it_dispositivos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_dispositivos_informacionforeignke_8f4f2080_fk_it_inform` (`informacionforeignkey_id`),
  ADD KEY `it_dispositivos_modelosforeignkey_id_1b054888_fk_it_modelos_id` (`modelosforeignkey_id`),
  ADD KEY `it_dispositivos_usuariosforeignkey_id_e3cc0f6a_fk_it_usuarios_id` (`usuariosforeignkey_id`);

--
-- Indices de la tabla `it_empresas`
--
ALTER TABLE `it_empresas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `it_equipos`
--
ALTER TABLE `it_equipos`
  ADD PRIMARY KEY (`id_id`),
  ADD KEY `it_equipos_empresasforeignkey_id_5b720653_fk_it_empresas_id` (`empresasforeignkey_id`),
  ADD KEY `it_equipos_modelosforeignkey_id_13ea58d9_fk_it_modelos_id` (`modelosforeignkey_id`),
  ADD KEY `it_equipos_usuariosforeignkey_id_6a2ca1ea_fk_it_usuarios_id` (`usuariosforeignkey_id`);

--
-- Indices de la tabla `it_impresoras`
--
ALTER TABLE `it_impresoras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_impresoras_informacionforeignke_f8f40f1b_fk_it_inform` (`informacionforeignkey_id`),
  ADD KEY `it_impresoras_modelosforeignkey_id_c4bb4312_fk_it_modelos_id` (`modelosforeignkey_id`);

--
-- Indices de la tabla `it_informacion`
--
ALTER TABLE `it_informacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_informacion_ubicacionesforeignke_97341117_fk_it_ubicac` (`ubicacionesforeignkey_id`);

--
-- Indices de la tabla `it_marcas`
--
ALTER TABLE `it_marcas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `it_modelos`
--
ALTER TABLE `it_modelos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_modelos_tipos_equipos_marcas_fdc153a2_fk_it_tipos_` (`tipos_equipos_marcas_id`);

--
-- Indices de la tabla `it_tipos_equipos`
--
ALTER TABLE `it_tipos_equipos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `it_tipos_equipos_marcas`
--
ALTER TABLE `it_tipos_equipos_marcas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_tipos_equipos_mar_marcasforeignkey_id_40f07749_fk_it_marcas` (`marcasforeignkey_id`),
  ADD KEY `it_tipos_equipos_mar_tipos_equiposforeign_29816146_fk_it_tipos_` (`tipos_equiposforeignkey_id`);

--
-- Indices de la tabla `it_ubicaciones`
--
ALTER TABLE `it_ubicaciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `it_usuarios`
--
ALTER TABLE `it_usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `it_usuarios_departamentosEmpresa_b9cafc86_fk_it_depart` (`departamentosEmpresasforeignfey_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `it_departamentos`
--
ALTER TABLE `it_departamentos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `it_departamentosempresas`
--
ALTER TABLE `it_departamentosempresas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `it_dispositivos`
--
ALTER TABLE `it_dispositivos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_empresas`
--
ALTER TABLE `it_empresas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `it_impresoras`
--
ALTER TABLE `it_impresoras`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_informacion`
--
ALTER TABLE `it_informacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_marcas`
--
ALTER TABLE `it_marcas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_modelos`
--
ALTER TABLE `it_modelos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_tipos_equipos`
--
ALTER TABLE `it_tipos_equipos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_tipos_equipos_marcas`
--
ALTER TABLE `it_tipos_equipos_marcas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_ubicaciones`
--
ALTER TABLE `it_ubicaciones`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `it_usuarios`
--
ALTER TABLE `it_usuarios`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `it_departamentosempresas`
--
ALTER TABLE `it_departamentosempresas`
  ADD CONSTRAINT `it_departamentosempr_departamentosforeign_c6ebd2f8_fk_it_depart` FOREIGN KEY (`departamentosforeignkey_id`) REFERENCES `it_departamentos` (`id`),
  ADD CONSTRAINT `it_departamentosempr_empresasforeignkey_i_5edad373_fk_it_empres` FOREIGN KEY (`empresasforeignkey_id`) REFERENCES `it_empresas` (`id`);

--
-- Filtros para la tabla `it_dispositivos`
--
ALTER TABLE `it_dispositivos`
  ADD CONSTRAINT `it_dispositivos_informacionforeignke_8f4f2080_fk_it_inform` FOREIGN KEY (`informacionforeignkey_id`) REFERENCES `it_informacion` (`id`),
  ADD CONSTRAINT `it_dispositivos_modelosforeignkey_id_1b054888_fk_it_modelos_id` FOREIGN KEY (`modelosforeignkey_id`) REFERENCES `it_modelos` (`id`),
  ADD CONSTRAINT `it_dispositivos_usuariosforeignkey_id_e3cc0f6a_fk_it_usuarios_id` FOREIGN KEY (`usuariosforeignkey_id`) REFERENCES `it_usuarios` (`id`);

--
-- Filtros para la tabla `it_equipos`
--
ALTER TABLE `it_equipos`
  ADD CONSTRAINT `it_equipos_empresasforeignkey_id_5b720653_fk_it_empresas_id` FOREIGN KEY (`empresasforeignkey_id`) REFERENCES `it_empresas` (`id`),
  ADD CONSTRAINT `it_equipos_id_id_6b68c797_fk_it_informacion_id` FOREIGN KEY (`id_id`) REFERENCES `it_informacion` (`id`),
  ADD CONSTRAINT `it_equipos_modelosforeignkey_id_13ea58d9_fk_it_modelos_id` FOREIGN KEY (`modelosforeignkey_id`) REFERENCES `it_modelos` (`id`),
  ADD CONSTRAINT `it_equipos_usuariosforeignkey_id_6a2ca1ea_fk_it_usuarios_id` FOREIGN KEY (`usuariosforeignkey_id`) REFERENCES `it_usuarios` (`id`);

--
-- Filtros para la tabla `it_impresoras`
--
ALTER TABLE `it_impresoras`
  ADD CONSTRAINT `it_impresoras_informacionforeignke_f8f40f1b_fk_it_inform` FOREIGN KEY (`informacionforeignkey_id`) REFERENCES `it_informacion` (`id`),
  ADD CONSTRAINT `it_impresoras_modelosforeignkey_id_c4bb4312_fk_it_modelos_id` FOREIGN KEY (`modelosforeignkey_id`) REFERENCES `it_modelos` (`id`);

--
-- Filtros para la tabla `it_informacion`
--
ALTER TABLE `it_informacion`
  ADD CONSTRAINT `it_informacion_ubicacionesforeignke_97341117_fk_it_ubicac` FOREIGN KEY (`ubicacionesforeignkey_id`) REFERENCES `it_ubicaciones` (`id`);

--
-- Filtros para la tabla `it_modelos`
--
ALTER TABLE `it_modelos`
  ADD CONSTRAINT `it_modelos_tipos_equipos_marcas_fdc153a2_fk_it_tipos_` FOREIGN KEY (`tipos_equipos_marcas_id`) REFERENCES `it_tipos_equipos_marcas` (`id`);

--
-- Filtros para la tabla `it_tipos_equipos_marcas`
--
ALTER TABLE `it_tipos_equipos_marcas`
  ADD CONSTRAINT `it_tipos_equipos_mar_marcasforeignkey_id_40f07749_fk_it_marcas` FOREIGN KEY (`marcasforeignkey_id`) REFERENCES `it_marcas` (`id`),
  ADD CONSTRAINT `it_tipos_equipos_mar_tipos_equiposforeign_29816146_fk_it_tipos_` FOREIGN KEY (`tipos_equiposforeignkey_id`) REFERENCES `it_tipos_equipos` (`id`);

--
-- Filtros para la tabla `it_usuarios`
--
ALTER TABLE `it_usuarios`
  ADD CONSTRAINT `it_usuarios_departamentosEmpresa_b9cafc86_fk_it_depart` FOREIGN KEY (`departamentosEmpresasforeignfey_id`) REFERENCES `it_departamentosempresas` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
