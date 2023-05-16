PRAGMA foreign_keys = true;

-- 建立 Member 表格
DROP TABLE IF EXISTS Member;
CREATE TABLE Member (
    Email VARCHAR PRIMARY KEY,
    Name VARCHAR NOT NULL,
    Password VARCHAR NOT NULL,
    Tel VARCHAR
);

-- 建立 Menu 表格
DROP TABLE IF EXISTS Menu;
CREATE TABLE Menu (
    M_ID VARCHAR PRIMARY KEY,
    Name VARCHAR NOT NULL,
    Price REAL NOT NULL
);

-- 建立 Branch 表格
DROP TABLE IF EXISTS Branch;
CREATE TABLE Branch (
    Name VARCHAR PRIMARY KEY,
    Address VARCHAR,
    Tel VARCHAR 
);

-- 建立 Material 表格
DROP TABLE IF EXISTS Material;
CREATE TABLE Material (
    Ma_ID VARCHAR PRIMARY KEY,
    Name VARCHAR NOT NULL,
    Cost REAL NOT NULL,
    Remain_num INTEGER NOT NULL
);

-- 建立 Purchase 表格
DROP TABLE IF EXISTS Purchase;
CREATE TABLE Purchase (
    O_ID VARCHAR PRIMARY KEY,
    Time DATE NOT NULL,
    Buyer VARCHAR NOT NULL,
    Branch VARCHAR NOT NULL,
    FOREIGN KEY (Buyer) REFERENCES Member(Email),
    FOREIGN KEY (Branch) REFERENCES Branch(Name)
);

-- 建立 Order_description 表格
DROP TABLE IF EXISTS Order_description;
CREATE TABLE Order_description (
    O_ID VARCHAR,
    M_ID VARCHAR,
    PRIMARY KEY (O_ID, M_ID),
    FOREIGN KEY (O_ID) REFERENCES Purchase(O_ID),
    FOREIGN KEY (M_ID) REFERENCES Menu(M_ID) ON DELETE CASCADE ON UPDATE CASCADE 
);

-- 建立 Employee 表格
DROP TABLE IF EXISTS Employee;
CREATE TABLE Employee (
    E_ID VARCHAR PRIMARY KEY,
    Name VARCHAR NOT NULL,
    Password VARCHAR NOT NULL,
    Tel VARCHAR,
    Branch VARCHAR NOT NULL,
    FOREIGN KEY (Branch) REFERENCES Branch(Name)
);

-- 建立 Recipe 表格
DROP TABLE IF EXISTS Recipe;
CREATE TABLE Recipe (
    M_ID VARCHAR,
    Ma_ID VARCHAR,
    PRIMARY KEY (M_ID, Ma_ID),
    FOREIGN KEY (M_ID) REFERENCES Menu(M_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Ma_ID) REFERENCES Material(Ma_ID)
);