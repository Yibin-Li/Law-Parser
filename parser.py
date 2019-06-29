import pandas as pd
from pyhanlp import *

""" Extract decision and create decision.csv with decision and pid """
# pollution_df = pd.read_csv("pollution_data/pollution_original_parsed.csv")
# print(pollution_df['decision'])
# decision_df = pollution_df[['pid', 'case_number_id', 'title', 'decision']]
# print(decision_df[:6])
# decision_df.to_csv("decision.csv", encoding='utf-8-sig')

""" Extract name information from pid; update decision.csv"""
# decision_df = pd.read_csv("./decision_origin.csv")
# pollution_df = pd.read_csv("pollution_data/pollution.csv")
# name_lst = []
# for index, row in decision_df.iterrows():
#     pid = row['pid']
#     k = pollution_df.loc[(pollution_df['Id'] == pid) & (pollution_df['Role'].isin(["Appellant", "Defendant"]))]
#     name_lst.append(k['Name'].values)
# # name_series = pd.Series(name_lst)
# decision_df['name'] = name_lst
# decision_df = decision_df.reindex(columns=["pid", "case_number_id", "title", "name", "decision"])
# decision_df.to_csv("decision.csv", encoding='utf-8-sig')

""" Fixing missing name in "name" column; update decision.csv"""
# def find_name(s):
#     name = []
#     if "等" in s:
#         for i in range(len(s)):
#             if s[i] == "等":
#                 name.append(s[:i])
#     elif "犯" in s:
#         for i in range(len(s)):
#             if s[i] == "犯" and s[i+1] == "污":
#                 name.append(s[:i])
#     else:
#         for i in range(len(s)):
#             if s[i] == "污" and s[i+1] == "染":
#                 name.append(s[:i])
#     return name
#
# decision_df = pd.read_csv("./decision.csv")
# for index, row in decision_df.iterrows():
#     if len(row["name"]) < 3:
#         name = find_name(row["title"])
#         #print(row["name"])
#         decision_df.at[index,'name'] = name
# decision_df.to_csv("decision.csv", encoding='utf-8-sig')

""" NLP Stuff"""
# title = decision_df['title']
# print(title)
# for i in title:
#     s_hanlp = HanLP.segment(i)
#     print(s_hanlp)
w = "赵某、蔡某犯污染环境罪一审刑事判决书"
k = "陈某甲污染环境罪一审刑事判决书"
v = "陈某甲等污染环境罪一审刑事判决书"
s_hanlp_w = HanLP.segment(w)
s_hanlp_k = HanLP.segment(k)
#print(s_hanlp_w)
#print(type(s_hanlp_k))

# for i in range(3):
#     name.append(s_hanlp_k.get(i).word)

print("done")
# print(find_name(w), " ", find_name(k), " ", find_name(v))
