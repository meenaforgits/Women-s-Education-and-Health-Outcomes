import os

import pandas as pd
import numpy as np
import requests

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import pearsonr, spearmanr
import statsmodels.api as sm


# Set the study year

YEAR = 2022


# Create folders for data and graphs

os.makedirs("data", exist_ok=True)
os.makedirs("graphs", exist_ok=True)


# Define indicators

indicators = {
    "Female Literacy": "SE.ADT.LITR.FE.ZS",
    "Female Secondary Completion": "SE.SEC.CMPT.LO.FE.ZS",
    "Maternal Mortality": "SH.STA.MMRT",
    "Skilled Birth Attendance": "SH.STA.BRTC.ZS",
    "Infant Mortality": "SP.DYN.IMRT.IN",
    "Under5 Mortality": "SH.DYN.MORT",
    "GDP per Capita": "NY.GDP.PCAP.CD",
    "Health Expenditure": "SH.XPD.CHEX.PC.CD"
}


# Download data from the World Bank

def get_world_bank_data(indicator_code):

    url = (
        f"https://api.worldbank.org/v2/"
        f"country/all/indicator/{indicator_code}"
        f"?format=json&per_page=30000"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if len(data) < 2 or data[1] is None:
        return pd.DataFrame()

    df = pd.json_normalize(data[1])

    df = df[
        [
            "country.value",
            "countryiso3code",
            "date",
            "value"
        ]
    ]

    df.columns = [
        "Country",
        "ISO3",
        "Year",
        "Value"
    ]

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    df["Value"] = pd.to_numeric(
        df["Value"],
        errors="coerce"
    )

    return df


# Download data only if it has not already been saved

datasets = {}

print("\nChecking data files...\n")

for name, code in indicators.items():

    # Make a simple filename from the indicator name
    filename = name.lower().replace(" ", "_") + ".csv"

    filepath = os.path.join(
        "data",
        filename
    )

    # If the file already exists, use it
    if os.path.exists(filepath):

        print("Using saved data:", name)

        data = pd.read_csv(filepath)

    # Otherwise download it
    else:

        print("Downloading:", name)

        data = get_world_bank_data(code)

        data.to_csv(
            filepath,
            index=False
        )

        print("Saved:", filepath)

    # Keep only the selected year
    data = data[
        data["Year"] == YEAR
    ].copy()

    # Rename the value column
    data = data.rename(
        columns={"Value": name}
    )

    datasets[name] = data

    print(
        "Countries with data:",
        data[name].notna().sum()
    )


# Merge all datasets

master = None

for name, data in datasets.items():

    current = data[
        [
            "Country",
            "ISO3",
            "Year",
            name
        ]
    ].copy()

    if master is None:

        master = current

    else:

        master = master.merge(
            current,
            on=["Country", "ISO3", "Year"],
            how="outer"
        )


master = master.sort_values(
    "Country"
).reset_index(drop=True)


print("\nFull dataset:")
print(master.head())

print("\nDataset shape:")
print(master.shape)


# Check missing data

print("\nMissing data:")
print(master.isna().sum())

print("\nPercentage missing:")
print(
    (master.isna().mean() * 100).round(2)
)


# Define country groups

nordics = [
    "Sweden",
    "Norway",
    "Denmark",
    "Finland",
    "Iceland"
]

south_asia = [
    "India",
    "Pakistan",
    "Bangladesh",
    "Nepal",
    "Sri Lanka"
]

sub_saharan_africa = [
    "Niger",
    "Chad",
    "Mali",
    "Uganda",
    "Ethiopia"
]


# Assign each country to a group

def assign_group(country):

    if country in nordics:
        return "Nordics"

    elif country in south_asia:
        return "South Asia"

    elif country in sub_saharan_africa:
        return "Sub-Saharan Africa"

    else:
        return "Other"


master["Group"] = master["Country"].apply(
    assign_group
)


# Variables used for the main analysis

analysis_variables = [
    "Female Literacy",
    "Maternal Mortality",
    "Infant Mortality",
    "GDP per Capita",
    "Health Expenditure"
]


# Keep countries with complete data for the main analysis

analysis = master.dropna(
    subset=analysis_variables
).copy()


print(
    "\nCountries in final analysis:",
    len(analysis)
)


# Summary statistics

print("\nSummary statistics:")
print(
    analysis[analysis_variables].describe()
)


# Group comparison

group_data = analysis[
    analysis["Group"] != "Other"
].copy()


group_summary = (
    group_data
    .groupby("Group")[analysis_variables]
    .mean()
)


print("\nAverage values by country group:")
print(group_summary)


# Female literacy vs maternal mortality

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=analysis,
    x="Female Literacy",
    y="Maternal Mortality",
    hue="Group",
    s=80
)

