CREATE DATABASE spider_user DEFAULT CHARACTER
SET utf8 DEFAULT COLLATE utf8_general_ci;

USE spider_user;

CREATE TABLE user_info (
	id INT auto_increment PRIMARY KEY,
	user_avator_url VARCHAR (200),
	user_token VARCHAR (50) UNIQUE NOT NULL,
	user_name VARCHAR (50) NOT NULL,
	user_headline VARCHAR (200),
	user_location VARCHAR (100),
	user_business VARCHAR (50),
	user_employments VARCHAR (100),
	user_educations VARCHAR (100),
	user_description VARCHAR (250),
	user_gender INT,
	user_following_count INT,
	user_follower_count INT,
	user_answer_count INT,
	user_question_count INT,
	user_voteup_count INT,
	INDEX (user_token)
) ENGINE = INNODB DEFAULT CHARACTER
SET = utf8;

CREATE TABLE follow_relation (
	follow_from VARCHAR (50) NOT NULL,
	follow_in VARCHAR (50) NOT NULL,
	PRIMARY KEY (follow_from, follow_in)
) ENGINE = INNODB DEFAULT CHARACTER
SET = utf8;