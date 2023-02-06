from random import uniform, choice, random, randint, randrange, sample
from faker import Faker
from datetime import datetime, timedelta


class Map:
    def __init__(self, id, coordinates_lat, coordinates_long, name):
        self.id = id
        self.coordinates_lat = coordinates_lat
        self.coordinates_long = coordinates_long
        self.name = name


Maps = ['*']
Maps_names = ['Hogwarts', 'Durmstrang', 'Ilvermorny', 'Mahoutokoro', 'Uagadou', 'Koldovstoretz']

for i in range(0, 6):
    coordinate_lat = uniform(57.648222, 56.781418)
    coordinate_long = uniform(-4.119478, -2.648709)
    name = Maps_names[i]
    Maps.append(Map(i + 1, coordinate_lat, coordinate_long, name))


class People:
    def __init__(self, id, name, faculty, post, access_map, living_building_id):
        self.id = id
        self.name = name
        self.faculty = faculty
        self.post = post
        self.access_map = access_map
        self.living_building_id = living_building_id


Peoples = ['*']
Faculties = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin', 'None']
Posts = ['Teacher', 'Student', 'Curator']
fake = Faker()

for i in range(1, 6601):
    faculty = choice(Faculties)
    name = fake.name()
    magic = random()

    if magic >= 0.95:
        post = Posts[0]
        access_map = True
    elif magic >= 0.90:
        post = Posts[2]
        access_map = False
    else:
        post = Posts[1]
        access_map = False

    if faculty == 'Gryffindor':
        living_building_id = randrange(1, 27, 5)
    elif faculty == 'Hufflepuff':
        living_building_id = randrange(2, 28, 5)
    elif faculty == 'Ravenclaw':
        living_building_id = randrange(3, 29, 5)
    elif faculty == 'Slytherin':
        living_building_id = randrange(4, 30, 5)
    else:
        living_building_id = randrange(5, 31, 5)

    Peoples.append(People(i, name, faculty, post, access_map, living_building_id))


class Location:
    def __init__(self, id, name, aviable_visit, amount_people, map_id):
        self.id = id
        self.name = name
        self.aviable_visit = aviable_visit
        self.amount_people = amount_people
        self.map_id = map_id


Locations = ['*']
Location_name = ['School', 'Quidditch field', 'Village', 'forbidden Forest', 'Residential buildings', 'Garden']
id_loc = 1
for i in range(len(Maps_names)):
    map_id = i + 1
    for j in range(len(Location_name)):
        name = Location_name[j]
        time_hour = randint(1, 24)
        if name == 'forbidden Forest':
            aviable_visit = False
        elif name == 'Village' and (10 <= time_hour <= 14 or 15 <= time_hour <= 19):
            aviable_visit = False
        elif (name == 'Garden' or name == 'Quidditch field') and 8 > time_hour > 22:
            aviable_visit = False
        else:
            aviable_visit = True
        if aviable_visit:
            amount_people = randint(1, 150)
        else:
            amount_people = 0
        Locations.append(Location(id_loc, name, aviable_visit, amount_people, map_id))
        id_loc += 1


class Premises:
    def __init__(self, id, location_id, name, description):
        self.id = id
        self.location_id = location_id
        self.name = name
        self.description = description


Premise = ['*']
Premises_name = ['Dining room', 'Study room', 'Living room']
Premises_description1 = ['A place where all students gather for a meal three times a day',
                         "students living quarters where they sleep, study and rest"]
Premises_description = ['Transfiguration study room', 'Charms study room', 'Potions study room',
                        'Magic History Cabinet', 'Defence Against the Dark Arts', 'Astronomy study room',
                        'Herbology study room']
n_loc = len(Locations)
id_prem = 1
for i in range(1, n_loc - 1):
    location_id = i + 1
    if Locations[i].name == 'School':
        for j in range(1, 10):
            if random() > 0.90:
                name = Premises_name[0]
                description = Premises_description1[0]
            else:
                name = Premises_name[1]
                description = choice(Premises_description)
            Premise.append(Premises(id_prem, location_id, name, description))
            id_prem += 1
    elif Locations[i].name == 'Residential buildings':
        for j in range(1, 50):
            name = Premises_name[2]
            description = Premises_description1[1]
            Premise.append(Premises(id_prem, location_id, name, description))
            id_prem += 1


