import numpy as np
# def avgNestedLists(nested_vals):
#     """
#     Averages a 2-D array and returns a 1-D array of all of the columns
#     averaged together, regardless of their dimensions.
#     """
#     output = []
#     maximum = 0
#     for lst in nested_vals:
#         if len(lst) > maximum:
#             maximum = len(lst)
#     for index in range(maximum): # Go through each index of longest list
#         temp = []
#         for lst in nested_vals: # Go through each list
#             if index < len(lst): # If not an index error
#                 temp.append(lst[index])
#         output.append(np.nanmean(temp))
#     return output

a = [1,2,3,4,5,6,7,8,9,10]
b= [2,3,4,5,6,7,8,9,10,11,12,13]
c = [2,3,4,5,6,7,8,9,10,11,12,13,123,124,43,423,3,34,5]
d = [2,3,4,5,6,7,8]
# print(np.mean(np.array([d,c]).tolist(), axis=0))
a = np.array('50 50 50 50 50 50 50 50'.split())
print(a[0])
