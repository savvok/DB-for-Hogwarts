CREATE OR REPLACE FUNCTION tracking_check() returns TRIGGER as $$
DECLARE
ph_id INTEGER;
time_track TIMESTAMP;
begin
    if new.disturbance_fixation = True then
        SELECT DISTINCT Phoenix_id into ph_id FROM Observation
            JOIN Map ON Map.Map_id = Observation.Map_id
            JOIN Location ON Location.Map_id = Map.Map_id
            JOIN Tracking ON Tracking.Location_id = Location.Location_id
            WHERE Tracking_id = new.Tracking_id;
        SELECT Time INTO time_track FROM Tracking WHERE Tracking_id = new.Tracking_id;
        INSERT INTO Alert(Time, phoenix_id,tracking_id) VALUES (time_track, ph_id,new.Tracking_id);
    end if;
    return NEW;

end;
$$ language plpgsql;


CREATE TRIGGER disturb_check
    AFTER INSERT OR UPDATE ON Tracking
    FOR EACH ROW
    EXECUTE PROCEDURE tracking_check();


CREATE OR REPLACE FUNCTION disturb_fixation() returns TRIGGER as $$
begin
    INSERT INTO Disturbance_fixation(disturbance_id, people_id) VALUES (NEW.disturbance_id, NEW.people_distr)
end;
$$ language plpgsql;

CREATE TRIGGER fixation_distr
    AFTER INSERT OR UPDATE ON Disturbance
    FOR EACH ROW
    EXECUTE PROCEDURE disturb_fixation();


CREATE OR REPLACE FUNCTION feed_check() returns TRIGGER as $$
DECLARE
    cur1 INTEGER;
begin
    SELECT Observation.Curator_id INTO cur1 FROM Observation
    WHERE Phoenix_id = new.Phoenix_id AND Observation.Time <= new.Time
    ORDER BY Observation.Time DESC LIMIT 1;
    if new.Curator_id <> cur1 then
        RAISE NOTICE 'Phoenix was fed by the wrong curator, check id';
        return new;
    end if;
    return new;
end;
$$ language plpgsql;

CREATE TRIGGER check_feed
    AFTER INSERT OR UPDATE ON Feed
    FOR EACH ROW
    EXECUTE PROCEDURE feed_check();


CREATE OR REPLACE FUNCTION dangerous_check() returns TRIGGER as $$
DECLARE
    dang BOOL;
begin
    SELECT Location.aviable_visit INTO dang FROM Location
        JOIN Tracking ON Tracking.Location_id = Location.Location_id
        WHERE new.Location_id = Location.Location_id;

    if new.disturbance_fixation = False AND dang = False then
        RAISE NOTICE 'Attention! It is dangerous here now';
        new.disturbance_fixation = True;
        return NEW;
    end if;
    return NEW;
end;
$$ language plpgsql;

CREATE TRIGGER check_dangerous
    BEFORE INSERT OR UPDATE ON Tracking
    FOR EACH ROW
    EXECUTE PROCEDURE dangerous_check();