DROP INDEX IF EXISTS
    adresse_fussballer_id_idx,
    auszeichnung_fussballer_id_idx,
    fussballer_nachname_idx;

DROP TABLE IF EXISTS
    adresse,
    auszeichnung,
    fussballer;

DROP TYPE IF EXISTS
    position;