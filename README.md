# PhonePe Pulse Data Visualization and Exploration

## Introduction

* The PhonePe Pulse Data Visualization and Exploration project aims to analyze transactions and user data from the Pulse dataset, which is cloned from the PhonePe Pulse GitHub repository. By leveraging Streamlit and Plotly, this user-friendly tool allows you to explore insights related to states, years, quarters, districts, transaction types, and user brands.

## Key Features

* Interactive Map: Visualize transaction data across different states in India.
* User-Friendly Interface: Built using Streamlit for easy interaction.
* Insights Exploration: Dive into data insights on various metrics.

## Workflow

## 1.Importing Libraries:

  * Ensure you have the necessary Python libraries/modules installed:
      * Plotly: For plotting and visualizing data.
      * Pandas: To create a DataFrame with the scraped data.
      * mysql.connector: For storing and retrieving data.
      * Streamlit: To create the graphical user interface.
      * json: For loading JSON files.

  * If any libraries are missing, install them using !pip install [library_name].
  * Import the required libraries into your script.

## 2. Data Extraction:

* Clone the PhonePe Pulse GitHub repository.
* This step fetches data from the PhonePe Pulse repository and stores it in a suitable format (e.g., JSON).

## 3. Data Transformation:

* Convert the available JSON files into a readable and understandable DataFrame format.
* Iterate through each folder, open the JSON files, and extract relevant keys and values.
* Create a DataFrame and save it as a CSV file locally.
  
## Repository Link

* You can find the code and detailed instructions in the PhonePe Pulse Data Visualization and Exploration GitHub repository.

* Feel free to adapt this README to your project specifics! 🚀
