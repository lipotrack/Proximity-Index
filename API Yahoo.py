import yfinance as yf
import csv
import pandas

for sector in ("technology", "financial-services", "consumer-cyclical", "healthcare", "industrials"
, "communication-services", "consumer-defensive", "energy", "real-estate", "basic-materials", "utilities") :
    tech = yf.Sector(sector)
    values = tech.top_companies
    print(tech, values)