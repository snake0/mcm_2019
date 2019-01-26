import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('Data/MCM_NFLIS_Data.xlsx', sheet_name='Data')


#
# counties = pd.Series(df["FIPS_Combined"]).unique()
# substances = pd.Series(df["SubstanceName"]).unique()
# years = pd.Series(df["YYYY"]).unique()
# states = pd.Series(df["State"]).unique()


def report2():
    # for substance in substances:
    #
    #     for year in years:
    #         # print(year)
    #         for county in counties:
    #             # picking the data we need from specific states, counties, drugs, etc.

    dr = np.array(
        df[(df['FIPS_State'] == 51) & (df['YYYY'] == 2010)]
            .drop_duplicates(subset=['COUNTY'], keep='first', inplace=False)
            .loc[:, 'TotalDrugReportsCounty']
    ).sum()
    print(dr)
    # print(county, ", Drug Reports = ", dr)


# print()


def report1():
    dr = np.array(df[df['FIPS_State'] == 51].drop_duplicates(subset=["COUNTY"]).loc[:, 'COUNTY']).size
    print(dr)
    # for year in years:
    #     for county in counties:
    #         info = np.array(df.loc[(df["FIPS_Combined"] == county) & (df["YYYY"] == year), "TotalDrugReportsCounty"])
    #     # print(county, ", Drug Reports = ", info)


def main():
    # x = np.linspace(0, 10, 200)
    # data_obj = {'x': x,
    #             'y1': 2 * x + 1,
    #             'y2': 3 * x + 1.2,
    #             'mean': 0.5 * x * np.cos(2 * x) + 2.5 * x + 1.1}
    #
    # fig, ax = plt.subplots()
    #
    # ax.fill_between('x', 'y1', 'y2', color='yellow', data=data_obj)
    #
    # # Plot the "centerline" with `plot`
    # ax.plot('x', 'mean', color='black', data=data_obj)
    #
    # plt.show()
    report1()


if __name__ == '__main__':
    main()
