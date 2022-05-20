import pulp
from pulp import LpVariable, LpMinimize, LpProblem, lpSum

userconstraints = {'user1_task1': [20, 23, 1, 1],
            'user1_task2': [18, 23, 1, 2],
            'user1_task3': [19, 21, 1, 1],
            'user1_task4': [12, 20, 1, 3],
            'user1_task5': [6, 12, 1, 3],
            'user1_task6': [18, 20, 1, 2],
            'user1_task7': [4, 10, 1, 2],
            'user1_task8': [12, 18, 1, 2],
            'user1_task9': [7, 14, 1, 3],
            'user1_task10': [8, 14, 1, 3],'user2_task1': [11, 22, 1, 2],
            'user2_task2': [5, 11, 1, 2],
            'user2_task3': [5, 23, 1, 1],
            'user2_task4': [6, 20, 1, 3],
            'user2_task5': [19, 19, 1, 1],
            'user2_task6': [18, 21, 1, 2],
            'user2_task7': [3, 23, 1, 3],
            'user2_task8': [21, 23, 1, 2],
            'user2_task9': [13, 17, 1, 1],
            'user2_task10': [6, 11, 1, 2],
            'user3_task1': [20, 23, 1, 2],
            'user3_task2': [15, 21, 1, 3],
            'user3_task3': [11, 15, 1, 2],
            'user3_task4': [2, 17, 1, 3],
            'user3_task5': [13, 16, 1, 2],
            'user3_task6': [10, 18, 1, 2],
            'user3_task7': [21, 23, 1, 2],
            'user3_task8': [20, 23, 1, 1],
            'user3_task9': [7, 21, 1, 2],
            'user3_task10': [0, 7, 1, 3],
            'user4_task1': [1, 8, 1, 1],
            'user4_task2': [11, 20, 1, 2],
            'user4_task3': [12, 19, 1, 3],
            'user4_task4': [11, 16, 1, 3],
            'user4_task5': [16, 18, 1, 1],
            'user4_task6': [19, 23, 1, 3],
            'user4_task7': [22, 23, 1, 1],
            'user4_task8': [12, 19, 1, 2],
            'user4_task9': [8, 20, 1, 2],
            'user4_task10': [4, 12, 1, 2],
            'user5_task1': [4, 20, 1, 1],
            'user5_task2': [18, 22, 1, 3],
            'user5_task3': [4, 16, 1, 1],
            'user5_task4': [2, 16, 1, 3],
            'user5_task5': [16, 23, 1, 2],
            'user5_task6': [6, 18, 1, 2],
            'user5_task7': [2, 6, 1, 1],
            'user5_task8': [13, 17, 1, 3],
            'user5_task9': [15, 23, 1, 1],
            'user5_task10': [17, 23, 1, 1]}




# def compute_energy_schedule(user_tasks, price_guideline):
#     for i in range(24):
#         totalvariables.append(LpVariable(name="total_demand_" + i))

def compute_schedule_user_energy_demand(userconstraints, price_guideline):
    totalvariables = []
    sumsvariables = []
    energymodel = LpProblem("Energy_schedule_problem", sense=LpMinimize)
    for i in range(24):
        # List of variables representing the total demand per hour
        totalvariables.append(LpVariable(name="total_demand_" + str(i)))
        # List containing lists of all variables to compute sum constraints for total demand
        # e.g task1_0 and task2_0 are the variables representing the demand of task 1 and task 2 in timeslot 0
        # Only task1_0 and task2_0 will be added into sumsvariable[0], and a constraint will be built from them
        sumsvariables.append([])

    uniquemaker = 0
    for k,v in userconstraints.items():
        v.append(uniquemaker)
        uniquemaker = uniquemaker + 1

    taskconstraints = {tuple(v): k for k, v in userconstraints.items()}
    print(taskconstraints)
    for user_task in taskconstraints:
        ready_time = user_task[0]
        deadline = user_task[1]
        energy_perhour = user_task[2]
        energy_demand = user_task[3]
        taskslist = []
        for i in range(deadline - ready_time + 1):
            namestring = taskconstraints[user_task] + "_" + str((i + ready_time))
            x = LpVariable(name=namestring, lowBound=0, upBound=energy_perhour)
            energymodel += (0 <= x <= energy_perhour )
            sumsvariables[i + ready_time].append(x)
            taskslist.append(x)
        energymodel += (lpSum(taskslist) == energy_demand, taskconstraints[user_task] + "_demand_constraint")
    obj_list = []
    print("Price guideline is : " + str(price_guideline))
    print("Length of price guideline is: " + str(len(price_guideline)))
    for i in range(24):
        if sumsvariables[i]:
            energymodel += (totalvariables[i] == lpSum(sumsvariables[i]), "total_demand_sum_" + str(i))
        else:
            energymodel += (totalvariables[i] == 0, "total_demand_sum_" + i)
        print(i)
        energymodel += (0<=totalvariables[i], "min_total_demand_constraint_" + str(i))
        obj_list.append(price_guideline[i]*totalvariables[i])
    obj_func = (lpSum(obj_list))
    energymodel += obj_func
    energymodel.writeLP("schedulexample")
    energysolved = energymodel.solve()
    objectiveValues = []
    for i in totalvariables:
        objectiveValues.append(i.varValue)
    return objectiveValues

#Below is just some code used to test the scheduler
testguideline = [4.51285340120281, 3.43658107523701, 3.68255559134804, 3.06271757467767, 3.45627812546856, 4.02803853654439, 3.53047024505285, 4.29234009190491, 5.01899399964376, 4.7831896810001, 5.39649373091393, 3.62164525353888, 6.52511405066837, 4.34263631482957, 5.85722269007359, 6.38160238785678, 6.11551929701169, 6.29475554382194, 6.5131445728803, 5.25018950601471, 5.913804588632, 5.12382685690879, 5.62943812228955, 5.75354475562452]
print(len(testguideline))
schedule = compute_schedule_user_energy_demand(userconstraints,testguideline)
print(schedule)
for i in range(24):
    if schedule[i] == 20.0:
        print(i)
    else:
        pass
countdemanders = 0
for k,v in userconstraints.items():
    if v[0] <= 13 and v[1] >= 13:
        print("User task is: " + k + " And their energy demand is: " + str(v[2]))
        countdemanders = countdemanders+1
    else:
        pass
print("There are " + str(countdemanders) + " tasks capable of asking for energy at hour 13")
print(len(testguideline))
print(len(schedule))