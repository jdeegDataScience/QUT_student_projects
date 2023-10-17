import pandas as pd
import numpy as np

# Music_shop_v1
# load dataset
music_data = pd.read_csv('Music_shop_v1.csv', na_filter=False, encoding='latin-1')


# check for duplicate records ; 292 duplicates in data
music_data.duplicated().value_counts()


# check for NAs
info = music_data.isna().sum()
cols = len(music_data.isna().sum())
for i in range(cols):
    print(f"{info.index[i]}, {info[i]}")


# check ranges of numeric features
cols = ['Energy', 'Loudness', 'Speechiness', 'Instrumentalness']
for i in range(len(cols)):
    print(f'{cols[i]}\nmin: {music_data[cols[i]].min()}\nmax:{music_data[cols[i]].max()}\n')


# Plot distributions of variables
# Distribution of Energy
energy_dist = sns.distplot(music_data['Energy'])
print("Energy")
plt.show()
# Distribution of Loudness
loudness_dist = sns.distplot(music_data['Loudness'])
print("\nLoudness")
plt.show()
# Distribution of Speechiness
speechiness_dist = sns.distplot(music_data['Speechiness'])
print("\nSpeechiness")
plt.show()
# Distribution of Instrumentalness
instrumentalness_dist = sns.distplot(music_data['Instrumentalness'])
print("\nInstrumentalness")
plt.show()
# Distribution of time_signature
time_signature_dist = sns.distplot(music_data['time_signature'])
print("\ntime_signature")
plt.show()
