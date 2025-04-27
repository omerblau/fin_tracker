# Financial Tracker & Analyzer

## Project Goal

This project aims to provide a simple, automated, and user-friendly way to view and analyze personal financial information, with a specific focus on accommodating data formats commonly used by Israeli banks and credit card companies (which often involve Hebrew text and specific structures).

## Inspiration

The core idea and initial structure were inspired by the fantastic tutorial by **Tech With Tim**:

-   **Video:** [How To Automate Your Finances with Python - Full Tutorial (Pandas, Streamlit, Plotly & More)](https://www.youtube.com/watch?v=wqBlmAWqa6A&t=242s)
-   **Channel:** [Tech With Tim](https://www.youtube.com/@TechWithTim)

I highly recommend checking out his content!

## Building Upon the Idea

While Tim's tutorial provides a great foundation, this project builds upon it by:

1.  **Automating XLSX to CSV Conversion:** Many banks (including mine, similar to Tim's example) provide transaction data in `.xlsx` format. Tim's method involved manually exporting sheets to CSV via Google Sheets. This can be tedious, especially if the workbook contains multiple sheets (e.g., different credit cards, different transaction types). This project includes scripts to automatically convert _all_ sheets within an `.xlsx` file into individual CSV files.
2.  **Automating CSV Cleaning:** The raw CSVs generated often require cleaning (removing header/footer rows, dropping irrelevant columns). This project includes automated steps to clean the CSVs, preparing them for analysis. The cleaning process is being developed to handle specific formats from Israeli financial institutions.
3.  **Simplifying the Workflow:** The goal is to make the process from downloading the bank's file to seeing the analysis as seamless as possible for the end-user.

## Current Status & Future Plans

This project is actively under development.

**Current Features:**

-   Automated conversion of multi-sheet `.xlsx` files from an `inputs` directory into raw CSVs in a `csvs` directory.
-   Automated cleaning of these raw CSVs, placing the results in `clean_csvs`.
-   Basic Streamlit web interface (`f.py`) to upload _one_ cleaned CSV and view the raw data, separated by credit card.

**Planned Features / Next Steps:**

1.  **Web-Based Conversion:** Allow users to upload their `.xlsx` file directly via the Streamlit web page, triggering the conversion and cleaning process.
2.  **Automatic Data Loading:** Automatically load the _most recently_ generated clean CSV(s) into the Streamlit dashboard, removing the manual upload step.
3.  **Transaction Categorization & Tagging:** Implement a system to allow users to categorize transactions (e.g., "Groceries", "Restaurants", "Utilities"). The system should "remember" tags for specific vendors/descriptions to automate future categorization.
4.  **Enhanced Analysis & Visualization:** Develop more sophisticated analysis and visualizations based on the categorized data (spending trends, budget tracking, etc.).
5.  **Bank/Card Specific Adapters:** Refine the cleaning process to specifically handle formats from different Israeli banks and credit card companies, ensuring consistent output.
