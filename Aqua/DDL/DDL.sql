CREATE DATABASE IF NOT EXISTS aqua;
 
USE aqua;

CREATE TABLE IF NOT EXISTS master_symptoms (
    unique_product_id VARCHAR(255) NOT NULL,
    symptom_id INT NOT NULL,
	symptom_text VARCHAR(255) NOT NULL,
	symptom_question VARCHAR(255) NOT NULL,
	vector VARCHAR(20000) NOT NULL,
    PRIMARY KEY (unique_product_id, symptom_id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS wo_symptom_cooccurence (
	unique_product_id VARCHAR(255) NOT NULL,
	work_order_id VARCHAR(255) NOT NULL,	
	symptom_id INT not null
)   ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS wo_parts (
	unique_product_id VARCHAR(255) NOT NULL,
	work_order_id VARCHAR(255) not null,
	part_id INT ,
	number_of_parts INT 
)   ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS parts_master (
	unique_product_id VARCHAR(255) NOT NULL,
	part_id INT NOT NULL,
	part_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (part_id)
)   ENGINE=INNODB;


