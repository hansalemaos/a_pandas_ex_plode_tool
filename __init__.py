import ast
import json
import math
import operator
from collections import defaultdict
from functools import reduce
from typing import Union, Any

from BruteCodecChecker import CodecChecker
import numpy as np
import pandas as pd
import regex
import ujson
from flatten_any_dict_iterable_or_whatsoever import ProtectedList, fla_tu
from flatten_everything import flatten_everything
#from pandas.core.base import PandasObject
from pandas.core.frame import DataFrame, Series,Index
from copy import deepcopy
from a_pandas_ex_df_to_string import ds_to_string
regexfornanstrings=regex.compile(r'''^(?:\#N(?:/A(?:\ N/A)?|A)|\-(?:1\.\#(?:IND|QNAN)|NaN|nan)|1\.\#(?:IND|QNAN)|<(?:NA(?:N>|>)|nan>)|N(?:/A|ULL|aN|one(?:Type)?|A)|n(?:/a|an|p\.nan|ull)|pd\.NA)$''')



def _to_nested_df(df: pd.DataFrame, groupby: str, subkeys: list) -> dict:
    """

    df = pd.read_csv(    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")


    df[:5]
       PassengerId  Survived  Pclass                                               Name     Sex  ...            Ticket     Fare  Cabin Embarked
    0            1         0       3                            Braund, Mr. Owen Harris    male  ...         A/5 21171   7.2500    NaN        S
    1            2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...          PC 17599  71.2833    C85        C
    2            3         1       3                             Heikkinen, Miss. Laina  female  ...  STON/O2. 3101282   7.9250    NaN        S
    3            4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...            113803  53.1000   C123        S
    4            5         0       3                           Allen, Mr. William Henry    male  ...            373450   8.0500    NaN        S

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

        Parameters:
            df: pd.DataFrame
                DataFrame to convert
            groupby: str
                column whose values will be the top-level keys
            subkeys: list
                columns whose values will be the nested keys
        Returns:
            dict

    """
    nested_dict = lambda: defaultdict(nested_dict)

    def qq_ds_drop_duplicates(
        df, subset=None, keep="first", inplace=False, ignore_index=False
    ):
        df2 = ds_to_string(df)
        df22 = df2.drop_duplicates(
            subset=subset, keep=keep, inplace=inplace, ignore_index=ignore_index
        )

        return df.loc[df22.index].copy()

    def getFromDict(dataDict, mapList):
        # https://stackoverflow.com/a/14692747/15096247
        return reduce(operator.getitem, mapList, dataDict)

    nest = nested_dict()
    useasindex = groupby
    df2 = df.copy()
    use_as_index_var = "__useasindex___"
    subkeys_ = subkeys.copy()
    subkeys_ = [x for x in subkeys_ if x != useasindex]
    subkeys_.append(groupby)
    subkeys_.append(use_as_index_var)
    df2[use_as_index_var] = [useasindex] * len(df2)
    withoutduplicates = qq_ds_drop_duplicates(df2, subset=useasindex)
    alldictkeys = subkeys_.copy()
    asdi = (
        withoutduplicates.groupby(useasindex)[subkeys_]
        .apply(lambda x: x.set_index(use_as_index_var).to_dict(orient="index"))
        .to_dict()
    )
    kick_when_finished = list(asdi.keys())
    successkeys = []
    for key, item in asdi.items():
        for ini, serie in enumerate(alldictkeys):
            if serie == use_as_index_var:
                continue
            ini2 = 0
            for val, val2 in zip(df2[serie].to_list(), df2[useasindex].to_list()):
                tempindi = [val2, serie]
                getFromDict(nest, tempindi)[ini2] = val
                successkeys.append(tempindi.copy())
                ini2 = ini2 + 1
    dictionary_without_ugly_lambda = deepcopy(nest)

    for keys in successkeys:
        allkeys = []
        for tempkey in keys:

            allkeys.append(tempkey)
            value_in_next_key = getFromDict(nest, allkeys)
            is_next_value_dict = isinstance(value_in_next_key, dict)
            if is_next_value_dict:
                getFromDict(dictionary_without_ugly_lambda, allkeys[:-1])[
                    allkeys[-1]
                ] = dict(
                    getFromDict(dictionary_without_ugly_lambda, allkeys[:-1])[
                        allkeys[-1]
                    ]
                )
    dictionary_without_ugly_lambda = dict(dictionary_without_ugly_lambda)
    for kickitem in kick_when_finished:
        del dictionary_without_ugly_lambda[kickitem][useasindex]

    return dictionary_without_ugly_lambda.copy()


def _try_first_with_df_groupby(df: pd.DataFrame, groupby: str, subkeys: list) -> dict:
    """
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
    """
    useasindex = groupby
    df2 = df.copy()
    use_as_index_var = "__useasindex___"
    subkeys_ = subkeys.copy()
    subkeys_ = [x for x in subkeys_ if x != useasindex]
    subkeys_.append(groupby)
    subkeys_.append(use_as_index_var)
    df2[use_as_index_var] = [useasindex] * len(df2)
    asdi = (
        df2.groupby(useasindex)[subkeys_]
        .apply(lambda x: x.set_index(use_as_index_var).to_dict(orient="index"))
        .to_dict()
    )
    updateddict = {}
    for key, item in asdi.items():
        print(key)
        print(item[useasindex])
        updateddict[key] = item[useasindex].copy()
    return updateddict


def _to_dict(df: pd.DataFrame, groupby: str, subkeys: list) -> dict:
    """
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
    """
    try:
        return _try_first_with_df_groupby(df, groupby, subkeys)
    except Exception as Fe:
        return _to_nested_df(df, groupby, subkeys)


def _sort_values_after_converting_to_string(df):
    dfunstacked = _unstack_df(df)
    dfsavecopy = dfunstacked.copy()
    dfsavecopy["subindexXX_"] = list(range(len(dfunstacked)))
    dfsavecopy.index = list(range(len(dfunstacked)))
    sortedlist = sorted(
        [
            (str(x), x, y)
            for y, x in zip(dfsavecopy["subindexXX_"], dfsavecopy["aa_all_keys"])
        ]
    )
    reindexlist = [x[-1] for x in sortedlist]
    dfnew = dfsavecopy.reindex(reindexlist).drop(columns="subindexXX_").copy()

    return dfnew  # .stack_dataframe()