class Living_building:
    def __init__(self, id, location_id, faculty, amount):
        self.id = id
        self.location_id = location_id
        self.faculty = faculty
        self.amount = amount


Living_buildings = ['*']
id_liv = 1

for i in range(1, n_loc - 1):
    location_id = i
    if Locations[i].name == 'Residential buildings':
        for j in range(0, 5):
            amount = 0
            faculty = Faculties[j]

            for x in range(1, 6601):
                if Peoples[x].living_building_id == id_liv:
                    amount += 1

            Living_buildings.append(Living_building(id_liv, location_id, faculty, amount))
            id_liv += 1


class Tracking:
    def __init__(self, tracking_id, people_id, time, disturbance_fixation, location_id):
        self.tracking_id = tracking_id
        self.people_id = people_id
        self.time = time
        self.disturbance_fixation = disturbance_fixation
        self.location_id = location_id


start_datetime = datetime(1940, 1, 19)
Trackings = ['*']
track_id = 1
for i in range(1, 11):
    start_datetime = start_datetime + timedelta(days=1)
    for j in range(1, 1001):
        time = start_datetime + timedelta(hours=randint(8, 23), minutes=randint(0, 59))
        if random() > 0.98:
            disturbance_fixation = True
        else:
            disturbance_fixation = False
        location_id = randint(1, 36)
        id_p = randint(1, 6600)
        Trackings.append(Tracking(track_id, id_p, time, disturbance_fixation, location_id))
        track_id += 1


class Curator:
    def __init__(self, id, people_id, magic_skills):
        self.id = id
        self.people_id = people_id
        self.magic_skills = magic_skills


Curators = ['*']
Magic_skills = ['Accio', 'Lumos', 'Oculus Reparo', 'Muffliato', 'Petrificus Totalus', 'Confundo', 'Stupefy',
                'Wingardium Leviosa', 'Expecto Patronum', 'Locomotor Wibbly', 'Nox', 'Riddikulus', 'Homenum Revelio',
                'Obliviate', 'Protego', 'Obscuro', 'Crucio', 'Sectum Sempra', 'Expelliarmus', 'Geminio', 'Engorgio',
                'Imperio', 'Avada Kedavra']
for i in range(1, 6601):
    id = 1
    if Peoples[i].post == 'Curator':
        magic_skills = choice(Magic_skills)
        Curators.append(Curator(id, i, magic_skills))
        id += 1


class Phoenix:
    def __init__(self, id, people_id, reincarnation):
        self.id = id
        self.people_id = people_id
        self.reincarnation = reincarnation


Phoenixs = ['*']
Phoenixs_names = ['Fawkes', 'Tonks', 'Errol', 'Nagini', 'Trevor', 'Rubeus']

for i in range(1, 7):
    name = Phoenixs_names[i - 1]
    liv_ph_id = randrange(5, 31, 5)
    Peoples.append(People(6600 + i, name, 'None', 'None', True, liv_ph_id))
    reincarnation = randint(15, 30)

    Phoenixs.append(Phoenix(i, 6600 + i, reincarnation))


class Observation:
    def __init__(self, map_id, curator_id, phoenix_id, time):
        self.map_id = map_id
        self.curator_id = curator_id
        self.phoenix_id = phoenix_id
        self.time = time


Observations = ['*']
start_datetime2 = datetime(1940, 1, 19)
for j in range(1, 11):
    start_datetime2 = start_datetime2 + timedelta(days=1)
    for i in range(1, 7):
        curator_id = randint(1, len(Curators)-1)
        time = start_datetime2
        Observations.append(Observation(i, curator_id, 'NULL', time))

        curator_id = randint(1, len(Curators)-1)
        time = start_datetime2 + timedelta(hours=12)
        Observations.append(Observation(i, curator_id, i, time))


class Feed:
    def __init__(self, curator_id, phoenix_id, time):
        self.curator_id = curator_id
        self.phoenix_id = phoenix_id
        self.time = time


Feeding = ['*']
start_datetime1 = datetime(1940, 1, 19)
for i in range(1, 10):
    start_datetime1 = start_datetime1 + timedelta(days=1)
    for j in range(1, 7):
        curator_id = randint(1, len(Curators))
        for eat in range(1, 4):
            if eat == 1:
                time = start_datetime1 + timedelta(hours=12)
                Feeding.append(Feed(curator_id, j, time))
            elif eat == 2:
                time = start_datetime1 + timedelta(hours=16)
                Feeding.append(Feed(curator_id, j, time))
            else:
                time = start_datetime1 + timedelta(hours=20)
                Feeding.append(Feed(curator_id, j, time))


