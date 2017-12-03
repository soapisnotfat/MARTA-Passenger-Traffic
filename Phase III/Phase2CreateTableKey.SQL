CREATE TABLE User(
	Username 		varchar(50),
	Password 		CHAR(32) NOT NULL,  -- <====(Can be INT, CHAR, VARCHAR, or BLOB)
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
		ON DELETE RESTRICT ON UPDATE CASCADE,
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



--
-- Dumping data for table `Breezecard`
--

INSERT INTO `Breezecard` (`BreezecardNum`, `Value`, `BelongsTo`) VALUES
('0123456780987654', 140.25, NULL),
('0475861680208144', 35.25, 'commuter14'),
('0524807425551662', 59.50, 'ignacio.john'),
('0919948381768459', 126.50, 'commuter14'),
('1156635952683150', 141.00, NULL),
('1258825691462690', 144.75, NULL),
('1325138309325420', 97.00, 'kellis'),
('1788613719481390', 127.00, 'busrider73'),
('2006517782865770', 127.25, 'commuter14'),
('2275718423410130', 143.25, 'commuter14'),
('2286669536044610', 0.50, 'commuter14'),
('2613198031233340', 45.00, 'commuter14'),
('2792083965359460', 20.00, 'sandrapatel'),
('3346822267258650', 113.00, NULL),
('3590098235166490', 16.25, 'commuter14'),
('4156771407939460', 110.50, NULL),
('4769432303280540', 68.50, 'sandrapatel'),
('4792323707679860', 34.00, 'commuter14'),
('4902965887533820', 79.75, 'sandrapatel'),
('5943709678229760', 133.50, 'commuter14'),
('6411414737900960', 41.00, 'ashton.woods'),
('6424673176102560', 27.00, 'commuter14'),
('6603808416168570', 41.50, 'busrider73'),
('7301442590825470', 6.00, 'sandrapatel'),
('7534785562588930', 85.50, 'adinozzo'),
('7792685035977770', 80.25, 'riyoy1996'),
('8753075721740010', 110.00, 'sandrapatel'),
('8802558078528210', 42.25, 'busrider73'),
('9248324548250130', 12.75, 'sandrapatel'),
('9286930794479390', 116.25, 'kellis'),
('9712526903816770', 68.50, 'busrider73'),
('9876543212345670', 92.50, NULL);

--
-- Dumping data for table `BusStationIntersection`
--

INSERT INTO `BusStationIntersection` (`StopID`, `Intersection`) VALUES
('31955', 'North Point Pkwy'),
('35161', 'Park Bridge Pkwy'),
('46612', 'Commerce Pkwy'),
('95834', 'Haynes Bridge Pkwy'),
('BUSDOME', NULL),
('BUSN11', 'Peachtree-Dunwoody Road'),
('BUSN4', '10th Street'),
('BUSS2', NULL);

--
-- Dumping data for table `Conflict`
--

INSERT INTO `Conflict` (`Username`, `BreezecardNum`, `DateAndTime`) VALUES
('kellis', '4769432303280540', '2017-10-23 16:21:49'),
('riyoy1996', '4769432303280540', '0000-00-00 00:00:00'),
('sandrapatel', '0475861680208144', '2018-11-12 00:00:01');

--
-- Dumping data for table `Passenger`
--

INSERT INTO `Passenger` (`Username`, `Email`) VALUES
('adinozzo', 'anthony.dinozzo@ncis.mil.gov'),
('ashton.woods', 'awoods30@gatech.edu'),
('ignacio.john', 'john@iconsulting.com'),
('kellis', 'kateellis@gatech.edu'),
('busrider73', 'lena.wexler@dayrep.com'),
('commuter14', 'LeonBarnes@superrito.com'),
('sandrapatel', 'sandra74@jourrapide.com'),
('riyoy1996', 'yamada.riyo@navy.mil.gov');

--
-- Dumping data for table `Station`
--

INSERT INTO `Station` (`StopID`, `Name`, `EnterFare`, `ClosedStatus`, `IsTrain`) VALUES
('31955', 'Old Milton Pkwy - North Point Pkwy', 2.00, 0, 0),
('35161', 'Old Milton Pkwy - Park Bridge Pkwy', 2.00, 1, 0),
('46612', 'Alpharetta Hwy - Commerce Pkwy', 2.00, 0, 0),
('95834', 'Old Milton Pkwy - Haynes Bridge Pkwy', 2.00, 0, 0),
('BUSDOME', 'Georgia Dome Bus Station', 4.00, 0, 0),
('BUSN11', 'North Springs', 2.00, 0, 0),
('BUSN4', 'Midtown', 5.00, 0, 0),
('BUSS2', 'West End', 2.50, 0, 0),
('E1', 'Georgia State', 2.50, 0, 1),
('E2', 'King Memorial', 2.50, 0, 1),
('E3', 'Inman Park/Reynolds Town', 2.50, 0, 1),
('E4', 'Edgewood/Candler Park', 2.50, 0, 1),
('E5', 'East Lake', 3.00, 0, 1),
('E6', 'Decatur', 2.50, 0, 1),
('E7', 'Avondale', 2.50, 0, 1),
('E8', 'Kensington', 3.00, 0, 1),
('E9', 'Indian Creek', 2.50, 0, 1),
('FP', 'Five Points', 8.00, 0, 1),
('N1', 'Peachtree Center', 6.00, 0, 1),
('N10', 'Sandy Springs', 2.00, 0, 1),
('N11', 'North Springs', 2.50, 0, 1),
('N2', 'Civic Center', 4.00, 0, 1),
('N3', 'North Avenue', 3.00, 0, 1),
('N4', 'Midtown', 5.00, 0, 1),
('N5', 'Arts Center', 4.00, 0, 1),
('N6', 'Lindbergh Center', 2.00, 0, 1),
('N7', 'Buckhead', 1.00, 0, 1),
('N8', 'Medical Center', 4.00, 0, 1),
('N9', 'Dunwoody', 3.00, 0, 1),
('P4', 'Bankhead', 1.00, 1, 1),
('S1', 'Garnett', 10.00, 0, 1),
('S2', 'West End', 25.00, 0, 1),
('S3', 'Oakland City', 5.00, 0, 1),
('S4', 'Lakewood/Ft. McPherson', 2.50, 1, 1),
('S5', 'East Point', 2.50, 0, 1),
('S6', 'College Park', 2.50, 0, 1),
('S7', 'Atlanta Airport', 2.50, 0, 1),
('W1', 'GA Dome, GA World Congress Center, Phillips Arena,', 2.50, 0, 1),
('W2', 'Vine City', 2.50, 0, 1),
('W3', 'Ashby', 2.50, 0, 1),
('W4', 'West Lake', 2.50, 0, 1),
('W5', 'Hamilton E. Holmes', 2.50, 1, 1);

--
-- Dumping data for table `Trip`
--

INSERT INTO `Trip` (`Tripfare`, `StartTime`, `BreezecardNum`, `StartsAt`, `EndsAt`) VALUES
(1.50, '2017-10-10 00:00:00', '7534785562588930', 'BUSS2', 'BUSDOME'),
(9.00, '2017-10-27 04:31:30', '7301442590825470', 'N4', 'N7'),
(1.00, '2017-10-27 09:40:11', '8753075721740010', 'N3', 'N4'),
(1.50, '2017-10-28 22:11:13', '9248324548250130', 'N4', 'N11'),
(3.50, '2017-10-28 23:30:10', '6411414737900960', 'N11', 'N4'),
(1.00, '2017-10-31 21:30:00', '1325138309325420', 'FP', NULL),
(3.50, '2017-10-31 22:31:10', '7792685035977770', 'E1', 'N3'),
(2.00, '2017-10-31 22:33:10', '0524807425551662', 'S7', 'N4'),
(10.50, '2017-11-02 13:11:11', '1788613719481390', 'BUSDOME', 'BUSN11'),
(4.00, '2017-11-02 13:11:11', '2792083965359460', '31955', '46612'),
(1.50, '2017-11-03 09:44:11', '0524807425551662', 'N4', 'N11'),
(2.75, '2017-11-05 16:21:49', '0524807425551662', 'N11', 'N4');

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`Username`, `Password`, `IsAdmin`) VALUES
('adinozzo', 'c67e443eaa780debf5ee2d71a2a7dc39', 0),
('admin', '0192023a7bbd73250516f069df18b500', 1),
('ashton.woods', '27465020c9ea11fc41fac2af1daeba5f', 0),
('busrider73', '0e63f5aa002eca0b0e293ee6b733c50a', 0),
('commuter14', '439c7fd92969510d873330e327c0f64d', 0),
('eoneil', '6b11eaa6bbd19c856b59688fae281d56', 1),
('ignacio.john', '6f5de409600e6ac40b8e7698bbd004f6', 0),
('kellis', '370133f7117dc65e277d6dbb858450c1', 0),
('kparker', '09e5af83d93166c76b351d52a8fe69b5', 1),
('riyoy1996', '7039e7594e4f4fd6789e9810150e64b9', 0),
('sandrapatel', '63c9e8af485ed2e845d29c2874e584ea', 0);
\