def _delete_duplicates_nested(variable):
    tempdict = {}
    try:
        if isiter(variable):
            for _ in variable:
                try:
                    tempdict[_] = _
                except Exception:
                    tempdict[str(_)] = _
            nomoredupli = [x[1] for x in tempdict.items()]
            return nomoredupli
        else:
            return variable

    except Exception:
        return variable


def delete_duplicates_in_column_full_of_iters(df: pd.Series) -> pd.Series:
    """
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
    """
    df2 = df.copy()
    return df2.map(_delete_duplicates_nested)


def isiter(objectX: Any) -> bool:
    if isinstance(objectX, (np.ndarray, pd.DataFrame, pd.Series)):
        return True
    if isinstance(objectX, (str, bytes)):
        return False
    try:
        some_object_iterator = iter(objectX)
        return True
    except TypeError as te:
        # print(te)
        return False


def _if_not_list_to_list(list_: Any) -> list:
    if not isinstance(list_, list):
        try:
            list_ = list_.tolist()
        except Exception:
            list_ = list(list_)
    return list_


def all_nans_in_df_to_pdNA(
    df: Union[pd.Series, pd.DataFrame],
    include_na_strings: bool = True,
    include_empty_iters: bool = False,
    include_0_len_string: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    """
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
    """
    isseries = isinstance(df, pd.Series)

    df1 = df.copy()
    if isseries:
        df1 = df1.to_frame().copy()
    for col in df1.columns:
        df1[col] = df1[col].apply(
            qq_s_isnan,
            nan_back=True,
            include_na_strings=include_na_strings,
            include_empty_iters=include_empty_iters,
            include_0_len_string=include_0_len_string,
        )
    if isseries:
        return df1[df1.columns[0]]
    return df1


def is_nan_true_false_check(
    df: Union[pd.Series, pd.DataFrame],
    include_na_strings: bool = True,
    include_empty_iters: bool = False,
    include_0_len_string: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    """
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

    """
    isseries = isinstance(df, pd.Series)

    df1 = df.copy()
    if isseries:
        df1 = df1.to_frame().copy()
    for col in df1.columns:
        df1[col] = df1[col].apply(
            qq_s_isnan,
            nan_back=False,
            include_na_strings=include_na_strings,
            include_empty_iters=include_empty_iters,
            include_0_len_string=include_0_len_string,
        )
    if isseries:
        return df1[df1.columns[0]]
    return df1


def qq_s_isnan(
    wert: Any,
    nan_back: bool = False,
    include_na_strings: bool = True,
    include_empty_iters: bool = False,
    include_0_len_string: bool = False,
    debug: bool = False,
) -> Any:
    """
   Parameters
   ----------

    wert: Any
        variable to check
    nan_back: bool
        False: returns True/False
        True: returns pd.NA
        (default = False)
    include_na_strings: bool
        Treated as nan:

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
        [], {} are treated as nan (default = False )


    include_0_len_string: bool
        treats '' as nan (default = False )

    debug: bool
        Print exceptions (default = False )
    """

    if include_empty_iters:
        if isiter(wert):
            try:
                if any(wert) is False:
                    if nan_back is True:
                        return pd.NA
                    return True
            except Exception as Fehler:
                if debug is True:
                    print(Fehler)
            try:
                if np.any(wert) is False:
                    if nan_back is True:
                        return pd.NA
                    return True
            except Exception as Fehler:
                if debug is True:
                    print(Fehler)
            try:
                if len(wert) == 0:
                    if nan_back is True:
                        return pd.NA
                    return True
            except Exception as Fehler:
                if debug is True:
                    print(Fehler)
    try:
        if pd.isna(wert) is True:
            if nan_back is True:
                return pd.NA
            return True
    except Exception as Fehler:
        if debug is True:
            print(Fehler)

    try:
        if pd.isnull(wert) is True:
            if nan_back is True:
                return pd.NA
            return True
    except Exception as Fehler:
        if debug is True:
            print(Fehler)
    # try:
    #     if np.isnan(wert) is True:
    #         if nan_back is True:
    #             return pd.NA
    #         return True
    # except Exception as Fehler:
    #     if debug is True:
    #         print(Fehler)
    try:
        if math.isnan(wert) is True:
            if nan_back is True:
                return pd.NA
            return True
    except Exception as Fehler:
        if debug is True:
            print(Fehler)

    try:
        if wert is None:
            if nan_back is True:
                return pd.NA
            return True
    except Exception as Fehler:
        if debug is True:
            print(Fehler)

    if include_0_len_string:
        try:
            if wert == "":
                if nan_back is True:
                    return pd.NA
                return True
        except Exception as Fehler:
            if debug is True:
                print(Fehler)
    if include_na_strings:
        try:

            nanda = regexfornanstrings.search(str(wert))
            if nanda is not None:
                if nan_back is True:
                    return pd.NA
                return True
        except Exception as Fehler:
            if debug is True:
                print(Fehler)
            return False
    if nan_back is True:
        return wert
    return False


def _exs_normalize_lists_in_series(
    list_: Any, maxlen: int, seriesback: bool = True
) -> Union[list, pd.Series]:
    if qq_s_isnan(list_):
        if seriesback:
            return pd.Series([pd.NA] * maxlen)
        else:
            return [pd.NA] * maxlen

    list_ = _if_not_list_to_list(list_)

    add_lists = (maxlen - len(list_)) * [pd.NA]
    if seriesback:
        return pd.Series(list_ + add_lists, dtype='object')
    return list_ + add_lists


def normalize_lists_in_column_end_user(
    df: Union[pd.Series, pd.DataFrame], column: Union[str, None] = None
) -> pd.Series:
    """
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
    """

    isseries = isinstance(df, pd.Series)
    if isseries:
        df_ = df.to_frame().copy()
        column = df_.columns[0]
    else:
        df_ = df.copy()

    normalized = normalize_lists_in_column(df=df_, column=column, seriesback=False)
    return normalized


def normalize_lists_in_column(
    df: Union[pd.Series, pd.DataFrame],
    column: Union[str, None],
    seriesback: bool = True,
) -> Union[pd.Series, pd.DataFrame]:
    """
    Parameters
    ----------
    df: Union[pd.Series, pd.DataFrame]
        pd.Series, pd.DataFrame with lists in cells
    column: Union[str, None]
        None can only be used if a pd.Series is passed. If a DataFrame is passed, a column needs to be passed too.
    seriesback: bool
        for transforming to df or list
    """
    isseries = isinstance(df, pd.Series)
    df5 = df.copy()
    if isseries:
        df5 = df5.to_frame().copy()
        column = df5.columns[0]
    maxlen = df5[column].dropna().map(lambda x: len(x)).max()
    df5 = df5[column].map(
        lambda x: _exs_normalize_lists_in_series(x, maxlen, seriesback=seriesback)
    )
    if isseries:
        return df5[df5.columns[0]]
    return df5


def explode_lists_and_tuples_in_column(
    df: Union[pd.Series, pd.DataFrame],
    column: Union[str, None] = None,
    concat_with_df: bool = False,
) -> pd.DataFrame:
    """
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

    """
    isseries = isinstance(df, pd.Series)
    if isseries:
        df_ = df.to_frame().copy()
        column = df_.columns[0]
    else:
        df_ = df.copy()
    df5 = normalize_lists_in_column(df_, column)
    df5 = pd.concat(df5.to_list(), axis=1).T
    df5.columns = [f"{column}_{x}" for x in df5.columns]

    if concat_with_df:
        df2 = df_.copy()
        originalindex = df2.index.to_list()
        df2 = df2.reset_index(drop=True)
        df5 = pd.concat([df2, df5], axis=1)
        df5.index = originalindex
    # if isseries:
    #     return df5[df5.columns[0]]
    return df5.copy()


def qq_s_lists_to_df(df: pd.DataFrame, column: str) -> pd.DataFrame:
    maxlen = df[column].dropna().map(lambda x: len(x)).max()
    df5 = df[column].map(
        lambda x: _exs_normalize_lists_in_series(x, maxlen, seriesback=True)
    )
    return pd.concat(df5.to_list(), axis=1).T.copy()


def qq_ds_merge_multiple_dfs_and_series_on_index(
    df: pd.DataFrame,
    list_with_ds: list[Union[pd.Series, pd.DataFrame]],
    how="inner",
    on=None,
    sort=False,
    suffixes=("_x", "_y"),
    indicator=False,
    validate=None,
) -> pd.DataFrame:
    """
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
    """
    # pd.merge in a for-loop
    df2 = df.copy()
    if not isinstance(list_with_ds, list):
        list_with_ds=[list_with_ds]
    for ini, x in enumerate(list_with_ds):
        if isinstance(x, pd.Series):
            x = x.to_frame().copy()
        df2 = (
            pd.merge(
                df2.copy(),
                x.copy(),
                how=how,
                on=on,
                sort=sort,
                indicator=indicator,
                validate=validate,
                left_index=True,
                right_index=True,
                suffixes=(
                    f"{suffixes[0]}_{str(ini).zfill(3)}",  # important to have a format that can be filtered easily
                    f"{suffixes[1]}_{str(ini).zfill(3)}",
                ),
            )
        ).copy()
    return df2


def qq_ds_merge_multiple_dfs_and_series_on_column(
    df: pd.DataFrame,
    list_with_ds: list[Union[pd.Series, pd.DataFrame]],
    column: str,
    how="inner",
    sort=False,
    suffixes=("_x", "_y"),
    indicator=False,
    validate=None,
) -> pd.DataFrame:
    """
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
    """
    # pd.merge in a for-loop (is there a way to do this with pandas directly?)
    df2 = df.copy()
    if not isinstance(list_with_ds, list):
        list_with_ds=[list_with_ds]
    for ini, x in enumerate(list_with_ds):
        if isinstance(x, pd.Series):
            x = x.to_frame().copy()
        df2 = (
            pd.merge(
                df2.copy(),
                x.copy(),
                how=how,
                right_on=column,
                left_on=column,
                sort=sort,
                indicator=indicator,
                validate=validate,
                left_index=False,
                right_index=False,
                suffixes=(
                    f"{suffixes[0]}_{str(ini).zfill(3)}",  # important to have a format that can be filtered easily
                    f"{suffixes[1]}_{str(ini).zfill(3)}",
                ),
            )
        ).copy()  # Copy! Copy! Copy! Maybe not necessary, but changing the original data is a no-go.
    return df2


def qq_d_sort_columns_alphabetically(
    df: pd.DataFrame, reverse: bool = False
) -> pd.DataFrame:
    """
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
    """
    sortedcols = [
        y[1] for y in sorted([(str(x), x) for x in df.columns], key=lambda x: x[0])
    ]
    if reverse:
        sortedcols = list(reversed(sortedcols))
    return df.filter(sortedcols).copy()


def getFromDict(dataDict, mapList):
    # https://stackoverflow.com/a/14692747/15096247
    return reduce(operator.getitem, mapList, dataDict)


def explode_dicts_in_column(
    df: pd.DataFrame, column_to_explode: str, drop_exploded_column: bool = True
) -> pd.DataFrame:
    """

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
    """

    nesti = df.copy()
    allbetter = nesti[column_to_explode].apply(nested_something_to_df)
    alltogetherdf = []
    for ini, goodformatdf in enumerate(allbetter):
        dftoconcat = pd.concat(
            ([nesti.iloc[ini].to_frame()] * len(goodformatdf)), axis=1
        ).T.reset_index(drop=True)
        betterresult = pd.concat([dftoconcat, goodformatdf], axis=1)
        alltogetherdf.append(betterresult)
    done = pd.concat(alltogetherdf, axis=0, ignore_index=True).copy()
    if drop_exploded_column:
        done = done.drop(columns=column_to_explode).copy()
    return done


def d_update_original_iter(
    dataframe: pd.DataFrame, original_iter: Any, verbose: bool = False,
) -> Any:
    """

    from pprint import pprint as pp
    #from: 'https://stackoverflow.com/questions/61984148/how-to-handle-nested-lists-and-dictionaries-in-pandas-dataframe'
    data = {
        "title": "Golf Simulator",
        "genres": ["Sports", "Golf"],
        "score": 85,
        "critic_reviews": [
            {"review_critic": "XYZ", "review_score": 90},
            {"review_critic": "ABC", "review_score": 90},
            {"review_critic": "123", "review_score": 90},
        ],
        "url": "http://example.com/golf-simulator"
    }
    df = pd.Q_AnyNestedIterable_2df(data)  # create DF

    df['updated_value'] = df.aa_value.copy() #new column to update the values
    df.loc[df.updated_value.str.contains("[Gg]olf", na=False), "updated_value"] = "UPDATED11" #updating the values
    mod_iter = df.d_update_original_iter(data, 'updated_value', verbose=True) #now we are updating our input iterable
    pp(mod_iter)



    Parameters
    ----------
    dataframe: pd.DataFrame
        DataFrame, must have the column "aa_all_keys"
    original_iter: Any
        The original iterable that was used to create the DataFrame
    verbose: bool
        Shows results before and after (default =  False)

    How to use:
    Nested dict from: 'https://stackoverflow.com/questions/61984148/how-to-handle-nested-lists-and-dictionaries-in-pandas-dataframe'
    data = {
        "title": "Golf Simulator",
        "genres": ["Sports", "Golf"],
        "score": 85,
        "critic_reviews": [
            {"review_critic": "XYZ", "review_score": 90},
            {"review_critic": "ABC", "review_score": 90},
            {"review_critic": "123", "review_score": 90},
        ],
        "url": "http://example.com/golf-simulator"
    }
    df = pd.Q_AnyNestedIterable_2df(data) #create DF

           level_0  ...                           aa_value
0   critic_reviews  ...                                XYZ
1   critic_reviews  ...                                 90
2   critic_reviews  ...                                ABC
3   critic_reviews  ...                                 90
4   critic_reviews  ...                                123
5   critic_reviews  ...                                 90
6           genres  ...                             Sports
7           genres  ...                               Golf
8            score  ...                                 85
9            title  ...                     Golf Simulator
10             url  ...  http://example.com/golf-simulator

With MultiIndex:
df.d_stack()

level_0        level_1 level_2
critic_reviews 0.0     review_critic  (critic_reviews, 0, review_critic)                                XYZ
                       review_score    (critic_reviews, 0, review_score)                                 90
               1.0     review_critic  (critic_reviews, 1, review_critic)                                ABC
                       review_score    (critic_reviews, 1, review_score)                                 90
               2.0     review_critic  (critic_reviews, 2, review_critic)                                123
                       review_score    (critic_reviews, 2, review_score)                                 90
genres         NaN     NaN                                     (genres,)                             Sports
                       NaN                                     (genres,)                               Golf
score          NaN     NaN                                      (score,)                                 85
title          NaN     NaN                                      (title,)                     Golf Simulator
url            NaN     NaN                                        (url,)  http://example.com/golf-simulator

Let's update the values:
    df['updated_value'] = df.aa_value.copy() #new column
    df.loc[df.updated_value.str.contains("[Gg]olf", na=False), "updated_value"] = "UPDATED11" #let's update the values

                                                             aa_all_keys  ... updated_value
level_0        level_1 level_2                                            ...
critic_reviews 0.0     review_critic  (critic_reviews, 0, review_critic)  ...           XYZ
                       review_score    (critic_reviews, 0, review_score)  ...            90
               1.0     review_critic  (critic_reviews, 1, review_critic)  ...           ABC
                       review_score    (critic_reviews, 1, review_score)  ...            90
               2.0     review_critic  (critic_reviews, 2, review_critic)  ...           123
                       review_score    (critic_reviews, 2, review_score)  ...            90
genres         NaN     NaN                                     (genres,)  ...        Sports
                       NaN                                     (genres,)  ...     UPDATED11
score          NaN     NaN                                      (score,)  ...            85
title          NaN     NaN                                      (title,)  ...     UPDATED11
url            NaN     NaN                                        (url,)  ...     UPDATED11
[11 rows x 3 columns]

Let's update the original iterable:

mod_iter = df.d_update_original_iter(data, 'updated_value', verbose=True) #now we are updating our input iterable (actually we get an updated copy of it)

{'title': 'UPDATED11',
 'genres': ['Sports', 'UPDATED11'],
 'score': 85,
 'critic_reviews': [{'review_critic': 'XYZ', 'review_score': 90},
  {'review_critic': 'ABC', 'review_score': 90},
  {'review_critic': '123', 'review_score': 90}],
 'url': 'UPDATED11'}

If the value is a tuple, it will be replaced by a list:
 ('Sports', 'Golf') -> ['Sports', 'UPDATED11']
    """
    data = deepcopy(original_iter)
    updatedcolumn = "aa_value"
    df = _unstack_df(dataframe)

    for name, group in df.groupby("aa_all_keys"):
        if len(group[updatedcolumn]) > 1:
            transformed = group.T.loc[updatedcolumn].to_frame().T
            keys = name
            new_value = make_several_columns_fit_in_one(
                transformed, transformed.columns
            )[0]
        else:
            keys = name
            new_value = group[updatedcolumn].item()
        keysasstring = ""
        oldvalue = ""
        if verbose:
            keysasstring = str(
                "[" + "][".join(list([str(x) for x in keys])) + "]"
            ).ljust(60)
            oldvalue = getFromDict(data, keys)
        setInDict(data, keys, new_value)
        if verbose:
            if str(oldvalue) != str(getFromDict(data, keys)):
                print(f"{keysasstring} Old value: {oldvalue}")
                print(f"{keysasstring} Updated value: {getFromDict(data, keys)}\n")
    return data


def _unstack_df(df: pd.DataFrame) -> pd.DataFrame:
    """
        Don't use df.unstack()!!!!

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
    df1=pd.Q_AnyNestedIterable_2df(nested, unstack=False)
    print(df1)
    df1.d_unstack()
                          aa_all_keys aa_value
    Anna  Buy             (Anna, Buy)       55
          Quantity   (Anna, Quantity)      154
          Sell           (Anna, Sell)       83
          TF               (Anna, TF)    False
    Annie Buy            (Annie, Buy)       74
          Quantity  (Annie, Quantity)       96
          Sell          (Annie, Sell)       83
          TF              (Annie, TF)     True
    Bob   Buy              (Bob, Buy)       25
          Quantity    (Bob, Quantity)      100
          Sell            (Bob, Sell)       33
          TF                (Bob, TF)    False
    Moli  Buy             (Moli, Buy)       75
          Quantity   (Moli, Quantity)      300
          Sell           (Moli, Sell)       53
          TF               (Moli, TF)     True
    Out[63]:
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
        Parameters:
            df:pd.DataFrame
                pd.DataFrame
        Returns:
            pd.DataFrame

    """
    if df.shape[1] != 2:
        return df
    return df.reset_index(drop=False).copy()  # copying might not be necessary


def unstacked_df_back_to_multiindex(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
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

    """
    if dataframe.shape[1] == 2:
        return dataframe
    dfup = dataframe.copy()
    # keys in  dataframe.columns always start with "level_ https://github.com/pandas-dev/pandas/issues/22260"
    multiindexcols = [x for x in dfup.columns if str(x).startswith("level_")]
    # https://pandas.pydata.org/docs/user_guide/advanced.html
    restoremultiindex = list(
        zip(*([dfup[x] for x in multiindexcols]))
    )  # create a list of tuples for multi index [(key1, key2, key3), (key1, key2, key3)]
    index = pd.MultiIndex.from_tuples(restoremultiindex, names=multiindexcols)
    return (
        dfup.set_index(index).drop(columns=multiindexcols).copy()
    )  # copying might not be necessary, but no way I want to change the original data


def setInDict(dataDict, mapList, value):
    """
    Update dict
    """
    # https://stackoverflow.com/a/14692747/15096247
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


def nested_something_to_df(nested_whatever: Any, unstack: bool = True,) -> pd.DataFrame:
    """
    This code should handle any iterable, no matter how deep it is nested.
    You can convert the iterable in a stacked DataFrame or an unstacked DataFrame.
    It's not relevant to decide here because you can convert unstacked to stacked or stacked to
    unstacked any time you want by using df.d_stack() or df.d_unstack() respectively:

    unstacked_dataframe = pd.Q_AnyNestedIterable_2df(
    nested_iter, unstack=True
    )

    No matter if stacked or unstacked, there always will be the 2 columns: ['aa_all_keys', 'aa_value']
    Those are the most important ones.
    With 'aa_all_keys', you can update the values of the original iterable
    You can use pandas to update the values of your original iterable in 'aa_value'

    Examples

    https://stackoverflow.com/questions/72745879/nested-dictionaries-grab-top-level-keys-where-specified-field-in-sub-dictionar
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
    pd.Q_AnyNestedIterable_2df(nested,unstack=False)
    Out[18]:
                          aa_all_keys aa_value
    Moli  Buy             (Moli, Buy)       75
          Sell           (Moli, Sell)       53
          Quantity   (Moli, Quantity)      300
          TF               (Moli, TF)     True
    Anna  Buy             (Anna, Buy)       55
          Sell           (Anna, Sell)       83
          Quantity   (Anna, Quantity)      154
          TF               (Anna, TF)    False
    Bob   Buy              (Bob, Buy)       25
          Sell            (Bob, Sell)       33
          Quantity    (Bob, Quantity)      100
          TF                (Bob, TF)    False
    Annie Buy            (Annie, Buy)       74
          Sell          (Annie, Sell)       83
          Quantity  (Annie, Quantity)       96
          TF              (Annie, TF)     True

    pd.Q_AnyNestedIterable_2df(nested,unstack=True)
    Out[19]:
       level_0   level_1        aa_all_keys aa_value
    0     Moli       Buy        (Moli, Buy)       75
    1     Moli      Sell       (Moli, Sell)       53
    2     Moli  Quantity   (Moli, Quantity)      300
    3     Moli        TF         (Moli, TF)     True
    4     Anna       Buy        (Anna, Buy)       55
    5     Anna      Sell       (Anna, Sell)       83
    6     Anna  Quantity   (Anna, Quantity)      154
    7     Anna        TF         (Anna, TF)    False
    8      Bob       Buy         (Bob, Buy)       25
    9      Bob      Sell        (Bob, Sell)       33
    10     Bob  Quantity    (Bob, Quantity)      100
    11     Bob        TF          (Bob, TF)    False
    12   Annie       Buy       (Annie, Buy)       74
    13   Annie      Sell      (Annie, Sell)       83
    14   Annie  Quantity  (Annie, Quantity)       96
    15   Annie        TF        (Annie, TF)     True

    Use pandas to change the values:

    df.loc[df.aa_value == True]
       level_0 level_1  aa_all_keys aa_value
    3     Moli      TF   (Moli, TF)     True
    15   Annie      TF  (Annie, TF)     True

    df.loc[df.aa_value == True, 'aa_value'] = False

    df.loc[df.aa_value == False]

       level_0 level_1  aa_all_keys aa_value
    3     Moli      TF   (Moli, TF)    False
    7     Anna      TF   (Anna, TF)    False
    11     Bob      TF    (Bob, TF)    False
    15   Annie      TF  (Annie, TF)    False


    nested_updated=df.d_update_original_iter(nested, 'aa_value', verbose=True)
    Works like a charm :)

    {'Moli': {'Buy': 75, 'Sell': 53, 'Quantity': 300, 'TF': False},
     'Anna': {'Buy': 55, 'Sell': 83, 'Quantity': 154, 'TF': False},
     'Bob': {'Buy': 25, 'Sell': 33, 'Quantity': 100, 'TF': False},
     'Annie': {'Buy': 74, 'Sell': 83, 'Quantity': 96, 'TF': False}}


    Tuples as values will be converted to lists:

    'key': (True,False) -> 'key': [True, False]


    More examples:

        stackoverflowlink = '''https://stackoverflow.com/questions/72990265/convert-nested-list-in-dictionary-to-dataframe/72990346'''
        data = {'a': 'test',
                'b': 1657,
                'c': 'asset',
                'd': [['2089', '0.0'], ['2088', '0.0']],
                'e': [['2088', '0.0'], ['2088', '0.0'], ['2088', '0.00']],
                'f': [['2088', '0.0', "x", "foo"], ['2088', '0.0', 'bar', "i"], ['2088', '0.00', "z", "0.2"]],
                "x": ["test1", "test2"]}
        pd.Q_AnyNestedIterable_2df(data, unstack=False)
        Out[8]:
              aa_all_keys aa_value
        a NaN        (a,)     test
        b NaN        (b,)     1657
        c NaN        (c,)    asset
        d 0        (d, 0)     2089
          0        (d, 0)      0.0
          1        (d, 1)     2088
          1        (d, 1)      0.0
        e 0        (e, 0)     2088
          0        (e, 0)      0.0
          1        (e, 1)     2088
          1        (e, 1)      0.0
          2        (e, 2)     2088
          2        (e, 2)     0.00
        f 0        (f, 0)      foo
        .....

        stackoverflowlink = "https://stackoverflow.com/questions/73430585/how-to-convert-a-list-of-nested-dictionaries-includes-tuples-as-a-dataframe"
        data = [{'cb': ({'Name': 'A', 'ID': 1, 'num': 50},
           {'Name': 'A', 'ID': 2, 'num': 68}),
          'final_value': 118},
         {'cb': ({'Name': 'A', 'ID': 1, 'num': 50},
           {'Name': 'A', 'ID': 4, 'num': 67}),
          'final_value': 117},
         {'cb': ({'Name': 'A', 'ID': 1, 'num': 50},
           {'Name': 'A', 'ID': 6, 'num': 67}),
          'final_value': 117}]
        pd.Q_AnyNestedIterable_2df(data, unstack=False)
        Out[9]:
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


        stackoverflowlink = "https://stackoverflow.com/questions/69943509/problems-when-flatten-a-dict"
        data = [{'id':'1',
        'application_details':{'phone':None, 'email':None},
        'employer': {'Name':'Nom', 'email':None},
        'application_contacts': [{'email':'test@test.com', 'adress':'X'}]},
        {'id':'2',
        'application_details':{'phone':None, 'email':'testy@test_a.com'},
        'employer': {'Name':'Nom', 'email': None},
        'application_contacts': [{'email': None, 'adress':'Z'}]},
        {'id':'3',
        'application_details':{'phone':None, 'email':'testy@test_a.com'},
        'employer': {'Name':'Nom', 'email': None},
        'application_contacts': [{'email': None, 'adress':'Y'}]}]
        pd.Q_AnyNestedIterable_2df(data, unstack=False)
        Out[11]:
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



        Parameters:
            nested_whatever:Any
                Any nested iterable (list, tuple, DataFrame, dict, Series ...)
            unstack:bool
                stack or unstacked - can be changed later by using df.d_stack() or df.d_unstack() respectivly (default=True)
        Returns:
            pd.DataFrame




    """
    #no more warning when having dicts with 1486 subdicts : https://github.com/hansalemaos/a_pandas_ex_plode_tool/blob/main/recursion%20_hardcore_test.py
    flattenddict =  fla_tu(nested_whatever)  # flatten every iterable
    # from pprint import pprint as pp
    # pp(flattenddict)
    # depending on the iterable, we have to convert it to a list and get the first (and only) tuple (which always has the same length -> 2 - value and keys[s])

    # flattenddict = [
    #     list(x)[0] if "generator" in str(type(x)) else x for x in flattenddict
    # ]
    # now we have a dataframe, but all keys from our iterable are in one column

    df = pd.DataFrame(flattenddict)
    df.columns = [
        "aa_value",
        "aa_all_keys",
    ]
    indexdf = qq_s_lists_to_df(
        df, "aa_all_keys"
    )  # We need to explode the column aa_all_keys
    # enumerate columns, to distinguish better.
    indexdf.columns = [f"aa_key_{x}" for x in indexdf.columns]
    # merge the exploded columns with the 2=colum dataframe! we need the data twice! 1x for the index right now, and
    # the second one 'aa_all_keys' later to transform the df stacked->unstacked / unstacked->stacked
    # and to update the original iter
    df = qq_ds_merge_multiple_dfs_and_series_on_index(df, [indexdf])

    # merge the exploded columns with the 2=columns DataFrame! We need the data twice! 1x for the index right now, and
    # the second one 'aa_all_keys' later to transform the DataFrame stacked->unstacked / unstacked->stacked
    # and to update the original iterable -> d_update_original_iter
    df.index = [df[f"aa_key_{x}"].__array__() for x in range(len(df.columns) - 2)]

    # Very important, we need to make sure to put the keys of the nested iter in the right order
    df = qq_d_sort_columns_alphabetically(df)

    try:

        df = df.sort_values("aa_all_keys")

    except Exception:
        # To avoid exceptions like: TypeError: '<' not supported between instances of 'int' and 'str'

        df["TEMMMMMMMMMMMP"] = df.aa_all_keys.astype("string")
        df = df.sort_values(by="TEMMMMMMMMMMMP").drop(columns=["TEMMMMMMMMMMMP"]).copy()

    # We can now drop the columns because the key-data is now present in the index
    df = df.drop(columns=[x for x in df.columns if x.startswith("aa_key_")])

    # At this point there are only 2 columns -> (["aa_value", "aa_all_keys"] )
    # It might not be necessary to copy the DataFrame here, but no way I want to change the original data
    if unstack:
        # df = adjust_dataframe_and_dtypes(df, nested_whatever)
        # One column for each key (key1, key2...), one for the value[s] ("aa_value") and one for all keys as tuple ("aa_all_keys")
        return df.reset_index().copy()
    # The 2 columns version
    return df.copy()


def df_loc(
    df: pd.DataFrame,
    condition: Union[pd.Series, pd.DataFrame],
    column: Union[None, str] = None,
) -> Union[pd.Series, pd.DataFrame]:
    """
    df.d_dfloc(df.aa_value.str.contains("author")) is the same as df.loc[df.aa_value.str.contains('author')].copy()

    df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
    print(df)
    print(df.d_dfloc(df.Sex.str.contains(r"^\bmale\b$", regex=True, na=False)))
    df.d_dfloc(df.Sex.str.contains(r"^\bmale\b$", regex=True, na=False),column='Name')
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
    """
    if column is not None:
        return df.loc[condition, column].copy()
    else:
        return df.loc[condition].copy()


def df_loc_drop(
    df: pd.DataFrame, condition: Union[pd.Series, pd.DataFrame]
) -> pd.DataFrame:
    """
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
    df.d_drop_rows_with_df_loc(df.Sex.str.contains(r"^\bmale\b$", regex=True, na=False))
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
    """
    df5 = df_loc(df=df, condition=condition, column=None)
    df_index_to_drop = df5.index
    return df.drop(df_index_to_drop).copy()


def df_loc_set(
    df: pd.DataFrame,
    condition: Union[pd.Series, pd.DataFrame],
    new_data: Any,
    column: str,
) -> pd.DataFrame:
    """
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
    df.d_set_values_with_df_loc(condition = df.Sex.str.contains(r"^\bmale\b$", regex=True, na=False),column = 'Fare',new_data = 100000)
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
    """
    df5 = df_loc(df=df, condition=condition, column=column)
    df_indextouse = df5.index
    df_ = df.copy()
    df_.loc[df_indextouse, column] = new_data
    return df_.copy()


def read_textfile_with_all_encoding_to_df(filepath: str) -> pd.DataFrame:
    r"""
    There are plenty of good libraries out there that help you with finding the right encoding for your file,
    but sometimes they don't work like expected, and you have to choose the best encoding manually. This method
    opens any file in all encodings available in your env and returns all results in a DataFrame.


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
    """
    with open(filepath, mode="rb") as f:
        data = f.read()

    codch = CodecChecker()
    codch.try_convert_bytes(data)
    allmyresults = codch.results.copy()
    df = pd.DataFrame.from_records(
        [{"codec": x[0]} | x[1] for x in allmyresults.items()]
    )
    return df


def df_loc_add(
    df: pd.DataFrame,
    condition: Union[pd.Series, pd.DataFrame],
    add_to_colum: Any,
    column: str,
    throw_towel_early: bool = False,
    as_last_chance_convert_to_string: bool = False,
) -> pd.DataFrame:
    """
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
    """
    df5 = df_loc(df=df, condition=condition, column=column)
    df_index_to_drop = df5.index
    dont_give_up_results = []
    if throw_towel_early:
        df7 = df5 + add_to_colum
        finalresults = df7.to_list()
    else:
        try:
            df7 = df5 + add_to_colum
            finalresults = df7.to_list()
        except Exception:
            for value in df5:
                try:
                    newval = value + add_to_colum
                    dont_give_up_results.append(newval)
                except Exception:
                    if as_last_chance_convert_to_string:
                        newval = str(value) + str(add_to_colum)
                        dont_give_up_results.append(newval)
                    else:
                        dont_give_up_results.append(pd.NA)
            finalresults = dont_give_up_results.copy()

    df_ = df.copy()
    df_.loc[df_index_to_drop, column] = finalresults
    return df_.copy()


def flatten_all_iters_in_cells(df: pd.Series) -> pd.Series:
    """
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
    """
    df2 = df.map(lambda x: np.fromiter(flatten_everything(x), dtype="object")).copy()
    return df2


def series_as_flattened_list(df) -> list:
    """
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
    """
    return list(flatten_everything(df))


def make_several_columns_fit_in_one(df: pd.DataFrame, columns: list) -> list:
    """
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

    """
    aslistwithindex = [x for x in np.array(df[columns].to_records())]
    return [list(x)[1:] for x in aslistwithindex]


def get_dtype(variable, wanted_types):
    return isinstance(variable, wanted_types)


def df_loc_dtypes(
    df: pd.DataFrame,
    allowed_dtypes: Any = (int, float),
    fillvalue: Any = pd.NA,
    column: str = "aa_value",
) -> pd.Series:
    """
    If you are working with nested iterables, you often have to lead with different data types.
    Since df = pd.Q_AnyNestedIterable_2df(data,unstack=False) always creates only 2 columns: ['aa_all_keys' , 'aa_value']
    That means that we have quite frequently different data types in the column 'aa_value'
    This method helps to filter out only the data types that you want to work with.
    That way, there will be no exceptions because of wrong data types!

    Check out the example

    stackoverflowlink = "https://stackoverflow.com/questions/73430585/how-to-convert-a-list-of-nested-dictionaries-includes-tuples-as-a-dataframe"
    data = [{'cb': ({'Name': 'A', 'ID': 1, 'num': 50},
       {'Name': 'A', 'ID': 2, 'num': 68}),
      'final_value': 118},
     {'cb': ({'Name': 'A', 'ID': 1, 'num': 50},
       {'Name': 'A', 'ID': 4, 'num': 67}),
      'final_value': 117},
     {'cb': ({'Name': 'A', 'ID': 1, 'num': 50},
       {'Name': 'A', 'ID': 6, 'num': 67}),
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

    df.loc[df.aa_value >30,'aa_value'] = 90000000

    Traceback (most recent call last):
    ....
    TypeError: '>' not supported between instances of 'str' and 'int'  <------------------- Here is the problem!

    df.loc[df.d_filter_dtypes(allowed_dtypes=(int,float),fillvalue=pd.NA,column='aa_value') > 30] <------- No more exception!

                                aa_all_keys aa_value
    0 cb          0   num   (0, cb, 0, num)       50
                  1   num   (0, cb, 1, num)       68
      final_value NaN NaN  (0, final_value)      118
    1 cb          0   num   (1, cb, 0, num)       50
                  1   num   (1, cb, 1, num)       67
      final_value NaN NaN  (1, final_value)      117
    2 cb          0   num   (2, cb, 0, num)       50
                  1   num   (2, cb, 1, num)       67
      final_value NaN NaN  (2, final_value)      117


    df.d_filter_dtypes(allowed_dtypes=(int,float),fillvalue=pd.NA,column='aa_value') > 30, 'aa_value'] = 900000  #No we can update the column
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

        Parameters:
            df:pd.DataFrame
            allowed_dtypes:Any
                (default = (int,float))
            fillvalue:Any
                (default = pd.NA)
            column:str
                (default = 'aa_value')
        Returns:
            pd.Series


    """
    dfn = df.copy()
    dfn.loc[
        ~(
            dfn[column].apply(lambda variable: get_dtype(variable, allowed_dtypes))
            == True
        ),
        column,
    ] = fillvalue
    return dfn.copy()[column]


def read_corrupt_json(filepath: str) -> dict:
    r"""
    Usage: pd.Q_CorruptJsonFile_2dict(r'C:\corruptjson1.json')

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

    """
    filename = filepath

    def apply_literal_eval_(x):
        try:
            return ast.literal_eval(x)
        except Exception:
            return x

    def apply_literal_eval(variable):
        try:
            return ast.literal_eval(variable)
        except Exception:
            return pd.NA

    def apply_jsonloads(variable):
        try:
            return json.loads(variable)
        except Exception:
            return pd.NA

    def apply_ujsonloads(variable):
        try:
            return ujson.loads(variable)
        except Exception:
            return pd.NA

    ujson_file_reading_result = None
    try:
        ujson_file_reading_result = ujson.load(filename)
    except Exception:
        pass

    with open(filename, mode="rb") as f:
        data = f.read()
    codch = CodecChecker()

    codch.try_convert_bytes(data)
    allmyresults = codch.results.copy()

    df = nested_something_to_df(allmyresults, True)
    df.aa_value = df.aa_value.str.replace("\n", "", regex=False).str.replace(
        "\r", "", regex=False
    )
    df.aa_value = df.aa_value.fillna("")

    df["ast_results"] = df.aa_value.apply(apply_literal_eval)
    literal_eval_after_newline_removed = df.loc[~df.ast_results.isna()].copy()
    df["regex_search"] = df.aa_value.str.extract(r"(\{.*})")

    df["json_loads"] = df.regex_search.apply(apply_jsonloads)
    json_after_head_tail_removed = df.loc[~df.json_loads.isna()].copy()
    df["ujson_loads"] = df.regex_search.apply(apply_ujsonloads)
    ujson_after_head_tail_removed = df.loc[~df.ujson_loads.isna()].copy()
    ujson_results = []
    regexsplit_1 = regex.compile(r"(\}\s*,?\s*\{)")
    regexsearch1 = regex.compile(r"^[\{\},\s]+$")
    for _ in list(
        flatten_everything(
            df.regex_search.dropna().apply(lambda x: regexsplit_1.split(x))
        )
    ):
        if not _.startswith("{"):
            _ = "{" + _
        if not _.endswith("}"):
            _ = _ + "}"
        if regexsearch1.search(_) is None:
            try:
                loaded = ujson.loads(_)
                ujson_results.append(loaded)
            except Exception:
                pass
    regex_results = []
    splitregex_ = regex.compile(r"(\}\s*,?\s*\{)")
    splitregex = regex.compile(r'((?:[\{"\s,]*)[^"]+":\s*)')
    regex_firstsearch = regex.compile(r"^[\{\},\s]+$")
    regex_sep = regex.compile(r"\s*:\s*$")

    for ini0, _ in enumerate(
        list(
            flatten_everything(
                df.regex_search.dropna().apply(lambda x: splitregex_.split(x))
            )
        )
    ):
        if not _.startswith("{"):
            _ = "{" + _
        if not _.endswith("}"):
            _ = _ + "}"
        nestedresults = []
        if regex_firstsearch.search(_) is None:
            try:
                regexresu = splitregex.split(_)
                arrangenestedresults_keys_together = []
                arrangenestedresults_values_together = []
                for ini, rege in enumerate(regexresu):
                    if ini == 0:
                        if rege == "":
                            continue
                    if regex_sep.search(rege) is not None:

                        arrangenestedresults_keys_together.append(
                            (True, ini0, rege, ini)
                        )

                        continue
                    else:

                        arrangenestedresults_values_together.append(
                            (False, ini0, rege, ini)
                        )

                zipped = ProtectedList(
                    list(
                        zip(
                            arrangenestedresults_keys_together,
                            arrangenestedresults_values_together,
                        )
                    )
                )

                nestedresults.append(zipped.copy())
            except Exception:
                pass
        regex_results.append(nestedresults)

    df = nested_something_to_df(regex_results)
    df = unstacked_df_back_to_multiindex(df)
    df = _unstack_df(df)

    allmyresults = []
    for name, group in df.aa_value.groupby([df.level_0, df.level_1, df.level_2]):
        allmyresults.append((name[0], name[2], group.iloc[2], group.iloc[6]))
    df = pd.DataFrame(allmyresults)
    df.columns = ["aa_try", "aa_item", "aa_key", "aa_value"]
    df.aa_key = df.aa_key.str.strip(r':{," ')
    df.aa_value = df.aa_value.str.strip(r':{," }')

    df.aa_value.str.replace(r'"?\s*\}.{0,2}$', "", regex=True)
    df.aa_value = df.aa_value.apply(apply_literal_eval_)
    allgoodresultsdf = _to_nested_df(
        df, groupby="aa_try", subkeys=["aa_try", "aa_value", "aa_key"],
    )
    allgoodresultsdict = _delete_duplicates_nested(
        [x[1] for x in allgoodresultsdf.items()]
    )
    finaldict = {
        "ujson_file_reading_result": ujson_file_reading_result,
        "literal_eval_after_newline_removed": literal_eval_after_newline_removed,
        "json_after_head_tail_removed": json_after_head_tail_removed,
        "ujson_after_head_tail_removed": ujson_after_head_tail_removed,
        "regex_get_single_item_keys": allgoodresultsdict,
    }
    return finaldict


def pd_add_explode_tools():
    pd.Q_CorruptJsonFile_2dict = read_corrupt_json
    pd.Q_ReadFileWithAllEncodings_2df = read_textfile_with_all_encoding_to_df
    pd.Q_AnyNestedIterable_2df = nested_something_to_df
    DataFrame.d_filter_dtypes = df_loc_dtypes
    DataFrame.d_multiple_columns_to_one = make_several_columns_fit_in_one
    DataFrame.d_df_to_nested_dict = _to_nested_df
    DataFrame.d_add_value_to_existing_columns_with_loc = df_loc_add
    DataFrame.d_set_values_with_df_loc = df_loc_set
    DataFrame.d_drop_rows_with_df_loc = df_loc_drop
    DataFrame.d_dfloc = df_loc
    DataFrame.d_stack = unstacked_df_back_to_multiindex
    DataFrame.d_unstack = _unstack_df
    DataFrame.d_sort_columns_with_sorted = qq_d_sort_columns_alphabetically
    DataFrame.d_merge_multiple_dfs_and_series_on_one_column = (
        qq_ds_merge_multiple_dfs_and_series_on_column
    )
    DataFrame.d_merge_multiple_dfs_and_series_on_index = (
        qq_ds_merge_multiple_dfs_and_series_on_index
    )
    DataFrame.ds_all_nans_to_pdNA = all_nans_in_df_to_pdNA
    DataFrame.ds_explode_dicts_in_column = explode_dicts_in_column
    DataFrame.ds_isna = is_nan_true_false_check
    Series.ds_all_nans_to_pdNA = all_nans_in_df_to_pdNA
    Series.ds_explode_dicts_in_column = explode_dicts_in_column
    Series.ds_isna = is_nan_true_false_check

    Series.s_delete_duplicates_from_iters_in_cells = (
        delete_duplicates_in_column_full_of_iters
    )
    Series.s_flatten_all_iters_in_cells = flatten_all_iters_in_cells
    Series.s_as_flattened_list = series_as_flattened_list
    Series.s_explode_lists_and_tuples = explode_lists_and_tuples_in_column
    DataFrame.ds_normalize_lists = normalize_lists_in_column_end_user
    Series.ds_normalize_lists = normalize_lists_in_column_end_user

    DataFrame.d_update_original_iter = d_update_original_iter
