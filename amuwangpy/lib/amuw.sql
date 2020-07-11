/*
 Navicat Premium Data Transfer

 Source Server         : amuw
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 02/03/2020 15:38:30
*/

PRAGMA foreign_keys = false;

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
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "name" text,
  "pwd" int,
  "names" text,
  "indata" text
);

PRAGMA foreign_keys = true;
