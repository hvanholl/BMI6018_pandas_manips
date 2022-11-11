# Assignment 6 Melt, aggregate, and pivot

# Demonstrate Melt, pivot, aggregation, iteration, group by

import pandas as pd
import numpy as np
migraine = pd.read_csv('migraine.csv')
newline = '\n'

# Melt and Groupby function -----------------------------------------------------

# Create a list of the columns that carry patient symptom information, exlcudes the outcome type and the patient age
symptoms = migraine.columns[1:-1]
# print(symptoms)

melted = migraine.melt(id_vars = ['Type', 'Age'],     # id values are the migraine type and the patient demographic info
              value_vars = [x for x in symptoms],     # for the values include every column in symptoms
              var_name = 'symptom', value_name = 'result')  # name the column names (variable) as the symptom and the value as the result
# To summarize the data, groupby the symptom and aggregate the mean and sum of the value column in the melted df
symptom_summary = melted.groupby('symptom').agg(mean = ('result', 'mean'), total = ('result', 'sum'))

print(f'{newline}A view of the first few rows of the melted dataframe')             
print(melted.head)

print(f'{newline}A summary of the symptom values, median and total')
print(symptom_summary)
# The resulting dataframe has four columns (2 identifiers, one variable, and one value) 


# Pivot and aggregate function -----------------------------------------------------

# The pivot_table function can handle duplicates, the pivot cannot so it was not working with this dataset
pivot = pd.pivot_table(migraine, 
                       index = ['Type'],    # For each category of migraine
                       columns = ['Intensity'],   # Across the intensity scale
                       values = 'Visual',    # how associated are they with visual effects
                       aggfunc = np.mean)    # Took the mean to account for the different frequencies
# It was interesting that the highest value was for aura without migraine, so the disorder is more characterized by visual effects than the pain. This is obviously not a statistically sound approach but an interesting quick data exploration. 

print(f'{newline}A view of the resulting pivot table. Indexed by type, intensity value as columns, the mean of the visual effects symptom are the values')
print(pivot)


# Aggregate and groupby -----------------------------------------------

# groupby the type and use aggregate to get the mean of every column in the df
agg = migraine.groupby('Type').agg('mean')
# for the yes/no phenotypes, you can see the proportion of cases where each symptom is seen. You can see the average duration in days, frequency per month, and intensity (0-3 scale)

print(f'{newline}The original migraine dataframe grouped by Type and aggregated by mean for each column')
print(agg)


# Iteration ----------------------------------------------------------

# Goal is to get the proportion of cases where light sensitivity or visual effects occur with a family history
both = 0       # set a variable equal to zero to start the count
family = 0      #
photo = 0
for row in migraine.itertuples():       # iterate through dataframe with itertuples. It converts each row to a tuple.
    if row.Visual == 1 and row.DPF == 1:      # If light sensitivity plus visual is greater than or equal to one (needs to have at least one of these symptoms).
        both += 1     # Add one to the count
    if row.DPF == 1:    # family history alone
        family += 1
    if row.Visual == 1: #visual effects alone
        photo += 1
both = both/len(migraine)*100      
family = family/len(migraine)*100
photo = photo/len(migraine)*100

print(f'{newline}Both: {both}, family history only: {family}, photo only: {photo}')

expect = family*photo/100
print(f'{newline}The expected value for having family history and visual effects by chance is {expect}% which is not much different than the actual value ({both}%). This is likely (without actually calculating a p-value) not significantly related.')

