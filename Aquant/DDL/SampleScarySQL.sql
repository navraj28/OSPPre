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
