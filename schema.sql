CREATE TABLE stasjoner (
    stasjons_id INT PRIMARY KEY,
    navn TEXT NOT NULL
);
CREATE TABLE tog (
    tog_nr INT PRIMARY KEY,
    tog_type INT NOT NULL,
    antall_seter INT NOT NULL
);
CREATE TABLE avganger (
    avgangs_id INT PRIMARY KEY,
    avgang_tog_nr INT NOT NULL,
    antall_togsett INT NOT NULL CHECK (antall_togsett IN (1, 2)),
    fra_stasjons_id INT NOT NULL,
    til_stasjons_id INT NOT NULL,
    avgangstid TEXT NOT NULL,
    plattform INT,
    FOREIGN KEY (avgang_tog_nr) REFERENCES tog(tog_nr),
    FOREIGN KEY (fra_stasjons_id) REFERENCES stasjoner(stasjons_id),
    FOREIGN KEY (til_stasjons_id) REFERENCES stasjoner(stasjons_id)
);
CREATE TABLE stopp (
    stopp_id INT PRIMARY KEY,
    avgangs_id INT NOT NULL,
    stasjons_id INT NOT NULL,
    rekkefolge INT NOT NULL,
    ankomst_tid TEXT,
    avgangs_tid TEXT,
    FOREIGN KEY (avgangs_id) REFERENCES avganger(avgangs_id),
    FOREIGN KEY (stasjons_id) REFERENCES stasjoner(stasjons_id)
);
CREATE TABLE priser(
    pris_id INT PRIMARY KEY,
    stasjons_id INT NOT NULL,
    billett_type TEXT NOT NULL,
    pris INT NOT NULL CHECK (pris >= 0),
    FOREIGN KEY (stasjons_id) REFERENCES stasjoner(stasjons_id)
);
CREATE TABLE billetter (
    billett_id INT PRIMARY KEY,
    kunde_navn TEXT,
    billett_type TEXT NOT NULL CHECK (
        billett_type IN (
            'voksen',
            'student',
            'honnør',
            'ungdom',
            'vernepliktig',
            'barn',
            'hentebillett',
            'flytog-ansatt'
        )
    ),
    billett_fra_id INT NOT NULL,
    billett_til_id INT NOT NULL,
    tid_kjøpt TEXT NOT NULL,
    tid_utløpt TEXT NOT NULL,
    aktivert TEXT NOT NULL DEFAULT 'nei' CHECK (aktivert IN ('ja', 'nei')),
    pris INT NOT NULL CHECK (pris >= 0),
    FOREIGN KEY (billett_fra_id) REFERENCES stasjoner(stasjons_id),
    FOREIGN KEY (billett_til_id) REFERENCES stasjoner(stasjons_id)
);
CREATE TABLE forsinkelser (
    forsinkelse_id INT PRIMARY KEY,
    forsinkelse_avgangs_id INT NOT NULL,
    forsinkelse_dato TEXT NOT NULL,
    minutter_forsinket INT NOT NULL,
    FOREIGN KEY (forsinkelse_avgangs_id) REFERENCES avganger(avgangs_id)
);