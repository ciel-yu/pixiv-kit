BEGIN TRANSACTION;
CREATE TABLE `works` (
	`user_id`	INTEGER NOT NULL,
	`works`	TEXT,
	PRIMARY KEY(user_id)
);
CREATE TABLE `user` (
	`user_id`	INTEGER NOT NULL,
	`user_name`	TEXT,
	`user_nick`	TEXT,
	`bookmark`	INTEGER NOT NULL DEFAULT 0,
	`works`	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY(user_id)
);
CREATE TABLE `image_content` (
	`image_id`	INTEGER NOT NULL,
	`page_no`	INTEGER NOT NULL DEFAULT 0,
	`url`	TEXT NOT NULL DEFAULT '',
	`check_time`	INTEGER,
	`path`	TEXT,
	`size`	INTEGER NOT NULL DEFAULT -1,
	`checksum`	TEXT,
	PRIMARY KEY(image_id,page_no)
);
CREATE TABLE "image" (
	`image_id`	INTEGER NOT NULL,
	`user_id`	INTEGER NOT NULL DEFAULT -1,
	`title`	TEXT NOT NULL DEFAULT '',
	`caption`	TEXT NOT NULL DEFAULT '',
	`tags`	TEXT NOT NULL DEFAULT '',
	`page_count`	INTEGER NOT NULL DEFAULT 0,
	`type`	TEXT NOT NULL DEFAULT '',
	`status`	INTEGER NOT NULL DEFAULT -1,
	PRIMARY KEY(image_id)
);
CREATE TABLE `bookmark` (
	`user_id`	INTEGER NOT NULL,
	`bookmark`	TEXT,
	PRIMARY KEY(user_id)
);
COMMIT;
