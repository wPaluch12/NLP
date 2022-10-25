from os import listdir
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = []
additions_list = []
removal_list = []
changes_list = []
dates = []
ustawa_list = []
ustawa_followed_list = []
ustawa_notfollowed_list = []
ustawa_zmiana_list = []

pattern_core = r'((\bart)|(\blp)|(\bw\b)|(\bust)|(\brozdział)|(\bpoz)|(\blit)|(\bdział)|(\bpkt)|(\b§)|(\b[1-9]))'
pattern_additions = fr'(dodaje)\s*(się)\s*{pattern_core}[^:"]*((\b)|(\s))'
pattern_removal = fr'(((skreśla\s+się)|(uchyla\s+się))\s+{pattern_core}[^:,;.]*)|({pattern_core}[^:,;.]*((skreśla\s+się)|(uchyla\s+się))\s+(?![a-z]))'
pattern_change = fr'{pattern_core}[a-z1-9 .,:;]*((\botrzymuje)|(\botrzymują))\s*(\bbrzmienie)'
pattern_date = r'(\bz)\s+(dnia)\s+\d{1,2}\s+[a-zźś]{1,12}\s+\d{4}\s+(r.)'
ustawa_core = r'\bustaw((a\b)|(y\b)|(ie\b)|(ę\b)|(ą\b)|(o\b)|(y\b)|(\b)|(om\b)|(ami\b)|(ach\b))'
pattern_ustawa = fr'{ustawa_core}'
pattern_ustawa_followed = fr'{ustawa_core}(?=\s+z\s+dnia\b)'
pattern_ustawa_notfollowed = fr'{ustawa_core}(?!\s+z\s+dnia\b)'
pattern_ustawa_zmiana = fr'[^o]\s*(?<!zmianie)\s+{ustawa_core}'

for file in listdir("ustawy"):
    with open(f'ustawy/{file}') as f:
        text = f.read().replace('\n',' ').replace(u'\xa0', u' ')
    files.append(file)
    additions_list.append(len(re.findall(pattern_additions, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))
    removal_list.append(len(re.findall(pattern_removal, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))
    changes_list.append(len(re.findall(pattern_change, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))
    date = re.search(pattern_date, text, re.IGNORECASE | re.MULTILINE | re.UNICODE).group(0)
    dates.append(int(re.search(r'\d{4}', date, re.IGNORECASE | re.MULTILINE | re.UNICODE).group(0)))
    ustawa_list.append(len(re.findall(pattern_ustawa, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))
    ustawa_followed_list.append(len(re.findall(pattern_ustawa_followed, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))
    ustawa_notfollowed_list.append(len(re.findall(pattern_ustawa_notfollowed, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))
    ustawa_zmiana_list.append(len(re.findall(pattern_ustawa_zmiana, text, re.IGNORECASE | re.MULTILINE | re.UNICODE)))

data1 = {'year': dates, 'additions': additions_list, 'removes': removal_list, 'changes': changes_list}
data2 = {'year': dates, 'ustawa_list': ustawa_list, 'ustawa_followed_list': ustawa_followed_list, 'ustawa_notfollowed_list': ustawa_notfollowed_list, "ustawa_zmiana_list": ustawa_zmiana_list}

df1 = pd.DataFrame(data=data1)
df1['total'] = df1['additions'] + df1['removes'] + df1['changes']
df1 = df1.groupby(['year']).sum()
df1['additions'] = df1['additions']/df1['total']
df1['removes'] = df1['removes']/df1['total']
df1['changes'] = df1['changes']/df1['total']

N = len(df1.index)
ind = np.arange(N)
width = 0.20

xvals = df1['additions']
bar1 = plt.bar(ind, xvals, width, color='r')

yvals = df1['removes']
bar2 = plt.bar(ind + width, yvals, width, color='g')

zvals = df1['changes']
bar3 = plt.bar(ind + width * 2, zvals, width, color='b')


plt.xlabel("Years")
plt.ylabel('Percentage')
plt.title("Percentage of amendments of a given type changed in the consecutive years")

plt.xticks(ind + width, df1.index)
plt.legend((bar1, bar2, bar3, ), ('additions', 'removes', 'changes'))
plt.grid()
plt.show()

df2 = pd.DataFrame(data=data2)
df2 = df2.groupby(['year']).sum()
df2 = df2.sum()
print(df2)

all = df2['ustawa_list']- df2['ustawa_followed_list']- df2['ustawa_notfollowed_list']
print(f"roznica:{all}")




N = len(df2.index)
ind = np.arange(N)
width = 0.20

xvals = df2['ustawa_list']
bar1 = plt.bar(ind, xvals, width, color='r')

yvals = df2['ustawa_followed_list']
bar2 = plt.bar(ind + width, yvals, width, color='g')

zvals = df2['ustawa_notfollowed_list']
bar3 = plt.bar(ind + width * 2, zvals, width, color='b')

avals = df2['ustawa_zmiana_list']
bar4 = plt.bar(ind + width * 3, avals, width, color='pink')

plt.xlabel("Years")
plt.ylabel('Sum')
plt.title("Numbers")

plt.xticks(ind + width, df2.index)
plt.legend((bar1, bar2, bar3, bar4), ('ustawa', 'z dnia', 'bez z dnia', 'o zmianie'))
plt.show()


