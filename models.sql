CREATE TABLE operators (
    id INT AUTO_INCREMENT PRIMARY KEY, -- creates an integer column 'id' that auto-increments with each new record and sets it as the primary key
    name VARCHAR(100) NOT NULL, -- operator name
    color VARCHAR(7)     -- colour e.g. "#FF0000" for maps later
);

CREATE TABLE stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- station name
    code VARCHAR(10) -- station code
);

CREATE TABLE journeys (
    id INT AUTO_INCREMENT PRIMARY KEY,

    operator INT NOT NULL, -- foreign key to operators table
    originStation INT NOT NULL, -- foreign key to stations table
    destinationStation INT NOT NULL, -- foreign key to stations table

    journeyDate DATE NOT NULL, -- date of the journey

    trainNumber VARCHAR(50), -- e.g. "Amtrak 123", "VIA 45"

    locomotiveType VARCHAR(50), -- e.g. "Siemens Venture", "GE Genesis"
    locomotiveNumber VARCHAR(50), -- fleet number or identifier

    carType VARCHAR(50), -- e.g. "Amfleet II", "LRC"
    carNumber VARCHAR(50), -- fleet number or identifier

    gpxPath VARCHAR(255), -- path to the GPX file for the journey

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (operator) REFERENCES operators(id), -- sets up foreign key relationship with operators table
    FOREIGN KEY (originStation) REFERENCES stations(id), -- sets up foreign key relationship with stations table
    FOREIGN KEY (destinationStation) REFERENCES stations(id) -- sets up foreign key relationship with stations table
);

-- Junction table to link journeys and stations (for stops made during the journey)
CREATE TABLE journey_stops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    journeyID INT NOT NULL, -- foreign key to journeys table
    stationID INT NOT NULL, -- foreign key to stations table
    stopOrder INT NOT NULL, -- order of the stop in the journey

    FOREIGN KEY (journeyID) REFERENCES journeys(id), -- sets up foreign key relationship with journeys table
    FOREIGN KEY (stationID) REFERENCES stations(id) -- sets up foreign key relationship with stations table
);

ALTER TABLE operators ADD CONSTRAINT uq_operator_name UNIQUE (name); -- ensures operator names are unique
ALTER TABLE stations ADD CONSTRAINT uq_station_code UNIQUE (code); -- ensures station codes are unique