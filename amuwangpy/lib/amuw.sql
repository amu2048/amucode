/*
 Navicat Premium Data Transfer

 Source Server         : 456757
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 11/07/2020 17:23:35
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for _user_old_20200711
-- ----------------------------
DROP TABLE IF EXISTS "_user_old_20200711";
CREATE TABLE "_user_old_20200711" (
  "name" text,
  "pwd" int,
  "names" text,
  "indata" text
);

-- ----------------------------
-- Records of "_user_old_20200711"
-- ----------------------------
INSERT INTO "_user_old_20200711" VALUES ('amu', 123, '管理', NULL);

-- ----------------------------
-- Table structure for code
-- ----------------------------
DROP TABLE IF EXISTS "code";
CREATE TABLE "code" (
  "ok" TEXT,
  "code" TEXT
);

-- ----------------------------
-- Table structure for gonggao
-- ----------------------------
DROP TABLE IF EXISTS "gonggao";
CREATE TABLE "gonggao" (
  "ID" int,
  "content" text,
  PRIMARY KEY ("ID")
);

-- ----------------------------
-- Records of "gonggao"
-- ----------------------------
INSERT INTO "gonggao" VALUES (1, '欢迎来到牛大爷管理系统，使用问题请联系管理员：阿木：微信号：liu10-6');

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Records of "sqlite_sequence"
-- ----------------------------
INSERT INTO "sqlite_sequence" VALUES ('user', 2);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" text,
  "pwd" int,
  "names" text,
  "indata" text
);

-- ----------------------------
-- Records of "user"
-- ----------------------------
INSERT INTO "user" VALUES (1, 'amu', 123, '管理', NULL);
INSERT INTO "user" VALUES (2, 'root', 123456, '超级管理员', NULL);

-- ----------------------------
-- Auto increment value for user
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 2 WHERE name = 'user';

PRAGMA foreign_keys = true;
