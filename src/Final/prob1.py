"""
You have solar panels that are mounted on a pole in your front yard. They have three settings that tip the panels at 
different angles with respect to the horizontal. As the seasons change, the settings allow you to capture more solar 
energy by better aligning the tipping angle of the panels with the position of the sun in the sky. Let these settings 
be called 0, 1, and 2.
You are given the following:
A table that maps the day-of-year (1 to 366) and the setting (0, 1, 2) to an estimate of the energy you could collect.
 Let this table be E[d, s], 0 < d <= 366, and 0 <= s < 3. So E[d, s] will return the amount of energy you could collect
  if the panels are in setting s on day-of-year d.
Design an algorithm that will work out the days you should change from one setting to another over the year in order 
to maximize your solar energy collection. Note: You can only make a maximum of four changes in settings in a year.
"""
import numpy as np

days = 4

E = np.reshape(np.random.random(days*3), (days, -1))
settings = [0, 1, 2]
print(E)

def solar_panels(day, curr_set, changes):
    if day >= days:
        return 0.0
    # there are no more changes
    if changes >= 4:
        return sum(E[day:,curr_set])

    today_value = E[day][curr_set]
    return today_value + max(solar_panels(day + 1, setting, changes + (setting != curr_set)) for setting in settings)


def solar_dp(curr_set, days):
    change_limit = 4
    settings = 3
    # create cache
    c = np.zeros((days, settings, change_limit))

    # fill in base cases
    for i in range(days):
        for j in range(settings):
            c[i, j, change_limit - 1] = sum(E[i:, j])

    for i in range(days):
        for j in range(settings):
            for k in range(change_limit):
                c[i, j, k] = E[i][j] + max(c[i + 1, setting, k + (setting != curr_set)] for setting in range(settings))

    return max(c[days])


def traceback(c, days, best_setting):
    curr = (0, best_setting, 0)
    for i in range(days):
        m = max(c[curr[0] + 1, j, :] for j in range(3))
        next_curr = location(m)

        if next_curr[2] != curr[2]:
            print(f"At day {curr[0]}, panels changed to position{next_curr[1]}")
        else:
            print(f"Panels continued at postiion {next_curr[1]}")

        print(f" {E[i]} energy was gained today to make the total so far {E[next_curr]}")

    print(f"best Path resulted in {max(c[days])} gained")


print(solar_panels(0, 0, 0))
print(solar_panels(0, 1, 0))
print(solar_panels(0, 2, 0))

print(solar_dp(0, len(E)))
print(solar_dp(1, len(E)))
print(solar_dp(2, len(E)))
