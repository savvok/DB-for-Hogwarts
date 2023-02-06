CREATE INDEX name_index ON People using hash(name);
CREATE INDEX faculty_index on People using hash(faculty);
CREATE INDEX post_index on People using hash(post);
CREATE INDEX amount_people_index on Location using btree(amount_people);

EXPLAIN SELECT * FROM People WHERE name = 'Melissa Henderson';
EXPLAIN SELECT * FROM People WHERE name = 'Michael Sanchez' AND faculty = 'Gryffindor' AND post = 'Student';
