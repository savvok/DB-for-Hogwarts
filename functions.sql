CREATE OR REPLACE PROCEDURE alert_disturbance(track_id INTEGER) as $$
DECLARE
    ph_id INTEGER;
    time_track TIMESTAMP;
    begin
        if (SELECT COUNT(*) FROM Tracking WHERE Tracking_id = track_id) <= 0 then
            RAISE NOTICE 'Track with this id does not exist';
            return;
        elsif(SELECT Tracking.Disturbance_fixation FROM Tracking WHERE Tracking_id = track_id) = True then
            SELECT DISTINCT Phoenix_id into ph_id FROM Observation
                JOIN Map ON Map.Map_id = Observation.Map_id
                JOIN Location ON Location.Map_id = Map.Map_id
                JOIN Tracking ON Tracking.Location_id = Location.Location_id
                WHERE Tracking_id = track_id;
            SELECT Time INTO time_track FROM Tracking WHERE Tracking_id = track_id;
            INSERT INTO Alert(Time, phoenix_id,tracking_id) VALUES (time_track, ph_id,track_id);

        end if;

    end;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION handling_disturbances(alerts_id INTEGER, dang_level VARCHAR)
returns table(
    time_dist TIMESTAMP,
    danger VARCHAR,
    people_distr INTEGER,
    people_protector INTEGER,
    phoenix_id INTEGER,
    curator_id INTEGER,
    location_id INTEGER,
    alert_id INTEGER
    )as $$
DECLARE
    time_distr TIMESTAMP;
    id_distr INTEGER;
    id_protector INTEGER;
    id_cur INTEGER;
    loc_id INTEGER;
    ph_id INTEGER;

    begin
        if (SELECT COUNT(*) FROM Alert WHERE Alert.Alert_id = alerts_id) <= 0 then
            RAISE NOTICE 'Track with this id does not exist';
            return;
        else
            SELECT Tracking.Time INTO time_distr FROM Tracking
                JOIN Alert ON Alert.Tracking_id = Tracking.Tracking_id
                WHERE Alert.Alert_id = alerts_id;

            SELECT Tracking.People_id INTO id_distr FROM Tracking
                JOIN Alert ON Alert.Tracking_id = Tracking.Tracking_id
                WHERE Alert.Alert_id = alerts_id;

            SELECT Tracking.Location_id INTO loc_id FROM Tracking
                JOIN Alert ON Alert.Tracking_id = Tracking.Tracking_id
                WHERE Alert.Alert_id = alerts_id;

            SELECT Tracking.People_id INTO id_protector FROM Tracking
                JOIN People ON People.People_id = Tracking.People_id
                WHERE People.Post = 'Teacher' AND Tracking.Location_id = loc_id
                LIMIT 1;

            SELECT Alert.Phoenix_id INTO ph_id FROM Alert WHERE Alert.Alert_id = alerts_id;

            SELECT Curator.Curator_id INTO id_cur FROM Curator
                JOIN People ON People.People_id = Curator.People_id
                JOIN Tracking ON Tracking.People_id = People.People_id
                WHERE People.Post = 'Curator' AND Tracking.Location_id = loc_id
                LIMIT 1;

            INSERT INTO Disturbance(time, danger, people_distr, people_protector,
                                    phoenix_id, curator_id, location_id,
                                    alert_id) VALUES (time_distr, dang_level,
                                    id_distr,id_protector,ph_id,id_cur,loc_id,alerts_id);

            return query SELECT Disturbance.time, Disturbance.danger, Disturbance.people_distr, Disturbance.people_protector,
                                    Disturbance.phoenix_id, Disturbance.curator_id, Disturbance.location_id,
                                    Disturbance.alert_id FROM Disturbance
                WHERE Disturbance.alert_id = alerts_id;

        end if;
    end;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION feeding(name_ph VARCHAR, feeding_time TIMESTAMP)
returns table(
    datetime TIMESTAMP,
    curator_id INTEGER,
    phoenix_id INTEGER
    ) as $$
DECLARE
cur_id INTEGER;
ph_id INTEGER;
    begin
        SELECT Phoenix.Phoenix_id INTO ph_id FROM Phoenix
            JOIN People ON People.People_id = Phoenix.People_id
            WHERE People.Name = name_ph;


        if (SELECT COUNT(*) FROM Phoenix WHERE Phoenix.Phoenix_id = ph_id) <= 0 then
            RAISE NOTICE 'Phoenix with this id does not exist';
            return;
        else

            SELECT Observation.Curator_id INTO cur_id FROM Observation
                WHERE Observation.Phoenix_id = ph_id AND Observation.Time <= feeding_time
                ORDER BY Observation.Time DESC LIMIT 1;


        INSERT INTO Feed(time, curator_id, phoenix_id) VALUES (feeding_time, cur_id, ph_id);
        return query SELECT Feed.time, Feed.curator_id, Feed.phoenix_id FROM Feed
            WHERE Feed.phoenix_id =  ph_id AND
                Feed.curator_id = cur_id AND
                Feed.time = feeding_time;
        end if;
    end;
$$ language plpgsql;



CREATE OR REPLACE FUNCTION decency(teach_id INTEGER, check_id INTEGER)
returns INTEGER AS $$
DECLARE
distrs INTEGER;
begin
    if (SELECT COUNT(*) FROM People WHERE People_id = teach_id) <= 0 then
        RAISE NOTICE 'Teacher with this id does not exist';
            return NULL;
    elsif (SELECT COUNT(*) FROM People WHERE People_id = check_id) <= 0 then
        RAISE NOTICE 'Checked person with this id does not exist';
            return NULL;
    elsif (SELECT Post FROM People WHERE People_id = teach_id) <> 'Teacher' then
        RAISE NOTICE 'You are not a teacher, you do not have access';
            return NULL;
    else
            SELECT COUNT(disturbance_id) INTO distrs FROM Disturbance
            WHERE Disturbance.people_distr = check_id;
            return distrs;

    end if;
end;

$$ language plpgsql;


CREATE OR REPLACE PROCEDURE dangerous(teach_id INTEGER, loc_id INTEGER) as $$
begin
    if (SELECT COUNT(*) FROM People WHERE People_id = teach_id) <= 0 then
        RAISE NOTICE 'Teacher with this id does not exist';
        return;
    elsif (SELECT Post FROM People WHERE People_id = teach_id) <> 'Teacher' then
        RAISE NOTICE 'You are not a teacher, you do not have access';
        return;
    else
        UPDATE Location
        SET aviable_visit = 'False' WHERE Location_id = loc_id;
    end if;
end;

$$ language plpgsql;