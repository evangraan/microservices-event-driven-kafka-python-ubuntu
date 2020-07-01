```
kafka=# \dt;
         List of relations
 Schema |   Name   | Type  | Owner 
--------+----------+-------+-------
 public | cleaners | table | kafka
 public | medical  | table | kafka
 public | patients | table | kafka
 public | porters  | table | kafka
 public | rooms    | table | kafka
 public | waiting  | table | kafka
(6 rows)

kafka=# \d cleaners
                                    Table "public.cleaners"
  Column  |         Type          | Collation | Nullable |               Default                
----------+-----------------------+-----------+----------+--------------------------------------
 id       | integer               |           | not null | nextval('cleaners_id_seq'::regclass)
 name     | character varying(32) |           |          | 
 occupied | boolean               |           |          | 
Indexes:
    "cleaners_pkey" PRIMARY KEY, btree (id)

kafka=# \d medical
                                    Table "public.medical"
  Column  |         Type          | Collation | Nullable |               Default               
----------+-----------------------+-----------+----------+-------------------------------------
 id       | integer               |           | not null | nextval('medical_id_seq'::regclass)
 name     | character varying(32) |           |          | 
 occupied | boolean               |           |          | 
Indexes:
    "medical_pkey" PRIMARY KEY, btree (id)

kafka=# \d porters
                                    Table "public.porters"
  Column  |         Type          | Collation | Nullable |               Default               
----------+-----------------------+-----------+----------+-------------------------------------
 id       | integer               |           | not null | nextval('porters_id_seq'::regclass)
 name     | character varying(32) |           |          | 
 occupied | boolean               |           |          | 
Indexes:
    "porters_pkey" PRIMARY KEY, btree (id)

kafka=# \d rooms
                                    Table "public.rooms"
  Column  |         Type          | Collation | Nullable |              Default              
----------+-----------------------+-----------+----------+-----------------------------------
 id       | integer               |           | not null | nextval('rooms_id_seq'::regclass)
 name     | character varying(32) |           |          | 
 occupied | boolean               |           |          | 
Indexes:
    "rooms_pkey" PRIMARY KEY, btree (id)

kafka=# \d waiting
                                      Table "public.waiting"
   Column    |         Type          | Collation | Nullable |               Default               
-------------+-----------------------+-----------+----------+-------------------------------------
 id          | integer               |           | not null | nextval('waiting_id_seq'::regclass)
 patient     | character varying(32) |           |          | 
 room        | character varying(32) |           |          | 
 waiting_for | character varying(32) |           |          | 
Indexes:
    "waiting_pkey" PRIMARY KEY, btree (id)

kafka=# \d patients
                                    Table "public.patients"
  Column  |         Type          | Collation | Nullable |               Default                
----------+-----------------------+-----------+----------+--------------------------------------
 id       | integer               |           | not null | nextval('patients_id_seq'::regclass)
 uuid     | character varying(32) |           |          | 
 room     | character varying(32) |           |          | 
 released | boolean               |           |          | 
Indexes:
    "patients_pkey" PRIMARY KEY, btree (id)
```