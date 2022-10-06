## Library to handle any nested iterable (list, tuple, dict, json, etc.) in Pandas - no matter how deeply it is nested!

## Update:

**2022/09/30:** DataFrame is now created directly from iter

**2022/09/30:** No more warning (PerformanceWarning: DataFrame is highly fragmented), when DataFrame is created from a huge nested dict (depth: 1486)  Try it: https://raw.githubusercontent.com/hansalemaos/a_pandas_ex_plode_tool/main/recursion%20_hardcore_test.py

```python
pip install a-pandas-ex-plode-tool
```

```python
from a_pandas_ex_plode_tool import pd_add_explode_tools
pd_add_explode_tools()
import pandas as pd
df = pd.read_csv("https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_long.csv")
```

**HANDLE NESTED ITERABLES**

The code above will add some methods to **pd. / pd.DataFrame / pd.Series**, you can use pandas like you did before, but you will have a couple of methods more:

- pd.Q_AnyNestedIterable_2df()
- pd.Q_CorruptJsonFile_2dict()
- pd.Q_ReadFileWithAllEncodings_2df()
- df.d_filter_dtypes()
- df.d_multiple_columns_to_one()
- df.d_df_to_nested_dict()
- df.d_add_value_to_existing_columns_with_loc()
- df.d_set_values_with_df_loc()
- df.d_drop_rows_with_df_loc()
- df.d_dfloc()
- df.d_stack()
- df.d_unstack()
- df.d_sort_columns_with_sorted()
- df.d_merge_multiple_dfs_and_series_on_one_column()
- df.d_merge_multiple_dfs_and_series_on_index()
- df.d_update_original_iter()
- df.ds_all_nans_to_pdNA()
- df.ds_explode_dicts_in_column()
- df.ds_isna()
- df.ds_normalize_lists()
- df.s_delete_duplicates_from_iters_in_cells()
- df.s_flatten_all_iters_in_cells()
- df.s_as_flattened_list()
- df.s_explode_lists_and_tuples()

**All methods added to pandas have one of these prefixes:**

- **ds_** (for DataFrames and Series)

- **s_** (only for Series)

- **d_** (only for DataFrames)

- **Q_** (added to pd.)

### pd.Q_AnyNestedIterable_2df() / df.d_filter_dtypes() / df.d_update_original_iter()

