-- Active: 1776995574789@@localhost@3306@footballiq
CREATE DATABASE footballiq;
USE footballiq;
CREATE TABLE players (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    club VARCHAR(100),
    goals INT,
    assists INT
);
