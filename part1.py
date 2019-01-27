import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('Data/MCM_NFLIS_Data.xlsx', sheet_name='Data')

counties = pd.Series(df["FIPS_Combined"]).unique()
substances = pd.Series(df["SubstanceName"]).unique()
years = pd.Series(df["YYYY"]).unique()
states = pd.Series(df["State"]).unique()

def drug_in_state(state, substance_name):
    ret = []
    for year in years:
        dr = df[(df['SubstanceName'] == substance_name)
                & (df['YYYY'] == year)
                & (df['State'] == state)
                ].loc[:, 'DrugReports']
        ret.append(np.array(dr).sum())
    return ret


def drug_in_county_percent(county, substance_name, amount):
    ret = []
    for year in years:
        m = np.array(df[(df['SubstanceName'] == substance_name)
                        & (df['COUNTY'] == county)
                        & (df['YYYY'] == year)].loc[:, 'DrugReports'])
        if amount[year - 2010] == 0 or m.size == 0:
            ret.append(0)
        else:
            ret.append(m[0] / amount[year - 2010])
    return ret


def get_counties(state):
    return pd.Series(df[df['State'] == state].loc[:, 'COUNTY']).unique()


def show_percentage(state, substance_name, k):
    ret = {}
    cs = get_counties(state)
    amount = drug_in_state(state, substance_name)
    i = 0
    for county in cs:
        i = i + 1
        percent = drug_in_county_percent(county, substance_name, amount)
        plt.subplot(1, 5, k)
        plt.plot(years, percent,
                 label=str(county),
                 linestyle='-.',
                 marker='s',
                 linewidth=1.5)
        if i > 5:
            break
    plt.grid(ls='--')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel(substance_name + ' in ' + state)
    plt.ylim((0, 0.27))
    return ret


def report1(drug):
    k = 1
    plt.figure(figsize=(25, 5))
    for state in states:
        show_percentage(state, drug, k)
        k = k + 1
    plt.show()


def get_drug_amount(substance_name):
    ret = []
    for year in years:
        s = np.array(df[(df['SubstanceName'] == substance_name)
                        & (df['YYYY'] == year)]
                     .loc[:, 'DrugReports']).sum()
        ret.append(s)
    return ret


def get_year_drug_distribute(year, substance_name):
    amount = get_drug_amount(substance_name)
    s = amount[year - 2010]
    if s == 0:
        return [0] * states.length()
    ret = []
    for state in states:
        s_state = np.array(df[(df['SubstanceName'] == substance_name)
                              & (df['YYYY'] == year)
                              & (df['State'] == state)]
                           .loc[:, 'DrugReports']).sum()
        ret.append(s_state / s)
    return ret


def report2(substance_name):
    plt.figure(figsize=(25, 8))

    for year in years:
        plt.subplot(2, 4, year - 2009)
        data = get_year_drug_distribute(year, substance_name)
        colors = ['tomato', 'lightskyblue', 'goldenrod', 'green', 'y']
        label = []
        draw = []
        color = []
        for i in range(5):
            if data[i] != 0:
                label.append(states[i])
                draw.append(data[i])
                color.append(colors[i])
        size = len(draw)
        explode = [0] * size
        explode[int(draw.index(max(draw)))] = 0.07

        plt.pie(draw,
                labels=label,
                autopct='%3.2f%%',
                pctdistance=0.6,
                explode=explode,
                colors=color
                )
        plt.title(substance_name + ' in ' + str(year))
        plt.legend(loc='upper right',
                   bbox_to_anchor=(1.1, 1.05),
                   fontsize=14,
                   borderaxespad=0.3)

    plt.axis('equal')
    plt.show()


def get_state_drug_rank(state, year):
    ret = []
    amount = []
    for substance_name in substances:
        s_state = np.array(df[(df['SubstanceName'] == substance_name)
                              & (df['YYYY'] == year)
                              & (df['State'] == state)]
                           .loc[:, 'DrugReports']).sum()
        amount.append(s_state)

    new_df = pd.DataFrame({
        'SubstanceName': substances,
        'DrugReports': amount
    })
    sorted_df = new_df.sort_values('DrugReports', inplace=False)
    return sorted_df


def report3(state):
    plt.figure(figsize=(30, 10))
    for year in years:
        plt.subplot(2, 4, year - 2009)

        rank_df = get_state_drug_rank(state, year)
        rank_df = rank_df[rank_df['DrugReports'] > 50]

        names = np.array(rank_df.loc[:, 'SubstanceName'])
        nums = np.array(rank_df.loc[:, 'DrugReports'])
        plt.barh(names, nums, color='indianred')

        plt.ylabel('Substances')
        plt.xlabel('reports in ' + state + ' of year ' + str(year))
        plt.grid(ls='--', axis='x')

    plt.show()


def main():
    report3('OH')


if __name__ == '__main__':
    main()
