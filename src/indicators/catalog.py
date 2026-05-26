SERIES: list[dict] = [

    #####################################################
    ################### INTEREST RATES ##################
    #####################################################

    # Auto loan rates
    {"id": "TERMCBAUTO48NS",        "name": "Consumer Auto Loan Rate 48-Month",              "frequency": "m", "category": "Interest Rates"},
    {"id": "RIFLPBCIANM72NM",       "name": "Consumer Auto Loan Rate 72-Month",              "frequency": "sa", "category": "Interest Rates"},

    # Corporate bond yields
    {"id": "DAAA",                  "name": "Moody's Aaa Corporate Bond Yield",              "frequency": "d", "category": "Interest Rates"},
    {"id": "DBAA",                  "name": "Moody's Baa Corporate Bond Yield",              "frequency": "d", "category": "Interest Rates"},

    # High yield spreads & yields
    {"id": "BAMLH0A0HYM2",         "name": "ICE BofA US HY OAS",                            "frequency": "d", "category": "Interest Rates"},
    {"id": "BAMLH0A0HYM2EY",       "name": "ICE BofA US HY Effective Yield",                "frequency": "d", "category": "Interest Rates"},

    # Investment grade spreads
    {"id": "BAMLC0A0CM",           "name": "ICE BofA US Corporate OAS",                     "frequency": "d", "category": "Interest Rates"},
    {"id": "BAMLC0A4CBBB",         "name": "ICE BofA BBB US Corporate OAS",                 "frequency": "d", "category": "Interest Rates"},

    # CCC spread
    {"id": "BAMLH0A3HYC",          "name": "ICE BofA CCC & Lower HY OAS",                   "frequency": "d", "category": "Interest Rates"},

    # Credit card rate
    {"id": "TERMCBCCALLNS",        "name": "Credit Card Rate All Accounts",                  "frequency": "m", "category": "Interest Rates"},

    # Treasury spreads & breakevens
    {"id": "T10Y2Y",               "name": "10Y - 2Y Treasury Spread",                      "frequency": "d", "category": "Interest Rates"},
    {"id": "T10Y3M",               "name": "10Y - 3M Treasury Spread",                      "frequency": "d", "category": "Interest Rates"},
    {"id": "T10YIE",               "name": "10Y Breakeven Inflation Rate",                   "frequency": "d", "category": "Interest Rates"},
    {"id": "T10YFF",               "name": "10Y Treasury - Fed Funds Spread",                "frequency": "d", "category": "Interest Rates"},
    {"id": "T5YIE",                "name": "5Y Breakeven Inflation Rate",                    "frequency": "d", "category": "Interest Rates"},
    {"id": "T1YFF",                "name": "1Y Treasury - Fed Funds Spread",                 "frequency": "d", "category": "Interest Rates"},

    # Corp vs Treasury spreads
    {"id": "AAA10Y",               "name": "Moody's Aaa vs 10Y Treasury",                   "frequency": "d", "category": "Interest Rates"},
    {"id": "BAA10Y",               "name": "Moody's Baa vs 10Y Treasury",                   "frequency": "d", "category": "Interest Rates"},

    # Mortgage & prime
    {"id": "MORTGAGE30US",         "name": "30Y Fixed Mortgage Rate",                        "frequency": "w", "category": "Interest Rates"},
    {"id": "DPRIME",               "name": "Bank Prime Loan Rate",                           "frequency": "d", "category": "Interest Rates"},

     #####################################################
    ################### EXCHANGE RATES ##################
    #####################################################

    {"id": "DTWEXBGS",             "name": "Nominal Broad USD Index",                        "frequency": "d", "category": "Exchange Rates"},
    {"id": "DEXUSEU",              "name": "USD / EUR Spot Rate",                            "frequency": "d", "category": "Exchange Rates"},
    {"id": "DEXJPUS",              "name": "JPY / USD Spot Rate",                            "frequency": "d", "category": "Exchange Rates"},
    {"id": "DEXCHUS",              "name": "CNY / USD Spot Rate",                            "frequency": "d", "category": "Exchange Rates"},
    {"id": "DEXUSUK",              "name": "USD / GBP Spot Rate",                            "frequency": "d", "category": "Exchange Rates"},

    #####################################################
    ########FINANCIAL CONDITIONS & SENTIMENT ############
    #####################################################

    {"id": "VISASMIDSA",           "name": "Visa Spending Momentum - Discretionary",         "frequency": "m", "category": "Financial Indicators"},
    {"id": "UMCSENT",              "name": "U of Michigan Consumer Sentiment",               "frequency": "m", "category": "Financial Indicators"},
    {"id": "MICH",                 "name": "U of Michigan Inflation Expectation",            "frequency": "m", "category": "Financial Indicators"},
    {"id": "NFCI",                 "name": "Chicago Fed National Financial Conditions Index","frequency": "w", "category": "Financial Indicators"},
    {"id": "STLFSI4",              "name": "St. Louis Fed Financial Stress Index",           "frequency": "w", "category": "Financial Indicators"},

    # Volatility indices
    {"id": "VIXCLS",               "name": "CBOE VIX",                                      "frequency": "d", "category": "Financial Indicators"},
    {"id": "GVZCLS",               "name": "CBOE Gold ETF Volatility Index",                 "frequency": "d", "category": "Financial Indicators"},
    {"id": "OVXCLS",               "name": "CBOE Crude Oil ETF Volatility Index",            "frequency": "d", "category": "Financial Indicators"},
    {"id": "RVXCLS",               "name": "CBOE Russell 2000 Volatility Index",             "frequency": "d", "category": "Financial Indicators"},
    {"id": "VXVCLS",               "name": "CBOE S&P 500 3-Month Volatility Index",          "frequency": "d", "category": "Financial Indicators"},
    {"id": "VXEEMCLS",             "name": "CBOE Emerging Markets ETF Volatility Index",     "frequency": "d", "category": "Financial Indicators"},

    #####################################################
    ########### LABOR MARKET ###########################
    #####################################################

    {"id": "U6RATE",               "name": "U-6 Unemployment Rate",                         "frequency": "m", "category": "Labor Market"},
    {"id": "LNS14027660",          "name": "Unemployment Rate - HS Grads 25+",              "frequency": "m", "category": "Labor Market"},
    {"id": "UEMP27OV",             "name": "Unemployed 27 Weeks & Over",                    "frequency": "m", "category": "Labor Market"},

    # Nonfarm payrolls by sector
    {"id": "PAYEMS",               "name": "Total Nonfarm Payrolls",                         "frequency": "m", "category": "Labor Market"},
    {"id": "USCONS",               "name": "Payrolls - Construction",                        "frequency": "m", "category": "Labor Market"},
    {"id": "CES1021100001",        "name": "Payrolls - Oil & Gas Extraction",                "frequency": "m", "category": "Labor Market"},
    {"id": "CES3133600101",        "name": "Payrolls - Motor Vehicles & Parts",              "frequency": "m", "category": "Labor Market"},
    {"id": "CES4348400001",        "name": "Payrolls - Truck Transportation",                "frequency": "m", "category": "Labor Market"},
    {"id": "CES5051800001",        "name": "Payrolls - Computing Infrastructure",            "frequency": "m", "category": "Labor Market"},
    {"id": "CES6562000101",        "name": "Payrolls - Health Care",                         "frequency": "m", "category": "Labor Market"},
    {"id": "CES6054150001",        "name": "Payrolls - Computer Systems Design",             "frequency": "m", "category": "Labor Market"},
    {"id": "CES9091000001",        "name": "Payrolls - Federal Government",                  "frequency": "m", "category": "Labor Market"},
    {"id": "CES9091100001",        "name": "Payrolls - Federal excl. Postal",                "frequency": "m", "category": "Labor Market"},

    # JOLTS
    {"id": "JTSJOL",               "name": "JOLTS Job Openings",                             "frequency": "m", "category": "Labor Market"},
    {"id": "JTSHIR",               "name": "JOLTS Hires",                                    "frequency": "m", "category": "Labor Market"},
    {"id": "JTSLDL",               "name": "JOLTS Layoffs & Discharges",                     "frequency": "m", "category": "Labor Market"},
    {"id": "JTSQUR",               "name": "JOLTS Quits",                                    "frequency": "m", "category": "Labor Market"},

    # Job postings
    {"id": "IHLIDXUS",             "name": "Indeed Job Postings - Total US",                 "frequency": "d", "category": "Labor Market"},
    {"id": "IHLIDXUSTPSOFTDEVE",   "name": "Indeed Job Postings - Software Dev",             "frequency": "d", "category": "Labor Market"},

    # Disability
    {"id": "LNU00074597",          "name": "Population with Disability 16+",                 "frequency": "m", "category": "Labor Market"},

    #####################################################
    ########### PRODUCTION & BUSINESS ACTIVITY #########
    #####################################################

    {"id": "ATLSBUSRGEP",          "name": "Business Expectations: Sales Revenue Growth",    "frequency": "m", "category": "Production & Business"},
    {"id": "TLMFGCONS",            "name": "Construction Spending - Manufacturing",          "frequency": "m", "category": "Production & Business"},
    {"id": "TLHLTHCONS",           "name": "Construction Spending - Health Care",            "frequency": "m", "category": "Production & Business"},
    {"id": "TLPWRCONS",            "name": "Construction Spending - Power",                  "frequency": "m", "category": "Production & Business"},
    {"id": "ACTLISCOUUS",          "name": "Housing Active Listing Count",                   "frequency": "m", "category": "Production & Business"},
    {"id": "RHORUSQ156N",          "name": "Homeownership Rate",                             "frequency": "q", "category": "Production & Business"},
    {"id": "MNFCTRIRSA",           "name": "Manufacturers Inventories to Sales Ratio",       "frequency": "m", "category": "Production & Business"},
    {"id": "RSXFS",                "name": "Advance Retail Sales - Retail Trade",            "frequency": "m", "category": "Production & Business"},
    {"id": "WHLSLRIRSA",           "name": "Wholesalers Inventories to Sales Ratio",         "frequency": "m", "category": "Production & Business"},

    #####################################################
    ########### NATIONAL ACCOUNTS & TRADE ##############
    #####################################################

    {"id": "IMPCH",                "name": "US Imports from China",                          "frequency": "m", "category": "National Accounts"},
    {"id": "FRGSHPUSM649NCIS",     "name": "Cass Freight Index - Shipments",                 "frequency": "m", "category": "National Accounts"},
    {"id": "BOPGSTB",              "name": "Trade Balance: Goods & Services",                "frequency": "m", "category": "National Accounts"},
    {"id": "FORTREASPOS41408",     "name": "China Holdings of US Treasuries",                "frequency": "m", "category": "National Accounts"},
    {"id": "PPIACO",               "name": "PPI All Commodities",                            "frequency": "m", "category": "National Accounts"},

    #####################################################
    ########### RECESSION & INTERNATIONAL ##############
    #####################################################

    {"id": "SAHMREALTIME",         "name": "Sahm Rule Recession Indicator",                  "frequency": "m", "category": "Recession Indicators"},
    {"id": "IRLTLT01DEM156N",      "name": "Germany 10Y Government Bond Yield",              "frequency": "m", "category": "International"},
    {"id": "IRLTLT01JPM156N",      "name": "Japan 10Y Government Bond Yield",                "frequency": "m", "category": "International"},
]

##################################################################
##################################################################

# Frequency codes --> used by fetch_all.py

DAILY   = [s for s in SERIES if s["frequency"] == "d"]
WEEKLY  = [s for s in SERIES if s["frequency"] == "w"]
MONTHLY = [s for s in SERIES if s["frequency"] == "m"]

ID_TO_NAME: dict[str, str] = {s["id"]: s["name"] for s in SERIES}
