CREATE TABLE User
(
	Username varchar(255) NOT NULL,
	Password varchar(255) NOT NULL,
	PRIMARY KEY (Username)
);
/*Username is unique*/

CREATE TABLE Admin
(
	admin_Username varchar(255) NOT NULL,
	PRIMARY KEY (Admin_Username)
	CONSTRAINT 'FK Admin' FOREIGN KEY ('admin_Username') REFERENCES 'User' ('Username')
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Passenger
(
	passenger_Username varchar(255) NOT NULL,
	Email varchar(255) NOT NULL,
	PRIMARY KEY (Passenger_Username)
	CONSTRAINT CHECK Email
	CONSTRAINT 'FK Passenger' FOREIGN KEY ('passenger_Username') REFERENCES 'User' ('Username')
	ON DELETE CASCADE ON UPDATE CASCADE
);
/*Username must be unique.
Email addr must be unique
password at least 8 char
must have at least 1 BreezeCard
Email addr kdjfbhsk@nkjds.snkd*/

CREATE TABLE BreezeCard
(
	card_Number int(16) NOT NULL,
	card_Value varchar(255) NOT NULL,
	PassengerEmail varchar(255) DEFAULT NULL,
	PRIMARY KEY (Card_number)
	CONSTRAINT 'FK BreezeCard' FOREIGN KEY ('PassengerEmail') REFERENCES 'Passenger' ('Email')
	ON DELETE CASCADE ON UPDATE CASCADE
);
/*card_Value <= $1000.00*/

CREATE TABLE Station
(
	StopID varchar(255) NOT NULL,
	enter_Fare varchar(255) NOT NULL,
	closed_Status varchar(255) NOT NULL,
	PRIMARY KEY (StopID)
);
/*Fare to enter: $0.00 to $50.00 inclusive*/


CREATE TABLE BusStation
(
	bus_station_Name varchar(255) NOT NULL,
	station_StopID varchar(255) DEFAULT NULL,
	intersection varchar(255) NOT NULL,
	PRIMARY KEY (bus_station_Name, station_StopID)
	CONSTRAINT 'FK BusStation' FOREIGN KEY ('station_StopID') REFERENCES 'Station' ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE TrainStation
(
	train_station_Name varchar(255) NOT NULL,
	station_StopID varchar(255) DEFAULT NULL,
	PRIMARY KEY (train_station_Name, station_StopID)
	CONSTRAINT 'FK TrainStation' FOREIGN KEY ('station_StopID') REFERENCES 'Station' ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Trip
(
	start_Time varchar(255) NOT NULL,
	current_Fare varchar(255) NOT NULL,
	BCNumber varchar(255) DEFAULT NULL,
	station_StopID varchar(255) DEFAULT NULL,
	PRIMARY KEY (start_Time, BCNumber)
	CONSTRAINT 'FK Trip1' FOREIGN KEY ('station_StopID') REFERENCES 'Station' ('StopID')
	ON DELETE CASCADE ON UPDATE CASCADE
	CONSTRAINT 'FK Trip2' FOREIGN KEY ('BCNumber') REFERENCES 'BreezeCard' ('card_Number')
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Conflict
(
	PassengerEmail varchar(255) DEFAULT NULL,
	BCNumber varchar(255) DEFAULT NULL,
	date_Time varchar(255) NOT NULL,
	PRIMARY KEY (PassengerEmail, BCNumber)
	CONSTRAINT 'FK Conflict1' FOREIGN KEY ('PassengerEmail') REFERENCES 'Passenger' ('Email')
	ON DELETE CASCADE ON UPDATE CASCADE
	CONSTRAINT 'FK Conflict2' FOREIGN KEY ('BCNumber') REFERENCES 'BreezeCard' ('card_Number')
	ON DELETE CASCADE ON UPDATE CASCADE
);















