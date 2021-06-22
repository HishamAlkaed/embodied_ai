import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

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

deniers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
           0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
           0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15,0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15,
           0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
           0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
           0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
           0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35,0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35,
           0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
           0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45,0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45]
infected_sum = np.sum([total_recovered, total_dead, total_infected], axis=0)
# uncomment those lines for total infected regression table/model (deniers & total infected)
model_infected = sm.OLS(deniers, infected_sum).fit()
# print(model_infected.summary())
''' plot max infected per run curve'''
# fig = plt.figure()
# plt.plot(infected_sum, label="Hospitalized", color=(0, 0, 1))  # Blue
# plt.title("Plot of the peaks of the infected")
# plt.xlabel("Runs")
# plt.ylabel("Population")
# plt.legend()
# plt.show()

# uncomment those lines for total dead regression table/model (deniers & total dead)
# model_death = sm.OLS(deniers, total_dead).fit()
# print(model_death.summary())

# uncomment those lines for infected peaks regression table/model (deniers & peak of infected)
# model_peak = sm.OLS(deniers, infected_max).fit()
# print(model_peak.summary())
''' plot peaks curve of infected'''
fig = plt.figure()
plt.plot(infected_max, label="Hospitalized", color=(0, 0, 1))  # Blue
plt.title("Plot of the peaks of the infected")
plt.xlabel("Runs")
plt.ylabel("Population")
plt.legend()
plt.show()

# uncomment those lines for total hospitalized regression table/model (deniers & hospitalized)
# model_death = sm.OLS(deniers, hospitalized).fit()
# print(model_death.summary())