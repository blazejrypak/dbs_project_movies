CREATE TABLE Movies (
	adult boolean default 'False',
	budget integer default 0,
	homepage character varying(1000),
	movieID serial not null primary key,
	imdb_id character varying(20),
	original_language character varying(2) not null REFERENCES Languages(iso_639_1),
	original_title character varying(500) not null ,
	overview text,
	popularity float default 0,
	poster_path character varying(500),
	release_date date,
	revenue integer default 0,
	runtime float default 0,
	status character varying(20),
	tagline character varying(1000),
	title character varying(1000) not null ,
	video boolean default 'False',
	vote_average float,
	vote_count integer default 0,
	created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE Movie_Ratings (
       ID serial not null PRIMARY KEY ,
       userID int REFERENCES auth_user(id) on delete cascade,
       movieID int REFERENCES Movies(movieID) on delete cascade,
       rating float4 not null,
       created_at timestamp with time zone,
       updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS Genres
(
    genreID serial not null primary key,
    name character varying(100) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE Movies_Genres
(
    id serial not null primary key,
    genre_id int not null REFERENCES Genres(genreID),
    movie_id int not null REFERENCES Movies(movieID)
);


CREATE TABLE Languages
(
    iso_639_1 character varying(2) not null unique primary key,
    name character varying(100) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE Movies_Languages
(
    id serial not null primary key,
    movie_id int not null REFERENCES Movies(movieID),
    language_id character varying(2) not null REFERENCES  Languages(iso_639_1)
);

CREATE TABLE ProductionCompanies
(
    ProductionCompanyID serial not null primary key ,
    name character varying(200) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE Movies_ProductionCompanies
(
    id serial not null primary key,
    movie_id int not null REFERENCES Movies(movieID),
    ProductionCompanies_id int not null REFERENCES ProductionCompanies(ProductionCompanyID)
);


CREATE TABLE ProductionCountries
(
    iso_639_1 character varying(2) not null unique primary key,
    name character varying(200) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE Movies_ProductionCountries
(
    id serial not null primary key,
    movie_id int not null REFERENCES Movies(movieID),
    ProductionCountry_iso character varying(2) not null REFERENCES ProductionCountries(iso_639_1)
);

CREATE TABLE Casts
(
    id serial not null primary key,
    character character varying(200) not null ,
    credit_id character varying(250),
    gender int not null ,
    movie_id int not null REFERENCES Movies(movieID) on delete cascade,
    name character varying(200) not null ,
    "order" integer not null ,
    profile_path character varying(500),
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- SQL TO POPULATE Movies_Genres table with random product, from https://stackoverflow.com/a/10607880
INSERT INTO Movies_Genres (genre_id, movie_id)
SELECT genre_ID, movie_ID
FROM (SELECT genreid AS genre_ID, row_number() over () AS rn FROM movie_db.public.genres) x
JOIN (SELECT movieid AS movie_ID, (row_number() over () % small.ct) + 1 AS rn FROM movie_db.public.movies , (SELECT count(*) AS ct FROM movie_db.public.genres) AS small) y USING (rn);

-- SQL TO POPULATE Movies_Languages table with random product, from https://stackoverflow.com/a/10607880
INSERT INTO Movies_Languages (language_id, movie_id)
SELECT language_ID, movie_ID
FROM (SELECT iso_639_1 AS language_ID, row_number() over () AS rn FROM movie_db.public.languages) x
JOIN (SELECT movieid AS movie_ID, (row_number() over () % small.ct) + 1 AS rn FROM movie_db.public.movies , (SELECT count(*) AS ct FROM movie_db.public.languages) AS small) y USING (rn);

-- SQL TO POPULATE Movies_productionCountries table with random product, from https://stackoverflow.com/a/10607880
INSERT INTO Movies_ProductionCountries (productioncountry_iso, movie_id)
SELECT productioncountry_iso_ID, movie_ID
FROM (SELECT iso_639_1 AS productioncountry_iso_ID, row_number() over () AS rn FROM movie_db.public.productioncountries) x
JOIN (SELECT movieid AS movie_ID, (row_number() over () % small.ct) + 1 AS rn FROM movie_db.public.movies , (SELECT count(*) AS ct FROM movie_db.public.productioncountries) AS small) y USING (rn);

-- SQL TO POPULATE Movies_productionCompanies table with random product, from https://stackoverflow.com/a/10607880
INSERT INTO Movies_ProductionCompanies (productioncompanies_id, movie_id)
SELECT productioncompanies_id_ID, movie_ID
FROM (SELECT productioncompanyid AS productioncompanies_id_ID, row_number() over () AS rn FROM movie_db.public.productioncompanies) x
JOIN (SELECT movieid AS movie_ID, (row_number() over () % small.ct) + 1 AS rn FROM movie_db.public.movies , (SELECT count(*) AS ct FROM movie_db.public.productioncompanies) AS small) y USING (rn);
