CREATE TABLE USER
(
	Username	VARCHAR(25), 	NOT NULL,
	Password 	VARCHAR(25)		NOT NULL,
	PRIMARY KEY (Username),
);

CREATE TABLE PASSENGER
(
	Passenger_Username	VARCHAR(25)		NOT NULL,
	Passenger_Email		VARCHAR(50)		NOT NULL,
	PRIMARY KEY (Passenger_Username),
	UNIQUE (Passenger_Email),
	CONSTRAINT CHECK Passenger_Email,   #这个啊 好像在ppt里没有这一条欸
	FOREIGN KEY ('Passenger_Username') REFERENCES USER('Username')
	ON DELETE CASCADE ON UPDATE CASCADE
);

/*
password at least 8 charaters
Email addr match '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$' 
*/

CREATE TABLE BREEZECARD
(
	Card_Number 		INT 			NOT	NULL,
	Card_Value 			DECIMAL(6, 2), 	NOT NULL,
	Passenger_Username 	VARCHAR(25),    # no need to add "DEFAULT NULL"
	Suspension_Status	BOOLEAN			NOT NULL,
	PRIMARY KEY (Card_Number),
	FOREIGN KEY ('Passenger_Username') REFERENCES PASSENGER ('Passenger_Username')
	ON DELETE CASCADE ON UPDATE CASCADE
);
/*card_Value in interval [0.00, 1000.00] */

CREATE TABLE STATION
(
	StopID 			INT 			NOT NULL,
	Name			VARCHAR(30)		NOT NULL,
	Station_Type	VARCHAR(5),		NOT NULL,
	Enter_Fare 		DECIMAL(4, 2), 	NOT NULL,
	Closed_Status 	BOOLEAN			NOT NULl,
	PRIMARY KEY (StopID)
);
/*Fare to enter: $0.00 to $50.00 inclusive*/


CREATE TABLE BUSSTATION
(
	Bus_Dtation_Name 	VARCHAR(30) 	NOT NULL,
	Station_StopID 		INT 			NOT NULL,
	Intersection 		VARCHAR(30),
	PRIMARY KEY (Bus_Dtation_Name, Station_StopID),
	FOREIGN KEY ('Station_StopID') REFERENCES STATION ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE TRIP
(
	Start_Time 		CHAR(19) 		NOT NULL, 	# YYYY-MM-DD HH:MM:SS
	Current_Fare 	DECIMAL(4, 2), 	NOT NULL,
	BCNumber 		INT 			NOT NULL,
	Station_StopID 	INT, 			NOT NULL,
	PRIMARY KEY (Start_Time, BCNumber)
	FOREIGN KEY ('Station_StopID') REFERENCES STATION ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ('BCNumber') REFERENCES BREEZECARD ('card_Number')
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE CONFLICT
(
	Passenger_Username 	VARCHAR(25)		NOT NULL,
	BCNumber 			INT 			NOT NULL,
	date_Time 			DATE,			NOT NULL,
	PRIMARY KEY (PassengerEmail, BCNumber)
	FOREIGN KEY ('PassengerEmail') REFERENCES PASSENGER ('Email')
	ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ('BCNumber') REFERENCES BREEZECARD ('card_Number')
	ON DELETE CASCADE ON UPDATE CASCADE
);