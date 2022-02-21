CREATE TABLE IF NOT EXISTS cavideos(
	video_id text,
	trending_date text,
	title text,
	channel_title text,
	category_id bigint,
	publish_time timestamp,
	tags text,
	views bigint,
	likes bigint,
	dislikes bigint,
	comment_count bigint,
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
	channel_title text,
	category_id bigint,
	publish_time timestamp,
	tags text,
	views bigint,
	likes bigint,
	dislikes bigint,
	comment_count bigint,
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
	channel_title text,
	category_id bigint,
	publish_time timestamp,
	tags text,
	views bigint,
	likes bigint,
	dislikes bigint,
	comment_count bigint,
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
	channel_title text,
	category_id bigint,
	publish_time timestamp,
	tags text,
	views bigint,
	likes bigint,
	dislikes bigint,
	comment_count bigint,
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
	channel_title text,
	category_id bigint,
	publish_time timestamp,
	tags text,
	views bigint,
	likes bigint,
	dislikes bigint,
	comment_count bigint,
	thumbnail_link text,
	comments_disabled boolean,
	ratings_disabled boolean,
	video_error_or_removed boolean,
	description text
);