class Alert:
    def __init__(self, id, time, phoenix_id, tracking_id):
        self.id = id
        self.time = time
        self.phoenix_id = phoenix_id
        self.tracking_id = tracking_id


Alerts = ['*']
id_a = 1
for i in range(1, 10001):
    if Trackings[i].disturbance_fixation:
        time = Trackings[i].time + timedelta(minutes=10)
        phoenix_id = randint(1, 6)
        tracking_id = Trackings[i].tracking_id
        Alerts.append(Alert(id_a, time, phoenix_id, tracking_id))
        id_a += 1

Teachers = []
for i in range(1, 6601):
    if Peoples[i].post == 'Teacher':
        Teachers.append(i)


class Disturbance:
    def __init__(self, id, time, danger, people_distr, phoenix_id, people_protector, curator_id, location_id, alert_id):
        self.id = id
        self.time = time
        self.danger = danger
        self.people_distr = people_distr
        self.phoenix_id = phoenix_id
        self.people_protector = people_protector
        self.curator_id = curator_id
        self.location_id = location_id
        self.alert_id = alert_id


Disturbances = ['*']
Dangerous = ['low', 'average', 'high', 'very high']
id_distr = 1
for i in range(1, 10001):
    if Trackings[i].disturbance_fixation:
        time = Trackings[i].time + timedelta(minutes=10)
        dang = random()
        if dang > 0.99:
            danger = Dangerous[3]
        elif dang > 0.90:
            danger = Dangerous[2]
        elif dang > 0.5:
            danger = Dangerous[1]
        else:
            danger = Dangerous[0]
        people_distr = Trackings[i].people_id
        phoenix_id = randint(1, 6)
        people_protector = choice(Teachers)
        curator_id = randint(1, len(Curators)-1)
        location_id = Trackings[i].location_id
        Disturbances.append(
            Disturbance(id_distr, time, danger, people_distr, phoenix_id, people_protector, curator_id, location_id,
                        id_distr))
        id_distr += 1


class Disturbance_fixation:
    def __init__(self, people_id, disturbance_id):
        self.people_id = people_id
        self.disturbance_id = disturbance_id


Disturbances_fix = ['*']
for i in range(1, len(Disturbances)):
    people_id = Disturbances[i].people_distr
    disturbance_id = Disturbances[i].id
    Disturbances_fix.append(Disturbance_fixation(people_id, disturbance_id))

out = open("INSERT.txt", "w")


def wt(n, List, Headers):
    global out
    for i in range(1, n + 1):
        out.write("(")
        for j in range(len(Headers)):
            out.write("'")
            out.write(str(getattr(List[i], Headers[j])))
            out.write("'")
            if j != len(Headers) - 1:
                out.write(",")
        out.write(")")
        if i == n:
            out.write(";")
        else:
            out.write(",")
    out.write("\n")


print('---------------------------------- Maps')
for i in range(1, 6):
    print(Maps[i].id, Maps[i].name, Maps[i].coordinates_long, Maps[i].coordinates_lat)

out.write('INSERT INTO Map(name, coordinates_long, coordinates_lat) VALUES ')
wt(len(Maps_names), Maps, ['name', 'coordinates_long', 'coordinates_lat'])

print('\n---------------------------------- Locations')
print(n_loc)
for i in range(1, 7):
    print(Locations[i].map_id, Locations[i].id, Locations[i].name, Locations[i].aviable_visit,
          Locations[i].amount_people)

out.write('INSERT INTO Location(name, aviable_visit, amount_people, map_id) VALUES ')
wt(n_loc-1, Locations, ['name', 'aviable_visit', 'amount_people', 'map_id'])

print('\n---------------------------------- Living buildings')
print(len(Living_buildings))
for i in range(1, 6):
    print(Living_buildings[i].id, Living_buildings[i].location_id, Living_buildings[i].faculty,
          Living_buildings[i].amount)

out.write('INSERT INTO Living_building(location_id, faculty, amount) VALUES ')
wt(len(Living_buildings) - 1, Living_buildings, ['location_id', 'faculty', 'amount'])

