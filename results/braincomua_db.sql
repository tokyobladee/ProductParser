-- PostgreSQL database dump for braincomua_db
-- Dump created for project results without connection secrets

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;

-- Table: auth_group
DROP TABLE IF EXISTS "auth_group" CASCADE;
CREATE TABLE "auth_group" (
"id" INTEGER NOT NULL,
"name" CHARACTER VARYING(150) NOT NULL,
    PRIMARY KEY ("id")
);


-- Table: auth_group_permissions
DROP TABLE IF EXISTS "auth_group_permissions" CASCADE;
CREATE TABLE "auth_group_permissions" (
"id" BIGINT NOT NULL,
"group_id" INTEGER NOT NULL,
"permission_id" INTEGER NOT NULL,
    PRIMARY KEY ("id")
);


-- Table: auth_permission
DROP TABLE IF EXISTS "auth_permission" CASCADE;
CREATE TABLE "auth_permission" (
"id" INTEGER NOT NULL,
"name" CHARACTER VARYING(255) NOT NULL,
"content_type_id" INTEGER NOT NULL,
"codename" CHARACTER VARYING(100) NOT NULL,
    PRIMARY KEY ("id")
);

INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (25, 'Can add product', 7, 'add_product');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (26, 'Can change product', 7, 'change_product');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (27, 'Can delete product', 7, 'delete_product');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (28, 'Can view product', 7, 'view_product');

-- Table: auth_user
DROP TABLE IF EXISTS "auth_user" CASCADE;
CREATE TABLE "auth_user" (
"id" INTEGER NOT NULL,
"password" CHARACTER VARYING(128) NOT NULL,
"last_login" TIMESTAMP WITH TIME ZONE NULL,
"is_superuser" BOOLEAN NOT NULL,
"username" CHARACTER VARYING(150) NOT NULL,
"first_name" CHARACTER VARYING(150) NOT NULL,
"last_name" CHARACTER VARYING(150) NOT NULL,
"email" CHARACTER VARYING(254) NOT NULL,
"is_staff" BOOLEAN NOT NULL,
"is_active" BOOLEAN NOT NULL,
"date_joined" TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY ("id")
);


-- Table: auth_user_groups
DROP TABLE IF EXISTS "auth_user_groups" CASCADE;
CREATE TABLE "auth_user_groups" (
"id" BIGINT NOT NULL,
"user_id" INTEGER NOT NULL,
"group_id" INTEGER NOT NULL,
    PRIMARY KEY ("id")
);


-- Table: auth_user_user_permissions
DROP TABLE IF EXISTS "auth_user_user_permissions" CASCADE;
CREATE TABLE "auth_user_user_permissions" (
"id" BIGINT NOT NULL,
"user_id" INTEGER NOT NULL,
"permission_id" INTEGER NOT NULL,
    PRIMARY KEY ("id")
);


-- Table: django_admin_log
DROP TABLE IF EXISTS "django_admin_log" CASCADE;
CREATE TABLE "django_admin_log" (
"id" INTEGER NOT NULL,
"action_time" TIMESTAMP WITH TIME ZONE NOT NULL,
"object_id" TEXT NULL,
"object_repr" CHARACTER VARYING(200) NOT NULL,
"action_flag" SMALLINT NOT NULL,
"change_message" TEXT NOT NULL,
"content_type_id" INTEGER NULL,
"user_id" INTEGER NOT NULL,
    PRIMARY KEY ("id")
);


-- Table: django_content_type
DROP TABLE IF EXISTS "django_content_type" CASCADE;
CREATE TABLE "django_content_type" (
"id" INTEGER NOT NULL,
"app_label" CHARACTER VARYING(100) NOT NULL,
"model" CHARACTER VARYING(100) NOT NULL,
    PRIMARY KEY ("id")
);

INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (1, 'admin', 'logentry');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (2, 'auth', 'permission');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (3, 'auth', 'group');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (4, 'auth', 'user');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (6, 'sessions', 'session');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (7, 'parser_app', 'product');

-- Table: django_migrations
DROP TABLE IF EXISTS "django_migrations" CASCADE;
CREATE TABLE "django_migrations" (
"id" BIGINT NOT NULL,
"app" CHARACTER VARYING(255) NOT NULL,
"name" CHARACTER VARYING(255) NOT NULL,
"applied" TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY ("id")
);

INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (1, 'contenttypes', '0001_initial', '2026-08-12 21:56:45.007497+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (2, 'auth', '0001_initial', '2026-08-12 21:56:45.066914+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (3, 'admin', '0001_initial', '2026-08-12 21:56:45.084161+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2026-08-12 21:56:45.089222+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-12 21:56:45.094220+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2026-08-12 21:56:45.105783+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2026-08-12 21:56:45.112320+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (8, 'auth', '0003_alter_user_email_max_length', '2026-08-12 21:56:45.118325+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (9, 'auth', '0004_alter_user_username_opts', '2026-08-12 21:56:45.123338+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (10, 'auth', '0005_alter_user_last_login_null', '2026-08-12 21:56:45.126851+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (11, 'auth', '0006_require_contenttypes_0002', '2026-08-12 21:56:45.128358+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2026-08-12 21:56:45.133369+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (13, 'auth', '0008_alter_user_username_max_length', '2026-08-12 21:56:45.143400+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2026-08-12 21:56:45.148427+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (15, 'auth', '0010_alter_group_name_max_length', '2026-08-12 21:56:45.154450+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (16, 'auth', '0011_update_proxy_permissions', '2026-08-12 21:56:45.158466+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2026-08-12 21:56:45.164474+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (18, 'sessions', '0001_initial', '2026-08-12 21:56:45.172084+00:00');
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (19, 'parser_app', '0001_initial', '2026-08-12 22:00:49.720507+00:00');

-- Table: django_session
DROP TABLE IF EXISTS "django_session" CASCADE;
CREATE TABLE "django_session" (
"session_key" CHARACTER VARYING(40) NOT NULL,
"session_data" TEXT NOT NULL,
"expire_date" TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY ("session_key")
);


-- Table: parser_app_product
DROP TABLE IF EXISTS "parser_app_product" CASCADE;
CREATE TABLE "parser_app_product" (
"id" BIGINT NOT NULL,
"parser_type" CHARACTER VARYING(32) NULL,
"source_url" CHARACTER VARYING(2048) NULL,
"full_name" CHARACTER VARYING(500) NULL,
"color" CHARACTER VARYING(255) NULL,
"memory_capacity" CHARACTER VARYING(255) NULL,
"manufacturer" CHARACTER VARYING(255) NULL,
"regular_price" CHARACTER VARYING(100) NULL,
"promotional_price" CHARACTER VARYING(100) NULL,
"image_urls" ARRAY NULL,
"product_code" CHARACTER VARYING(100) NULL,
"review_count" INTEGER NULL,
"screen_diagonal" CHARACTER VARYING(100) NULL,
"display_resolution" CHARACTER VARYING(100) NULL,
"characteristics" JSONB NULL,
    PRIMARY KEY ("id")
);

INSERT INTO "parser_app_product" ("id", "parser_type", "source_url", "full_name", "color", "memory_capacity", "manufacturer", "regular_price", "promotional_price", "image_urls", "product_code", "review_count", "screen_diagonal", "display_resolution", "characteristics") VALUES (4, NULL, 'https://example.com/django-integration-check', 'Django Integration Check', NULL, NULL, NULL, NULL, NULL, '["https://example.com/django-integration-check.jpg"]', 'DJANGO-INTEGRATION-CHECK', NULL, NULL, NULL, '{"purpose": "Django integration check"}');
INSERT INTO "parser_app_product" ("id", "parser_type", "source_url", "full_name", "color", "memory_capacity", "manufacturer", "regular_price", "promotional_price", "image_urls", "product_code", "review_count", "screen_diagonal", "display_resolution", "characteristics") VALUES (6, 'requests_bs4', 'https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html', 'Мобільний телефон Apple iPhone 16 Pro Max 256GB Black Titanium (MYWV3)', 'чорний', '256 Gb', 'Apple', '65 799 ₴', NULL, '["https://brain.com.ua/static/images/prod_img/3/0/U0961530_big_1738426632.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_2big_1738426633.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_3big_1738426634.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_4big_1738426635.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_5big_1738426637.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_6big_1738426638.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_7big_1738426639.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_8big_1738426640.jpg", "https://brain.com.ua/static/images/prod_img/3/0/U0961530_9big_1738426642.jpg"]', 'U0961530', 1, '6.9"', '1320 х 2868', '{"Вага": "227 г", "Колір": "чорний", "Безпека": "FaceID", "Виробник": "Apple", "Примітка": "Виробник може змінювати властивості, характеристики, зовнішній вигляд і комплектацію товарів без попередження", "Процесор": "Apple A18 Pro", "Штрихкод": "195949805783", "Відеоядро": "Apple Ax Series", "Навігація": "iBeacon, BeiDou, Galileo, QZSS, GPS, A-GPS", "Оснащення": "пило/вологозахист, гіроскоп", "Органайзер": "нотатки, телефонна книга, диктофон, секундомір, калькулятор, світовий час, годинник, календар, будильник", "Розміри (мм)": "163 х 77.6 х 8.25 мм", "Тип дисплея": "OLED (Super Retina XDR)", "Форм-фактор": "моноблок", "Мультимедіа": "ігри, мобільні сервіси Google, соціальні мережі, відеоплеєр, музичний плеєр", "Особливості": "IP68 certified", "Гарантія, міс": "12", "Кількість ядер": "6 core", "Основна камера": "48 + 48 + 12 Mpx", "Формат SIM-карти": "Nano, e-sim", "Функції камери": "розпізнавання обличчя, геотегінг, HDR, панорама, спалах, автофокус", "Матеріал екрану": "Ceramic Shield", "Діагональ екрану": "6.9\"", "Кількість SIM-карт": "1 SIM + e-sim", "Матеріал корпуса": "титан, алюміній", "Вбудована пам''ять": "256 Gb", "Вбудовані датчики": "датчик освітлення, компас, акселерометр, датчик наближення, гіроскоп, барометр", "Фронтальна камера": "12 Mpx", "Країна виробництва": "Китай", "Метод стабілізації": "оптична", "Операційна система": "iOS 18", "Особливості корпусу": "безрамковий дисплей, водонепроникні", "Бездротові технології": "бездротова зарядка, WI-FI, Bluetooth, NFC", "Інтерфейси і підключення": "USB Type-C", "Частота оновлення екрану": "120 Гц", "Покоління зв''язку (2G /3G/4G/5G)": "2G, 3G, 4G, 5G", "Діафрагма основної камери": "f/1.78 + f/2.2 + f/2.8", "Роздільна здатність екрану": "1320 х 2868", "Запис відео основної камери": "4K / 3840x2160 / стереозвук", "Діафрагма фронтальної камери": "f/1.9", "Запис відео фронтальної камери": "4K / 3840x2160 / стереозвук", "Кількість модулів основної камери": "3", "Кількість модулів фронтальної камери": "1"}');
INSERT INTO "parser_app_product" ("id", "parser_type", "source_url", "full_name", "color", "memory_capacity", "manufacturer", "regular_price", "promotional_price", "image_urls", "product_code", "review_count", "screen_diagonal", "display_resolution", "characteristics") VALUES (8, 'selenium', 'https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_15_128GB_Black-p1044347.html', 'Мобільний телефон Apple iPhone 15 128GB Black (MTP03)', 'чорний', '128 Gb', 'Apple', '32 999 ₴', '29 999 ₴', '["https://brain.com.ua/static/images/prod_img/8/9/U0854689_2big_1739047984.jpg", "https://brain.com.ua/static/images/prod_img/8/9/U0854689_3big_1739047985.jpg", "https://brain.com.ua/static/images/prod_img/8/9/U0854689_big_1739047983.jpg"]', 'U0854689', 1, '6.1"', '1179 х 2556', '{"Вага": "171 г", "Колір": "чорний", "Безпека": "FaceID", "Виробник": "Apple", "Примітка": "Виробник може змінювати властивості, характеристики, зовнішній вигляд і комплектацію товарів без попередження", "Процесор": "Apple A16 Bionic", "Штрихкод": "195949036019", "Навігація": "QZSS, Galileo, BeiDou, iBeacon, GPS, A-GPS", "Оснащення": "пило/вологозахист, гіроскоп", "Органайзер": "будильник, телефонна книга, диктофон, секундомір, нотатки, калькулятор, світовий час, годинник, календар", "Розміри (мм)": "147.6 x 71.6 x 7.80 мм", "Стан товару": "Новий", "Тип дисплея": "OLED", "Форм-фактор": "моноблок", "Мультимедіа": "соціальні мережі, відеоплеєр, музичний плеєр, мобільні сервіси Google, ігри", "Особливості": "IP68 certified", "Гарантія, міс": "12", "Кількість ядер": "6 core", "Основна камера": "48 + 12 Mpx", "Формат SIM-карти": "e-sim, Nano", "Функції камери": "розпізнавання обличчя, панорама, геотегінг, спалах, автофокус", "Діагональ екрану": "6.1\"", "Кількість SIM-карт": "1 SIM + e-sim", "Вбудована пам''ять": "128 Gb", "Вбудовані датчики": "компас, акселерометр, датчик освітлення, датчик наближення, гіроскоп, барометр", "Фронтальна камера": "12 Mpx", "Країна виробництва": "Китай", "Метод стабілізації": "оптична", "Операційна система": "iOS 17", "Особливості корпусу": "водонепроникні", "Бездротові технології": "Bluetooth, WI-FI, бездротова зарядка, NFC", "Інтерфейси і підключення": "USB Type-C", "Частота оновлення екрану": "60 Гц", "Покоління зв''язку (2G /3G/4G/5G)": "2G, 3G, 4G, 5G", "Діафрагма основної камери": "f/1.6 + f/2.4", "Роздільна здатність екрану": "1179 х 2556", "Запис відео основної камери": "4K / 3840x2160 / стереозвук", "Діафрагма фронтальної камери": "f/1.9", "Кількість модулів основної камери": "2", "Кількість модулів фронтальної камери": "1"}');
INSERT INTO "parser_app_product" ("id", "parser_type", "source_url", "full_name", "color", "memory_capacity", "manufacturer", "regular_price", "promotional_price", "image_urls", "product_code", "review_count", "screen_diagonal", "display_resolution", "characteristics") VALUES (9, 'playwright', 'https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_15_128GB_Black-p1044347.html', 'Мобільний телефон Apple iPhone 15 128GB Black (MTP03)', 'чорний', '128 Gb', 'Apple', '32 999 ₴', '29 999 ₴', '["https://brain.com.ua/static/images/prod_img/8/9/U0854689_big_1739047983.jpg", "https://brain.com.ua/static/images/prod_img/8/9/U0854689_2big_1739047984.jpg", "https://brain.com.ua/static/images/prod_img/8/9/U0854689_3big_1739047985.jpg"]', 'U0854689', 1, '6.1"', '1179 х 2556', '{"Вага": "171 г", "Колір": "чорний", "Безпека": "FaceID", "Виробник": "Apple", "Примітка": "Виробник може змінювати властивості, характеристики, зовнішній вигляд і комплектацію товарів без попередження", "Процесор": "Apple A16 Bionic", "Штрихкод": "195949036019", "Навігація": "QZSS, Galileo, BeiDou, iBeacon, GPS, A-GPS", "Оснащення": "пило/вологозахист, гіроскоп", "Органайзер": "будильник, телефонна книга, диктофон, секундомір, нотатки, калькулятор, світовий час, годинник, календар", "Розміри (мм)": "147.6 x 71.6 x 7.80 мм", "Стан товару": "Новий", "Тип дисплея": "OLED", "Форм-фактор": "моноблок", "Мультимедіа": "соціальні мережі, відеоплеєр, музичний плеєр, мобільні сервіси Google, ігри", "Особливості": "IP68 certified", "Гарантія, міс": "12", "Кількість ядер": "6 core", "Основна камера": "48 + 12 Mpx", "Формат SIM-карти": "e-sim, Nano", "Функції камери": "розпізнавання обличчя, панорама, геотегінг, спалах, автофокус", "Діагональ екрану": "6.1\"", "Кількість SIM-карт": "1 SIM + e-sim", "Вбудована пам''ять": "128 Gb", "Вбудовані датчики": "компас, акселерометр, датчик освітлення, датчик наближення, гіроскоп, барометр", "Фронтальна камера": "12 Mpx", "Країна виробництва": "Китай", "Метод стабілізації": "оптична", "Операційна система": "iOS 17", "Особливості корпусу": "водонепроникні", "Бездротові технології": "Bluetooth, WI-FI, бездротова зарядка, NFC", "Інтерфейси і підключення": "USB Type-C", "Частота оновлення екрану": "60 Гц", "Покоління зв''язку (2G /3G/4G/5G)": "2G, 3G, 4G, 5G", "Діафрагма основної камери": "f/1.6 + f/2.4", "Роздільна здатність екрану": "1179 х 2556", "Запис відео основної камери": "4K / 3840x2160 / стереозвук", "Діафрагма фронтальної камери": "f/1.9", "Кількість модулів основної камери": "2", "Кількість модулів фронтальної камери": "1"}');
