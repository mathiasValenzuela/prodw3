create database prodw3;

use prodw3;

create table usuario
(   
    id int(7) not null auto_increment,
    nombre varchar(30) not null,
    nickname varchar(30) not null unique,
    password varchar(40) not null,
    cellphone int(8) not null unique,
    email varchar(50) not null unique,
    primary key(id)
);

create table producto
(
    id int(7) not null auto_increment,
    url_img varchar(170) not null,
    nombre varchar(20) not null unique,
    precio_unitario int(7) not null,
    cantidad int(7) not null,
    descripcion varchar(30) not null,
    primary key(id)
);


create table shoppingList
(
    id int(7) not null,
    nro_pedido int(4) not null,
    nombre varchar(20) not null unique,
    precio_unitario int(7) not null,
    cantidad_requerida int(7) not null,
    sub_total int(8) not null,
    primary key (id)
);



/*
https://www.snackbar.cl/552-large_default/cerveza-cristal-lata-470cc-x24-unidades.jpg | cerveza cristal |    500 | cerveza ccu |
|  2 | https://www.spdigital.cl/img/products/new_web/1493382610753-Logitech_G203.jpg         | logitech G203   |    800 | mouse usb   |



insert into producto(url_img, nombre, precio_unitario, cantidad, descripcion) values ('https://is5-ssl.mzstatic.com/image/thumb/Purple122/v4/70/f4/84/70f48426-82d3-e9b7-c0b2-f4b3c8a05c9e/source/256x256bb.jpg','cerveza cristal', 500, 3 , 'cerveza ccu');

insert into producto(url_img, nombre, precio_unitario, cantidad, descripcion) values ('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQA7YJQ5qvMUYdvIDQfqI7IzMq5Qv2-f6CcgNkt0lAlSpiiRIrxvw&s','logitech G203', 800, 7,'mouse usb');


insert into producto(url_img, nombre, precio_unitario, cantidad, descripcion) values ('https://logodix.com/logo/1214954.png','msi notebook', 137000, 2,'notebook high-performance');
*/

