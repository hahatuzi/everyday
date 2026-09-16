# 01_数据类型+sql语句

---

## 目录

1. [数据类型](#一、数据类型)
2. [数据库和表操作](#二、数据库和表操作)
3. [集群安装](#三、集群安装)
4. [node](#四node)
5. [NameSpace](#五NameSpace)
6. [Pod](#六Pod)
7. [Controller](#七Controller)
8. [Service](#八Service)
9. [Label](#九Label)

---
## 一、数据类型
  ### 1.1 数值类型
  - **tinyint**---1byte---(-128,127)---(0,255)---大数值
  - **smallint**---2byte---(-128,127)---(0,255)---大整数值
  - **mediuint**---3byte---(-128,127)---(0,255)---大整数值
  - **int**---4byte---(-128,127)---(0,255)---大整数值
  - **bigint**---8byte---(-128,127)---(0,255)---极大整数值
  - **float**---4byte---(-128,127)---(0,255)---浮点数，单精度
  - **double**---8byte---(-128,127)---(0,255)---浮点数，双精度
  - **decimal**---    ---(依赖于M和D的值------小数值
---
  ### 1.2 字符串类型
---
  ### 1.3 日期类型
  - **date**----3byte---(-128,127)---(0,255)---大数值
  - **time**----3byte---(-128,127)---(0,255)---大整数值
  - **year**----3byte---(-128,127)---(0,255)---大整数值
  - **datetime**----8byte---(-128,127)---(0,255)---大整数值
  - **timestamp**----4byte---(-128,127)---(0,255)---极大整数值
---
## 二、数据库和表操作
  ### 2.1 数据库的常用操作
  - (1)查看所有的数据库:**show databases**
  - (2)创建数据库：**create database [if not exists] 数据库名字 [charset=utf8]**
  - (3)切换数据库：**use 数据库名称**
  - (4)删除数据库：**drop database [if exists] 数据库名称**
  - (5)修改数据库编码：**alter database 数据库名称 character set utf8**
---
  ### 2.2 表的常见操作
  - 创建:create table [if not exists] 表名( 字段名1 字段类型[(宽度)] [约束条件] [comment  '字段说明']) [ 表的一些设置]
  - 修改表添加列
    ```js
      // create table if nor exists student(
      //     id int,
      //     name varchar(20),
      //     age int,
      //     birthday date,
      //     address varchar(20)
      // );
    ```
## 三、sql增删改查
