BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"slug"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"email"	TEXT UNIQUE,
	"password"	TEXT,
	"role"	TEXT,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	"updated"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	"email_token"	VARCHAR(20),
	"verified"	INT DEFAULT 0,
	"token"	VARCHAR(255),
	"token_expiration"	DATETIME,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER,
	"title"	TEXT,
	"description"	TEXT,
	"photo"	TEXT,
	"price"	DECIMAL(10, 2),
	"category_id"	INTEGER,
	"seller_id"	INTEGER,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	"updated"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY("seller_id") REFERENCES "users"("id"),
	FOREIGN KEY("category_id") REFERENCES "categories"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "blocked_users" (
	"user_id"	INTEGER,
	"message"	TEXT,
	"created"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "banned_products" (
	"product_id"	INTEGER,
	"reason"	TEXT,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY("product_id") REFERENCES "products"("id"),
	PRIMARY KEY("product_id")
);
CREATE TABLE IF NOT EXISTS "orders" (
	"id"	INTEGER,
	"product_id"	INTEGER NOT NULL,
	"buyer_id"	INTEGER NOT NULL,
	"offer"	NUMERIC(10, 2),
	"created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	UNIQUE("product_id","buyer_id"),
	FOREIGN KEY("product_id") REFERENCES "products"("id"),
	FOREIGN KEY("buyer_id") REFERENCES "users"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "confirmed_orders" (
	"order_id"	INTEGER,
	"created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("order_id") REFERENCES "orders"("id"),
	PRIMARY KEY("order_id")
);
INSERT INTO "categories" VALUES (1,'Electrònica','electronica');
INSERT INTO "categories" VALUES (2,'Roba','roba');
INSERT INTO "categories" VALUES (3,'Joguines','joguines');
INSERT INTO "categories" VALUES (4,'Ondansetron','Sulfamethoxazole and Trimethoprim');
INSERT INTO "categories" VALUES (5,'Sciatic Rescue','Kleenex Clear Antibacterial Skin Cleanser');
INSERT INTO "categories" VALUES (6,'Diclofenac Sodium','smart sense acid reducer');
INSERT INTO "categories" VALUES (7,'ConZip','Moexipril Hydrochloride and Hydrochlorothiazide');
INSERT INTO "categories" VALUES (8,'Peppermint','BACMIN');
INSERT INTO "categories" VALUES (9,'Lorazepam','Disney PLANES FIRE and RESCUE ANTIBACTERIAL HAND WIPES');
INSERT INTO "categories" VALUES (10,'Olanzapine','HALOPERIDOL');
INSERT INTO "categories" VALUES (11,'NEXIUM','Chlorpheniramine Maleate');
INSERT INTO "categories" VALUES (12,'Progesterone','Ribavirin');
INSERT INTO "categories" VALUES (13,'Good Neighbor Pharmacy','Morphine sulfate');
INSERT INTO "categories" VALUES (14,'CareOne Miconazole 3','Metformin Hydrochloride');
INSERT INTO "users" VALUES (1,'Joan Pérez','joan@example.com','contrasenya1','wanner','2023-11-24 08:35:41','2023-11-24 08:35:41',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (2,'Anna García','anna@example.com','contrasenya2','wanner','2023-11-24 08:35:41','2023-11-24 08:35:41',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (3,'Elia Rodríguez','elia@example.com','contrasenya3','wanner','2023-11-24 08:35:41','2023-11-24 08:35:41',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (4,'Brien','bambrozewicz3@mail.ru','wS8`@}1z''#f''u@','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (5,'Kassandra','kbittany4@instagram.com','vW9/?7Q=`qi','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (6,'Melicent','mway5@prweb.com','rE2#i_Wl','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (7,'Doll','dtraill6@washingtonpost.com','aB6_?24h','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (8,'Victoria','vrylance7@opensource.org','zP2+n/de<7hvM9','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (9,'Rheba','rarnaud8@people.com.cn','gZ3%<Vt_NF','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (10,'Corine','cwindrus9@biblegateway.com','pN7=Yhzfn3F4','wanner','2023-04-15 07:10:24','2023-01-23 09:34:42',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (12,'pruebarole','2daw.equip12@fp.insjoaquimmir.cat','pbkdf2:sha256:600000$lgfAUD6pzL1Z52zo$17d9982142ca752577f4c6703d4b55e9336de2459ccee5c2251240c279dad0c8','moderator','2023-11-24 11:50:40','2024-02-16 17:29:12',NULL,1,'36dab477d8e3a45d2783d74c605d9706','2024-02-16 18:29:12.278214');
INSERT INTO "users" VALUES (13,'pruebamoderator','pruebamoderator@hotmail.com','pbkdf2:sha256:600000$bEUdx9kyLkDO6L3e$f02e6308ded34b523146e8949bff2c5543fadd4143e77cecd6e26d12b7614444','moderator','2023-11-24 15:11:19','2023-11-24 15:11:19',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (14,'pruebaadmin','pruebaadmin@hotmail.com','pbkdf2:sha256:600000$JejtcnxNBpoEWf7S$e9880d48dd9f70a248961670c9fa2a277bcc91b666c6032487bd6ea256a83aec','admin','2023-11-24 15:22:34','2023-11-24 15:22:34',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (15,'pruebatoken','pruebatoken@hotmail.com','pbkdf2:sha256:600000$Ghbob1jvLmYb05jW$9890ad54a7aeaeb07a7281121e419842874ec4ace365d8f8a509d72feb7781fb','wanner','2023-11-24 18:10:00','2023-11-24 18:10:00','3eWLOm51HxLxgH_n1YJfseaKei0',1,NULL,NULL);
INSERT INTO "users" VALUES (21,'pruebafinal','amartinezp@fp.insjoaquimmir.cat','pbkdf2:sha256:600000$9PafbViodpmiPrDX$d0beaf6feab5c8ad09e5d53871101e5f245eb90a2b1326989db5825d9e2bcb32','admin','2023-11-24 19:56:27','2023-11-24 20:04:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (25,'este','asdf@hotmail.com','pbkdf2:sha256:600000$q0GGLVQu4rfmJFsh$caec7f211f4be288bc84ffba4beb584ddde8472dce086e1d929768bb7df0b3e7','wanner','2023-12-01 14:32:17','2023-12-01 14:32:17','SGMU2MqbsEktXl6hN8L2ONz9cFM',0,NULL,NULL);
INSERT INTO "users" VALUES (26,'adri','adria.m.p@hotmail.com','pbkdf2:sha256:600000$IVVAVSsU98jhUs47$b29d205f6b7c1317485f4295f27e56e1b78192bddfc19c16e51a3a52e28002fa','wanner','2023-12-01 14:36:40','2023-12-01 14:37:21',NULL,1,NULL,NULL);
INSERT INTO "products" VALUES (4,'Zaam-Dox','lectus in quam fringilla rhoncus mauris enim leo rhoncus sed','image-1.png
',64,2,2,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (5,'Cookley','primis in faucibus orci luctus et ultrices','image-2.png',12,2,2,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (6,'Matsoft','eleifend donec ut dolor morbi vel lectus','image-3.png',38,1,5,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (7,'Izan','Izan','image-4.png',46,1,5,'2023-04-15 07:10:24','2024-02-16 16:39:26');
INSERT INTO "products" VALUES (8,'Flowdesk','id luctus nec molestie sed justo pellentesque viverra pede','image-5.png',23,3,4,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (9,'Gembucket','adipiscing elit proin interdum mauris non ligula pellentesque ultrices','image-6.png',16,2,4,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (10,'Mat Lam Tam','donec vitae nisi nam ultrices','image-7.png',40,2,3,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (11,'Solarbreeze','ac nulla sed vel','image-8.png',50,5,1,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (12,'Job','dolor vel est','image-9.png',54,3,2,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (13,'Tampflex','vehicula consequat morbi a ipsum integer a nibh','image-10.png',80,2,3,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (14,'Asoka','non velit donec diam neque vestibulum eget vulputate ut','image-11.png',82,5,2,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (15,'Bamity','nulla integer pede','image-12.png',41,3,4,'2023-04-15 07:10:24','2023-01-23 09:34:42');
INSERT INTO "products" VALUES (16,'Izan','Izan','image-4.png',44,1,5,'2023-11-24 15:07:18','2024-02-16 17:30:25');
INSERT INTO "products" VALUES (19,'pruebaconfig','pruebaconfig@gmail.com','260ee0f6-d1bc-447c-8c30-07cab937e9a1-camiseta_nino_portada.jpg',50,1,12,'2023-11-24 19:09:07','2023-11-24 19:09:07');
INSERT INTO "products" VALUES (20,'rewewrqew','rewqwerq','d0acf3cd-d979-4c96-a4e7-19a410bf2a22-camiseta_poliester_azul.jpg',50,1,21,'2023-11-24 20:15:02','2023-11-24 20:15:02');
INSERT INTO "products" VALUES (21,'ghdfhfgd','gdfhfghd','587c9383-9097-4f6d-ae59-e9b9fec63be7-captura_de_pantalla_2023-02-10_181450.png',100,11,14,'2023-12-13 18:30:20','2023-12-13 18:30:20');
INSERT INTO "blocked_users" VALUES (1,'rgwetergrgwre','2023-12-13 19:25:09.190228');
INSERT INTO "blocked_users" VALUES (2,'gerhhrh','2024-01-19 16:35:51.810116');
INSERT INTO "blocked_users" VALUES (15,'si que sale alfons','2024-01-26 17:06:06.688477');
INSERT INTO "banned_products" VALUES (4,'yujtukyuk','2023-12-13 19:28:55.770122');
INSERT INTO "banned_products" VALUES (5,'sasasa','2024-01-26 19:51:19.551171');
INSERT INTO "orders" VALUES (1,4,2,50,'2024-02-02 16:17:48');
INSERT INTO "orders" VALUES (2,5,4,75.5,'2024-02-02 16:17:48');
INSERT INTO "orders" VALUES (3,6,3,60.25,'2024-02-02 16:17:48');
INSERT INTO "orders" VALUES (4,12,7,50,'2024-02-16 17:49:06');
INSERT INTO "orders" VALUES (5,12,12,50,'2024-02-16 17:58:56');
INSERT INTO "orders" VALUES (6,19,12,50,'2024-02-16 18:04:33');
INSERT INTO "orders" VALUES (7,19,5,50,'2024-02-16 18:05:21');
INSERT INTO "confirmed_orders" VALUES (2,'2024-02-02 18:53:16');
INSERT INTO "confirmed_orders" VALUES (3,'2024-02-02 16:17:48');
COMMIT;
