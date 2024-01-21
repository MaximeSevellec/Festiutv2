DELIMITER |

CREATE TRIGGER Chevauchement_lieux
BEFORE INSERT ON event
FOR EACH ROW
BEGIN
    DECLARE overlap_count INT;
    SELECT COUNT(*)
    INTO overlap_count
    FROM Event
    WHERE adresseEvent = NEW.adresseEvent
        AND dateHeureDebutEvent < NEW.dateHeureFinEvent + INTERVAL 2 HOUR
        AND dateHeureFinEvent > NEW.dateHeureDebutEvent - INTERVAL 2 HOUR;
    IF overlap_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Chevauchement de dates détecté pour le même lieu et la même journée';
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE TRIGGER chevauchent_lieu_groupes
BEFORE INSERT ON event
FOR EACH ROW
BEGIN
    DECLARE overlap_count INT;
    SELECT COUNT(*)
    INTO overlap_count
    FROM Event
    WHERE adresseEvent = NEW.adresseEvent
        AND (
            (NEW.dateHeureDebutEvent < dateHeureFinEvent + INTERVAL 2 HOUR AND NEW.dateHeureFinEvent > dateHeureDebutEvent)
            OR (dateHeureDebutEvent < NEW.dateHeureFinEvent + INTERVAL 2 HOUR AND dateHeureFinEvent > NEW.dateHeureDebutEvent)
        )
        AND nom_groupe IS NOT NULL;

    IF overlap_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Deux groupes ne peuvent pas jouer au même endroit pendant les mêmes heures';
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE TRIGGER chevauchent_groupe
BEFORE INSERT ON event
FOR EACH ROW
BEGIN
    DECLARE overlap_count INT;
    SELECT COUNT(*)
    INTO overlap_count
    FROM Event
    WHERE nom_groupe = NEW.nom_groupe
        AND (
            (NEW.dateHeureDebutEvent < dateHeureFinEvent + INTERVAL 2 HOUR AND NEW.dateHeureFinEvent > dateHeureDebutEvent)
            OR (dateHeureDebutEvent < NEW.dateHeureFinEvent + INTERVAL 2 HOUR AND dateHeureFinEvent > NEW.dateHeureDebutEvent)
        );

    IF overlap_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le même groupe ne peut pas avoir des événements qui se chevauchent';
    END IF;
END |

DELIMITER ;


DELIMITER |

CREATE TRIGGER event_hors_festival
BEFORE INSERT ON event
FOR EACH ROW
BEGIN
    DECLARE festival_start_date DATETIME;
    DECLARE festival_end_date DATETIME;

    SELECT debutFest, finFest INTO festival_start_date, festival_end_date
    FROM Festival
    WHERE idFestival = NEW.idFestival;

    IF NEW.dateHeureDebutEvent < festival_start_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La date de début de l''événement ne peut pas être avant la date de début du festival';
    END IF;

    IF NEW.dateHeureFinEvent > festival_end_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La date de fin de l''événement ne peut pas être après la date de fin du festival';
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE TRIGGER plus_de_billets_que_de_places
BEFORE INSERT ON Billet
FOR EACH ROW
BEGIN
    DECLARE available_seats INT;
    SELECT (nbPlaceEvent - IFNULL(SUM(nbPlaceReserve), 0))
    INTO available_seats
    FROM Event
    LEFT JOIN Reserver ON Event.idEvent = Reserver.idEvent
    WHERE Event.idEvent = NEW.idEvent;

    IF NEW.nbPlaceBillet > available_seats THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Impossible d''acheter plus de billets que de places disponibles pour cet événement';
    END IF;
END |

DELIMITER ;

