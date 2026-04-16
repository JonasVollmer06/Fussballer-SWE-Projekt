SET default_tablespace = fussballerspace;

CREATE TYPE position_type AS ENUM ('TORWART', 'VERTEIDIGER', 'MITTELFELDSPIELER', 'STUERMER');

CREATE TABLE IF NOT EXISTS fussballer (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 100) PRIMARY KEY,
    version         INTEGER NOT NULL DEFAULT 0,
    nachname        TEXT NOT NULL,
    nationalitaet   TEXT NOT NULL,
    position        position_type,
    geburtsdatum    DATE CHECK (geburtsdatum < current_date),
    username        TEXT NOT NULL,
    erzeugt         TIMESTAMP NOT NULL,
    aktualisiert    TIMESTAMP NOT NULL
);


CREATE INDEX IF NOT EXISTS fussballer_nachname_idx ON fussballer(nachname);

CREATE TABLE IF NOT EXISTS adresse (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 100) PRIMARY KEY,
    plz             TEXT NOT NULL CHECK (plz ~ '\d{5}'),
    ort             TEXT NOT NULL,
    bundesland      TEXT NOT NULL,
    fussballer_id   INTEGER NOT NULL REFERENCES fussballer ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS adresse_fussballer_id_idx ON adresse(fussballer_id);

CREATE TABLE IF NOT EXISTS auszeichnung (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 100) PRIMARY KEY,
    bezeichnung     TEXT NOT NULL,
    saison          TEXT NOT NULL,
    fussballer_id   INTEGER NOT NULL REFERENCES fussballer ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS auszeichnung_fussballer_id_idx ON auszeichnung(fussballer_id);
