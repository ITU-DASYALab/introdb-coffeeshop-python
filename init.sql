drop table if exists user;
drop table if exists product;
drop table if exists purchase;

create table user(
	username string primary key, 
	email string, 
	password string
);
insert into user values
 ('Anna', 'anna@itu.dk', 'test'),
 ('Martin', 'mhent@itu.dk', 'test'),
 ('Omar', 'omsh@itu.dk', 'test');

create table product(
	productname string primary key, 
	price int, 
	description string
);
insert into product values
 ('Tea', 20, 'Used for our large collection of delicious teas'),
 ('Small', 17, 'Espresso, Americano, Cortado, and Cappuccino'),
 ('Large', 20, 'Caffee latte, Chai latte, Macha latte, and cocoa'),
 ('Fancy', 25, 'Iced/dirty versions of Large drinks');

create table purchase(
	purchasetime timestamp, 
	productname string, 
	username string,
	primary key (purchasetime, productname, username)
);
insert into purchase values
 ('2027-02-11 9:55'::timestamp, 'Tea', 'Martin'),
 ('2027-02-12 10:03'::timestamp, 'Small', 'Martin'),
 ('2027-02-12 10:05'::timestamp, 'Small', 'Omar'),
 ('2027-02-12 10:06'::timestamp, 'Large', 'Omar'),
 ('2027-02-19 9:00'::timestamp, 'Small', 'Martin');