**pd.Q_AnyNestedIterable_2df()** transforms any nasty iterable into a beautiful Pandas DataFrame with a [MultiIndex](https://pandas.pydata.org/docs/user_guide/advanced.html)

**df.d_filter_dtypes()** avoids TypeError Exceptions 

df.loc[df.aa_value >30,'aa_value'] = 90000000  

Traceback (most recent call last):  
....  
TypeError: '>' not supported between instances of 'str' and 'int' 

***df.loc[df.d_filter_dtypes(allowed_dtypes=(int,float),fillvalue=pd.NA,column='aa_value') > 30] <------- No more exception!***

**df.d_update_original_iter()** After you have updated the DataFrame, you can update the original nasty iterable and keep its ugly structure. 

##### I have tested these methods a lot with examples from Stack Overflow. Until now, everything has been working like a charm. Here are about 15 examples!

```python
Nested iterable from: 'https://stackoverflow.com/questions/61984148/how-to-handle-nested-lists-and-dictionaries-in-pandas-dataframe'
{'critic_reviews': [{'review_critic': 'XYZ', 'review_score': 90},
                    {'review_critic': 'ABC', 'review_score': 90},
                    {'review_critic': '123', 'review_score': 90}],
 'genres': ['Sports', 'Golf'],
 'score': 85,
 'title': 'Golf Simulator',
 'url': 'http://example.com/golf-simulator'}

df = pd.Q_AnyNestedIterable_2df(data,unstack=False)  # create DF stacked or unstacked, it doesn't matter
                                                         aa_all_keys                           aa_value
critic_reviews 0   review_critic  (critic_reviews, 0, review_critic)                                XYZ
                   review_score    (critic_reviews, 0, review_score)                                 90
               1   review_critic  (critic_reviews, 1, review_critic)                                ABC
                   review_score    (critic_reviews, 1, review_score)                                 90
               2   review_critic  (critic_reviews, 2, review_critic)                                123
                   review_score    (critic_reviews, 2, review_score)                                 90
genres         0   NaN                                   (genres, 0)                             Sports
               1   NaN                                   (genres, 1)                               Golf
score          NaN NaN                                      (score,)                                 85
title          NaN NaN                                      (title,)                     Golf Simulator
url            NaN NaN                                        (url,)  http://example.com/golf-simulator

#Avoid exceptions with df.d_filter_dtypes()
df.loc[df.aa_value.str.contains('[Gg]',na=False),'aa_value'] = 'UPDATE1111' #df.loc to update the dataframe (VERY IMPORTANT: To update the original iterable you have to pass 'aa_value')
                                                         aa_all_keys    aa_value
critic_reviews 0   review_critic  (critic_reviews, 0, review_critic)         XYZ
                   review_score    (critic_reviews, 0, review_score)          90
               1   review_critic  (critic_reviews, 1, review_critic)         ABC
                   review_score    (critic_reviews, 1, review_score)          90
               2   review_critic  (critic_reviews, 2, review_critic)         123
                   review_score    (critic_reviews, 2, review_score)          90
genres         0   NaN                                   (genres, 0)      Sports
               1   NaN                                   (genres, 1)  UPDATE1111
score          NaN NaN                                      (score,)          85
title          NaN NaN                                      (title,)  UPDATE1111
url            NaN NaN                                        (url,)  UPDATE1111
mod_iter = df.d_update_original_iter(data, verbose=True)  #updating the nested iterable, the new values have to be in the column 'aa_value', if you have added new columns to the dataframe, drop them before updating the original iterable
[genres][1]                                                  Old value: Golf
[genres][1]                                                  Updated value: UPDATE1111
[title]                                                      Old value: Golf Simulator
[title]                                                      Updated value: UPDATE1111
[url]                                                        Old value: http://example.com/golf-simulator
[url]                                                        Updated value: UPDATE1111

{'critic_reviews': [{'review_critic': 'XYZ', 'review_score': 90},
                    {'review_critic': 'ABC', 'review_score': 90},
                    {'review_critic': '123', 'review_score': 90}],
 'genres': ['Sports', 'UPDATE1111'],
 'score': 85,
 'title': 'UPDATE1111',
 'url': 'UPDATE1111'}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/73430585/how-to-convert-a-list-of-nested-dictionaries-includes-tuples-as-a-dataframe
data=
[{'cb': ({'ID': 1, 'Name': 'A', 'num': 50}, {'ID': 2, 'Name': 'A', 'num': 68}),
  'final_value': 118},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 50}, {'ID': 4, 'Name': 'A', 'num': 67}),
  'final_value': 117},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 50}, {'ID': 6, 'Name': 'A', 'num': 67}),
  'final_value': 117}]
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                             aa_all_keys aa_value
0 cb          0   ID      (0, cb, 0, ID)        1
                  Name  (0, cb, 0, Name)        A
                  num    (0, cb, 0, num)       50
              1   ID      (0, cb, 1, ID)        2
                  Name  (0, cb, 1, Name)        A
                  num    (0, cb, 1, num)       68
  final_value NaN NaN   (0, final_value)      118
1 cb          0   ID      (1, cb, 0, ID)        1
                  Name  (1, cb, 0, Name)        A
                  num    (1, cb, 0, num)       50
              1   ID      (1, cb, 1, ID)        4
                  Name  (1, cb, 1, Name)        A
                  num    (1, cb, 1, num)       67
  final_value NaN NaN   (1, final_value)      117
2 cb          0   ID      (2, cb, 0, ID)        1
                  Name  (2, cb, 0, Name)        A
                  num    (2, cb, 0, num)       50
              1   ID      (2, cb, 1, ID)        6
                  Name  (2, cb, 1, Name)        A
                  num    (2, cb, 1, num)       67
  final_value NaN NaN   (2, final_value)      117
df.loc[df.d_filter_dtypes(allowed_dtypes=(int,float),fillvalue=pd.NA,column='aa_value') > 30, 'aa_value'] = 900000
                             aa_all_keys aa_value
0 cb          0   ID      (0, cb, 0, ID)        1
                  Name  (0, cb, 0, Name)        A
                  num    (0, cb, 0, num)   900000
              1   ID      (0, cb, 1, ID)        2
                  Name  (0, cb, 1, Name)        A
                  num    (0, cb, 1, num)   900000
  final_value NaN NaN   (0, final_value)   900000
1 cb          0   ID      (1, cb, 0, ID)        1
                  Name  (1, cb, 0, Name)        A
                  num    (1, cb, 0, num)   900000
              1   ID      (1, cb, 1, ID)        4
                  Name  (1, cb, 1, Name)        A
                  num    (1, cb, 1, num)   900000
  final_value NaN NaN   (1, final_value)   900000
2 cb          0   ID      (2, cb, 0, ID)        1
                  Name  (2, cb, 0, Name)        A
                  num    (2, cb, 0, num)   900000
              1   ID      (2, cb, 1, ID)        6
                  Name  (2, cb, 1, Name)        A
                  num    (2, cb, 1, num)   900000
  final_value NaN NaN   (2, final_value)   900000
mod_iter = df.d_update_original_iter(data, verbose=True)
[0][cb][0][num]                                              Old value: 50
[0][cb][0][num]                                              Updated value: 900000
[0][cb][1][num]                                              Old value: 68
[0][cb][1][num]                                              Updated value: 900000
[0][final_value]                                             Old value: 118
[0][final_value]                                             Updated value: 900000
[1][cb][0][num]                                              Old value: 50
[1][cb][0][num]                                              Updated value: 900000
[1][cb][1][num]                                              Old value: 67
[1][cb][1][num]                                              Updated value: 900000
[1][final_value]                                             Old value: 117
[1][final_value]                                             Updated value: 900000
[2][cb][0][num]                                              Old value: 50
[2][cb][0][num]                                              Updated value: 900000
[2][cb][1][num]                                              Old value: 67
[2][cb][1][num]                                              Updated value: 900000
[2][final_value]                                             Old value: 117
[2][final_value]                                             Updated value: 900000
[{'cb': ({'ID': 1, 'Name': 'A', 'num': 900000},
         {'ID': 2, 'Name': 'A', 'num': 900000}),
  'final_value': 900000},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 900000},
         {'ID': 4, 'Name': 'A', 'num': 900000}),
  'final_value': 900000},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 900000},
         {'ID': 6, 'Name': 'A', 'num': 900000}),
  'final_value': 900000}]
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/69943509/problems-when-flatten-a-dict
data=
[{'application_contacts': [{'adress': 'X', 'email': 'test@test.com'}],
  'application_details': {'email': None, 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '1'},
 {'application_contacts': [{'adress': 'Z', 'email': None}],
  'application_details': {'email': 'testy@test_a.com', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '2'},
 {'application_contacts': [{'adress': 'Y', 'email': None}],
  'application_details': {'email': 'testy@test_a.com', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '3'}]
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                              aa_all_keys          aa_value
0 application_contacts 0     adress  (0, application_contacts, 0, adress)                 X
                             email    (0, application_contacts, 0, email)     test@test.com
  application_details  email NaN          (0, application_details, email)              None
                       phone NaN          (0, application_details, phone)              None
  employer             Name  NaN                      (0, employer, Name)               Nom
                       email NaN                     (0, employer, email)              None
  id                   NaN   NaN                                  (0, id)                 1
1 application_contacts 0     adress  (1, application_contacts, 0, adress)                 Z
                             email    (1, application_contacts, 0, email)              None
  application_details  email NaN          (1, application_details, email)  testy@test_a.com
                       phone NaN          (1, application_details, phone)              None
  employer             Name  NaN                      (1, employer, Name)               Nom
                       email NaN                     (1, employer, email)              None
  id                   NaN   NaN                                  (1, id)                 2
2 application_contacts 0     adress  (2, application_contacts, 0, adress)                 Y
                             email    (2, application_contacts, 0, email)              None
  application_details  email NaN          (2, application_details, email)  testy@test_a.com
                       phone NaN          (2, application_details, phone)              None
  employer             Name  NaN                      (2, employer, Name)               Nom
                       email NaN                     (2, employer, email)              None
  id                   NaN   NaN                                  (2, id)                 3
df.loc[df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'test_a\.\w+\b',na=False), 'aa_value'] = 'UPPPPPPPPPPPPPPPDATE.COM'
                                                              aa_all_keys                  aa_value
0 application_contacts 0     adress  (0, application_contacts, 0, adress)                         X
                             email    (0, application_contacts, 0, email)             test@test.com
  application_details  email NaN          (0, application_details, email)                      None
                       phone NaN          (0, application_details, phone)                      None
  employer             Name  NaN                      (0, employer, Name)                       Nom
                       email NaN                     (0, employer, email)                      None
  id                   NaN   NaN                                  (0, id)                         1
1 application_contacts 0     adress  (1, application_contacts, 0, adress)                         Z
                             email    (1, application_contacts, 0, email)                      None
  application_details  email NaN          (1, application_details, email)  UPPPPPPPPPPPPPPPDATE.COM
                       phone NaN          (1, application_details, phone)                      None
  employer             Name  NaN                      (1, employer, Name)                       Nom
                       email NaN                     (1, employer, email)                      None
  id                   NaN   NaN                                  (1, id)                         2
2 application_contacts 0     adress  (2, application_contacts, 0, adress)                         Y
                             email    (2, application_contacts, 0, email)                      None
  application_details  email NaN          (2, application_details, email)  UPPPPPPPPPPPPPPPDATE.COM
                       phone NaN          (2, application_details, phone)                      None
  employer             Name  NaN                      (2, employer, Name)                       Nom
                       email NaN                     (2, employer, email)                      None
  id                   NaN   NaN                                  (2, id)                         3
mod_iter = df.d_update_original_iter(data, verbose=True)
[1][application_details][email]                              Old value: testy@test_a.com
[1][application_details][email]                              Updated value: UPPPPPPPPPPPPPPPDATE.COM
[2][application_details][email]                              Old value: testy@test_a.com
[2][application_details][email]                              Updated value: UPPPPPPPPPPPPPPPDATE.COM
[{'application_contacts': [{'adress': 'X', 'email': 'test@test.com'}],
  'application_details': {'email': None, 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '1'},
 {'application_contacts': [{'adress': 'Z', 'email': None}],
  'application_details': {'email': 'UPPPPPPPPPPPPPPPDATE.COM', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '2'},
 {'application_contacts': [{'adress': 'Y', 'email': None}],
  'application_details': {'email': 'UPPPPPPPPPPPPPPPDATE.COM', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '3'}]
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/62765371/convert-nested-dataframe-to-a-simple-dataframeframe
data=
{'A': [1, 2, 3],
 'B': [4, 5, 6],
 'departure': [{'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'}]}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                   aa_all_keys                   aa_value
A         0 NaN                                         (A, 0)                          1
          1 NaN                                         (A, 1)                          2
          2 NaN                                         (A, 2)                          3
B         0 NaN                                         (B, 0)                          4
          1 NaN                                         (B, 1)                          5
          2 NaN                                         (B, 2)                          6
departure 0 actual                      (departure, 0, actual)                       None
            actual_runway        (departure, 0, actual_runway)                       None
            airport                    (departure, 0, airport)                     Findel
            delay                        (departure, 0, delay)                       None
            estimated                (departure, 0, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 0, estimated_runway)                       None
            gate                          (departure, 0, gate)                       None
            iata                          (departure, 0, iata)                        LUX
            icao                          (departure, 0, icao)                       ELLX
            scheduled                (departure, 0, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 0, terminal)                       None
            timezone                  (departure, 0, timezone)          Europe/Luxembourg
          1 actual                      (departure, 1, actual)                       None
            actual_runway        (departure, 1, actual_runway)                       None
            airport                    (departure, 1, airport)                     Findel
            delay                        (departure, 1, delay)                       None
            estimated                (departure, 1, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 1, estimated_runway)                       None
            gate                          (departure, 1, gate)                       None
            iata                          (departure, 1, iata)                        LUX
            icao                          (departure, 1, icao)                       ELLX
            scheduled                (departure, 1, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 1, terminal)                       None
            timezone                  (departure, 1, timezone)          Europe/Luxembourg
          2 actual                      (departure, 2, actual)                       None
            actual_runway        (departure, 2, actual_runway)                       None
            airport                    (departure, 2, airport)                     Findel
            delay                        (departure, 2, delay)                       None
            estimated                (departure, 2, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 2, estimated_runway)                       None
            gate                          (departure, 2, gate)                       None
            iata                          (departure, 2, iata)                        LUX
            icao                          (departure, 2, icao)                       ELLX
            scheduled                (departure, 2, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 2, terminal)                       None
            timezone                  (departure, 2, timezone)          Europe/Luxembourg
df.loc[df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value')== 'ELLX', 'aa_value'] = 'ELLX-UPDATED'
                                                   aa_all_keys                   aa_value
A         0 NaN                                         (A, 0)                          1
          1 NaN                                         (A, 1)                          2
          2 NaN                                         (A, 2)                          3
B         0 NaN                                         (B, 0)                          4
          1 NaN                                         (B, 1)                          5
          2 NaN                                         (B, 2)                          6
departure 0 actual                      (departure, 0, actual)                       None
            actual_runway        (departure, 0, actual_runway)                       None
            airport                    (departure, 0, airport)                     Findel
            delay                        (departure, 0, delay)                       None
            estimated                (departure, 0, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 0, estimated_runway)                       None
            gate                          (departure, 0, gate)                       None
            iata                          (departure, 0, iata)                        LUX
            icao                          (departure, 0, icao)               ELLX-UPDATED
            scheduled                (departure, 0, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 0, terminal)                       None
            timezone                  (departure, 0, timezone)          Europe/Luxembourg
          1 actual                      (departure, 1, actual)                       None
            actual_runway        (departure, 1, actual_runway)                       None
            airport                    (departure, 1, airport)                     Findel
            delay                        (departure, 1, delay)                       None
            estimated                (departure, 1, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 1, estimated_runway)                       None
            gate                          (departure, 1, gate)                       None
            iata                          (departure, 1, iata)                        LUX
            icao                          (departure, 1, icao)               ELLX-UPDATED
            scheduled                (departure, 1, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 1, terminal)                       None
            timezone                  (departure, 1, timezone)          Europe/Luxembourg
          2 actual                      (departure, 2, actual)                       None
            actual_runway        (departure, 2, actual_runway)                       None
            airport                    (departure, 2, airport)                     Findel
            delay                        (departure, 2, delay)                       None
            estimated                (departure, 2, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 2, estimated_runway)                       None
            gate                          (departure, 2, gate)                       None
            iata                          (departure, 2, iata)                        LUX
            icao                          (departure, 2, icao)               ELLX-UPDATED
            scheduled                (departure, 2, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 2, terminal)                       None
            timezone                  (departure, 2, timezone)          Europe/Luxembourg
mod_iter = df.d_update_original_iter(data, verbose=True)
[departure][0][icao]                                         Old value: ELLX
[departure][0][icao]                                         Updated value: ELLX-UPDATED
[departure][1][icao]                                         Old value: ELLX
[departure][1][icao]                                         Updated value: ELLX-UPDATED
[departure][2][icao]                                         Old value: ELLX
[departure][2][icao]                                         Updated value: ELLX-UPDATED
{'A': [1, 2, 3],
 'B': [4, 5, 6],
 'departure': [{'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX-UPDATED',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX-UPDATED',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX-UPDATED',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'}]}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/64359762/constructing-a-pandas-dataframe-with-columns-and-sub-columns-from-nested-diction
data=
{'level1': {'t1': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 8},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 9},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 8},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 9},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5, 'col2': 6, 'col3': 7, 'col4': 8},
                   's3': {'col1': 9, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}},
 'level2': {'t1': {'s1': {'col1': 5, 'col2': 4, 'col3': 9, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 5},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 13},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 20}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 8},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 9},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5, 'col2': 6, 'col3': 7, 'col4': 8},
                   's3': {'col1': 9, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}}}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                              aa_all_keys  aa_value
level1 t1 s1 col1  (level1, t1, s1, col1)         5
             col2  (level1, t1, s1, col2)         4
             col3  (level1, t1, s1, col3)         4
             col4  (level1, t1, s1, col4)         9
          s2 col1  (level1, t1, s2, col1)         1
                                   ...       ...
level2 t3 s3 col4  (level2, t3, s3, col4)        12
          s4 col1  (level2, t3, s4, col1)        13
             col2  (level2, t3, s4, col2)        14
             col3  (level2, t3, s4, col3)        15
             col4  (level2, t3, s4, col4)        16
[96 rows x 2 columns]
df.loc[(df.d_filter_dtypes(allowed_dtypes=(int),fillvalue=pd.NA,column='aa_value') > 5) & (df.d_filter_dtypes(allowed_dtypes=(int),fillvalue=pd.NA,column='aa_value') < 10), 'aa_value'] = 1000000
                              aa_all_keys  aa_value
level1 t1 s1 col1  (level1, t1, s1, col1)         5
             col2  (level1, t1, s1, col2)         4
             col3  (level1, t1, s1, col3)         4
             col4  (level1, t1, s1, col4)   1000000
          s2 col1  (level1, t1, s2, col1)         1
                                   ...       ...
level2 t3 s3 col4  (level2, t3, s3, col4)        12
          s4 col1  (level2, t3, s4, col1)        13
             col2  (level2, t3, s4, col2)        14
             col3  (level2, t3, s4, col3)        15
             col4  (level2, t3, s4, col4)        16
[96 rows x 2 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[level1][t1][s1][col4]                                       Old value: 9
[level1][t1][s1][col4]                                       Updated value: 1000000
[level1][t1][s2][col4]                                       Old value: 8
[level1][t1][s2][col4]                                       Updated value: 1000000
[level1][t1][s3][col2]                                       Old value: 8
[level1][t1][s3][col2]                                       Updated value: 1000000
[level1][t1][s3][col4]                                       Old value: 9
[level1][t1][s3][col4]                                       Updated value: 1000000
[level1][t1][s4][col4]                                       Old value: 9
[level1][t1][s4][col4]                                       Updated value: 1000000
[level1][t2][s1][col4]                                       Old value: 9
[level1][t2][s1][col4]                                       Updated value: 1000000
[level1][t2][s2][col4]                                       Old value: 8
[level1][t2][s2][col4]                                       Updated value: 1000000
[level1][t2][s3][col2]                                       Old value: 8
[level1][t2][s3][col2]                                       Updated value: 1000000
[level1][t2][s3][col4]                                       Old value: 9
[level1][t2][s3][col4]                                       Updated value: 1000000
[level1][t2][s4][col4]                                       Old value: 9
[level1][t2][s4][col4]                                       Updated value: 1000000
[level1][t3][s2][col2]                                       Old value: 6
[level1][t3][s2][col2]                                       Updated value: 1000000
[level1][t3][s2][col3]                                       Old value: 7
[level1][t3][s2][col3]                                       Updated value: 1000000
[level1][t3][s2][col4]                                       Old value: 8
[level1][t3][s2][col4]                                       Updated value: 1000000
[level1][t3][s3][col1]                                       Old value: 9
[level1][t3][s3][col1]                                       Updated value: 1000000
[level2][t1][s1][col3]                                       Old value: 9
[level2][t1][s1][col3]                                       Updated value: 1000000
[level2][t1][s1][col4]                                       Old value: 9
[level2][t1][s1][col4]                                       Updated value: 1000000
[level2][t1][s3][col2]                                       Old value: 8
[level2][t1][s3][col2]                                       Updated value: 1000000
[level2][t2][s1][col4]                                       Old value: 9
[level2][t2][s1][col4]                                       Updated value: 1000000
[level2][t2][s2][col4]                                       Old value: 8
[level2][t2][s2][col4]                                       Updated value: 1000000
[level2][t2][s3][col2]                                       Old value: 8
[level2][t2][s3][col2]                                       Updated value: 1000000
[level2][t2][s3][col4]                                       Old value: 9
[level2][t2][s3][col4]                                       Updated value: 1000000
[level2][t2][s4][col4]                                       Old value: 9
[level2][t2][s4][col4]                                       Updated value: 1000000
[level2][t3][s2][col2]                                       Old value: 6
[level2][t3][s2][col2]                                       Updated value: 1000000
[level2][t3][s2][col3]                                       Old value: 7
[level2][t3][s2][col3]                                       Updated value: 1000000
[level2][t3][s2][col4]                                       Old value: 8
[level2][t3][s2][col4]                                       Updated value: 1000000
[level2][t3][s3][col1]                                       Old value: 9
[level2][t3][s3][col1]                                       Updated value: 1000000
{'level1': {'t1': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 1000000},
                   's3': {'col1': 11,
                          'col2': 1000000,
                          'col3': 2,
                          'col4': 1000000},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 1000000},
                   's3': {'col1': 11,
                          'col2': 1000000,
                          'col3': 2,
                          'col4': 1000000},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5,
                          'col2': 1000000,
                          'col3': 1000000,
                          'col4': 1000000},
                   's3': {'col1': 1000000, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}},
 'level2': {'t1': {'s1': {'col1': 5,
                          'col2': 4,
                          'col3': 1000000,
                          'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 5},
                   's3': {'col1': 11, 'col2': 1000000, 'col3': 2, 'col4': 13},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 20}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 1000000},
                   's3': {'col1': 11,
                          'col2': 1000000,
                          'col3': 2,
                          'col4': 1000000},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5,
                          'col2': 1000000,
                          'col3': 1000000,
                          'col4': 1000000},
                   's3': {'col1': 1000000, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}}}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/72146094/problems-matching-values-from-nested-dictionary
data=
{'_links': {'next': None, 'prev': None},
 'limit': 250,
 'offset': 0,
 'runs': [{'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': None,
           'config': None,
           'config_ids': [],
           'created_by': 1,
           'created_on': 1651790693,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 1,
           'id': 13,
           'include_all': False,
           'is_completed': False,
           'milestone_id': None,
           'name': '2022-05-05-testrun',
           'passed_count': 2,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 0,
           'updated_on': 1651790693,
           'url': 'https://xxxxxxxxxx.testrail.io/index.php?/runs/view/13'},
          {'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': 1650989972,
           'config': None,
           'config_ids': [],
           'created_by': 5,
           'created_on': 1650966329,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 0,
           'id': 9,
           'include_all': False,
           'is_completed': True,
           'milestone_id': None,
           'name': 'This is a new test run',
           'passed_count': 0,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 3,
           'updated_on': 1650966329,
           'url': 'https://xxxxxxxxxx.testrail.io/index.php?/runs/view/9'}],
 'size': 2}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                          aa_all_keys                                           aa_value
_links next NaN                        (_links, next)                                               None
       prev NaN                        (_links, prev)                                               None
limit  NaN  NaN                              (limit,)                                                250
offset NaN  NaN                             (offset,)                                                  0
runs   0    assignedto_id    (runs, 0, assignedto_id)                                               None
                                               ...                                                ...
       1    suite_id              (runs, 1, suite_id)                                                  1
            untested_count  (runs, 1, untested_count)                                                  3
            updated_on          (runs, 1, updated_on)                                         1650966329
            url                        (runs, 1, url)  https://xxxxxxxxxx.testrail.io/index.php?/runs...
size   NaN  NaN                               (size,)                                                  2
[63 rows x 2 columns]
df.loc[(df.d_filter_dtypes(allowed_dtypes=(bool),fillvalue=pd.NA,column='aa_value') == False ), 'aa_value'] = True
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'https?://.*',na=False) ), 'aa_value'] = 'WWW.PYTHON.ORG'
                                          aa_all_keys        aa_value
_links next NaN                        (_links, next)            None
       prev NaN                        (_links, prev)            None
limit  NaN  NaN                              (limit,)             250
offset NaN  NaN                             (offset,)               0
runs   0    assignedto_id    (runs, 0, assignedto_id)            None
                                               ...             ...
       1    suite_id              (runs, 1, suite_id)               1
            untested_count  (runs, 1, untested_count)               3
            updated_on          (runs, 1, updated_on)      1650966329
            url                        (runs, 1, url)  WWW.PYTHON.ORG
size   NaN  NaN                               (size,)               2
[63 rows x 2 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[runs][0][include_all]                                       Old value: False
[runs][0][include_all]                                       Updated value: True
[runs][0][is_completed]                                      Old value: False
[runs][0][is_completed]                                      Updated value: True
[runs][0][url]                                               Old value: https://xxxxxxxxxx.testrail.io/index.php?/runs/view/13
[runs][0][url]                                               Updated value: WWW.PYTHON.ORG
[runs][1][include_all]                                       Old value: False
[runs][1][include_all]                                       Updated value: True
[runs][1][url]                                               Old value: https://xxxxxxxxxx.testrail.io/index.php?/runs/view/9
[runs][1][url]                                               Updated value: WWW.PYTHON.ORG
{'_links': {'next': None, 'prev': None},
 'limit': 250,
 'offset': 0,
 'runs': [{'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': None,
           'config': None,
           'config_ids': [],
           'created_by': 1,
           'created_on': 1651790693,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 1,
           'id': 13,
           'include_all': True,
           'is_completed': True,
           'milestone_id': None,
           'name': '2022-05-05-testrun',
           'passed_count': 2,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 0,
           'updated_on': 1651790693,
           'url': 'WWW.PYTHON.ORG'},
          {'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': 1650989972,
           'config': None,
           'config_ids': [],
           'created_by': 5,
           'created_on': 1650966329,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 0,
           'id': 9,
           'include_all': True,
           'is_completed': True,
           'milestone_id': None,
           'name': 'This is a new test run',
           'passed_count': 0,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 3,
           'updated_on': 1650966329,
           'url': 'WWW.PYTHON.ORG'}],
 'size': 2}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/73708706/how-to-get-values-from-list-of-nested-dictionaries/73839430#73839430
data=
{'results': [{'end_time': '2021-01-21',
              'key': 'q1',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['1']},
             {'end_time': '2021-01-21',
              'key': 'q2',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['False']},
             {'end_time': '2021-01-21',
              'key': 'q3',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['3']},
             {'end_time': '2021-01-21',
              'key': 'q4',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['3']}]}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                         aa_all_keys        aa_value
results 0 end_time    NaN     (results, 0, end_time)      2021-01-21
          key         NaN          (results, 0, key)              q1
          result_type NaN  (results, 0, result_type)  multipleChoice
          start_time  NaN   (results, 0, start_time)      2021-01-21
          value       0       (results, 0, value, 0)               1
        1 end_time    NaN     (results, 1, end_time)      2021-01-21
          key         NaN          (results, 1, key)              q2
          result_type NaN  (results, 1, result_type)  multipleChoice
          start_time  NaN   (results, 1, start_time)      2021-01-21
          value       0       (results, 1, value, 0)           False
        2 end_time    NaN     (results, 2, end_time)      2021-01-21
          key         NaN          (results, 2, key)              q3
          result_type NaN  (results, 2, result_type)  multipleChoice
          start_time  NaN   (results, 2, start_time)      2021-01-21
          value       0       (results, 2, value, 0)               3
        3 end_time    NaN     (results, 3, end_time)      2021-01-21
          key         NaN          (results, 3, key)              q4
          result_type NaN  (results, 3, result_type)  multipleChoice
          start_time  NaN   (results, 3, start_time)      2021-01-21
          value       0       (results, 3, value, 0)               3
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'^2021.*',na=False) ), 'aa_value'] = 10000000000 
                                         aa_all_keys        aa_value
results 0 end_time    NaN     (results, 0, end_time)     10000000000
          key         NaN          (results, 0, key)              q1
          result_type NaN  (results, 0, result_type)  multipleChoice
          start_time  NaN   (results, 0, start_time)     10000000000
          value       0       (results, 0, value, 0)               1
        1 end_time    NaN     (results, 1, end_time)     10000000000
          key         NaN          (results, 1, key)              q2
          result_type NaN  (results, 1, result_type)  multipleChoice
          start_time  NaN   (results, 1, start_time)     10000000000
          value       0       (results, 1, value, 0)           False
        2 end_time    NaN     (results, 2, end_time)     10000000000
          key         NaN          (results, 2, key)              q3
          result_type NaN  (results, 2, result_type)  multipleChoice
          start_time  NaN   (results, 2, start_time)     10000000000
          value       0       (results, 2, value, 0)               3
        3 end_time    NaN     (results, 3, end_time)     10000000000
          key         NaN          (results, 3, key)              q4
          result_type NaN  (results, 3, result_type)  multipleChoice
          start_time  NaN   (results, 3, start_time)     10000000000
          value       0       (results, 3, value, 0)               3
mod_iter = df.d_update_original_iter(data, verbose=True)
[results][0][end_time]                                       Old value: 2021-01-21
[results][0][end_time]                                       Updated value: 10000000000
[results][0][start_time]                                     Old value: 2021-01-21
[results][0][start_time]                                     Updated value: 10000000000
[results][1][end_time]                                       Old value: 2021-01-21
[results][1][end_time]                                       Updated value: 10000000000
[results][1][start_time]                                     Old value: 2021-01-21
[results][1][start_time]                                     Updated value: 10000000000
[results][2][end_time]                                       Old value: 2021-01-21
[results][2][end_time]                                       Updated value: 10000000000
[results][2][start_time]                                     Old value: 2021-01-21
[results][2][start_time]                                     Updated value: 10000000000
[results][3][end_time]                                       Old value: 2021-01-21
[results][3][end_time]                                       Updated value: 10000000000
[results][3][start_time]                                     Old value: 2021-01-21
[results][3][start_time]                                     Updated value: 10000000000
{'results': [{'end_time': 10000000000,
              'key': 'q1',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['1']},
             {'end_time': 10000000000,
              'key': 'q2',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['False']},
             {'end_time': 10000000000,
              'key': 'q3',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['3']},
             {'end_time': 10000000000,
              'key': 'q4',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['3']}]}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/66461902/flattening-nested-dictionary-into-dataframe-python
data=
{1: {2: {'IDs': {'BookID': ['543533254353', '4324232342'],
                 'SalesID': ['543267765345', '4353543'],
                 'StoreID': ['111111', '1121111']},
         'Name': 'boring Tales of Dragon Slayers'},
     'IDs': {'BookID': ['543533254353'],
             'SalesID': ['543267765345'],
             'StoreID': ['123445452543']},
     'Name': 'Thrilling Tales of Dragon Slayers'}}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                        aa_all_keys                           aa_value
1 IDs  BookID  0       NaN      (1, IDs, BookID, 0)                       543533254353
       SalesID 0       NaN     (1, IDs, SalesID, 0)                       543267765345
       StoreID 0       NaN     (1, IDs, StoreID, 0)                       123445452543
  Name NaN     NaN     NaN                (1, Name)  Thrilling Tales of Dragon Slayers
  2    IDs     BookID  0     (1, 2, IDs, BookID, 0)                       543533254353
                       1     (1, 2, IDs, BookID, 1)                         4324232342
               SalesID 0    (1, 2, IDs, SalesID, 0)                       543267765345
                       1    (1, 2, IDs, SalesID, 1)                            4353543
               StoreID 0    (1, 2, IDs, StoreID, 0)                             111111
                       1    (1, 2, IDs, StoreID, 1)                            1121111
       Name    NaN     NaN             (1, 2, Name)     boring Tales of Dragon Slayers
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'^\d+$',na=False) ), 'aa_value'] = df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'^\d+$',na=False) ), 'aa_value'].astype(float)
                                        aa_all_keys                           aa_value
1 IDs  BookID  0       NaN      (1, IDs, BookID, 0)                     543533254353.0
       SalesID 0       NaN     (1, IDs, SalesID, 0)                     543267765345.0
       StoreID 0       NaN     (1, IDs, StoreID, 0)                     123445452543.0
  Name NaN     NaN     NaN                (1, Name)  Thrilling Tales of Dragon Slayers
  2    IDs     BookID  0     (1, 2, IDs, BookID, 0)                     543533254353.0
                       1     (1, 2, IDs, BookID, 1)                       4324232342.0
               SalesID 0    (1, 2, IDs, SalesID, 0)                     543267765345.0
                       1    (1, 2, IDs, SalesID, 1)                          4353543.0
               StoreID 0    (1, 2, IDs, StoreID, 0)                           111111.0
                       1    (1, 2, IDs, StoreID, 1)                          1121111.0
       Name    NaN     NaN             (1, 2, Name)     boring Tales of Dragon Slayers
mod_iter = df.d_update_original_iter(data, verbose=True)
[1][2][IDs][BookID][0]                                       Old value: 543533254353
[1][2][IDs][BookID][0]                                       Updated value: 543533254353.0
[1][2][IDs][BookID][1]                                       Old value: 4324232342
[1][2][IDs][BookID][1]                                       Updated value: 4324232342.0
[1][2][IDs][SalesID][0]                                      Old value: 543267765345
[1][2][IDs][SalesID][0]                                      Updated value: 543267765345.0
[1][2][IDs][SalesID][1]                                      Old value: 4353543
[1][2][IDs][SalesID][1]                                      Updated value: 4353543.0
[1][2][IDs][StoreID][0]                                      Old value: 111111
[1][2][IDs][StoreID][0]                                      Updated value: 111111.0
[1][2][IDs][StoreID][1]                                      Old value: 1121111
[1][2][IDs][StoreID][1]                                      Updated value: 1121111.0
[1][IDs][BookID][0]                                          Old value: 543533254353
[1][IDs][BookID][0]                                          Updated value: 543533254353.0
[1][IDs][SalesID][0]                                         Old value: 543267765345
[1][IDs][SalesID][0]                                         Updated value: 543267765345.0
[1][IDs][StoreID][0]                                         Old value: 123445452543
[1][IDs][StoreID][0]                                         Updated value: 123445452543.0
{1: {2: {'IDs': {'BookID': [543533254353.0, 4324232342.0],
                 'SalesID': [543267765345.0, 4353543.0],
                 'StoreID': [111111.0, 1121111.0]},
         'Name': 'boring Tales of Dragon Slayers'},
     'IDs': {'BookID': [543533254353.0],
             'SalesID': [543267765345.0],
             'StoreID': [123445452543.0]},
     'Name': 'Thrilling Tales of Dragon Slayers'}}
Nested iterable from: 'https://stackoverflow.com/questions/61984148/how-to-handle-nested-lists-and-dictionaries-in-pandas-dataframe'
{'critic_reviews': [{'review_critic': 'XYZ', 'review_score': 90},
                    {'review_critic': 'ABC', 'review_score': 90},
                    {'review_critic': '123', 'review_score': 90}],
 'genres': ['Sports', 'Golf'],
 'score': 85,
 'title': 'Golf Simulator',
 'url': 'http://example.com/golf-simulator'}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)  # create DF stacked or unstacked, it doesn't matter
                                                         aa_all_keys                           aa_value
critic_reviews 0   review_critic  (critic_reviews, 0, review_critic)                                XYZ
                   review_score    (critic_reviews, 0, review_score)                                 90
               1   review_critic  (critic_reviews, 1, review_critic)                                ABC
                   review_score    (critic_reviews, 1, review_score)                                 90
               2   review_critic  (critic_reviews, 2, review_critic)                                123
                   review_score    (critic_reviews, 2, review_score)                                 90
genres         0   NaN                                   (genres, 0)                             Sports
               1   NaN                                   (genres, 1)                               Golf
score          NaN NaN                                      (score,)                                 85
title          NaN NaN                                      (title,)                     Golf Simulator
url            NaN NaN                                        (url,)  http://example.com/golf-simulator
df.loc[df.aa_value.str.contains('[Gg]',na=False),'aa_value'] = 'UPDATE1111' #df.loc to update the dataframe (VERY IMPORTANT: To update the original iterable you have to pass 'aa_value')
                                                         aa_all_keys    aa_value
critic_reviews 0   review_critic  (critic_reviews, 0, review_critic)         XYZ
                   review_score    (critic_reviews, 0, review_score)          90
               1   review_critic  (critic_reviews, 1, review_critic)         ABC
                   review_score    (critic_reviews, 1, review_score)          90
               2   review_critic  (critic_reviews, 2, review_critic)         123
                   review_score    (critic_reviews, 2, review_score)          90
genres         0   NaN                                   (genres, 0)      Sports
               1   NaN                                   (genres, 1)  UPDATE1111
score          NaN NaN                                      (score,)          85
title          NaN NaN                                      (title,)  UPDATE1111
url            NaN NaN                                        (url,)  UPDATE1111
mod_iter = df.d_update_original_iter(data, verbose=True)  #updating the nested iterable, the new values have to be in the column 'aa_value', if you have added new columns to the dataframe, drop them before updating the original iterable
[genres][1]                                                  Old value: Golf
[genres][1]                                                  Updated value: UPDATE1111
[title]                                                      Old value: Golf Simulator
[title]                                                      Updated value: UPDATE1111
[url]                                                        Old value: http://example.com/golf-simulator
[url]                                                        Updated value: UPDATE1111
{'critic_reviews': [{'review_critic': 'XYZ', 'review_score': 90},
                    {'review_critic': 'ABC', 'review_score': 90},
                    {'review_critic': '123', 'review_score': 90}],
 'genres': ['Sports', 'UPDATE1111'],
 'score': 85,
 'title': 'UPDATE1111',
 'url': 'UPDATE1111'}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/72990265/convert-nested-list-in-dictionary-to-dataframe/72990346
data=
{'a': 'test',
 'b': 1657,
 'c': 'asset',
 'd': [['2089', '0.0'], ['2088', '0.0']],
 'e': [['2088', '0.0'], ['2088', '0.0'], ['2088', '0.00']],
 'f': [['2088', '0.0', 'x', 'foo'],
       ['2088', '0.0', 'bar', 'i'],
       ['2088', '0.00', 'z', '0.2']],
 'x': ['test1', 'test2']}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
          aa_all_keys aa_value
a NaN NaN        (a,)     test
b NaN NaN        (b,)     1657
c NaN NaN        (c,)    asset
d 0   0     (d, 0, 0)     2089
      1     (d, 0, 1)      0.0
  1   0     (d, 1, 0)     2088
      1     (d, 1, 1)      0.0
e 0   0     (e, 0, 0)     2088
      1     (e, 0, 1)      0.0
  1   0     (e, 1, 0)     2088
      1     (e, 1, 1)      0.0
  2   0     (e, 2, 0)     2088
      1     (e, 2, 1)     0.00
f 0   0     (f, 0, 0)     2088
      1     (f, 0, 1)      0.0
      2     (f, 0, 2)        x
      3     (f, 0, 3)      foo
  1   0     (f, 1, 0)     2088
      1     (f, 1, 1)      0.0
      2     (f, 1, 2)      bar
      3     (f, 1, 3)        i
  2   0     (f, 2, 0)     2088
      1     (f, 2, 1)     0.00
      2     (f, 2, 2)        z
      3     (f, 2, 3)      0.2
x 0   NaN      (x, 0)    test1
  1   NaN      (x, 1)    test2
df.loc[df.aa_value == 1657,'aa_value'] = 1657*30
          aa_all_keys aa_value
a NaN NaN        (a,)     test
b NaN NaN        (b,)    49710
c NaN NaN        (c,)    asset
d 0   0     (d, 0, 0)     2089
      1     (d, 0, 1)      0.0
  1   0     (d, 1, 0)     2088
      1     (d, 1, 1)      0.0
e 0   0     (e, 0, 0)     2088
      1     (e, 0, 1)      0.0
  1   0     (e, 1, 0)     2088
      1     (e, 1, 1)      0.0
  2   0     (e, 2, 0)     2088
      1     (e, 2, 1)     0.00
f 0   0     (f, 0, 0)     2088
      1     (f, 0, 1)      0.0
      2     (f, 0, 2)        x
      3     (f, 0, 3)      foo
  1   0     (f, 1, 0)     2088
      1     (f, 1, 1)      0.0
      2     (f, 1, 2)      bar
      3     (f, 1, 3)        i
  2   0     (f, 2, 0)     2088
      1     (f, 2, 1)     0.00
      2     (f, 2, 2)        z
      3     (f, 2, 3)      0.2
x 0   NaN      (x, 0)    test1
  1   NaN      (x, 1)    test2
mod_iter = df.d_update_original_iter(data, verbose=True)
[b]                                                          Old value: 1657
[b]                                                          Updated value: 49710
{'a': 'test',
 'b': 49710,
 'c': 'asset',
 'd': [['2089', '0.0'], ['2088', '0.0']],
 'e': [['2088', '0.0'], ['2088', '0.0'], ['2088', '0.00']],
 'f': [['2088', '0.0', 'x', 'foo'],
       ['2088', '0.0', 'bar', 'i'],
       ['2088', '0.00', 'z', '0.2']],
 'x': ['test1', 'test2']}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/73430585/how-to-convert-a-list-of-nested-dictionaries-includes-tuples-as-a-dataframe
data=
[{'cb': ({'ID': 1, 'Name': 'A', 'num': 50}, {'ID': 2, 'Name': 'A', 'num': 68}),
  'final_value': 118},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 50}, {'ID': 4, 'Name': 'A', 'num': 67}),
  'final_value': 117},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 50}, {'ID': 6, 'Name': 'A', 'num': 67}),
  'final_value': 117}]
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                             aa_all_keys aa_value
0 cb          0   ID      (0, cb, 0, ID)        1
                  Name  (0, cb, 0, Name)        A
                  num    (0, cb, 0, num)       50
              1   ID      (0, cb, 1, ID)        2
                  Name  (0, cb, 1, Name)        A
                  num    (0, cb, 1, num)       68
  final_value NaN NaN   (0, final_value)      118
1 cb          0   ID      (1, cb, 0, ID)        1
                  Name  (1, cb, 0, Name)        A
                  num    (1, cb, 0, num)       50
              1   ID      (1, cb, 1, ID)        4
                  Name  (1, cb, 1, Name)        A
                  num    (1, cb, 1, num)       67
  final_value NaN NaN   (1, final_value)      117
2 cb          0   ID      (2, cb, 0, ID)        1
                  Name  (2, cb, 0, Name)        A
                  num    (2, cb, 0, num)       50
              1   ID      (2, cb, 1, ID)        6
                  Name  (2, cb, 1, Name)        A
                  num    (2, cb, 1, num)       67
  final_value NaN NaN   (2, final_value)      117
df.d_filter_dtypes(allowed_dtypes=(int,float),fillvalue=pd.NA,column='aa_value') > 30, 'aa_value'] = 900000
                             aa_all_keys aa_value
0 cb          0   ID      (0, cb, 0, ID)        1
                  Name  (0, cb, 0, Name)        A
                  num    (0, cb, 0, num)   900000
              1   ID      (0, cb, 1, ID)        2
                  Name  (0, cb, 1, Name)        A
                  num    (0, cb, 1, num)   900000
  final_value NaN NaN   (0, final_value)   900000
1 cb          0   ID      (1, cb, 0, ID)        1
                  Name  (1, cb, 0, Name)        A
                  num    (1, cb, 0, num)   900000
              1   ID      (1, cb, 1, ID)        4
                  Name  (1, cb, 1, Name)        A
                  num    (1, cb, 1, num)   900000
  final_value NaN NaN   (1, final_value)   900000
2 cb          0   ID      (2, cb, 0, ID)        1
                  Name  (2, cb, 0, Name)        A
                  num    (2, cb, 0, num)   900000
              1   ID      (2, cb, 1, ID)        6
                  Name  (2, cb, 1, Name)        A
                  num    (2, cb, 1, num)   900000
  final_value NaN NaN   (2, final_value)   900000
mod_iter = df.d_update_original_iter(data, verbose=True)
[0][cb][0][num]                                              Old value: 50
[0][cb][0][num]                                              Updated value: 900000
[0][cb][1][num]                                              Old value: 68
[0][cb][1][num]                                              Updated value: 900000
[0][final_value]                                             Old value: 118
[0][final_value]                                             Updated value: 900000
[1][cb][0][num]                                              Old value: 50
[1][cb][0][num]                                              Updated value: 900000
[1][cb][1][num]                                              Old value: 67
[1][cb][1][num]                                              Updated value: 900000
[1][final_value]                                             Old value: 117
[1][final_value]                                             Updated value: 900000
[2][cb][0][num]                                              Old value: 50
[2][cb][0][num]                                              Updated value: 900000
[2][cb][1][num]                                              Old value: 67
[2][cb][1][num]                                              Updated value: 900000
[2][final_value]                                             Old value: 117
[2][final_value]                                             Updated value: 900000
[{'cb': ({'ID': 1, 'Name': 'A', 'num': 900000},
         {'ID': 2, 'Name': 'A', 'num': 900000}),
  'final_value': 900000},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 900000},
         {'ID': 4, 'Name': 'A', 'num': 900000}),
  'final_value': 900000},
 {'cb': ({'ID': 1, 'Name': 'A', 'num': 900000},
         {'ID': 6, 'Name': 'A', 'num': 900000}),
  'final_value': 900000}]
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/69943509/problems-when-flatten-a-dict
data=
[{'application_contacts': [{'adress': 'X', 'email': 'test@test.com'}],
  'application_details': {'email': None, 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '1'},
 {'application_contacts': [{'adress': 'Z', 'email': None}],
  'application_details': {'email': 'testy@test_a.com', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '2'},
 {'application_contacts': [{'adress': 'Y', 'email': None}],
  'application_details': {'email': 'testy@test_a.com', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '3'}]
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                              aa_all_keys          aa_value
0 application_contacts 0     adress  (0, application_contacts, 0, adress)                 X
                             email    (0, application_contacts, 0, email)     test@test.com
  application_details  email NaN          (0, application_details, email)              None
                       phone NaN          (0, application_details, phone)              None
  employer             Name  NaN                      (0, employer, Name)               Nom
                       email NaN                     (0, employer, email)              None
  id                   NaN   NaN                                  (0, id)                 1
1 application_contacts 0     adress  (1, application_contacts, 0, adress)                 Z
                             email    (1, application_contacts, 0, email)              None
  application_details  email NaN          (1, application_details, email)  testy@test_a.com
                       phone NaN          (1, application_details, phone)              None
  employer             Name  NaN                      (1, employer, Name)               Nom
                       email NaN                     (1, employer, email)              None
  id                   NaN   NaN                                  (1, id)                 2
2 application_contacts 0     adress  (2, application_contacts, 0, adress)                 Y
                             email    (2, application_contacts, 0, email)              None
  application_details  email NaN          (2, application_details, email)  testy@test_a.com
                       phone NaN          (2, application_details, phone)              None
  employer             Name  NaN                      (2, employer, Name)               Nom
                       email NaN                     (2, employer, email)              None
  id                   NaN   NaN                                  (2, id)                 3
df.loc[df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'test_a\.\w+\b',na=False), 'aa_value'] = 'UPPPPPPPPPPPPPPPDATE.COM'
                                                              aa_all_keys                  aa_value
0 application_contacts 0     adress  (0, application_contacts, 0, adress)                         X
                             email    (0, application_contacts, 0, email)             test@test.com
  application_details  email NaN          (0, application_details, email)                      None
                       phone NaN          (0, application_details, phone)                      None
  employer             Name  NaN                      (0, employer, Name)                       Nom
                       email NaN                     (0, employer, email)                      None
  id                   NaN   NaN                                  (0, id)                         1
1 application_contacts 0     adress  (1, application_contacts, 0, adress)                         Z
                             email    (1, application_contacts, 0, email)                      None
  application_details  email NaN          (1, application_details, email)  UPPPPPPPPPPPPPPPDATE.COM
                       phone NaN          (1, application_details, phone)                      None
  employer             Name  NaN                      (1, employer, Name)                       Nom
                       email NaN                     (1, employer, email)                      None
  id                   NaN   NaN                                  (1, id)                         2
2 application_contacts 0     adress  (2, application_contacts, 0, adress)                         Y
                             email    (2, application_contacts, 0, email)                      None
  application_details  email NaN          (2, application_details, email)  UPPPPPPPPPPPPPPPDATE.COM
                       phone NaN          (2, application_details, phone)                      None
  employer             Name  NaN                      (2, employer, Name)                       Nom
                       email NaN                     (2, employer, email)                      None
  id                   NaN   NaN                                  (2, id)                         3
mod_iter = df.d_update_original_iter(data, verbose=True)
[1][application_details][email]                              Old value: testy@test_a.com
[1][application_details][email]                              Updated value: UPPPPPPPPPPPPPPPDATE.COM
[2][application_details][email]                              Old value: testy@test_a.com
[2][application_details][email]                              Updated value: UPPPPPPPPPPPPPPPDATE.COM
[{'application_contacts': [{'adress': 'X', 'email': 'test@test.com'}],
  'application_details': {'email': None, 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '1'},
 {'application_contacts': [{'adress': 'Z', 'email': None}],
  'application_details': {'email': 'UPPPPPPPPPPPPPPPDATE.COM', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '2'},
 {'application_contacts': [{'adress': 'Y', 'email': None}],
  'application_details': {'email': 'UPPPPPPPPPPPPPPPDATE.COM', 'phone': None},
  'employer': {'Name': 'Nom', 'email': None},
  'id': '3'}]
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/62765371/convert-nested-dataframe-to-a-simple-dataframeframe
data=
{'A': [1, 2, 3],
 'B': [4, 5, 6],
 'departure': [{'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'}]}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                   aa_all_keys                   aa_value
A         0 NaN                                         (A, 0)                          1
          1 NaN                                         (A, 1)                          2
          2 NaN                                         (A, 2)                          3
B         0 NaN                                         (B, 0)                          4
          1 NaN                                         (B, 1)                          5
          2 NaN                                         (B, 2)                          6
departure 0 actual                      (departure, 0, actual)                       None
            actual_runway        (departure, 0, actual_runway)                       None
            airport                    (departure, 0, airport)                     Findel
            delay                        (departure, 0, delay)                       None
            estimated                (departure, 0, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 0, estimated_runway)                       None
            gate                          (departure, 0, gate)                       None
            iata                          (departure, 0, iata)                        LUX
            icao                          (departure, 0, icao)                       ELLX
            scheduled                (departure, 0, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 0, terminal)                       None
            timezone                  (departure, 0, timezone)          Europe/Luxembourg
          1 actual                      (departure, 1, actual)                       None
            actual_runway        (departure, 1, actual_runway)                       None
            airport                    (departure, 1, airport)                     Findel
            delay                        (departure, 1, delay)                       None
            estimated                (departure, 1, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 1, estimated_runway)                       None
            gate                          (departure, 1, gate)                       None
            iata                          (departure, 1, iata)                        LUX
            icao                          (departure, 1, icao)                       ELLX
            scheduled                (departure, 1, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 1, terminal)                       None
            timezone                  (departure, 1, timezone)          Europe/Luxembourg
          2 actual                      (departure, 2, actual)                       None
            actual_runway        (departure, 2, actual_runway)                       None
            airport                    (departure, 2, airport)                     Findel
            delay                        (departure, 2, delay)                       None
            estimated                (departure, 2, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 2, estimated_runway)                       None
            gate                          (departure, 2, gate)                       None
            iata                          (departure, 2, iata)                        LUX
            icao                          (departure, 2, icao)                       ELLX
            scheduled                (departure, 2, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 2, terminal)                       None
            timezone                  (departure, 2, timezone)          Europe/Luxembourg
df.loc[df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value')== 'ELLX', 'aa_value'] = 'ELLX-UPDATED'
                                                   aa_all_keys                   aa_value
A         0 NaN                                         (A, 0)                          1
          1 NaN                                         (A, 1)                          2
          2 NaN                                         (A, 2)                          3
B         0 NaN                                         (B, 0)                          4
          1 NaN                                         (B, 1)                          5
          2 NaN                                         (B, 2)                          6
departure 0 actual                      (departure, 0, actual)                       None
            actual_runway        (departure, 0, actual_runway)                       None
            airport                    (departure, 0, airport)                     Findel
            delay                        (departure, 0, delay)                       None
            estimated                (departure, 0, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 0, estimated_runway)                       None
            gate                          (departure, 0, gate)                       None
            iata                          (departure, 0, iata)                        LUX
            icao                          (departure, 0, icao)               ELLX-UPDATED
            scheduled                (departure, 0, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 0, terminal)                       None
            timezone                  (departure, 0, timezone)          Europe/Luxembourg
          1 actual                      (departure, 1, actual)                       None
            actual_runway        (departure, 1, actual_runway)                       None
            airport                    (departure, 1, airport)                     Findel
            delay                        (departure, 1, delay)                       None
            estimated                (departure, 1, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 1, estimated_runway)                       None
            gate                          (departure, 1, gate)                       None
            iata                          (departure, 1, iata)                        LUX
            icao                          (departure, 1, icao)               ELLX-UPDATED
            scheduled                (departure, 1, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 1, terminal)                       None
            timezone                  (departure, 1, timezone)          Europe/Luxembourg
          2 actual                      (departure, 2, actual)                       None
            actual_runway        (departure, 2, actual_runway)                       None
            airport                    (departure, 2, airport)                     Findel
            delay                        (departure, 2, delay)                       None
            estimated                (departure, 2, estimated)  2020-07-07T06:30:00+00:00
            estimated_runway  (departure, 2, estimated_runway)                       None
            gate                          (departure, 2, gate)                       None
            iata                          (departure, 2, iata)                        LUX
            icao                          (departure, 2, icao)               ELLX-UPDATED
            scheduled                (departure, 2, scheduled)  2020-07-07T06:30:00+00:00
            terminal                  (departure, 2, terminal)                       None
            timezone                  (departure, 2, timezone)          Europe/Luxembourg
mod_iter = df.d_update_original_iter(data, verbose=True)
[departure][0][icao]                                         Old value: ELLX
[departure][0][icao]                                         Updated value: ELLX-UPDATED
[departure][1][icao]                                         Old value: ELLX
[departure][1][icao]                                         Updated value: ELLX-UPDATED
[departure][2][icao]                                         Old value: ELLX
[departure][2][icao]                                         Updated value: ELLX-UPDATED
{'A': [1, 2, 3],
 'B': [4, 5, 6],
 'departure': [{'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX-UPDATED',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX-UPDATED',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'},
               {'actual': None,
                'actual_runway': None,
                'airport': 'Findel',
                'delay': None,
                'estimated': '2020-07-07T06:30:00+00:00',
                'estimated_runway': None,
                'gate': None,
                'iata': 'LUX',
                'icao': 'ELLX-UPDATED',
                'scheduled': '2020-07-07T06:30:00+00:00',
                'terminal': None,
                'timezone': 'Europe/Luxembourg'}]}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/64359762/constructing-a-pandas-dataframe-with-columns-and-sub-columns-from-nested-diction
data=
{'level1': {'t1': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 8},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 9},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 8},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 9},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5, 'col2': 6, 'col3': 7, 'col4': 8},
                   's3': {'col1': 9, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}},
 'level2': {'t1': {'s1': {'col1': 5, 'col2': 4, 'col3': 9, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 5},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 13},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 20}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 8},
                   's3': {'col1': 11, 'col2': 8, 'col3': 2, 'col4': 9},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 9}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5, 'col2': 6, 'col3': 7, 'col4': 8},
                   's3': {'col1': 9, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}}}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                              aa_all_keys  aa_value
level1 t1 s1 col1  (level1, t1, s1, col1)         5
             col2  (level1, t1, s1, col2)         4
             col3  (level1, t1, s1, col3)         4
             col4  (level1, t1, s1, col4)         9
          s2 col1  (level1, t1, s2, col1)         1
                                   ...       ...
level2 t3 s3 col4  (level2, t3, s3, col4)        12
          s4 col1  (level2, t3, s4, col1)        13
             col2  (level2, t3, s4, col2)        14
             col3  (level2, t3, s4, col3)        15
             col4  (level2, t3, s4, col4)        16
[96 rows x 2 columns]
df.loc[(df.d_filter_dtypes(allowed_dtypes=(int),fillvalue=pd.NA,column='aa_value') > 5) & (df.d_filter_dtypes(allowed_dtypes=(int),fillvalue=pd.NA,column='aa_value') < 10), 'aa_value'] = 1000000
                              aa_all_keys  aa_value
level1 t1 s1 col1  (level1, t1, s1, col1)         5
             col2  (level1, t1, s1, col2)         4
             col3  (level1, t1, s1, col3)         4
             col4  (level1, t1, s1, col4)   1000000
          s2 col1  (level1, t1, s2, col1)         1
                                   ...       ...
level2 t3 s3 col4  (level2, t3, s3, col4)        12
          s4 col1  (level2, t3, s4, col1)        13
             col2  (level2, t3, s4, col2)        14
             col3  (level2, t3, s4, col3)        15
             col4  (level2, t3, s4, col4)        16
[96 rows x 2 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[level1][t1][s1][col4]                                       Old value: 9
[level1][t1][s1][col4]                                       Updated value: 1000000
[level1][t1][s2][col4]                                       Old value: 8
[level1][t1][s2][col4]                                       Updated value: 1000000
[level1][t1][s3][col2]                                       Old value: 8
[level1][t1][s3][col2]                                       Updated value: 1000000
[level1][t1][s3][col4]                                       Old value: 9
[level1][t1][s3][col4]                                       Updated value: 1000000
[level1][t1][s4][col4]                                       Old value: 9
[level1][t1][s4][col4]                                       Updated value: 1000000
[level1][t2][s1][col4]                                       Old value: 9
[level1][t2][s1][col4]                                       Updated value: 1000000
[level1][t2][s2][col4]                                       Old value: 8
[level1][t2][s2][col4]                                       Updated value: 1000000
[level1][t2][s3][col2]                                       Old value: 8
[level1][t2][s3][col2]                                       Updated value: 1000000
[level1][t2][s3][col4]                                       Old value: 9
[level1][t2][s3][col4]                                       Updated value: 1000000
[level1][t2][s4][col4]                                       Old value: 9
[level1][t2][s4][col4]                                       Updated value: 1000000
[level1][t3][s2][col2]                                       Old value: 6
[level1][t3][s2][col2]                                       Updated value: 1000000
[level1][t3][s2][col3]                                       Old value: 7
[level1][t3][s2][col3]                                       Updated value: 1000000
[level1][t3][s2][col4]                                       Old value: 8
[level1][t3][s2][col4]                                       Updated value: 1000000
[level1][t3][s3][col1]                                       Old value: 9
[level1][t3][s3][col1]                                       Updated value: 1000000
[level2][t1][s1][col3]                                       Old value: 9
[level2][t1][s1][col3]                                       Updated value: 1000000
[level2][t1][s1][col4]                                       Old value: 9
[level2][t1][s1][col4]                                       Updated value: 1000000
[level2][t1][s3][col2]                                       Old value: 8
[level2][t1][s3][col2]                                       Updated value: 1000000
[level2][t2][s1][col4]                                       Old value: 9
[level2][t2][s1][col4]                                       Updated value: 1000000
[level2][t2][s2][col4]                                       Old value: 8
[level2][t2][s2][col4]                                       Updated value: 1000000
[level2][t2][s3][col2]                                       Old value: 8
[level2][t2][s3][col2]                                       Updated value: 1000000
[level2][t2][s3][col4]                                       Old value: 9
[level2][t2][s3][col4]                                       Updated value: 1000000
[level2][t2][s4][col4]                                       Old value: 9
[level2][t2][s4][col4]                                       Updated value: 1000000
[level2][t3][s2][col2]                                       Old value: 6
[level2][t3][s2][col2]                                       Updated value: 1000000
[level2][t3][s2][col3]                                       Old value: 7
[level2][t3][s2][col3]                                       Updated value: 1000000
[level2][t3][s2][col4]                                       Old value: 8
[level2][t3][s2][col4]                                       Updated value: 1000000
[level2][t3][s3][col1]                                       Old value: 9
[level2][t3][s3][col1]                                       Updated value: 1000000
{'level1': {'t1': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 1000000},
                   's3': {'col1': 11,
                          'col2': 1000000,
                          'col3': 2,
                          'col4': 1000000},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 1000000},
                   's3': {'col1': 11,
                          'col2': 1000000,
                          'col3': 2,
                          'col4': 1000000},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5,
                          'col2': 1000000,
                          'col3': 1000000,
                          'col4': 1000000},
                   's3': {'col1': 1000000, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}},
 'level2': {'t1': {'s1': {'col1': 5,
                          'col2': 4,
                          'col3': 1000000,
                          'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 5},
                   's3': {'col1': 11, 'col2': 1000000, 'col3': 2, 'col4': 13},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 20}},
            't2': {'s1': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000},
                   's2': {'col1': 1, 'col2': 5, 'col3': 4, 'col4': 1000000},
                   's3': {'col1': 11,
                          'col2': 1000000,
                          'col3': 2,
                          'col4': 1000000},
                   's4': {'col1': 5, 'col2': 4, 'col3': 4, 'col4': 1000000}},
            't3': {'s1': {'col1': 1, 'col2': 2, 'col3': 3, 'col4': 4},
                   's2': {'col1': 5,
                          'col2': 1000000,
                          'col3': 1000000,
                          'col4': 1000000},
                   's3': {'col1': 1000000, 'col2': 10, 'col3': 11, 'col4': 12},
                   's4': {'col1': 13, 'col2': 14, 'col3': 15, 'col4': 16}}}}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/72146094/problems-matching-values-from-nested-dictionary
data=
{'_links': {'next': None, 'prev': None},
 'limit': 250,
 'offset': 0,
 'runs': [{'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': None,
           'config': None,
           'config_ids': [],
           'created_by': 1,
           'created_on': 1651790693,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 1,
           'id': 13,
           'include_all': False,
           'is_completed': False,
           'milestone_id': None,
           'name': '2022-05-05-testrun',
           'passed_count': 2,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 0,
           'updated_on': 1651790693,
           'url': 'https://xxxxxxxxxx.testrail.io/index.php?/runs/view/13'},
          {'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': 1650989972,
           'config': None,
           'config_ids': [],
           'created_by': 5,
           'created_on': 1650966329,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 0,
           'id': 9,
           'include_all': False,
           'is_completed': True,
           'milestone_id': None,
           'name': 'This is a new test run',
           'passed_count': 0,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 3,
           'updated_on': 1650966329,
           'url': 'https://xxxxxxxxxx.testrail.io/index.php?/runs/view/9'}],
 'size': 2}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                          aa_all_keys                                           aa_value
_links next NaN                        (_links, next)                                               None
       prev NaN                        (_links, prev)                                               None
limit  NaN  NaN                              (limit,)                                                250
offset NaN  NaN                             (offset,)                                                  0
runs   0    assignedto_id    (runs, 0, assignedto_id)                                               None
                                               ...                                                ...
       1    suite_id              (runs, 1, suite_id)                                                  1
            untested_count  (runs, 1, untested_count)                                                  3
            updated_on          (runs, 1, updated_on)                                         1650966329
            url                        (runs, 1, url)  https://xxxxxxxxxx.testrail.io/index.php?/runs...
size   NaN  NaN                               (size,)                                                  2
[63 rows x 2 columns]
df.loc[(df.d_filter_dtypes(allowed_dtypes=(bool),fillvalue=pd.NA,column='aa_value') ==False ), 'aa_value'] = True
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'https?://.*',na=False) ), 'aa_value'] = 'WWW.PYTHON.ORG'
                                          aa_all_keys        aa_value
_links next NaN                        (_links, next)            None
       prev NaN                        (_links, prev)            None
limit  NaN  NaN                              (limit,)             250
offset NaN  NaN                             (offset,)               0
runs   0    assignedto_id    (runs, 0, assignedto_id)            None
                                               ...             ...
       1    suite_id              (runs, 1, suite_id)               1
            untested_count  (runs, 1, untested_count)               3
            updated_on          (runs, 1, updated_on)      1650966329
            url                        (runs, 1, url)  WWW.PYTHON.ORG
size   NaN  NaN                               (size,)               2
[63 rows x 2 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[runs][0][include_all]                                       Old value: False
[runs][0][include_all]                                       Updated value: True
[runs][0][is_completed]                                      Old value: False
[runs][0][is_completed]                                      Updated value: True
[runs][0][url]                                               Old value: https://xxxxxxxxxx.testrail.io/index.php?/runs/view/13
[runs][0][url]                                               Updated value: WWW.PYTHON.ORG
[runs][1][include_all]                                       Old value: False
[runs][1][include_all]                                       Updated value: True
[runs][1][url]                                               Old value: https://xxxxxxxxxx.testrail.io/index.php?/runs/view/9
[runs][1][url]                                               Updated value: WWW.PYTHON.ORG
{'_links': {'next': None, 'prev': None},
 'limit': 250,
 'offset': 0,
 'runs': [{'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': None,
           'config': None,
           'config_ids': [],
           'created_by': 1,
           'created_on': 1651790693,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 1,
           'id': 13,
           'include_all': True,
           'is_completed': True,
           'milestone_id': None,
           'name': '2022-05-05-testrun',
           'passed_count': 2,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 0,
           'updated_on': 1651790693,
           'url': 'WWW.PYTHON.ORG'},
          {'assignedto_id': None,
           'blocked_count': 0,
           'completed_on': 1650989972,
           'config': None,
           'config_ids': [],
           'created_by': 5,
           'created_on': 1650966329,
           'custom_status1_count': 0,
           'custom_status2_count': 0,
           'custom_status3_count': 0,
           'custom_status4_count': 0,
           'custom_status5_count': 0,
           'custom_status6_count': 0,
           'custom_status7_count': 0,
           'description': None,
           'failed_count': 0,
           'id': 9,
           'include_all': True,
           'is_completed': True,
           'milestone_id': None,
           'name': 'This is a new test run',
           'passed_count': 0,
           'plan_id': None,
           'project_id': 1,
           'refs': None,
           'retest_count': 0,
           'suite_id': 1,
           'untested_count': 3,
           'updated_on': 1650966329,
           'url': 'WWW.PYTHON.ORG'}],
 'size': 2}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/73708706/how-to-get-values-from-list-of-nested-dictionaries/73839430#73839430
data=
{'results': [{'end_time': '2021-01-21',
              'key': 'q1',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['1']},
             {'end_time': '2021-01-21',
              'key': 'q2',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['False']},
             {'end_time': '2021-01-21',
              'key': 'q3',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['3']},
             {'end_time': '2021-01-21',
              'key': 'q4',
              'result_type': 'multipleChoice',
              'start_time': '2021-01-21',
              'value': ['3']}]}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                         aa_all_keys        aa_value
results 0 end_time    NaN     (results, 0, end_time)      2021-01-21
          key         NaN          (results, 0, key)              q1
          result_type NaN  (results, 0, result_type)  multipleChoice
          start_time  NaN   (results, 0, start_time)      2021-01-21
          value       0       (results, 0, value, 0)               1
        1 end_time    NaN     (results, 1, end_time)      2021-01-21
          key         NaN          (results, 1, key)              q2
          result_type NaN  (results, 1, result_type)  multipleChoice
          start_time  NaN   (results, 1, start_time)      2021-01-21
          value       0       (results, 1, value, 0)           False
        2 end_time    NaN     (results, 2, end_time)      2021-01-21
          key         NaN          (results, 2, key)              q3
          result_type NaN  (results, 2, result_type)  multipleChoice
          start_time  NaN   (results, 2, start_time)      2021-01-21
          value       0       (results, 2, value, 0)               3
        3 end_time    NaN     (results, 3, end_time)      2021-01-21
          key         NaN          (results, 3, key)              q4
          result_type NaN  (results, 3, result_type)  multipleChoice
          start_time  NaN   (results, 3, start_time)      2021-01-21
          value       0       (results, 3, value, 0)               3
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'^2021.*',na=False) ), 'aa_value'] = 10000000000 
                                         aa_all_keys        aa_value
results 0 end_time    NaN     (results, 0, end_time)     10000000000
          key         NaN          (results, 0, key)              q1
          result_type NaN  (results, 0, result_type)  multipleChoice
          start_time  NaN   (results, 0, start_time)     10000000000
          value       0       (results, 0, value, 0)               1
        1 end_time    NaN     (results, 1, end_time)     10000000000
          key         NaN          (results, 1, key)              q2
          result_type NaN  (results, 1, result_type)  multipleChoice
          start_time  NaN   (results, 1, start_time)     10000000000
          value       0       (results, 1, value, 0)           False
        2 end_time    NaN     (results, 2, end_time)     10000000000
          key         NaN          (results, 2, key)              q3
          result_type NaN  (results, 2, result_type)  multipleChoice
          start_time  NaN   (results, 2, start_time)     10000000000
          value       0       (results, 2, value, 0)               3
        3 end_time    NaN     (results, 3, end_time)     10000000000
          key         NaN          (results, 3, key)              q4
          result_type NaN  (results, 3, result_type)  multipleChoice
          start_time  NaN   (results, 3, start_time)     10000000000
          value       0       (results, 3, value, 0)               3
mod_iter = df.d_update_original_iter(data, verbose=True)
[results][0][end_time]                                       Old value: 2021-01-21
[results][0][end_time]                                       Updated value: 10000000000
[results][0][start_time]                                     Old value: 2021-01-21
[results][0][start_time]                                     Updated value: 10000000000
[results][1][end_time]                                       Old value: 2021-01-21
[results][1][end_time]                                       Updated value: 10000000000
[results][1][start_time]                                     Old value: 2021-01-21
[results][1][start_time]                                     Updated value: 10000000000
[results][2][end_time]                                       Old value: 2021-01-21
[results][2][end_time]                                       Updated value: 10000000000
[results][2][start_time]                                     Old value: 2021-01-21
[results][2][start_time]                                     Updated value: 10000000000
[results][3][end_time]                                       Old value: 2021-01-21
[results][3][end_time]                                       Updated value: 10000000000
[results][3][start_time]                                     Old value: 2021-01-21
[results][3][start_time]                                     Updated value: 10000000000
{'results': [{'end_time': 10000000000,
              'key': 'q1',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['1']},
             {'end_time': 10000000000,
              'key': 'q2',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['False']},
             {'end_time': 10000000000,
              'key': 'q3',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['3']},
             {'end_time': 10000000000,
              'key': 'q4',
              'result_type': 'multipleChoice',
              'start_time': 10000000000,
              'value': ['3']}]}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/66461902/flattening-nested-dictionary-into-dataframe-python
data=
{1: {2: {'IDs': {'BookID': ['543533254353', '4324232342'],
                 'SalesID': ['543267765345', '4353543'],
                 'StoreID': ['111111', '1121111']},
         'Name': 'boring Tales of Dragon Slayers'},
     'IDs': {'BookID': ['543533254353'],
             'SalesID': ['543267765345'],
             'StoreID': ['123445452543']},
     'Name': 'Thrilling Tales of Dragon Slayers'}}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                        aa_all_keys                           aa_value
1 IDs  BookID  0       NaN      (1, IDs, BookID, 0)                       543533254353
       SalesID 0       NaN     (1, IDs, SalesID, 0)                       543267765345
       StoreID 0       NaN     (1, IDs, StoreID, 0)                       123445452543
  Name NaN     NaN     NaN                (1, Name)  Thrilling Tales of Dragon Slayers
  2    IDs     BookID  0     (1, 2, IDs, BookID, 0)                       543533254353
                       1     (1, 2, IDs, BookID, 1)                         4324232342
               SalesID 0    (1, 2, IDs, SalesID, 0)                       543267765345
                       1    (1, 2, IDs, SalesID, 1)                            4353543
               StoreID 0    (1, 2, IDs, StoreID, 0)                             111111
                       1    (1, 2, IDs, StoreID, 1)                            1121111
       Name    NaN     NaN             (1, 2, Name)     boring Tales of Dragon Slayers
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'^\d+$',na=False) ), 'aa_value'] = df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='aa_value').str.contains(r'^\d+$',na=False) ), 'aa_value'].astype(float)
                                        aa_all_keys                           aa_value
1 IDs  BookID  0       NaN      (1, IDs, BookID, 0)                     543533254353.0
       SalesID 0       NaN     (1, IDs, SalesID, 0)                     543267765345.0
       StoreID 0       NaN     (1, IDs, StoreID, 0)                     123445452543.0
  Name NaN     NaN     NaN                (1, Name)  Thrilling Tales of Dragon Slayers
  2    IDs     BookID  0     (1, 2, IDs, BookID, 0)                     543533254353.0
                       1     (1, 2, IDs, BookID, 1)                       4324232342.0
               SalesID 0    (1, 2, IDs, SalesID, 0)                     543267765345.0
                       1    (1, 2, IDs, SalesID, 1)                          4353543.0
               StoreID 0    (1, 2, IDs, StoreID, 0)                           111111.0
                       1    (1, 2, IDs, StoreID, 1)                          1121111.0
       Name    NaN     NaN             (1, 2, Name)     boring Tales of Dragon Slayers
mod_iter = df.d_update_original_iter(data, verbose=True)
[1][2][IDs][BookID][0]                                       Old value: 543533254353
[1][2][IDs][BookID][0]                                       Updated value: 543533254353.0
[1][2][IDs][BookID][1]                                       Old value: 4324232342
[1][2][IDs][BookID][1]                                       Updated value: 4324232342.0
[1][2][IDs][SalesID][0]                                      Old value: 543267765345
[1][2][IDs][SalesID][0]                                      Updated value: 543267765345.0
[1][2][IDs][SalesID][1]                                      Old value: 4353543
[1][2][IDs][SalesID][1]                                      Updated value: 4353543.0
[1][2][IDs][StoreID][0]                                      Old value: 111111
[1][2][IDs][StoreID][0]                                      Updated value: 111111.0
[1][2][IDs][StoreID][1]                                      Old value: 1121111
[1][2][IDs][StoreID][1]                                      Updated value: 1121111.0
[1][IDs][BookID][0]                                          Old value: 543533254353
[1][IDs][BookID][0]                                          Updated value: 543533254353.0
[1][IDs][SalesID][0]                                         Old value: 543267765345
[1][IDs][SalesID][0]                                         Updated value: 543267765345.0
[1][IDs][StoreID][0]                                         Old value: 123445452543
[1][IDs][StoreID][0]                                         Updated value: 123445452543.0
{1: {2: {'IDs': {'BookID': [543533254353.0, 4324232342.0],
                 'SalesID': [543267765345.0, 4353543.0],
                 'StoreID': [111111.0, 1121111.0]},
         'Name': 'boring Tales of Dragon Slayers'},
     'IDs': {'BookID': [543533254353.0],
             'SalesID': [543267765345.0],
             'StoreID': [123445452543.0]},
     'Name': 'Thrilling Tales of Dragon Slayers'}}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/72017771/key-error-when-accessing-a-nested-dictionary
data=
[{'blocks': [{'block_id': 'BJNTn',
              'text': {'text': 'You have a new message.',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'WPn/l',
              'text': {'text': '*Heard By*\nFriend',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': '5yp',
              'text': {'text': '*Which Direction? *\nNorth',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'fKEpF',
              'text': {'text': '*Which Destination*\nNew York',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'qjAH',
              'text': {'text': '*New Customer:*\\Yes',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'yt4',
              'elements': [{'action_id': '+bc',
                            'text': {'bar': 'View results',
                                     'emoji': True,
                                     'type': 'plain_text'},
                            'type': 'button',
                            'url': 'www.example.com/results'}],
              'type': 'actions'},
             {'block_id': 'IBr',
              'text': {'text': ' ', 'type': 'mrkdwn', 'verbatim': False},
              'type': 'section'}],
  'bot_id': 'BPD4K3SJW',
  'subtype': 'bot_message',
  'text': "This content can't be displayed.",
  'timestamp': '1650905606.755969',
  'type': 'message',
  'username': 'admin'},
 {'blocks': [{'block_id': 'Smd',
              'text': {'text': 'You have a new message.',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': '6YaLt',
              'text': {'text': '*Heard By*\nOnline Search',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'w3o',
              'text': {'text': '*Which Direction: *\nNorth',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'PTQ',
              'text': {'text': '*Which Destination? *\nMiami',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'JCfSP',
              'text': {'text': '*New Customer? *\nNo',
                       'type': 'mrkdwn',
                       'verbatim': False},
              'type': 'section'},
             {'block_id': 'yt4',
              'elements': [{'action_id': '+bc',
                            'text': {'bar': 'View results',
                                     'emoji': True,
                                     'type': 'plain_text'},
                            'type': 'button',
                            'url': 'www.example.com/results'}],
              'type': 'actions'},
             {'block_id': 'RJOA',
              'text': {'text': ' ', 'type': 'mrkdwn', 'verbatim': False},
              'type': 'section'}],
  'bot_id': 'BPD4K3SJW',
  'subtype': 'bot_message',
  'text': "This content can't be displayed.",
  'timestamp': '1650899428.077709',
  'type': 'message',
  'username': 'admin'}]
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                              aa_all_keys                          aa_value
0 blocks    0.0 block_id NaN      NaN NaN        (0, blocks, 0, block_id)                             BJNTn
                text     text     NaN NaN      (0, blocks, 0, text, text)           You have a new message.
                         type     NaN NaN      (0, blocks, 0, text, type)                            mrkdwn
                         verbatim NaN NaN  (0, blocks, 0, text, verbatim)                             False
                type     NaN      NaN NaN            (0, blocks, 0, type)                           section
                                                                   ...                               ...
1 subtype   NaN NaN      NaN      NaN NaN                    (1, subtype)                       bot_message
  text      NaN NaN      NaN      NaN NaN                       (1, text)  This content can't be displayed.
  timestamp NaN NaN      NaN      NaN NaN                  (1, timestamp)                 1650899428.077709
  type      NaN NaN      NaN      NaN NaN                       (1, type)                           message
  username  NaN NaN      NaN      NaN NaN                   (1, username)                             admin
[88 rows x 2 columns]
df.loc[(df.d_filter_dtypes(allowed_dtypes=(bool),fillvalue=pd.NA,column='aa_value') == False), 'aa_value'] = 'NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'
                                                              aa_all_keys                                           aa_value
0 blocks    0.0 block_id NaN      NaN NaN        (0, blocks, 0, block_id)                                              BJNTn
                text     text     NaN NaN      (0, blocks, 0, text, text)                            You have a new message.
                         type     NaN NaN      (0, blocks, 0, text, type)                                             mrkdwn
                         verbatim NaN NaN  (0, blocks, 0, text, verbatim)  NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE B...
                type     NaN      NaN NaN            (0, blocks, 0, type)                                            section
                                                                   ...                                                ...
1 subtype   NaN NaN      NaN      NaN NaN                    (1, subtype)                                        bot_message
  text      NaN NaN      NaN      NaN NaN                       (1, text)                   This content can't be displayed.
  timestamp NaN NaN      NaN      NaN NaN                  (1, timestamp)                                  1650899428.077709
  type      NaN NaN      NaN      NaN NaN                       (1, type)                                            message
  username  NaN NaN      NaN      NaN NaN                   (1, username)                                              admin
[88 rows x 2 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[0][blocks][0][text][verbatim]                               Old value: False
[0][blocks][0][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[0][blocks][1][text][verbatim]                               Old value: False
[0][blocks][1][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[0][blocks][2][text][verbatim]                               Old value: False
[0][blocks][2][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[0][blocks][3][text][verbatim]                               Old value: False
[0][blocks][3][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[0][blocks][4][text][verbatim]                               Old value: False
[0][blocks][4][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[0][blocks][6][text][verbatim]                               Old value: False
[0][blocks][6][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[1][blocks][0][text][verbatim]                               Old value: False
[1][blocks][0][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[1][blocks][1][text][verbatim]                               Old value: False
[1][blocks][1][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[1][blocks][2][text][verbatim]                               Old value: False
[1][blocks][2][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[1][blocks][3][text][verbatim]                               Old value: False
[1][blocks][3][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[1][blocks][4][text][verbatim]                               Old value: False
[1][blocks][4][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[1][blocks][6][text][verbatim]                               Old value: False
[1][blocks][6][text][verbatim]                               Updated value: NOOOOOOOOOOOOOOOOOOO MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL
[{'blocks': [{'block_id': 'BJNTn',
              'text': {'text': 'You have a new message.',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'WPn/l',
              'text': {'text': '*Heard By*\nFriend',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': '5yp',
              'text': {'text': '*Which Direction? *\nNorth',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'fKEpF',
              'text': {'text': '*Which Destination*\nNew York',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'qjAH',
              'text': {'text': '*New Customer:*\\Yes',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'yt4',
              'elements': [{'action_id': '+bc',
                            'text': {'bar': 'View results',
                                     'emoji': True,
                                     'type': 'plain_text'},
                            'type': 'button',
                            'url': 'www.example.com/results'}],
              'type': 'actions'},
             {'block_id': 'IBr',
              'text': {'text': ' ',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'}],
  'bot_id': 'BPD4K3SJW',
  'subtype': 'bot_message',
  'text': "This content can't be displayed.",
  'timestamp': '1650905606.755969',
  'type': 'message',
  'username': 'admin'},
 {'blocks': [{'block_id': 'Smd',
              'text': {'text': 'You have a new message.',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': '6YaLt',
              'text': {'text': '*Heard By*\nOnline Search',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'w3o',
              'text': {'text': '*Which Direction: *\nNorth',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'PTQ',
              'text': {'text': '*Which Destination? *\nMiami',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'JCfSP',
              'text': {'text': '*New Customer? *\nNo',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'},
             {'block_id': 'yt4',
              'elements': [{'action_id': '+bc',
                            'text': {'bar': 'View results',
                                     'emoji': True,
                                     'type': 'plain_text'},
                            'type': 'button',
                            'url': 'www.example.com/results'}],
              'type': 'actions'},
             {'block_id': 'RJOA',
              'text': {'text': ' ',
                       'type': 'mrkdwn',
                       'verbatim': 'NOOOOOOOOOOOOOOOOOOO '
                                   'MOOOOOOOOOOOOOOOOOOOORE BOOOOOOOOOOOOOOOL'},
              'type': 'section'}],
  'bot_id': 'BPD4K3SJW',
  'subtype': 'bot_message',
  'text': "This content can't be displayed.",
  'timestamp': '1650899428.077709',
  'type': 'message',
  'username': 'admin'}]
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/73643077/how-to-transform-a-list-of-nested-dictionaries-into-a-data-frame-pd-json-normal
data=
[{'apple': {'price': 4, 'units': 3}},
 {'banana': {'price': 2, 'units': 20}},
 {'orange': {'price': 5, 'units': 15}}]
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                       aa_all_keys  aa_value
0 apple  price   (0, apple, price)         4
         units   (0, apple, units)         3
1 banana price  (1, banana, price)         2
         units  (1, banana, units)        20
2 orange price  (2, orange, price)         5
         units  (2, orange, units)        15
df.loc[(df.d_filter_dtypes(allowed_dtypes=(int),fillvalue=pd.NA,column='aa_value') >3) & (df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_1').str.contains("banana")), 'aa_value'] = 50000
   level_0 level_1 level_2         aa_all_keys  aa_value
0        0   apple   price   (0, apple, price)         4
1        0   apple   units   (0, apple, units)         3
2        1  banana   price  (1, banana, price)         2
3        1  banana   units  (1, banana, units)     50000
4        2  orange   price  (2, orange, price)         5
5        2  orange   units  (2, orange, units)        15
mod_iter = df.d_update_original_iter(data, verbose=True)
[1][banana][units]                                           Old value: 20
[1][banana][units]                                           Updated value: 50000
[{'apple': {'price': 4, 'units': 3}},
 {'banana': {'price': 2, 'units': 50000}},
 {'orange': {'price': 5, 'units': 15}}]
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/58110440/opening-nested-dict-in-a-single-column-to-multiple-columns-in-pandas
data=
{'simple25b': {'hands': {'0': {'currency': 'rm',
                               'handId': 'xyz',
                               'time': '2019-09-23 11:00:01'},
                         '1': {'currency': 'rm',
                               'handId': 'abc',
                               'time': '2019-09-23 11:01:18'}}},
 'simple5af': {'hands': {'0': {'currency': 'rm',
                               'handId': 'akg',
                               'time': '2019-09-23 10:53:22'},
                         '1': {'currency': 'rm',
                               'handId': 'mzc',
                               'time': '2019-09-23 10:54:15'},
                         '2': {'currency': 'rm',
                               'handId': 'swk',
                               'time': '2019-09-23 10:56:03'},
                         '3': {'currency': 'rm',
                               'handId': 'pQc',
                               'time': '2019-09-23 10:57:15'},
                         '4': {'currency': 'rm',
                               'handId': 'ywh',
                               'time': '2019-09-23 10:58:53'}}}}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                aa_all_keys             aa_value
simple25b hands 0 currency  (simple25b, hands, 0, currency)                   rm
                  handId      (simple25b, hands, 0, handId)                  xyz
                  time          (simple25b, hands, 0, time)  2019-09-23 11:00:01
                1 currency  (simple25b, hands, 1, currency)                   rm
                  handId      (simple25b, hands, 1, handId)                  abc
                  time          (simple25b, hands, 1, time)  2019-09-23 11:01:18
simple5af hands 0 currency  (simple5af, hands, 0, currency)                   rm
                  handId      (simple5af, hands, 0, handId)                  akg
                  time          (simple5af, hands, 0, time)  2019-09-23 10:53:22
                1 currency  (simple5af, hands, 1, currency)                   rm
                  handId      (simple5af, hands, 1, handId)                  mzc
                  time          (simple5af, hands, 1, time)  2019-09-23 10:54:15
                2 currency  (simple5af, hands, 2, currency)                   rm
                  handId      (simple5af, hands, 2, handId)                  swk
                  time          (simple5af, hands, 2, time)  2019-09-23 10:56:03
                3 currency  (simple5af, hands, 3, currency)                   rm
                  handId      (simple5af, hands, 3, handId)                  pQc
                  time          (simple5af, hands, 3, time)  2019-09-23 10:57:15
                4 currency  (simple5af, hands, 4, currency)                   rm
                  handId      (simple5af, hands, 4, handId)                  ywh
                  time          (simple5af, hands, 4, time)  2019-09-23 10:58:53
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_3').str.contains("time")), 'aa_value'] = pd.to_datetime(df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_3').str.contains("time")), 'aa_value'])
      level_0 level_1  ...                      aa_all_keys             aa_value
0   simple25b   hands  ...  (simple25b, hands, 0, currency)                   rm
1   simple25b   hands  ...    (simple25b, hands, 0, handId)                  xyz
2   simple25b   hands  ...      (simple25b, hands, 0, time)  2019-09-23 11:00:01
3   simple25b   hands  ...  (simple25b, hands, 1, currency)                   rm
4   simple25b   hands  ...    (simple25b, hands, 1, handId)                  abc
5   simple25b   hands  ...      (simple25b, hands, 1, time)  2019-09-23 11:01:18
6   simple5af   hands  ...  (simple5af, hands, 0, currency)                   rm
7   simple5af   hands  ...    (simple5af, hands, 0, handId)                  akg
8   simple5af   hands  ...      (simple5af, hands, 0, time)  2019-09-23 10:53:22
9   simple5af   hands  ...  (simple5af, hands, 1, currency)                   rm
10  simple5af   hands  ...    (simple5af, hands, 1, handId)                  mzc
11  simple5af   hands  ...      (simple5af, hands, 1, time)  2019-09-23 10:54:15
12  simple5af   hands  ...  (simple5af, hands, 2, currency)                   rm
13  simple5af   hands  ...    (simple5af, hands, 2, handId)                  swk
14  simple5af   hands  ...      (simple5af, hands, 2, time)  2019-09-23 10:56:03
15  simple5af   hands  ...  (simple5af, hands, 3, currency)                   rm
16  simple5af   hands  ...    (simple5af, hands, 3, handId)                  pQc
17  simple5af   hands  ...      (simple5af, hands, 3, time)  2019-09-23 10:57:15
18  simple5af   hands  ...  (simple5af, hands, 4, currency)                   rm
19  simple5af   hands  ...    (simple5af, hands, 4, handId)                  ywh
20  simple5af   hands  ...      (simple5af, hands, 4, time)  2019-09-23 10:58:53
[21 rows x 6 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
{'simple25b': {'hands': {'0': {'currency': 'rm',
                               'handId': 'xyz',
                               'time': Timestamp('2019-09-23 11:00:01')},
                         '1': {'currency': 'rm',
                               'handId': 'abc',
                               'time': Timestamp('2019-09-23 11:01:18')}}},
 'simple5af': {'hands': {'0': {'currency': 'rm',
                               'handId': 'akg',
                               'time': Timestamp('2019-09-23 10:53:22')},
                         '1': {'currency': 'rm',
                               'handId': 'mzc',
                               'time': Timestamp('2019-09-23 10:54:15')},
                         '2': {'currency': 'rm',
                               'handId': 'swk',
                               'time': Timestamp('2019-09-23 10:56:03')},
                         '3': {'currency': 'rm',
                               'handId': 'pQc',
                               'time': Timestamp('2019-09-23 10:57:15')},
                         '4': {'currency': 'rm',
                               'handId': 'ywh',
                               'time': Timestamp('2019-09-23 10:58:53')}}}}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/62059970/how-can-i-convert-nested-dictionary-to-pd-dataframe-faster
data=
{'file': 'name',
 'main': [{'answer': [{'comment': 'It is defined as',
                       'user': 'John',
                       'value': [{'my_value': 5, 'value_2': 10},
                                 {'my_value': 24, 'value_2': 30}]},
                      {'comment': 'as John said above it simply means',
                       'user': 'Sam',
                       'value': [{'my_value': 9, 'value_2': 10},
                                 {'my_value': 54, 'value_2': 19}]}],
           'closed': 'no',
           'question': 'what is ?',
           'question_no': 'Q.1'}]}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                                            aa_all_keys                            aa_value
file NaN NaN         NaN NaN     NaN NaN                                        (file,)                                name
main 0   answer      0   comment NaN NaN                  (main, 0, answer, 0, comment)                    It is defined as
                         user    NaN NaN                     (main, 0, answer, 0, user)                                John
                         value   0   my_value  (main, 0, answer, 0, value, 0, my_value)                                   5
                                     value_2    (main, 0, answer, 0, value, 0, value_2)                                  10
                                 1   my_value  (main, 0, answer, 0, value, 1, my_value)                                  24
                                     value_2    (main, 0, answer, 0, value, 1, value_2)                                  30
                     1   comment NaN NaN                  (main, 0, answer, 1, comment)  as John said above it simply means
                         user    NaN NaN                     (main, 0, answer, 1, user)                                 Sam
                         value   0   my_value  (main, 0, answer, 1, value, 0, my_value)                                   9
                                     value_2    (main, 0, answer, 1, value, 0, value_2)                                  10
                                 1   my_value  (main, 0, answer, 1, value, 1, my_value)                                  54
                                     value_2    (main, 0, answer, 1, value, 1, value_2)                                  19
         closed      NaN NaN     NaN NaN                              (main, 0, closed)                                  no
         question    NaN NaN     NaN NaN                            (main, 0, question)                           what is ?
         question_no NaN NaN     NaN NaN                         (main, 0, question_no)                                 Q.1
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_6').str.contains("value_2",na=False)), 'aa_value'] = df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_6').str.contains("value_2",na=False)), 'aa_value']*1000
   level_0  ...                            aa_value
0     file  ...                                name
1     main  ...                    It is defined as
2     main  ...                                John
3     main  ...                                   5
4     main  ...                               10000
5     main  ...                                  24
6     main  ...                               30000
7     main  ...  as John said above it simply means
8     main  ...                                 Sam
9     main  ...                                   9
10    main  ...                               10000
11    main  ...                                  54
12    main  ...                               19000
13    main  ...                                  no
14    main  ...                           what is ?
15    main  ...                                 Q.1
[16 rows x 9 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[main][0][answer][0][value][0][value_2]                      Old value: 10
[main][0][answer][0][value][0][value_2]                      Updated value: 10000
[main][0][answer][0][value][1][value_2]                      Old value: 30
[main][0][answer][0][value][1][value_2]                      Updated value: 30000
[main][0][answer][1][value][0][value_2]                      Old value: 10
[main][0][answer][1][value][0][value_2]                      Updated value: 10000
[main][0][answer][1][value][1][value_2]                      Old value: 19
[main][0][answer][1][value][1][value_2]                      Updated value: 19000
{'file': 'name',
 'main': [{'answer': [{'comment': 'It is defined as',
                       'user': 'John',
                       'value': [{'my_value': 5, 'value_2': 10000},
                                 {'my_value': 24, 'value_2': 30000}]},
                      {'comment': 'as John said above it simply means',
                       'user': 'Sam',
                       'value': [{'my_value': 9, 'value_2': 10000},
                                 {'my_value': 54, 'value_2': 19000}]}],
           'closed': 'no',
           'question': 'what is ?',
           'question_no': 'Q.1'}]}
```

```python
#Nested iterable from: 
https://stackoverflow.com/questions/39634369/4-dimensional-nested-dictionary-to-pandas-data-frame
data=
{'orders': [{'created_at': '2016-09-20T22:04:49+02:00',
             'email': 'test@aol.com',
             'id': 4314127108,
             'line_items': [{'destination_location': {'address1': 'Teststreet '
                                                                  '12',
                                                      'address2': '',
                                                      'city': 'Berlin',
                                                      'country_code': 'DE',
                                                      'id': 2383331012,
                                                      'name': 'Test Test',
                                                      'zip': '10117'},
                             'gift_card': False,
                             'name': 'Blueberry Cup'},
                            {'destination_location': {'address1': 'Teststreet '
                                                                  '12',
                                                      'address2': '',
                                                      'city': 'Berlin',
                                                      'country_code': 'DE',
                                                      'id': 2383331012,
                                                      'name': 'Test Test',
                                                      'zip': '10117'},
                             'gift_card': False,
                             'name': 'Strawberry Cup'}]}]}
df = pd.Q_AnyNestedIterable_2df(data,unstack=False)
                                                                                                 aa_all_keys                   aa_value
orders 0 created_at NaN NaN                  NaN                                     (orders, 0, created_at)  2016-09-20T22:04:49+02:00
         email      NaN NaN                  NaN                                          (orders, 0, email)               test@aol.com
         id         NaN NaN                  NaN                                             (orders, 0, id)                 4314127108
         line_items 0   destination_location address1      (orders, 0, line_items, 0, destination_locatio...              Teststreet 12
                                             address2      (orders, 0, line_items, 0, destination_locatio...                           
                                             city          (orders, 0, line_items, 0, destination_locatio...                     Berlin
                                             country_code  (orders, 0, line_items, 0, destination_locatio...                         DE
                                             id            (orders, 0, line_items, 0, destination_locatio...                 2383331012
                                             name          (orders, 0, line_items, 0, destination_locatio...                  Test Test
                                             zip           (orders, 0, line_items, 0, destination_locatio...                      10117
                        gift_card            NaN                       (orders, 0, line_items, 0, gift_card)                      False
                        name                 NaN                            (orders, 0, line_items, 0, name)              Blueberry Cup
                    1   destination_location address1      (orders, 0, line_items, 1, destination_locatio...              Teststreet 12
                                             address2      (orders, 0, line_items, 1, destination_locatio...                           
                                             city          (orders, 0, line_items, 1, destination_locatio...                     Berlin
                                             country_code  (orders, 0, line_items, 1, destination_locatio...                         DE
                                             id            (orders, 0, line_items, 1, destination_locatio...                 2383331012
                                             name          (orders, 0, line_items, 1, destination_locatio...                  Test Test
                                             zip           (orders, 0, line_items, 1, destination_locatio...                      10117
                        gift_card            NaN                       (orders, 0, line_items, 1, gift_card)                      False
                        name                 NaN                            (orders, 0, line_items, 1, name)             Strawberry Cup
df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_6').str.contains("value_2",na=False)), 'aa_value'] = df.loc[(df.d_filter_dtypes(allowed_dtypes=(str),fillvalue=pd.NA,column='level_6').str.contains("value_2",na=False)), 'aa_value']*1000
   level_0  ...                              aa_value
0   orders  ...             2016-09-20T22:04:49+02:00
1   orders  ...                          test@aol.com
2   orders  ...                            4314127108
3   orders  ...                         Teststreet 12
4   orders  ...                                      
5   orders  ...  FRANKFURT IST VIEL BESSER ALS BERLIN
6   orders  ...                                    DE
7   orders  ...                            2383331012
8   orders  ...                             Test Test
9   orders  ...                                 10117
10  orders  ...                                 False
11  orders  ...                         Blueberry Cup
12  orders  ...                         Teststreet 12
13  orders  ...                                      
14  orders  ...  FRANKFURT IST VIEL BESSER ALS BERLIN
15  orders  ...                                    DE
16  orders  ...                            2383331012
17  orders  ...                             Test Test
18  orders  ...                                 10117
19  orders  ...                                 False
20  orders  ...                        Strawberry Cup
[21 rows x 8 columns]
mod_iter = df.d_update_original_iter(data, verbose=True)
[orders][0][line_items][0][destination_location][city]       Old value: Berlin
[orders][0][line_items][0][destination_location][city]       Updated value: FRANKFURT IST VIEL BESSER ALS BERLIN
[orders][0][line_items][1][destination_location][city]       Old value: Berlin
[orders][0][line_items][1][destination_location][city]       Updated value: FRANKFURT IST VIEL BESSER ALS BERLIN
{'orders': [{'created_at': '2016-09-20T22:04:49+02:00',
             'email': 'test@aol.com',
             'id': 4314127108,
             'line_items': [{'destination_location': {'address1': 'Teststreet '
                                                                  '12',
                                                      'address2': '',
                                                      'city': 'FRANKFURT IST '
                                                              'VIEL BESSER ALS '
                                                              'BERLIN',
                                                      'country_code': 'DE',
                                                      'id': 2383331012,
                                                      'name': 'Test Test',
                                                      'zip': '10117'},
                             'gift_card': False,
                             'name': 'Blueberry Cup'},
                            {'destination_location': {'address1': 'Teststreet '
                                                                  '12',
                                                      'address2': '',
                                                      'city': 'FRANKFURT IST '
                                                              'VIEL BESSER ALS '
                                                              'BERLIN',
                                                      'country_code': 'DE',
                                                      'id': 2383331012,
                                                      'name': 'Test Test',
                                                      'zip': '10117'},
                             'gift_card': False,
                             'name': 'Strawberry Cup'}]}]}
```

### **df.s_delete_duplicates_from_iters_in_cells**

```python
    delete_duplicates_in_column_full_of_iters(df: pandas.core.series.Series) -> pandas.core.series.Series
        df = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        getdi = lambda x: [    (randrange(1, 4), randrange(1, 4)) for v in range(20)]  #create some random tuples
        df["dicttest"] = df.lkey.apply(lambda x: getdi(x))
        print(df)
        df["dicttest"]=df.dicttest.s_delete_duplicates_from_iters_in_cells()
        print(df)
          lkey  value                                           dicttest
        0  foo      1  [(2, 1), (3, 3), (3, 3), (2, 1), (1, 2), (1, 2...
        1  bar      2  [(3, 2), (1, 1), (1, 1), (1, 2), (3, 2), (1, 2...
        2  baz      3  [(1, 2), (3, 1), (2, 1), (2, 1), (1, 1), (2, 3...
        3  foo      5  [(2, 3), (2, 3), (3, 3), (2, 2), (1, 2), (1, 2...
          lkey  value                                           dicttest
        0  foo      1  [(2, 1), (3, 3), (1, 2), (1, 3), (3, 2), (2, 3...
        1  bar      2  [(3, 2), (1, 1), (1, 2), (2, 1), (3, 1), (3, 3...
        2  baz      3  [(1, 2), (3, 1), (2, 1), (1, 1), (2, 3), (3, 3...
        3  foo      5  [(2, 3), (3, 3), (2, 2), (1, 2), (1, 1), (1, 3...
            Parameters:
            df : pd.Series
                Column with duplicates that are difficult to handle
            Returns:
                pd.Series
```

### df.ds_explode_dicts_in_column()

```python
    explode_dicts_in_column(df: pandas.core.frame.DataFrame, column_to_explode: str, drop_exploded_column: bool = True) -> pandas.core.frame.DataFrame
        df = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        getdi = lambda x: {    v: {v * randrange(1, 10): v * randrange(1, 10)} for v in range((randrange(1, 10)))} #create random nested dicts
        df["dicttest"] = df.lkey.apply(getdi)
        print(df)
        print(df.ds_explode_dicts_in_column('dicttest'))
          lkey  value                                           dicttest
        0  foo      1  {0: {0: 0}, 1: {1: 7}, 2: {2: 8}, 3: {3: 18}, ...
        1  bar      2  {0: {0: 0}, 1: {9: 4}, 2: {10: 6}, 3: {3: 21},...
        2  baz      3  {0: {0: 0}, 1: {9: 7}, 2: {2: 10}, 3: {21: 27}...
        3  foo      5                                        {0: {0: 0}}
           lkey value  level_0  level_1 aa_all_keys  aa_value
        0   foo     1        0        0      (0, 0)         0
        1   foo     1        1        1      (1, 1)         7
        2   foo     1        2        2      (2, 2)         8
        3   foo     1        3        3      (3, 3)        18
        4   foo     1        4       32     (4, 32)        16
        5   foo     1        5       35     (5, 35)        15
        6   bar     2        0        0      (0, 0)         0
        7   bar     2        1        9      (1, 9)         4
        8   bar     2        2       10     (2, 10)         6
        9   bar     2        3        3      (3, 3)        21
        10  bar     2        4       24     (4, 24)        36
        11  baz     3        0        0      (0, 0)         0
        12  baz     3        1        9      (1, 9)         7
        13  baz     3        2        2      (2, 2)        10
        14  baz     3        3       21     (3, 21)        27
        15  baz     3        4       28     (4, 28)        20
        16  baz     3        5       15     (5, 15)        30
        17  baz     3        6        6      (6, 6)         6
        18  baz     3        7       21     (7, 21)         7
        19  baz     3        8       24     (8, 24)        48
        20  foo     5        0        0      (0, 0)         0
            Parameters:
                df:pd.DataFrame
                    pd.DataFrame
                column_to_explode:str
                    column with dict in cells
                drop_exploded_column:bool
                    Drop column after exploding (default = True  )
            Returns:
                pd.DataFrame
```

### df.d_df_to_nested_dict()

```python
    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to convert
    groupby: str
        column whose values will be the top level keys
    subkeys: list
        columns wholse values will be the nested keys

    df = pd.read_csv(    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")

        Nested dict from DataFrame:
    df[:5].d_df_to_nested_dict(groupby='Survived', subkeys=['PassengerId', 'Age', 'Pclass', 'Name', 'Sex'])

    {0: {'PassengerId': {0: 1, 4: 5},
      'Age': {0: 22.0, 4: 35.0},
      'Pclass': {0: 3, 4: 3},
      'Name': {0: 'Braund, Mr. Owen Harris', 4: 'Allen, Mr. William Henry'},
      'Sex': {0: 'male', 4: 'male'}},
     1: {'PassengerId': {1: 2, 2: 3, 3: 4},
      'Age': {1: 38.0, 2: 26.0, 3: 35.0},
      'Pclass': {1: 1, 2: 3, 3: 1},
      'Name': {1: 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)',
       2: 'Heikkinen, Miss. Laina',
       3: 'Futrelle, Mrs. Jacques Heath (Lily May Peel)'},
      'Sex': {1: 'female', 2: 'female', 3: 'female'}}}


    df[:5].d_df_to_nested_dict(groupby='Sex', subkeys=['PassengerId', 'Name'])
    Out[39]:
    {'male': {'PassengerId': {0: 1, 4: 5},
      'Name': {0: 'Braund, Mr. Owen Harris', 4: 'Allen, Mr. William Henry'}},
     'female': {'PassengerId': {1: 2, 2: 3, 3: 4},
      'Name': {1: 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)',
       2: 'Heikkinen, Miss. Laina',
       3: 'Futrelle, Mrs. Jacques Heath (Lily May Peel)'}}}
```

### df.s_explode_lists_and_tuples()

```python
    explode_lists_and_tuples_in_column(df: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], column: Optional[str] = None, concat_with_df: bool = False) -> pandas.core.frame.DataFrame
        df = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                            'value': [1, 2, 3, 5]})
        getdi = lambda x: [    (randrange(1, 4), randrange(1, 4)) for v in range(randrange(1,5))]  #create some random tuples
        df["dicttest"] = df.lkey.apply(lambda x: getdi(x))
        print(df)
        df1=df.s_explode_lists_and_tuples(column='dicttest', concat_with_df=True)
        print(df1)
        df2=df.s_explode_lists_and_tuples(column='dicttest', concat_with_df=False)
        print(df2)
        df3=df.dicttest.s_explode_lists_and_tuples(column=None)
        print(df3)

          lkey  value                  dicttest
        0  foo      1                  [(3, 3)]
        1  bar      2  [(2, 3), (2, 1), (2, 2)]
        2  baz      3          [(2, 3), (2, 3)]
        3  foo      5                  [(1, 2)]

          lkey  value                  dicttest dicttest_0 dicttest_1 dicttest_2
        0  foo      1                  [(3, 3)]     (3, 3)       <NA>       <NA>
        1  bar      2  [(2, 3), (2, 1), (2, 2)]     (2, 3)     (2, 1)     (2, 2)
        2  baz      3          [(2, 3), (2, 3)]     (2, 3)     (2, 3)       <NA>
        3  foo      5                  [(1, 2)]     (1, 2)       <NA>       <NA>

          dicttest_0 dicttest_1 dicttest_2
        0     (3, 3)       <NA>       <NA>
        1     (2, 3)     (2, 1)     (2, 2)
        2     (2, 3)     (2, 3)       <NA>
        3     (1, 2)       <NA>       <NA>

          dicttest_0 dicttest_1 dicttest_2
        0     (3, 3)       <NA>       <NA>
        1     (2, 3)     (2, 1)     (2, 2)
        2     (2, 3)     (2, 3)       <NA>
        3     (1, 2)       <NA>       <NA>

            Parameters:
                df: Union[pd.Series, pd.DataFrame]
                    pd.Series, pd.DataFrame with lists/tuples in cells
                column: Union[str, None]
                    None can only be used if a pd.Series is passed. If a DataFrame is passed, a column needs to be passed too.
                concat_with_df: bool
                    if True -> returns df + exploded Series as DataFrame
                    if False -> returns exploded Series as DataFrame
            Returns:
                pd.DataFrame
                     Missing values are filled with pd.NA
```

### df.s_flatten_all_iters_in_cells()

```python
    flatten_all_iters_in_cells(df: pandas.core.series.Series) -> pandas.core.series.Series
        df = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        getdi = lambda x: [    (randrange(1, 4), randrange(1, 4)) for v in range(20)]  #create some random tuples
        df["dicttest"] = df.lkey.apply(lambda x: getdi(x))
        print(df)
        df["dicttest"]=df.dicttest.s_flatten_all_iters_in_cells()
        print(df)
          lkey  value                                           dicttest
        0  foo      1  [(2, 2), (3, 3), (3, 2), (1, 3), (1, 2), (2, 2...
        1  bar      2  [(1, 1), (3, 1), (1, 3), (3, 2), (3, 1), (2, 2...
        2  baz      3  [(3, 1), (1, 1), (3, 3), (1, 3), (3, 2), (3, 3...
        3  foo      5  [(3, 3), (3, 3), (3, 2), (2, 3), (3, 3), (2, 3...
          lkey  value                                           dicttest
        0  foo      1  [2, 2, 3, 3, 3, 2, 1, 3, 1, 2, 2, 2, 1, 3, 1, ...
        1  bar      2  [1, 1, 3, 1, 1, 3, 3, 2, 3, 1, 2, 2, 3, 1, 3, ...
        2  baz      3  [3, 1, 1, 1, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 1, ...
        3  foo      5  [3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 3, ...
            Parameters:
            df : pd.Series
                Column with duplicates that are difficult to handle
            Returns:
                pd.Series
```

### df.d_multiple_columns_to_one()

```python
    make_several_columns_fit_in_one(df: pandas.core.frame.DataFrame, columns: list) -> list
        df = pd.read_csv(
        "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
        )[:20]
        print(df)
        df['Ticket_Fare_Embarked'] = df.d_multiple_columns_to_one(columns=['Ticket','Fare', 'Embarked'])
            PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0             1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1             2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2             3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3             4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4             5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        5             6         0       3                                   Moran, Mr. James    male  ...      0            330877   8.4583   NaN         Q
        6             7         0       1                            McCarthy, Mr. Timothy J    male  ...      0             17463  51.8625   E46         S
        7             8         0       3                     Palsson, Master. Gosta Leonard    male  ...      1            349909  21.0750   NaN         S
        8             9         1       3  Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)  female  ...      2            347742  11.1333   NaN         S
        9            10         1       2                Nasser, Mrs. Nicholas (Adele Achem)  female  ...      0            237736  30.0708   NaN         C
        10           11         1       3                    Sandstrom, Miss. Marguerite Rut  female  ...      1           PP 9549  16.7000    G6         S
        11           12         1       1                           Bonnell, Miss. Elizabeth  female  ...      0            113783  26.5500  C103         S
        12           13         0       3                     Saundercock, Mr. William Henry    male  ...      0         A/5. 2151   8.0500   NaN         S
        13           14         0       3                        Andersson, Mr. Anders Johan    male  ...      5            347082  31.2750   NaN         S
        14           15         0       3               Vestrom, Miss. Hulda Amanda Adolfina  female  ...      0            350406   7.8542   NaN         S
        15           16         1       2                   Hewlett, Mrs. (Mary D Kingcome)   female  ...      0            248706  16.0000   NaN         S
        16           17         0       3                               Rice, Master. Eugene    male  ...      1            382652  29.1250   NaN         Q
        17           18         1       2                       Williams, Mr. Charles Eugene    male  ...      0            244373  13.0000   NaN         S
        18           19         0       3  Vander Planke, Mrs. Julius (Emelia Maria Vande...  female  ...      0            345763  18.0000   NaN         S
        19           20         1       3                            Masselmani, Mrs. Fatima  female  ...      0              2649   7.2250   NaN         C
        [20 rows x 12 columns]
        df
        Out[30]:
            PassengerId  Survived  Pclass                                               Name     Sex  ...            Ticket     Fare  Cabin Embarked          Ticket_Fare_Embarked
        0             1         0       3                            Braund, Mr. Owen Harris    male  ...         A/5 21171   7.2500    NaN        S          [A/5 21171, 7.25, S]
        1             2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...          PC 17599  71.2833    C85        C        [PC 17599, 71.2833, C]
        2             3         1       3                             Heikkinen, Miss. Laina  female  ...  STON/O2. 3101282   7.9250    NaN        S  [STON/O2. 3101282, 7.925, S]
        3             4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...            113803  53.1000   C123        S             [113803, 53.1, S]
        4             5         0       3                           Allen, Mr. William Henry    male  ...            373450   8.0500    NaN        S             [373450, 8.05, S]
        5             6         0       3                                   Moran, Mr. James    male  ...            330877   8.4583    NaN        Q           [330877, 8.4583, Q]
        6             7         0       1                            McCarthy, Mr. Timothy J    male  ...             17463  51.8625    E46        S           [17463, 51.8625, S]
        7             8         0       3                     Palsson, Master. Gosta Leonard    male  ...            349909  21.0750    NaN        S           [349909, 21.075, S]
        8             9         1       3  Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)  female  ...            347742  11.1333    NaN        S          [347742, 11.1333, S]
        9            10         1       2                Nasser, Mrs. Nicholas (Adele Achem)  female  ...            237736  30.0708    NaN        C          [237736, 30.0708, C]
        10           11         1       3                    Sandstrom, Miss. Marguerite Rut  female  ...           PP 9549  16.7000     G6        S            [PP 9549, 16.7, S]
        11           12         1       1                           Bonnell, Miss. Elizabeth  female  ...            113783  26.5500   C103        S            [113783, 26.55, S]
        12           13         0       3                     Saundercock, Mr. William Henry    male  ...         A/5. 2151   8.0500    NaN        S          [A/5. 2151, 8.05, S]
        13           14         0       3                        Andersson, Mr. Anders Johan    male  ...            347082  31.2750    NaN        S           [347082, 31.275, S]
        14           15         0       3               Vestrom, Miss. Hulda Amanda Adolfina  female  ...            350406   7.8542    NaN        S           [350406, 7.8542, S]
        15           16         1       2                   Hewlett, Mrs. (Mary D Kingcome)   female  ...            248706  16.0000    NaN        S             [248706, 16.0, S]
        16           17         0       3                               Rice, Master. Eugene    male  ...            382652  29.1250    NaN        Q           [382652, 29.125, Q]
        17           18         1       2                       Williams, Mr. Charles Eugene    male  ...            244373  13.0000    NaN        S             [244373, 13.0, S]
        18           19         0       3  Vander Planke, Mrs. Julius (Emelia Maria Vande...  female  ...            345763  18.0000    NaN        S             [345763, 18.0, S]
        19           20         1       3                            Masselmani, Mrs. Fatima  female  ...              2649   7.2250    NaN        C              [2649, 7.225, C]
        [20 rows x 13 columns]
            Parameters:
                df: pd.DataFrame
                    DataFrame
                columns: list
                    columns to squeeze
            Returns:
                list
```

### df.ds_normalize_lists()

```python
    normalize_lists_in_column_end_user(df: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], column: Optional[str] = None) -> pandas.core.series.Series
        df = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        getdi = lambda x: [    (randrange(1, 4), randrange(1, 4)) for v in range(randrange(1,5))]  #create some random tuples
        df["dicttest"] = df.lkey.apply(lambda x: getdi(x))
        print(df)
        df1=df.ds_normalize_lists(column='dicttest')
        print(df1)
        df2=df.dicttest.ds_normalize_lists(column='dicttest')
        print(df2)

          lkey  value          dicttest
        0  foo      1          [(3, 2)]
        1  bar      2          [(3, 1)]
        2  baz      3  [(3, 2), (3, 3)]
        3  foo      5  [(2, 3), (2, 1)]

        0      [(3, 2), <NA>]
        1      [(3, 1), <NA>]
        2    [(3, 2), (3, 3)]
        3    [(2, 3), (2, 1)]
        Name: dicttest, dtype: object

        0      [(3, 2), <NA>]
        1      [(3, 1), <NA>]
        2    [(3, 2), (3, 3)]
        3    [(2, 3), (2, 1)]
        Name: dicttest, dtype: object

            Parameters:
                df: Union[pd.Series, pd.DataFrame]
                    pd.Series, pd.DataFrame with lists/tuples in cells
                column: Union[str, None]
                    None can only be used if a pd.Series is passed. If a DataFrame is passed, a column needs to be passed too.
            Returns:
                pd.DataFrame
                     Missing values are filled with pd.NA
```

### df.d_merge_multiple_dfs_and_series_on_index() / df.d_merge_multiple_dfs_and_series_on_one_column()

```python
    qq_ds_merge_multiple_dfs_and_series_on_index(df: pandas.core.frame.DataFrame, list_with_ds: list[typing.Union[pandas.core.series.Series, pandas.core.frame.DataFrame]], how='inner', on=None, sort=False, suffixes=('_x', '_y'), indicator=False, validate=None) -> pandas.core.frame.DataFrame
        df1 = pd.DataFrame({'lkeyaaaaaaaaaaaaaaaaaa': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        df2 = pd.DataFrame({'lkeybbbbbbbbbb': ['foo', 'bar', 'baz', 'foo'],
                            'value': [5, 6, 7, 8]})
        df3 = pd.DataFrame({'lkeyccccccccccccccc': ['foo', 'bar', 'baz', 'foo'],
                            'value': [15, 16, 17, 18]})
        df4 = pd.DataFrame({'lkeyddddddddddddd': ['foo', 'bar', 'baz', 'foo'],
                            'value': [115, 116, 117, 118]})
        df5 = pd.DataFrame({'lkeyeeeee': ['foo', 'bar', 'baz', 'foo'],
                            'value': [1115, 1116, 1117, 1118]})
        df1.d_merge_multiple_dfs_and_series_on_index(list_with_ds=[df2,df3,df4,df5], how="outer")
        Out[85]:
          lkeyaaaaaaaaaaaaaaaaaa  value_x_000 lkeybbbbbbbbbb  value_y_000 lkeyccccccccccccccc  value_x_002 lkeyddddddddddddd  value_y_002 lkeyeeeee  value
        0                    foo            1            foo            5                 foo           15               foo          115       foo   1115
        1                    bar            2            bar            6                 bar           16               bar          116       bar   1116
        2                    baz            3            baz            7                 baz           17               baz          117       baz   1117
        3                    foo            5            foo            8                 foo           18               foo          118       foo   1118
            Parameters:
                df : pd.DataFrame
                    DataFrame
                list_with_ds: list[Union[pd.Series, pd.DataFrame]]
                    A list of DataFrames and Series you want to merge
                how: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = "inner"  )
                on: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = None  )
                sort: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = False  )
                suffixes: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = ("_x", "_y"))
                indicator: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = False  )
                validate: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = None  )
            Returns:
                pd.DataFrame
```

```python
    qq_ds_merge_multiple_dfs_and_series_on_column(df: pandas.core.frame.DataFrame, list_with_ds: list[typing.Union[pandas.core.series.Series, pandas.core.frame.DataFrame]], column: str, how='inner', sort=False, suffixes=('_x', '_y'), indicator=False, validate=None) -> pandas.core.frame.DataFrame
        df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        df2 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                            'value': [5, 6, 7, 8]})
        df3 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                            'value': [15, 16, 17, 18]})
        df4 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                            'value': [115, 116, 117, 118]})
        df5 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                            'value': [1115, 1116, 1117, 1118]})
        df1.d_merge_multiple_dfs_and_series_on_one_column(list_with_ds=[df2,df3,df4,df5],column='lkey',    how="outer",
            sort=False,
            suffixes=("_x", "_y"),
            indicator=False,
            validate=None,)

           lkey  value_x_000  value_y_000  value_x_002  value_y_002  value
        0   foo            1            5           15          115   1115
        1   foo            1            5           15          115   1118
        2   foo            1            5           15          118   1115
        3   foo            1            5           15          118   1118
        4   foo            1            5           18          115   1115
        5   foo            1            5           18          115   1118
        6   foo            1            5           18          118   1115
        7   foo            1            5           18          118   1118
        8   foo            1            8           15          115   1115
        9   foo            1            8           15          115   1118
        10  foo            1            8           15          118   1115
        11  foo            1            8           15          118   1118
        12  foo            1            8           18          115   1115
        13  foo            1            8           18          115   1118
        14  foo            1            8           18          118   1115
        15  foo            1            8           18          118   1118
        16  foo            5            5           15          115   1115
        17  foo            5            5           15          115   1118
        18  foo            5            5           15          118   1115
        19  foo            5            5           15          118   1118
        20  foo            5            5           18          115   1115
        21  foo            5            5           18          115   1118
        22  foo            5            5           18          118   1115
        23  foo            5            5           18          118   1118
        24  foo            5            8           15          115   1115
        25  foo            5            8           15          115   1118
        26  foo            5            8           15          118   1115
        27  foo            5            8           15          118   1118
        28  foo            5            8           18          115   1115
        29  foo            5            8           18          115   1118
        30  foo            5            8           18          118   1115
        31  foo            5            8           18          118   1118
        32  bar            2            6           16          116   1116
        33  baz            3            7           17          117   1117
            Parameters:
                df:pd.DataFrame:
                    DataFrame
                list_with_ds:list[Union[pd.Series, pd.DataFrame]]
                    A list of DataFrames and Series you want to merge
                column:str
                    Column to merge on - has to be present in every df
                how: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = "inner"  )
                sort: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = False  )
                suffixes: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = ("_x", "_y"))
                indicator: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = False  )
                validate: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
                    (default = None  )
            Returns:
                pd.DataFrame
```

### df.dicttest.s_as_flattened_list()

```python
    series_as_flattened_list(df) -> list
        df = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                        'value': [1, 2, 3, 5]})
        getdi = lambda x: [    (randrange(1, 4), randrange(1, 4)) for v in range(20)]  #create some random tuples
        df["dicttest"] = df.lkey.apply(lambda x: getdi(x))
        print(df)

        lkey  value                                           dicttest
        0  foo      1  [(3, 2), (3, 3), (3, 1), (1, 2), (2, 1), (3, 2...
        1  bar      2  [(1, 3), (3, 3), (1, 2), (3, 3), (2, 3), (1, 3...
        2  baz      3  [(1, 1), (1, 1), (3, 3), (1, 2), (1, 1), (2, 2...
        3  foo      5  [(2, 1), (2, 1), (1, 3), (1, 3), (3, 2), (2, 1...

        list_=df.dicttest.s_as_flattened_list()
        print(list_[:20])
        [3, 2, 3, 3, 3, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1, 2, 3, 3, 2, 2]
            Parameters:
                df: pd.Series
                    Series to flatten (removes all keys in dicts, only keeps the values)
            Returns:
                list
```

### df1.d_stack() / df1.d_unstack()

```python
    unstacked_df_back_to_multiindex(dataframe: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
            Don't use df.stack()!!!!

        nested = {
        "Moli": {
            "Buy": 75,
            "Sell": 53,
            "Quantity": 300,
            "TF": True},
        "Anna": {
            "Buy": 55,
            "Sell": 83,
            "Quantity": 154,
            "TF": False},
        "Bob": {
            "Buy": 25,
            "Sell": 33,
            "Quantity": 100,
            "TF": False},
        "Annie": {
            "Buy": 74,
            "Sell": 83,
            "Quantity": 96,
            "TF": True}
        }
        df1=pd.Q_AnyNestedIterable_2df(nested, unstack=True)
        print(df1)
        df1.d_stack()
           level_0   level_1        aa_all_keys aa_value
        0     Anna       Buy        (Anna, Buy)       55
        1     Anna  Quantity   (Anna, Quantity)      154
        2     Anna      Sell       (Anna, Sell)       83
        3     Anna        TF         (Anna, TF)    False
        4    Annie       Buy       (Annie, Buy)       74
        5    Annie  Quantity  (Annie, Quantity)       96
        6    Annie      Sell      (Annie, Sell)       83
        7    Annie        TF        (Annie, TF)     True
        8      Bob       Buy         (Bob, Buy)       25
        9      Bob  Quantity    (Bob, Quantity)      100
        10     Bob      Sell        (Bob, Sell)       33
        11     Bob        TF          (Bob, TF)    False
        12    Moli       Buy        (Moli, Buy)       75
        13    Moli  Quantity   (Moli, Quantity)      300
        14    Moli      Sell       (Moli, Sell)       53
        15    Moli        TF         (Moli, TF)     True
        Out[64]:
                                aa_all_keys aa_value
        level_0 level_1
        Anna    Buy             (Anna, Buy)       55
                Quantity   (Anna, Quantity)      154
                Sell           (Anna, Sell)       83
                TF               (Anna, TF)    False
        Annie   Buy            (Annie, Buy)       74
                Quantity  (Annie, Quantity)       96
                Sell          (Annie, Sell)       83
                TF              (Annie, TF)     True
        Bob     Buy              (Bob, Buy)       25
                Quantity    (Bob, Quantity)      100
                Sell            (Bob, Sell)       33
                TF                (Bob, TF)    False
        Moli    Buy             (Moli, Buy)       75
                Quantity   (Moli, Quantity)      300
                Sell           (Moli, Sell)       53
                TF               (Moli, TF)     True

            Parameters:
                dataframe:pd.DataFrame
                    pd.DataFrame
            Returns:
                pd.DataFrame
```

### pd.Q_ReadFileWithAllEncodings_2df()

        There are plenty of good libraries out there that help you with finding the right encoding for your file,
        but sometimes they don't work like expected, and you have to choose the best encoding manually. This method
        opens any file in all encodings available in your env and returns all results in a DataFrame.

```python
        pd.Q_ReadFileWithAllEncodings_2df(r"C:\Users\Gamer\Documents\Downloads\corruptjson1.json")
                        codec                                     strict_encoded  \
        0           ascii  ['ascii' codec can't decode byte 0xef in posit...
        1    base64_codec                                [Incorrect padding]
        2            big5  [({\r\n"doc_id": "some_number",\r\n"url": "www...
        3       big5hkscs  [({\r\n"doc_id": "some_number",\r\n"url": "www...
        4       bz2_codec                              [Invalid data stream]
        ..            ...                                                ...
        115         utf_7  ['utf7' codec can't decode byte 0xef in positi...
        116         utf_8  [({\r\n"doc_id": "some_number",\r\n"url": "www...
        117     utf_8_sig  [({\r\n"doc_id": "some_number",\r\n"url": "www...
        118      uu_codec               [Missing "begin" line in input data]
        119    zlib_codec  [Error -3 while decompressing data: incorrect ...
             strict_bad                                     ignore_encoded  \
        0          True  [({\r\n"doc_id": "some_number",\r\n"url": "www...
        1          True                                                 []



            Parameters:
                filepath (str): file path
            Returns:
                pd.DataFrame
```

### pd.Q_CorruptJsonFile_2dict()

```python
    read_corrupt_json(filepath: str) -> dict
        Usage: pdQ_CorruptJsonFile_2dictf(r'C:\corruptjson1.json')

        If you need to read a corrupted JSON file, you can try this method.
        It will first try to read the file using ujson.
        Second step: The file will be read using all encoders found in your env. Each result will be passed to ast.literal_eval, json.loads and ujson.loads
        Third step: Keys and values are extracted using regex

        All positive results are returned as a dict, you have to check which one fits best to your needs

            finaldict = {
                "ujson_file_reading_result": ujson_file_reading_result,
                "literal_eval_after_newline_removed": literal_eval_after_newline_removed,
                "json_after_head_tail_removed": json_after_head_tail_removed,
                "ujson_after_head_tail_removed": ujson_after_head_tail_removed,
                "regex_get_single_item_keys": allgoodresultsdict,
            }

        If the keys are not double-quoted, it won't work.
        It works well with spaces and not correctly escaped characters

        Example from https://stackoverflow.com/questions/59927549/how-to-fix-a-possibly-corrupted-json-file-problems-with-a-curly-bracket-charact

        {
        "doc_id": "some_number",
        "url": "www.seedurl1.com",
        "scrape_date": "2019-10-22 16:17:22",
        "publish_date": "unknown",
        "author": "unknown",
        "urls_out": [
        "https://www.something.com",
        "https://www.sometingelse.com/smth"
        ],
        "text": "lots of text here"
        }
        ﻿{
        "doc_id": "some_other_number",
        "url": "www.seedurl2.com/smth",
        "scrape_date": "2019-10-22 17:44:40",
        "publish_date": "unknown",
        "author": "unknown",
        "urls_out": [
        "www.anotherurl.com/smth",
        "http://urlx.com/smth.htm"
        ],
        "text": "lots more text over here."
        }

        Result:
        {'ujson_file_reading_result': None,
         'literal_eval_after_newline_removed': Empty DataFrame
         Columns: [level_0, level_1, level_2, aa_all_keys, aa_value, ast_results]
         Index: [],
         'json_after_head_tail_removed':       level_0  ...                                         json_loads
         862  punycode  ...  {'doc_id': 'some_number', 'url': 'www.seedurl1...
         865  punycode  ...  {'doc_id': 'some_number', 'url': 'www.seedurl1...

         [2 rows x 8 columns],
         'ujson_after_head_tail_removed':       level_0  ...                                        ujson_loads
         862  punycode  ...  {'doc_id': 'some_number', 'url': 'www.seedurl1...
         865  punycode  ...  {'doc_id': 'some_number', 'url': 'www.seedurl1...

         [2 rows x 9 columns],
         'regex_get_single_item_keys': [{'aa_value': {0: 'some_number',
            1: 'www.seedurl1.com',
            2: '2019-10-22 16:17:22',
            3: 'unknown',
            4: 'unknown',
            5: ['https://www.something.com', 'https://www.sometingelse.com/smth'],
            6: 'lots of text here'},
           'aa_key': {0: 'doc_id',
            1: 'url',
            2: 'scrape_date',
            3: 'publish_date',
            4: 'author',
            5: 'urls_out',
            6: 'text'}},
          {'aa_value': {7: 'some_other_number',
            8: 'www.seedurl2.com/smth',
            9: '2019-10-22 17:44:40',
            10: 'unknown',
            ........

            Parameters:
                filepath (str): file path
            Returns:
                dict
```

### df.d_sort_columns_with_sorted()

```python
    qq_d_sort_columns_alphabetically(df: pandas.core.frame.DataFrame, reverse: bool = False) -> pandas.core.frame.DataFrame
        Sorts columns alphabetically with sorted()! Not with natsort()!
        df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
        print(df)
        df.d_sort_columns_with_sorted()
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...      ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...      0            211536  13.0000   NaN         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607  23.4500   NaN         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...      0            111369  30.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...      0            370376   7.7500   NaN         Q
        [891 rows x 12 columns]
        Out[66]:
              Age Cabin Embarked     Fare                                               Name  ...  Pclass     Sex  SibSp Survived            Ticket
        0    22.0   NaN        S   7.2500                            Braund, Mr. Owen Harris  ...       3    male      1        0         A/5 21171
        1    38.0   C85        C  71.2833  Cumings, Mrs. John Bradley (Florence Briggs Th...  ...       1  female      1        1          PC 17599
        2    26.0   NaN        S   7.9250                             Heikkinen, Miss. Laina  ...       3  female      0        1  STON/O2. 3101282
        3    35.0  C123        S  53.1000       Futrelle, Mrs. Jacques Heath (Lily May Peel)  ...       1  female      1        1            113803
        4    35.0   NaN        S   8.0500                           Allen, Mr. William Henry  ...       3    male      0        0            373450
        ..    ...   ...      ...      ...                                                ...  ...     ...     ...    ...      ...               ...
        886  27.0   NaN        S  13.0000                              Montvila, Rev. Juozas  ...       2    male      0        0            211536
        887  19.0   B42        S  30.0000                       Graham, Miss. Margaret Edith  ...       1  female      0        1            112053
        888   NaN   NaN        S  23.4500           Johnston, Miss. Catherine Helen "Carrie"  ...       3  female      1        0        W./C. 6607
        889  26.0  C148        C  30.0000                              Behr, Mr. Karl Howell  ...       1    male      0        1            111369
        890  32.0   NaN        Q   7.7500                                Dooley, Mr. Patrick  ...       3    male      0        0            370376
        [891 rows x 12 columns]
            Parameters:
                df : pd.DataFrame
                reverse: bool
                    Z-A instead of A-Z (default = False)

            Returns:
                pd.DataFrame
```

### df.ds_isna()

```python
    is_nan_true_false_check(df: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], include_na_strings: bool = True, include_empty_iters: bool = False, include_0_len_string: bool = False) -> Union[pandas.core.series.Series, pandas.core.frame.DataFrame]
        df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
        df.ds_isna()
        Out[107]:
             PassengerId  Survived  Pclass   Name    Sex  ...  Parch  Ticket   Fare  Cabin  Embarked
        0          False     False   False  False  False  ...  False   False  False   True     False
        1          False     False   False  False  False  ...  False   False  False  False     False
        2          False     False   False  False  False  ...  False   False  False   True     False
        3          False     False   False  False  False  ...  False   False  False  False     False
        4          False     False   False  False  False  ...  False   False  False   True     False
        ..           ...       ...     ...    ...    ...  ...    ...     ...    ...    ...       ...
        886        False     False   False  False  False  ...  False   False  False   True     False
        887        False     False   False  False  False  ...  False   False  False  False     False
        888        False     False   False  False  False  ...  False   False  False   True     False
        889        False     False   False  False  False  ...  False   False  False  False     False
        890        False     False   False  False  False  ...  False   False  False   True     False
        [891 rows x 12 columns]
        df.Cabin.ds_isna()
        Out[108]:
        0       True
        1      False
        2       True
        3      False
        4       True
               ...
        886     True
        887    False
        888     True
        889    False
        890     True
        Name: Cabin, Length: 891, dtype: bool
            Parameters:
                df: Union[pd.Series, pd.DataFrame]
                    pd.Series, pd.DataFrame
                include_na_strings: bool
                    When True -> treated as nan:

                    [
                    "<NA>",
                    "<NAN>",
                    "<nan>",
                    "np.nan",
                    "NoneType",
                    "None",
                    "-1.#IND",
                    "1.#QNAN",
                    "1.#IND",
                    "-1.#QNAN",
                    "#N/A N/A",
                    "#N/A",
                    "N/A",
                    "n/a",
                    "NA",
                    "#NA",
                    "NULL",
                    "null",
                    "NaN",
                    "-NaN",
                    "nan",
                    "-nan",
                    ]

                    (default =True)
                include_empty_iters: bool
                    When True -> [], {} are treated as nan (default = False )

                include_0_len_string: bool
                    When True -> '' is treated as nan (default = False )
                    Returns:
                dict
            Returns:
                Union[pd.Series, pd.DataFrame]
```

### df.d_add_value_to_existing_columns_with_loc()

```python
    df_loc_add(df: pandas.core.frame.DataFrame, condition: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], add_to_colum: Any, column: str, throw_towel_early: bool = False, as_last_chance_convert_to_string: bool = False) -> pandas.core.frame.DataFrame
        df = pd.read_csv(
        "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
        )
        print(df[:6])
        df[:6].d_add_value_to_existing_columns_with_loc(condition=(df.Pclass == 3), add_to_colum=100000, column="Fare")
           PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0            1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1            2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2            3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3            4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4            5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        5            6         0       3                                   Moran, Mr. James    male  ...      0            330877   8.4583   NaN         Q
        [6 rows x 12 columns]
        Out[37]:
           PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket         Fare Cabin  Embarked
        0            1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171  100007.2500   NaN         S
        1            2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599      71.2833   C85         C
        2            3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282  100007.9250   NaN         S
        3            4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803      53.1000  C123         S
        4            5         0       3                           Allen, Mr. William Henry    male  ...      0            373450  100008.0500   NaN         S
        5            6         0       3                                   Moran, Mr. James    male  ...      0            330877  100008.4583   NaN         Q
        [6 rows x 12 columns]
            Parameters:
                df: pd.DataFrame
                    DataFrame to update
                condition: Union[pd.Series, pd.DataFrame]
                    Pass a condition with df.loc: df.loc[df['shield'] > 6]
                add_to_colum:: Any
                    Value that you want to add to old values
                column: str
                    Column which should be updated
                throw_towel_early: bool
                    If False: If there is an exception, will be iterating line by line changing each value.
                    If it fails, it will keep the old value. (default = False)
                as_last_chance_convert_to_string: bool
                    If you want to change the value at any cost, you can change both values to strings and add them up, which will result in:
                    1+1 = "11"
                    "Big" + "Brother" = "BigBrother"
            Returns:
                pd.DataFrame
```

### df.d_drop_rows_with_df_loc()

```python
    df_loc_drop(df: pandas.core.frame.DataFrame, condition: Union[pandas.core.series.Series, pandas.core.frame.DataFrame]) -> pandas.core.frame.DataFrame
        df.d_drop_rows_with_df_loc(df.level_1.str.contains("aa_k")) is the same as df.loc[~df.level_1.str.contains('aa_k')].copy()
        df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
        df
        Out[54]:
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...      ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...      0            211536  13.0000   NaN         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607  23.4500   NaN         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...      0            111369  30.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...      0            370376   7.7500   NaN         Q
        [891 rows x 12 columns]
        df.d_drop_rows_with_df_loc(df.Sex.str.contains(r"male$", regex=True, na=False))
        Out[55]:
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        8              9         1       3  Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)  female  ...      2            347742  11.1333   NaN         S
        9             10         1       2                Nasser, Mrs. Nicholas (Adele Achem)  female  ...      0            237736  30.0708   NaN         C
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...      ...   ...       ...
        880          881         1       2       Shelley, Mrs. William (Imanita Parrish Hall)  female  ...      1            230433  26.0000   NaN         S
        882          883         0       3                       Dahlberg, Miss. Gerda Ulrika  female  ...      0              7552  10.5167   NaN         S
        885          886         0       3               Rice, Mrs. William (Margaret Norton)  female  ...      5            382652  29.1250   NaN         Q
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607  23.4500   NaN         S
        [314 rows x 12 columns]
            Parameters:
                df: pd.DataFrame
                    DataFrame
                condition: Union[pd.Series, pd.DataFrame]
                    Condition with df.loc: df.loc[df['shield'] > 6]
            Returns:
                pd.DataFrame
```

### df.d_set_values_with_df_loc

```python
    df_loc_set(df: pandas.core.frame.DataFrame, condition: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], new_data: Any, column: str) -> pandas.core.frame.DataFrame
        df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")

        df
        Out[51]:
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...      ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...      0            211536  13.0000   NaN         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607  23.4500   NaN         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...      0            111369  30.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...      0            370376   7.7500   NaN         Q
        [891 rows x 12 columns]
        df.d_set_values_with_df_loc(condition = df.Sex.str.contains(r"male$", regex=True, na=False),column = 'Fare',new_data = 100000)
        Out[52]:
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket         Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171  100000.0000   NaN         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599      71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282       7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803      53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...      0            373450  100000.0000   NaN         S
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...          ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...      0            211536  100000.0000   NaN         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053      30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607      23.4500   NaN         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...      0            111369  100000.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...      0            370376  100000.0000   NaN         Q
        [891 rows x 12 columns]


            Parameters:
                df: pd.Dataframe
                    DataFrame
                condition: Union[pd.Series, pd.DataFrame]
                    Pass a condition with df.loc: df.loc[df['shield'] > 6]
                new_data: Any
                    New values for update
                column: str
                    Column which should be updated
            Returns:
                pd.DataFrame
```

### df.d_dfloc()

```python
    df_loc(df: pandas.core.frame.DataFrame, condition: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], column: Optional[str] = None) -> Union[pandas.core.series.Series, pandas.core.frame.DataFrame]
        df.d_dfloc(df.aa_value.str.contains("author")) is the same as df.loc[df.aa_value.str.contains('author')].copy()

        df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
        print(df)
        print(df.d_dfloc(df.Sex.str.contains(r"male$", regex=True, na=False)))
        df.d_dfloc(df.Sex.str.contains(r"male$", regex=True, na=False),column='Name')
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...      ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...      0            211536  13.0000   NaN         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607  23.4500   NaN         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...      0            111369  30.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...      0            370376   7.7500   NaN         Q
        [891 rows x 12 columns]
             PassengerId  Survived  Pclass                            Name   Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3         Braund, Mr. Owen Harris  male  ...      0         A/5 21171   7.2500   NaN         S
        4              5         0       3        Allen, Mr. William Henry  male  ...      0            373450   8.0500   NaN         S
        5              6         0       3                Moran, Mr. James  male  ...      0            330877   8.4583   NaN         Q
        6              7         0       1         McCarthy, Mr. Timothy J  male  ...      0             17463  51.8625   E46         S
        7              8         0       3  Palsson, Master. Gosta Leonard  male  ...      1            349909  21.0750   NaN         S
        ..           ...       ...     ...                             ...   ...  ...    ...               ...      ...   ...       ...
        883          884         0       2   Banfield, Mr. Frederick James  male  ...      0  C.A./SOTON 34068  10.5000   NaN         S
        884          885         0       3          Sutehall, Mr. Henry Jr  male  ...      0   SOTON/OQ 392076   7.0500   NaN         S
        886          887         0       2           Montvila, Rev. Juozas  male  ...      0            211536  13.0000   NaN         S
        889          890         1       1           Behr, Mr. Karl Howell  male  ...      0            111369  30.0000  C148         C
        890          891         0       3             Dooley, Mr. Patrick  male  ...      0            370376   7.7500   NaN         Q
        [577 rows x 12 columns]
        Out[60]:
        0             Braund, Mr. Owen Harris
        4            Allen, Mr. William Henry
        5                    Moran, Mr. James
        6             McCarthy, Mr. Timothy J
        7      Palsson, Master. Gosta Leonard
                            ...
        883     Banfield, Mr. Frederick James
        884            Sutehall, Mr. Henry Jr
        886             Montvila, Rev. Juozas
        889             Behr, Mr. Karl Howell
        890               Dooley, Mr. Patrick
        Name: Name, Length: 577, dtype: object
            Parameters:
                df: pd.DataFrame
                    DataFrame
                condition: Union[pd.Series, pd.DataFrame]
                    Pass a condition with df.loc: df.loc[df['shield'] > 6]
                column: Union[None, str]
                    if a string is passed, the method will return pd.Series
                    None will return the whole DataFrame (default = None )
            Returns:
                Union[pd.Series, pd.DataFrame]
```

### df.df.ds_all_nans_to_pdNA()

```python
    all_nans_in_df_to_pdNA(df: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], include_na_strings: bool = True, include_empty_iters: bool = False, include_0_len_string: bool = False) -> Union[pandas.core.series.Series, pandas.core.frame.DataFrame]
        df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")

        df
        Out[86]:
             PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S
        ..           ...       ...     ...                                                ...     ...  ...    ...               ...      ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...      0            211536  13.0000   NaN         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...      0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...      2        W./C. 6607  23.4500   NaN         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...      0            111369  30.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...      0            370376   7.7500   NaN         Q
        [891 rows x 12 columns]
        df.ds_all_nans_to_pdNA()
        Out[87]:
             PassengerId  Survived  Pclass                                               Name     Sex  ... Parch            Ticket     Fare Cabin  Embarked
        0              1         0       3                            Braund, Mr. Owen Harris    male  ...     0         A/5 21171   7.2500  <NA>         S
        1              2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...     0          PC 17599  71.2833   C85         C
        2              3         1       3                             Heikkinen, Miss. Laina  female  ...     0  STON/O2. 3101282   7.9250  <NA>         S
        3              4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...     0            113803  53.1000  C123         S
        4              5         0       3                           Allen, Mr. William Henry    male  ...     0            373450   8.0500  <NA>         S
        ..           ...       ...     ...                                                ...     ...  ...   ...               ...      ...   ...       ...
        886          887         0       2                              Montvila, Rev. Juozas    male  ...     0            211536  13.0000  <NA>         S
        887          888         1       1                       Graham, Miss. Margaret Edith  female  ...     0            112053  30.0000   B42         S
        888          889         0       3           Johnston, Miss. Catherine Helen "Carrie"  female  ...     2        W./C. 6607  23.4500  <NA>         S
        889          890         1       1                              Behr, Mr. Karl Howell    male  ...     0            111369  30.0000  C148         C
        890          891         0       3                                Dooley, Mr. Patrick    male  ...     0            370376   7.7500  <NA>         Q
        [891 rows x 12 columns]
        df.Cabin.ds_all_nans_to_pdNA()
        Out[88]:
        0      <NA>
        1       C85
        2      <NA>
        3      C123
        4      <NA>
               ...
        886    <NA>
        887     B42
        888    <NA>
        889    C148
        890    <NA>
        Name: Cabin, Length: 891, dtype: object

            Parameters:
                df: Union[pd.Series, pd.DataFrame]
                    pd.Series, pd.DataFrame
                include_na_strings: bool
                    When True -> treated as nan:

                    [
                    "<NA>",
                    "<NAN>",
                    "<nan>",
                    "np.nan",
                    "NoneType",
                    "None",
                    "-1.#IND",
                    "1.#QNAN",
                    "1.#IND",
                    "-1.#QNAN",
                    "#N/A N/A",
                    "#N/A",
                    "N/A",
                    "n/a",
                    "NA",
                    "#NA",
                    "NULL",
                    "null",
                    "NaN",
                    "-NaN",
                    "nan",
                    "-nan",
                    ]

                    (default =True)
                include_empty_iters: bool
                    When True -> [], {} are treated as nan (default = False )

                include_0_len_string: bool
                    When True -> '' is treated as nan (default = False )
                    Returns:
                dict
            Returns:
                Union[pd.Series, pd.DataFrame]
```
