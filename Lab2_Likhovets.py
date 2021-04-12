import numpy as np
import copy

repl_m = np.array([[1, 2, 3, 0, 0, 2, 3, 0, 0, 0],
                   [1, 1, 2, 5, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 4, 10, 1, 2, 0, 0, 0],
                   [0, 5, 1, 1, 5, 0, 0, 0, 2, 4],
                   [0, 0, 1, 1, 1, 0, 0, 0, 2, 2],
                   [1, 0, 1, 0, 0, 1, 1, 2, 0, 0],
                   [1, 0, 1, 0, 0, 0, 1, 2, 0, 0],
                   [0, 0, 0, 0, 0, 1, 1, 1, 2, 0],
                   [0, 2, 0, 1, 0, 0, 0, 1, 1, 2],
                   [0, 1, 0, 0, 1, 0, 1, 1, 1, 1]])

prod_v = np.array([0, 29, 0, 10, 0, 0, 15, 20, 0, 0])
config_time_v = np.array([1000, 1000, 1200, 1200, 1400, 1100, 1150, 1200, 1100, 2000])
production_time_v = np.array([6000, 6600, 7200, 7200, 8400, 6600, 6900, 7200, 9000, 9000])
pumps_list = ["V1", "V2", "SV1", "SV2", "SV3", "W1", "W15", "W2", "SW2", "SW3"]


def addition_to_not_zero_elements(matrix, vector):
    for i, row in enumerate(matrix):
        for j, elem in enumerate(vector):
            if elem != 0:
                matrix[i, j] += vector[j]


# Including config time
# Need to minimize total time to produce prodV pumps
def get_matrix_and_list_mins_in_columns(matrix, config_time_v):
    temp = np.transpose(copy.copy(matrix))
    addition_to_not_zero_elements(matrix, config_time_v)
    min_index = 1000
    min_value = 1e15
    list_values = []
    list_indexes = []
    for i, row in enumerate(temp):
        for j, val in enumerate(row):
            if val < min_value and val != 0:
                min_index = j
                min_value = val
        if min_value < 1e15:
            list_values.append(min_value)
            list_indexes.append(min_index)
        min_value = 1e15
        min_index = 1000

    print("list_values\n", list_values)
    print("list_indexes\n", list_indexes)
    return list_values, list_indexes


def get_result():
    list_values, list_indexes = get_matrix_and_list_mins_in_columns(prod_time_m,
                                                                    config_time_v)
    conf_time = []
    for val in list_indexes:
        conf_time.append(config_time_v[val])
    conf_time_np = np.array(conf_time)
    print("Config time:", conf_time_np.max())
    arr_values = np.array(list_values)
    arr_values -= conf_time_np

    return (arr_values.max() + conf_time_np.max()), list_indexes


# Building matrix of total production time each pump (with one replacement)
prod_time_m = np.transpose(np.transpose(repl_m * prod_v) * production_time_v)

result = get_result()
print("Total time:", result[0], "mins equals to", (result[0] / 60), "hours")
print("\nPumps to produce:")
for i in result[1]:
    print(pumps_list[i], end=" ")