print('\n---------------------------------- Peoples')
print(len(Peoples))
for i in range(1, 6):
    print(Peoples[i].id, Peoples[i].name, Peoples[i].living_building_id, Peoples[i].faculty, Peoples[i].post,
          Peoples[i].access_map)

out.write('INSERT INTO People(name, living_building_id, faculty, post, access_map) VALUES ')
wt(len(Peoples) - 1, Peoples, ['name', 'living_building_id', 'faculty', 'post', 'access_map'])

print('\n---------------------------------- Premises')
print(len(Premise))
for i in range(1, 10):
    print(Premise[i].id, Premise[i].name, Premise[i].description, Premise[i].location_id)

out.write('INSERT INTO Premises(name, description, location_id) VALUES ')
wt(len(Premise) - 1, Premise, ['name', 'description', 'location_id'])

print('\n---------------------------------- Trackings')
print(len(Trackings))
for i in range(1, 100):
    print(Trackings[i].tracking_id, Trackings[i].people_id, Trackings[i].location_id, Trackings[i].time, Trackings[i].disturbance_fixation)

out.write('INSERT INTO Tracking(people_id, location_id, time, disturbance_fixation) VALUES ')
wt(len(Trackings) - 1, Trackings, ['people_id', 'location_id', 'time', 'disturbance_fixation'])

print('\n---------------------------------- Curators')
print(len(Curators))
for i in range(1, 6):
    print(Curators[i].id, Curators[i].people_id, Curators[i].magic_skills)

out.write('INSERT INTO Curator(people_id, magic_skills) VALUES ')
wt(len(Curators) - 1, Curators, ['people_id', 'magic_skills'])

print('\n---------------------------------- Phoenix')
for i in range(1, 6):
    print(Phoenixs[i].id, Phoenixs[i].people_id, Phoenixs[i].reincarnation)

out.write('INSERT INTO Phoenix(people_id, reincarnation) VALUES ')
wt(len(Phoenixs) - 1, Phoenixs, ['people_id', 'reincarnation'])

print('\n---------------------------------- Observation')
print(len(Observations))
for i in range(1, 10):
    print(Observations[i].map_id, Observations[i].curator_id, Observations[i].phoenix_id, Observations[i].time)

out.write('INSERT INTO Observation(map_id, curator_id, phoenix_id, time) VALUES ')
wt(len(Observations) - 1, Observations, ['map_id', 'curator_id', 'phoenix_id', 'time'])

print('\n---------------------------------- Feeding')
print(len(Feeding))
for i in range(1, len(Feeding)):
    print(Feeding[i].time, Feeding[i].curator_id, Feeding[i].phoenix_id)

out.write('INSERT INTO Feed(time, curator_id, phoenix_id) VALUES ')
wt(len(Feeding) - 1, Feeding, ['time', 'curator_id', 'phoenix_id'])

print('\n---------------------------------- Alerts')
print(len(Alerts))
for i in range(1, 10):
    print(Alerts[i].id, Alerts[i].time, Alerts[i].phoenix_id, Alerts[i].tracking_id)

out.write('INSERT INTO Alert(time, phoenix_id,tracking_id) VALUES ')
wt(len(Alerts) - 1, Alerts, ['time', 'phoenix_id','tracking_id'])

print('\n---------------------------------- Disturbance')
print(len(Disturbances))
for i in range(1, 10):
    print(Disturbances[i].id, Disturbances[i].time, Disturbances[i].danger, Disturbances[i].people_distr,
          Disturbances[i].people_protector, Disturbances[i].phoenix_id, Disturbances[i].curator_id,
          Disturbances[i].location_id, Disturbances[i].alert_id)

out.write('INSERT INTO Disturbance(time, danger, people_distr, people_protector, phoenix_id, curator_id, location_id, '
          'alert_id) VALUES ')
wt(len(Disturbances) - 1, Disturbances,
   ['time', 'danger', 'people_distr', 'people_protector', 'phoenix_id', 'curator_id', 'location_id',
    'alert_id'])

print('\n---------------------------------- Disturbance')
print(len(Disturbances_fix))
for i in range(1, 10):
    print(Disturbances_fix[i].disturbance_id, Disturbances_fix[i].people_id)

out.write('INSERT INTO Disturbance_fixation(disturbance_id, people_id) VALUES ')
wt(len(Disturbances_fix)-1,Disturbances_fix,['disturbance_id', 'people_id'])

out.close()
