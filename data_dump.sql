CREATE TABLE IF NOT EXISTS cavideos(
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
	description text
);

CREATE TABLE IF NOT EXISTS devideos(
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
	description text
);

CREATE TABLE IF NOT EXISTS frvideos(
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
	description text
);

CREATE TABLE IF NOT EXISTS invideos(
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
	description text
);

CREATE TABLE IF NOT EXISTS usvideos(
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
	description text
);

\copy cavideos from './data/CAvideos.csv' DELIMITER ',' CSV HEADER;

\copy devideos from './data/DEvideos.csv' DELIMITER ',' CSV HEADER;

\copy frvideos from './data/FRvideos.csv' DELIMITER ',' CSV HEADER;

\copy invideos from './data/INvideos.csv' DELIMITER ',' CSV HEADER;

\copy usvideos from './data/USvideos.csv' DELIMITER ',' CSV HEADER;