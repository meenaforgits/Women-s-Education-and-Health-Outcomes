This project investigates the relationship between female education and women's and children's health outcomes across countries.

The analysis compares countries from different socioeconomic and geographical contexts, including Nordic countries, South Asian countries, and selected Sub-Saharan African countries.

The main objective is to examine whether higher levels of female education are associated with better maternal and child health outcomes, while accounting for differences in economic development and healthcare expenditure.

Research Questions

The analysis focuses on the following questions:

Is higher female literacy associated with lower maternal mortality?
Is female education associated with lower infant and under-5 mortality?
Is female education associated with greater skilled birth attendance?
Do these relationships differ across Nordic, South Asian, and Sub-Saharan African countries?
Does the association between female education and health outcomes remain after accounting for GDP per capita and health expenditure?
Can the relationship between education and health extend beyond maternal and child health to broader women's health outcomes?
Data

The current analysis uses indicators from the World Bank Open Data API.

The indicators include:

Category	Indicator
Education	Female literacy
Education	Female secondary completion
Maternal health	Maternal mortality
Maternal health	Skilled birth attendance
Child health	Infant mortality
Child health	Under-5 mortality
Economic context	GDP per capita
Healthcare	Health expenditure per capita

The initial analysis uses 2022 data.

Indicator definitions
Maternal mortality: maternal deaths per 100,000 live births.
Infant mortality: deaths before age 1 per 1,000 live births.
Under-5 mortality: probability of dying before age 5, expressed per 1,000 live births.
Skilled birth attendance: percentage of births attended by skilled health personnel.
Female literacy: percentage of women who are literate.

The indicators retain their standard internationally reported units.

Country Comparison

Countries are grouped into three broad comparison groups:

Nordic countries
Sweden
Norway
Denmark
Finland
Iceland
South Asian countries
India
Pakistan
Bangladesh
Nepal
Sri Lanka
Selected Sub-Saharan African countries
Niger
Chad
Mali
Uganda
Ethiopia

The country groups are used for comparative analysis, while the broader dataset is used for the statistical analysis where sufficient data are available.

Analysis

The project follows several stages.

1. Data collection

Python retrieves the selected indicators from the World Bank API.

The raw datasets are saved locally so that they do not need to be downloaded every time the script is run.

2. Data cleaning

The datasets are filtered to the selected study year and merged using country and ISO3 country codes.

Missing data are examined before analysis.

3. Descriptive analysis

Summary statistics are calculated to understand the distribution and range of the indicators across countries.

4. Country-group comparison

Average indicator values are compared across the Nordic, South Asian, and Sub-Saharan African groups.

5. Correlation analysis

Pearson and Spearman correlations are used to examine associations between female education and health outcomes.

6. Regression analysis

Regression models examine the relationship between female education and:

Maternal mortality
Infant mortality

GDP per capita and health expenditure are included as additional explanatory variables to account for differences in economic and healthcare context.

The regression analysis is intended to assess associations, not establish causality.

Visualisations

The script generates graphs showing:

Female literacy vs maternal mortality
Female literacy vs infant mortality
Maternal mortality across country groups
Infant mortality across country groups
Female literacy across country groups
Correlations between the main indicators

All graphs are saved automatically in the graphs/ folder.

Technologies Used
Python
Pandas
NumPy
Requests
Matplotlib
Seaborn
SciPy
Statsmodels
World Bank API
Running the Project

Install the required Python packages:

pip install pandas numpy requests matplotlib seaborn scipy statsmodels

Then run:

python women_health_analysis.py

The script automatically creates the data and graphs folders if they do not already exist.

Previously downloaded data are reused on subsequent runs.

Limitations

This is an observational, cross-country analysis. Therefore, the results can identify associations but cannot establish that female education directly causes changes in health outcomes.

Other factors that may influence health outcomes include healthcare access, sanitation, urbanisation, fertility patterns, social conditions, healthcare infrastructure, and government policy.

Country-level indicators also represent population-level patterns and cannot necessarily be interpreted at the individual level.

Future Work

The next stage of the project will expand the analysis to include women's health beyond maternal and child health, particularly diabetes and other non-communicable disease indicators.

This will allow the project to explore whether female education is associated with health outcomes across the life course, rather than only during pregnancy and childhood.

Author

Meenakshi P. S.

MSc Big Data Biology
IBAB, Bengaluru
