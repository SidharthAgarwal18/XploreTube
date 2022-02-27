CREATE TABLE IF NOT EXISTS cavideos(
	id SERIAL PRIMARY KEY,
	video_id text,
	trending_date text,
	title text,
	channel_title text NOT NULL,
	category_id bigint,
	publish_time timestamp NOT NULL,
	tags text,
	views bigint NOT NULL,
	likes bigint NOT NULL,
	dislikes bigint NOT NULL,
	comment_count bigint NOT NULL,
	thumbnail_link text,
	comments_disabled boolean,
	ratings_disabled boolean,
	video_error_or_removed boolean,
	description text,
	comments text[] DEFAULT ARRAY[]::text[]
);

CREATE TABLE IF NOT EXISTS devideos(
	id SERIAL PRIMARY KEY,
	video_id text,
	trending_date text,
	title text,
	channel_title text NOT NULL,
	category_id bigint,
	publish_time timestamp NOT NULL,
	tags text,
	views bigint NOT NULL,
	likes bigint NOT NULL,
	dislikes bigint NOT NULL,
	comment_count bigint NOT NULL,
	thumbnail_link text,
	comments_disabled boolean,
	ratings_disabled boolean,
	video_error_or_removed boolean,
	description text,
	comments text[] DEFAULT ARRAY[]::text[]
);

CREATE TABLE IF NOT EXISTS frvideos(
	id SERIAL PRIMARY KEY,
	video_id text,
	trending_date text,
	title text,
	channel_title text NOT NULL,
	category_id bigint,
	publish_time timestamp NOT NULL,
	tags text,
	views bigint NOT NULL,
	likes bigint NOT NULL,
	dislikes bigint NOT NULL,
	comment_count bigint NOT NULL,
	thumbnail_link text,
	comments_disabled boolean,
	ratings_disabled boolean,
	video_error_or_removed boolean,
	description text,
	comments text[] DEFAULT ARRAY[]::text[]
);

CREATE TABLE IF NOT EXISTS invideos(
	id SERIAL PRIMARY KEY,
	video_id text,
	trending_date text,
	title text,
	channel_title text NOT NULL,
	category_id bigint,
	publish_time timestamp NOT NULL,
	tags text,
	views bigint NOT NULL,
	likes bigint NOT NULL,
	dislikes bigint NOT NULL,
	comment_count bigint NOT NULL,
	thumbnail_link text,
	comments_disabled boolean,
	ratings_disabled boolean,
	video_error_or_removed boolean,
	description text,
	comments text[] DEFAULT ARRAY[]::text[]
);

CREATE TABLE IF NOT EXISTS usvideos(
	id SERIAL PRIMARY KEY,
	video_id text,
	trending_date text,
	title text,
	channel_title text NOT NULL,
	category_id bigint,
	publish_time timestamp NOT NULL,
	tags text,
	views bigint NOT NULL,
	likes bigint NOT NULL,
	dislikes bigint NOT NULL,
	comment_count bigint NOT NULL,
	thumbnail_link text,
	comments_disabled boolean,
	ratings_disabled boolean,
	video_error_or_removed boolean,
	description text,
	comments text[] DEFAULT ARRAY[]::text[]
);

\timing
\copy cavideos(video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description) from './data/CAvideos.csv' DELIMITER ',' CSV HEADER;
\timing

\timing
\copy devideos(video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description) from './data/DEvideos.csv' DELIMITER ',' CSV HEADER;
\timing

\timing
\copy frvideos(video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description) from './data/FRvideos.csv' DELIMITER ',' CSV HEADER;
\timing

\timing
\copy invideos(video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description) from './data/INvideos.csv' DELIMITER ',' CSV HEADER;
\timing

\timing
\copy usvideos(video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description) from './data/USvideos.csv' DELIMITER ',' CSV HEADER;
\timing

DELETE FROM 
	cavideos a
		USING cavideos b
WHERE
	a.id < b.id
	AND a.video_id=b.video_id;

DELETE FROM 
	devideos a
		USING devideos b
WHERE
	a.id < b.id
	AND a.video_id=b.video_id;

DELETE FROM 
	frvideos a
		USING frvideos b
WHERE
	a.id < b.id
	AND a.video_id=b.video_id;

DELETE FROM 
	invideos a
		USING invideos b
WHERE
	a.id < b.id
	AND a.video_id=b.video_id;

DELETE FROM 
	usvideos a
		USING usvideos b
WHERE
	a.id < b.id
	AND a.video_id=b.video_id;

CREATE INDEX ca_index ON cavideos(video_id);
CREATE INDEX de_index ON devideos(video_id);
CREATE INDEX fr_index ON frvideos(video_id);
CREATE INDEX in_index ON invideos(video_id);
CREATE INDEX us_index ON usvideos(video_id);

