CREATE TABLE Movies (
	adult boolean default 'False',
	budget integer default 0,
	homepage character varying(1000),
	movieID serial not null primary key,
	imdb_id character varying(20),
	original_language character varying(5) not null ,
	original_title character varying(500) not null ,
	overview text,
	popularity float default 0,
	poster_path character varying(500),
	release_date date not null,
	revenue integer default 0,
	runtime float default 0 not null ,
	status character varying(20),
	tagline character varying(1000),
	title character varying(1000) not null ,
	video boolean default 'False',
	vote_average float,
	vote_count integer default 0,
	created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

CREATE TABLE Movie_Ratings (
       ID serial not null PRIMARY KEY ,
       userID int REFERENCES auth_user(id) on delete cascade,
       movieID int REFERENCES Movies(movieID) on delete cascade,
       rating int not null,
       created_at timestamp with time zone not null,
       updated_at timestamp with time zone not null
);

CREATE TABLE Genres
(
    genreID serial not null primary key,
    name character varying(100) not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

CREATE TABLE Movies_Genres
(
    genre_id int not null REFERENCES Genres(genreID),
    movie_id int not null REFERENCES Movies(movieID)
);


CREATE TABLE Languages
(
    languageID serial not null primary key ,
    iso_639_1 character varying(5) not null ,
    name character varying(100) not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

CREATE TABLE Movies_Languages
(
    movie_id int not null REFERENCES Movies(movieID),
    language_id int not null REFERENCES Languages(languageID)
);

CREATE TABLE ProductionCompanies
(
    ProductionCompanyID serial not null primary key ,
    name character varying(200) not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

CREATE TABLE Movies_ProductionCompanies
(
    movie_id int not null REFERENCES Movies(movieID),
    ProductionCompanies_id int not null REFERENCES ProductionCompanies(ProductionCompanyID)
);


CREATE TABLE ProductionCountries
(
    ProductionCountryID serial not null primary key ,
    iso_639_1 character varying(5) not null ,
    name character varying(200) not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

CREATE TABLE Movies_ProductionCountries
(
    movie_id int not null REFERENCES Movies(movieID),
    ProductionCountry_id int not null REFERENCES ProductionCountries(ProductionCountryID)
);

CREATE TABLE Casts
(
    castID serial not null primary key ,
    character character varying(200) not null ,
    credit_id character varying(250),
    gender int not null ,
    movie_id int not null REFERENCES Movies(movieID) on delete cascade,
    name character varying(200) not null ,
    "order" integer not null ,
    profile_path character varying(500),
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

SELECT * FROM Movies;