plt.xlabel("Female literacy (%)")
plt.ylabel("Maternal mortality ratio")
plt.title(
    "Female Literacy and Maternal Mortality"
)

plt.tight_layout()

plt.savefig(
    "graphs/female_literacy_maternal_mortality.png",
    dpi=300
)

plt.show()


# Female literacy vs infant mortality

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=analysis,
    x="Female Literacy",
    y="Infant Mortality",
    hue="Group",
    s=80
)

plt.xlabel("Female literacy (%)")
plt.ylabel("Infant mortality rate")
plt.title(
    "Female Literacy and Infant Mortality"
)

plt.tight_layout()

plt.savefig(
    "graphs/female_literacy_infant_mortality.png",
    dpi=300
)

plt.show()


# Maternal mortality by country group

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=group_data,
    x="Group",
    y="Maternal Mortality"
)

plt.xlabel("")
plt.ylabel("Maternal mortality ratio")
plt.title(
    "Maternal Mortality Across Country Groups"
)

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    "graphs/maternal_mortality_groups.png",
    dpi=300
)

plt.show()


# Infant mortality by country group

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=group_data,
    x="Group",
    y="Infant Mortality"
)

plt.xlabel("")
plt.ylabel("Infant mortality rate")
plt.title(
    "Infant Mortality Across Country Groups"
)

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    "graphs/infant_mortality_groups.png",
    dpi=300
)

plt.show()


# Female literacy by country group

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=group_data,
    x="Group",
    y="Female Literacy"
)

plt.xlabel("")
plt.ylabel("Female literacy (%)")
plt.title(
    "Female Literacy Across Country Groups"
)

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    "graphs/female_literacy_groups.png",
    dpi=300
)

plt.show()


# Correlation analysis

print("\nCorrelation analysis")


# Female literacy vs maternal mortality

r_maternal, p_maternal = pearsonr(
    analysis["Female Literacy"],
    analysis["Maternal Mortality"]
)

print(
    "\nFemale literacy vs maternal mortality"
)

print("Pearson r:", round(r_maternal, 3))
print("P-value:", round(p_maternal, 5))


# Female literacy vs infant mortality

r_infant, p_infant = pearsonr(
    analysis["Female Literacy"],
    analysis["Infant Mortality"]
)

print(
    "\nFemale literacy vs infant mortality"
)

print("Pearson r:", round(r_infant, 3))
print("P-value:", round(p_infant, 5))


# Spearman correlation

rho_maternal, p_spearman = spearmanr(
    analysis["Female Literacy"],
    analysis["Maternal Mortality"]
)

print("\nSpearman correlation:")
print(
    "Spearman rho:",
    round(rho_maternal, 3)
)

print(
    "P-value:",
    round(p_spearman, 5)
)


# Correlation matrix

correlation_matrix = (
    analysis[analysis_variables]
    .corr()
)

print("\nCorrelation matrix:")
print(correlation_matrix)


plt.figure(figsize=(10, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title(
    "Correlation Between Education and Health Indicators"
)

plt.tight_layout()

plt.savefig(
    "graphs/correlation_matrix.png",
    dpi=300
)

plt.show()


# Maternal mortality regression

X = analysis[
    [
        "Female Literacy",
        "GDP per Capita",
        "Health Expenditure"
    ]
]

X = sm.add_constant(X)

y = analysis["Maternal Mortality"]

model_maternal = sm.OLS(
    y,
    X
).fit()

print(
    "\nMaternal mortality regression:"
)

print(
    model_maternal.summary()
)


# Infant mortality regression

X = analysis[
    [
        "Female Literacy",
        "GDP per Capita",
        "Health Expenditure"
    ]
]

X = sm.add_constant(X)

y = analysis["Infant Mortality"]

model_infant = sm.OLS(
    y,
    X
).fit()

print(
    "\nInfant mortality regression:"
)

print(#
    model_infant.summary()
)


# Save the final analysis dataset

analysis.to_csv(
    "women_health_analysis.csv",
    index=False
)


# Save group summary

group_summary.to_csv(
    "country_group_summary.csv"
)


# Save correlation matrix

correlation_matrix.to_csv(
    "correlation_matrix.csv"
)


# Save regression results

with open(
    "maternal_mortality_regression.txt",
    "w"
) as file:

    file.write(
        model_maternal.summary().as_text()
    )


with open(
    "infant_mortality_regression.txt",
    "w"
) as file:

    file.write(
        model_infant.summary().as_text()
    )


print("\nAnalysis complete.")
print("Results and figures have been saved.")

