import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt


def open_and_read(x):
  susceptible = []
  infected = []
  recovered = []
  dead = []
  hospitalized = []
  # total_dead = []
  # total_recovered = []
  # total_infected = []
  # infected_max = []
  with open(x, 'r', newline='\n') as result_file:
    for i, line in enumerate(result_file):
      if i > 0:
        for index, list in enumerate(line.split(',')):
          if index == 0:
            susceptible.append(np.array(list[1:].replace("'", '').split(), dtype=int))
          elif index == 1:
            infected.append(np.array(list[1:].replace("'", '').split(), dtype=int))
            infected_max.append(np.max(np.array(list[1:].replace("'", '').split(), dtype=int)))
          elif index == 2:
            recovered.append(np.array(list[1:].replace("'", '').split(), dtype=int))
          elif index == 3:
            dead.append(np.array(list[1:].replace("'", '').split(), dtype=int))
          elif index == 4:
            hospitalized.append(np.array(list[1:].replace("'", '').split(), dtype=int))
          elif index == 5:
            total_recovered.append(np.array(list[1:].replace("'", '').split(), dtype=int))
          elif index == 6:
            total_dead.append(np.array(list[1:].replace("'", '').split(), dtype=int))
          elif index == 7:
            total_infected.append(np.array(list[1:].replace("'", '').split(), dtype=int))
  return susceptible, infected, recovered, dead, hospitalized

def avgNestedLists(nested_vals):
  """
  Averages a 2-D array and returns a 1-D array of all of the columns
  averaged together, regardless of their dimensions.
  """
  output = []
  maximum = 0
  for lst in nested_vals:
    if len(lst) > maximum:
      maximum = len(lst)
  for index in range(maximum):  # Go through each index of longest list
    temp = []
    for lst in nested_vals:  # Go through each list
      if index < len(lst):  # If not an index error
        temp.append(lst[index])
    output.append(np.nanmean(temp))
  return output


susceptible = []
infected = []
recovered = []
dead = []
hospitalized = []
total_dead = []
total_recovered = []
total_infected = []
infected_max = []


with open('C:/Users/Hisham/Desktop/p6/embodied_ai/code/embodied_ai/experiments/covid/data.csv', 'r', newline='\n') as result_file:
    for i, line in enumerate(result_file):
        if i > 0:
            for index, list in enumerate(line.split(',')):
                if index == 0:
                    susceptible.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                elif index == 1:
                    infected.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    infected_max.append(np.max(np.array(list[1:].replace("'", '').split(), dtype=int)))
                elif index == 2:
                    recovered.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                elif index == 3:
                    dead.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                elif index == 4:
                    hospitalized.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                elif index == 5:
                    total_recovered.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                elif index == 6:
                    total_dead.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                elif index == 7:
                    total_infected.append(np.array(list[1:].replace("'", '').split(), dtype=int))

def plot_lockdown(x, title):
  susceptible, infected, recovered, dead, hospitalized = open_and_read(x)
  plt.plot(avgNestedLists(susceptible), label="Susceptible", color=(1, 0.5, 0))  # Orange
  plt.plot(avgNestedLists(infected), label="Infected", color=(1, 0, 0))  # Red
  plt.plot(avgNestedLists(recovered), label="Recovered", color=(0, 1, 0))  # Green
  plt.plot(avgNestedLists(dead), label="Dead", color=(0, 0, 0))  # Black
  plt.plot(avgNestedLists(hospitalized), label="Hospitalized", color=(0, 0, 1))  # Blue
  plt.title(title)
  plt.xlabel("60 Seconds (60 Days)")
  plt.ylabel("Population")
  plt.tick_params(labelbottom=False)
  plt.legend()
  print(
    f'average dead over all runs: {avgNestedLists(total_dead)} \n average recovered over all runs: {avgNestedLists(recovered)[-1]} \n average infected over all runs: {50 - avgNestedLists(susceptible)[-1]}')
  print('the Variance of the INFECTED PEAK is:', np.var([max(x) for x in infected]))
  print('the Standard Deviation of the INFECTED PEAK is:', np.std([max(x) for x in infected]))
  print('the Variance of the TOTAL DEAD is:', np.var(total_dead))
  print('the Standard Deviation of the TOTAL DEAD is:', np.std(total_dead))
  plt.show()


