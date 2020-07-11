/*
 Navicat Premium Data Transfer

 Source Server         : 百度云数据库
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 106.12.6.59:3306
 Source Schema         : ndy

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 07/01/2020 09:51:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for gmtable
-- ----------------------------
DROP TABLE IF EXISTS `gmtable`;
CREATE TABLE `gmtable`  (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `picihao` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `bianhao` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `goudata` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `gzongjia` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `gtizhong` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `gdanjia` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `goumaidi` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `beizhu` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  `jiaoyiren` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_german2_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gmtable
-- ----------------------------
INSERT INTO `gmtable` VALUES (1, 'amu', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL COMMENT '用户名',
  `pwd` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NULL DEFAULT NULL COMMENT '密码'
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_german2_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('amu', '123456');

SET FOREIGN_KEY_CHECKS = 1;
