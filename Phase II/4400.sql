CREATE TABLE USER
(
	Username varchar(15) NOT NULL,
	Password varchar(15) NOT NULL,
	PRIMARY KEY (Username)
);

CREATE TABLE PASSENGER
(
	passenger_Username varchar(15) NOT NULL,
	Passenger_Email varchar(25) NOT NULL,
	PRIMARY KEY (Passenger_Username)
	UNIQUE (Passenger_Email)
	CONSTRAINT CHECK Passenger_Email
	FOREIGN KEY ('passenger_Username') REFERENCES USER('Username')
	ON DELETE CASCADE ON UPDATE CASCADE
);

/*Username must be unique.
Email addr must be unique
password at least 8 char
must have at least 1 BreezeCard
Email addr match '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$' */

CREATE TABLE BREEZECARD
(
	Card_Number int(16) NOT NULL,
	Card_Value char(6) NOT NULL,
	Passenger_Username varchar(25) DEFAULT NULL,
	PRIMARY KEY (Card_Number),
	UNIQUE (Passenger_Username),
	FOREIGN KEY ('Passenger_Username') REFERENCES PASSENGER ('Passenger_Username')
	ON DELETE CASCADE ON UPDATE CASCADE
);
/*card_Value <= $1000.00*/

CREATE TABLE STATION
(
	StopID varchar(255) NOT NULL,
	enter_Fare varchar(255) NOT NULL,
	closed_Status varchar(255) NOT NULL,
	PRIMARY KEY (StopID)
);
/*Fare to enter: $0.00 to $50.00 inclusive*/


CREATE TABLE BUSSTATION
(
	bus_station_Name varchar(255) NOT NULL,
	station_StopID varchar(255) DEFAULT NULL,
	intersection varchar(255) NOT NULL,
	PRIMARY KEY (bus_station_Name, station_StopID)
	FOREIGN KEY ('station_StopID') REFERENCES STATION ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE TRIP
(
	start_Time varchar(255) NOT NULL,
	current_Fare varchar(255) NOT NULL,
	BCNumber varchar(255) DEFAULT NULL,
	station_StopID varchar(255) DEFAULT NULL,
	PRIMARY KEY (start_Time, BCNumber)
	FOREIGN KEY ('station_StopID') REFERENCES STATION ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE
	FOREIGN KEY ('BCNumber') REFERENCES BREEZECARD ('card_Number')
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE CONFLICT
(
	PassengerEmail varchar(255) DEFAULT NULL,
	BCNumber varchar(255) DEFAULT NULL,
	date_Time varchar(255) NOT NULL,
	PRIMARY KEY (PassengerEmail, BCNumber)
	FOREIGN KEY ('PassengerEmail') REFERENCES PASSENGER ('Email')
	ON DELETE CASCADE ON UPDATE CASCADE
	FOREIGN KEY ('BCNumber') REFERENCES BREEZECARD ('card_Number')
	ON DELETE CASCADE ON UPDATE CASCADE
);