def box_plot_me(some_list, title):
  den0percent = some_list[:20]
  den5percent = some_list[20:40]
  den10percent = some_list[40:60]
  den15percent = some_list[60:80]
  den20percent = some_list[80:100]
  den25percent = some_list[100:120]
  den30percent = some_list[120:140]
  den35percent = some_list[140:160]
  den40percent = some_list[160:180]
  den45percent = some_list[180:200]
  den50percent = some_list[200:220]

  figure, ax = plt.subplots()
  ax.boxplot(
    [den0percent, den5percent, den10percent, den15percent, den20percent, den25percent, den30percent, den35percent,
     den40percent, den45percent, den50percent])
  ax.set_xticklabels([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
  ax.set_ylabel('n of infected')
  ax.set_xlabel('percentage of deniers')
  ax.set_title(title)
  figure.show()

deniers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
           5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
           7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
           10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
           12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
           15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
           17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
           20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
           22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
           25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]

'''uncomment those lines for total infected regression table/model (deniers & total infected)'''
infected_sum = [50-x[-1] for x in susceptible]
# model_infected = sm.OLS(infected_sum, deniers).fit()
# print(model_infected.summary())


'''uncomment those lines for total dead regression table/model (deniers & total dead)'''
# model_death = sm.OLS(total_dead, deniers).fit()
# # print(model_death.conf_int(0.05))
# print(model_death.summary())

'''uncomment those lines for infected peaks regression table/model (deniers & peak of infected)'''
# X = sm.add_constant(deniers)
# model_peak = sm.OLS(infected_max, deniers).fit()
# print(model_peak.summary())

'''uncomment those lines for total hospitalized regression table/model (deniers & hospitalized)'''
# model_death = sm.OLS(deniers, hospitalized).fit()
# print(model_death.summary())

''' plot total infected per run curve'''
# plt.plot(infected_sum, label="Hospitalized", color=(0, 0, 1))  # Blue
# plt.title("Plot of the peaks of the infected")
# plt.xlabel("Runs")
# plt.ylabel("Population")
# plt.legend()
# plt.show()

''' plot peaks curve of infected'''
# plt.plot(infected_max, label="curve of infected", color=(0, 0, 1))  # Blue
# plt.title("Plot of the peaks of the infected")
# plt.xlabel("Runs")
# plt.ylabel("Population")
# plt.legend()
# plt.show()

''' plot total infected per run curve'''
# plt.plot(total_dead, label="dead", color=(0, 0, 1))  # Blue
# plt.title("Plot of the total dead")
# plt.xlabel("Runs")
# plt.ylabel("Population")
# plt.legend()
# plt.show()

'''plot 0% deniers lockdown'''
plot_lockdown('C:/Users/Hisham/Desktop/p6/embodied_ai/code/embodied_ai/experiments/covid/data_files_w4/data_0.csv', 'Lockdown 0% Deniers')

'''plot 25% deniers lockdown'''
# plot_lockdown('C:/Users/Hisham/Desktop/p6/embodied_ai/code/embodied_ai/experiments/covid/data_files_w4/data_25.csv', 'Lockdown 25% Deniers')

'''plot 50% deniers lockdown'''
# plot_lockdown('C:/Users/Hisham/Desktop/p6/embodied_ai/code/embodied_ai/experiments/covid/data_files_w4/data_50.csv', 'Lockdown 50% Deniers')

''' boxplots peak of infected'''
# box_plot_me(infected_max, 'Lockdown infected peak')

''' boxplots total dead'''
# box_plot_me([x[0] for x in total_dead], 'Lockdown total dead')

''' boxplots of total infected'''
# infected_sum =[50-x[-1] for x in susceptible]
# box_plot_me(infected_sum, 'Lockdown total infected')
