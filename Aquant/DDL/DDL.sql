CREATE DATABASE IF NOT EXISTS aqua;
 
USE aqua;

CREATE TABLE IF NOT EXISTS master_symptoms (
    unique_product_id VARCHAR(255) NOT NULL,
    symptom_id INT NOT NULL,
	symptom_text VARCHAR(255) NOT NULL,
	symptom_question VARCHAR(255) NOT NULL,
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

Insert into `parts_master` (unique_product_id, part_id, part_name) values ('ManufacturerProductFamilyProductLine', 1, 'Radiator Cap');
Insert into `parts_master` (unique_product_id, part_id, part_name) values ('ManufacturerProductFamilyProductLine', 2, 'Oil Change');
Insert into `parts_master` (unique_product_id, part_id, part_name) values ('ManufacturerProductFamilyProductLine', 3, 'Battery');
Insert into `parts_master` (unique_product_id, part_id, part_name) values ('ManufacturerProductFamilyProductLine', 4, 'Screws');

1.	Question for the next Symptom, given SymptomIds, ABOVE A MIN Threshold

select symptom_id, count(*) CountOfSymptoms
from wo_symptom_cooccurence
where work_order_id IN
(
  select work_order_id
	from wo_symptom_cooccurence  
	where symptom_id IN (3) 
	    AND work_order_id IN 
			(
					select distinct work_order_id
					from wo_symptom_cooccurence  
					where symptom_id IN (2)
					AND work_order_id NOT IN 
					(
						select distinct work_order_id
						from wo_symptom_cooccurence  
						where symptom_id IN (1)
						group by work_order_id
					)
					group by work_order_id
			)
	group by work_order_id
 )
 group by symptom_id
 having count(*) > 1
 order by CountOfSymptoms desc 

	
2.	Finding TOP N SIMIALR WOs given symptoms	
	Inner query in above query
	
3.	Given a Symptom, suggest Parts with Probability % 

select part_id, count(*) CountOfPartInWO, avg(number_of_parts)
from wo_parts
where work_order_id IN
(
  select work_order_id
	from wo_symptom_cooccurence  
	where symptom_id IN (3) 
	    AND work_order_id IN 
			(
					select distinct work_order_id
					from wo_symptom_cooccurence  
					where symptom_id IN (2)
					AND work_order_id NOT IN 
					(
						select distinct work_order_id
						from wo_symptom_cooccurence  
						where symptom_id IN (1)
						group by work_order_id
					)
					group by work_order_id
			)
	group by work_order_id
 )
 group by part_id
 order by CountOfPartInWO desc 
	
//The total WO count is required to calculate the Probablity
  select count(distinct work_order_id)
	from wo_symptom_cooccurence  
	where symptom_id IN (3) 
	    AND work_order_id IN 
			(
					select distinct work_order_id
					from wo_symptom_cooccurence  
					where symptom_id IN (2)
					AND work_order_id NOT IN 
					(
						select distinct work_order_id
						from wo_symptom_cooccurence  
						where symptom_id IN (1)
						group by work_order_id
					)
					group by work_order_id
			)
