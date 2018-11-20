import csv
import itertools
import numpy as np
import pickle
import sys

from model import VRP


''' HYPERPARAMETERS '''



# if not using command line input

run = 'final_test'
scenario = [1, 2]


''' SEARCH CONFIGURATION '''

heuristic_test = [
    'scenario', [1, 2],
    'heuristic', [False, True],
    'pop_size', [12],
    'selection_size', [2],
    'aco_iterations', [10],
    'beta', [1],
    'evap_rate', [.1],
    'beta_evap', [0],
    'crossover_prob', [0.05, 0.2],
    'mutation_prob', [0.05, 0.1],
    'reduce_clusters', [0],
    'kmeans_iterations', [10],
    'squared_dist', [True],
    'time_limit', [10] # in minutes
]

further_test = [
    'scenario', [1, 2],
    'heuristic', [True],
    'pop_size', [10, 14],
    'selection_size', [2, 4],
    'aco_iterations', [15, 25],
    'beta', [1],
    'evap_rate', [.1],
    'beta_evap', [0],
    'crossover_prob', [0.1, 0.2],
    'mutation_prob', [0.05, 0.1],
    'reduce_clusters', [0, 4],
    'kmeans_iterations', [10, 20],
    'squared_dist', [True],
    'time_limit', [10] # in minutes
]

final_test = [
    'scenario', [scenario],
    'heuristic', [True],
    'pop_size', [14],
    'selection_size', [6],
    'aco_iterations', [17],
    'beta', [.99],
    'evap_rate', [.1],
    'beta_evap', [.1],
    'crossover_prob', [.07],
    'mutation_prob', [.07],
    'reduce_clusters', [6],
    'kmeans_iterations', [20],
    'squared_dist', [True],
    'time_limit', [120] # in minutes
]


''' SEARCH FUNCTIONS '''

# retrieving dict by run name
input_dict = globals()[run]
if len(sys.argv) == 3:
    scenario = int(sys.argv[1])
    run = 'final_test' + sys.argv[1] + sys.argv[2]

def gridsearch(dict_list, run_name):

    # creating cartesian product of the dictionary as 2D-list
    # 1.: create a clean list of all parameters without parameter names
    iteration = []
    # if done with one element
    done = False
    for i, e in enumerate(dict_list):
        if done == False:
            done = True
        else:
            iteration.append(e)
            done = False

    # init saving-lists
    best = []
    mean = []

    # creating all permutations
    print('All permutations of test-parameters:')
    nr_of_perms = 0
    permutations = []
    for v in (itertools.product(*iteration)):
        permutations.append(v)
        print(v)
        nr_of_perms += 1

    # persisting parameter setup
    with open('./results/' + run_name + '.pickle', 'wb') as f:
        pickle.dump(dict_list, f)

    # deploy it
    count = 0
    for v in permutations:
        count += 1
        print(run_name, count, 'of', nr_of_perms, ':')
        print(dict_list)
        best_run, mean_run = VRP(scenario=v[0], heuristic=v[1], pop_size=v[2], selection_size=v[3], aco_iterations=v[4], beta=v[5], evap_rate=v[6], beta_evap=v[7], crossover_prob=v[8], mutation_prob=v[9], reduce_clusters=v[10], kmeans_iterations=v[11], squared_dist=v[12], time_limit=v[13] * 60)

        # saving results
        best.append(best_run)
        mean.append(mean_run)
    # persisting
    print('Endresults for best:')
    with open('./results/' + run_name + '_best.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in best:
            print(i)
            writer.writerow(i)
    print('Endresults for mean:')
    with open('./results/' + run_name + '_mean.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in mean:
            print(i)
            writer.writerow(i)


if __name__ == '__main__':
    gridsearch(input_dict, run)