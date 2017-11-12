CREATE TABLE User(
	Username 		varchar(50),
	Password 		int NOT NULL,  -- <====(Can be INT, CHAR, VARCHAR, or BLOB)
	IsAdmin 		boolean NOT NULL,
	PRIMARY KEY (Username)
) ENGINE=InnoDB;

CREATE TABLE Passenger(
	Username 		varchar(50),
	Email 			varchar(50) NOT NULL,
	PRIMARY KEY (Username),  -- <====(Can be Email also, username is better though)
	UNIQUE (Email),
	FOREIGN KEY (Username) REFERENCES User(Username) 
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Breezecard(
	BreezecardNum 	char(16),
	Value 			decimal(6,2) NOT NULL,
	BelongsTo		varchar(50),
	PRIMARY KEY (BreezecardNum),
	FOREIGN KEY (BelongsTo) REFERENCES Passenger(Username) -- <====(Can also reference Email)
		ON DELETE SET NULL ON UPDATE CASCADE, -- <== Must be SET NULL
	CHECK (Value >= 0.00 AND Value <= 1000.00)
) ENGINE=InnoDB;

CREATE TABLE Conflict(
	Username 		varchar(50), -- <====(Can also be Email, although username is better)
	BreezecardNum 	char(16),
	DateTime 		timestamp NOT NULL,
	CONSTRAINT Pk_Conflict PRIMARY KEY (Username, BreezecardNum),
	FOREIGN KEY (Username) REFERENCES Passenger(Username)  -- <====(Can also reference Email)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (BreezecardNum) REFERENCES Breezecard(BreezecardNum) 
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Station(
	StopID 			varchar(50),
	Name 			varchar(50) NOT NULL,
	EnterFare 		decimal(4,2) NOT NULL,
	ClosedStatus 	boolean NOT NULL,
	IsTrain 		boolean NOT NULL,
	PRIMARY KEY (StopID),
	UNIQUE (Name, IsTrain),
	CHECK (EnterFare >= 0.00 AND EnterFare <= 50.00)
) ENGINE=InnoDB;

CREATE TABLE Trip(
	Tripfare 		decimal(4,2) NOT NULL,
	StartTime 		timestamp,
	BreezecardNum 	char(16),
	StartsAt 		varchar(50) NOT NULL,
	EndsAt 			varchar(50),
	CONSTRAINT Pk_Trip PRIMARY KEY (StartTime, BreezecardNum),
	FOREIGN KEY (BreezecardNum) REFERENCES Breezecard(BreezecardNum) 
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (StartsAt) REFERENCES Station(StopID)
		ON DELETE RESTRICT ON UPDATE CASCADE,    -- <===(ON DELETE SET NULL ok too)
	FOREIGN KEY (EndsAt) REFERENCES Station(StopID)
		ON DELETE RESTRICT ON UPDATE CASCADE     -- <===(ON DELETE SET NULL ok too)
) ENGINE=InnoDB;

CREATE TABLE BusStationIntersection(
	StopID 			varchar(50),
	Intersection 	varchar(255), -- <====(OK to be NOT NULL)
	PRIMARY KEY (StopID),
	FOREIGN KEY (StopID) REFERENCES Station(StopID)
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;
