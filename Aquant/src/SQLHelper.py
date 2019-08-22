import mysql.connector
from Objects import WorkOrder, RootSymptom, PartsRecommendation

class PartsByWorkOrder:
    def __init__(self, partId, partName, countInWOs, avgNumberOfParts):
        self.partId = partId
        self.partName = partName
        self.countInWOs = round(countInWOs)
        self.avgNumberOfParts = avgNumberOfParts

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="aqua"
)

cursor = mydb.cursor()

def fetchRootSymptomsFromDB():
    rootSymptoms = []
    cursor.execute("select * from master_symptoms")
    result = cursor.fetchall()
    for row in result:
        rootSymptoms.append( RootSymptom(row[0], row[1], row[2], row[3], row[4]) )
    return rootSymptoms

#Given a set of Symptoms, return the PartId & Num of WOs that it appeared in.
#Used to predict Parts & their Probability
def buildPartsQuery(workOrder):
    sqlSample = (   'select part_id, count(*) CountOfPartInWO '
                    'from wo_parts '
                    'where work_order_id IN '
                    '('
                    '   select work_order_id '
                    '   from wo_symptom_cooccurence '
                    '   where symptom_id IN (3) '
                    ') '
                    'group by part_id '
                    'order by CountOfPartInWO desc '
                )

    beginning = ('select A.part_id, B.part_name, count(*) CountOfPartInWO, avg(A.number_of_parts) '
            'from wo_parts A, parts_master b '
            'where A.part_id = B.part_id AND A.work_order_id IN '
            '('
            '   select work_order_id '
            '   from wo_symptom_cooccurence '
            '   where symptom_id IN ('
            )    

    innerQueryStatic = (  'AND work_order_id IN '
                            '( '
                            '   select distinct work_order_id '
                            '   from wo_symptom_cooccurence '
                            '   where symptom_id IN ( '
                        )

    innerNotInQueryStatic = (  'AND work_order_id NOT IN '
                            '( '
                            '   select distinct work_order_id '
                            '   from wo_symptom_cooccurence '
                            '   where symptom_id IN ( '
                        )

    groupByQueryStatic = (  'group by work_order_id '
                            ') '
                        )  
    closingQueryStatic = (  'group by A.part_id '
                            'order by CountOfPartInWO desc '
                        )  

    firstIteration = True
    finalSQL = ""
    innerQuery = ""
    for sympromId in workOrder.rootSymptomIds:
        if firstIteration:
            finalSQL = beginning + str(sympromId) + ') '
            firstIteration = False
            continue
        innerQuery = innerQuery + innerQueryStatic + str(sympromId) + ') '

#    for sympromId in workOrder.rootSymptomIdsNotPresent:
#        innerQuery = innerQuery + innerNotInQueryStatic + str(sympromId) + ') '
    notInSymptoms = ""
    for sympromId in workOrder.rootSymptomIdsNotPresent:
        notInSymptoms = notInSymptoms + str(sympromId) + ","
    if notInSymptoms != "":
        notInSymptoms = notInSymptoms.rstrip(',')
        innerQuery = innerQuery + innerNotInQueryStatic + notInSymptoms + ') '

    finalSQL = finalSQL + innerQuery

    for sympromId in workOrder.rootSymptomIds:        
        finalSQL = finalSQL + groupByQueryStatic

#    for sympromId in workOrder.rootSymptomIdsNotPresent:        
#        finalSQL = finalSQL + groupByQueryStatic
    if len(workOrder.rootSymptomIdsNotPresent) >= 1:
        finalSQL = finalSQL + groupByQueryStatic

    finalSQL = finalSQL + closingQueryStatic
    cursor.execute(finalSQL)
    result = cursor.fetchall()
    results = []
    for row in result:
        results.append( PartsByWorkOrder(row[0], row[1], row[2], row[3]) )
    return results

#Given a set of Symptoms, find Total Num of WOs that it appeared in.
#Used to calculate Probability for Parts 
def buildWOCountQuery(workOrder):
    beginning = ('select count(distinct work_order_id) '
            'from wo_symptom_cooccurence '
            'where symptom_id IN ( '
            )    

    innerQueryStatic = (  'AND work_order_id IN '
                            '( '
                            '   select distinct work_order_id '
                            '   from wo_symptom_cooccurence '
                            '   where symptom_id IN ( '
                        )

    innerNotInQueryStatic = (  'AND work_order_id NOT IN '
                            '( '
                            '   select distinct work_order_id '
                            '   from wo_symptom_cooccurence '
                            '   where symptom_id IN ( '
                        )

    groupByQueryStatic = (  'group by work_order_id '
                            ') '
                        )  

    firstIteration = True
    finalSQL = ""
    innerQuery = ""
    for sympromId in workOrder.rootSymptomIds:
        if firstIteration:
            finalSQL = beginning + str(sympromId) + ') '
            firstIteration = False
            continue
        innerQuery = innerQuery + innerQueryStatic + str(sympromId) + ') '

    notInSymptoms = ""
    for sympromId in workOrder.rootSymptomIdsNotPresent:
        notInSymptoms = notInSymptoms + str(sympromId) + ","

    if notInSymptoms != "":
        notInSymptoms = notInSymptoms.rstrip(',')
        innerQuery = innerQuery + innerNotInQueryStatic + notInSymptoms + ') '

    finalSQL = finalSQL + innerQuery

    brackets = 0
    if len(workOrder.rootSymptomIdsNotPresent) >= 1:
        brackets = 1
    for i in range(len(workOrder.rootSymptomIds) + brackets -1):
        finalSQL = finalSQL + groupByQueryStatic
    
    cursor.execute(finalSQL)
    result = cursor.fetchall()
    for row in result:
        return row[0] 

def getPartsPredictiction(workOrder):
    totalWOsWithTheseSymptoms = buildWOCountQuery(workOrder)
    partsByWO = buildPartsQuery(workOrder)
    partRecommendations = []
    #Loop thru partsByWO - as long as the Part is used in ALL WOs or stop a 4

    for indx, partAndWO in enumerate(partsByWO):
        if indx > 5 and partAndWO.countInWOs < totalWOsWithTheseSymptoms:
            break
        percentage = round((partAndWO.countInWOs/totalWOsWithTheseSymptoms)*100)

        partRecommendations.append(PartsRecommendation(partAndWO.partId, partAndWO.partName, percentage, partAndWO.avgNumberOfParts))

    return partRecommendations


