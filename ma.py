import os
import pandas as pd
import geopandas as gdp
from shapely import wkt
import matplotlib.pyplot as plt

'''
Index(['zip', 'object_id_1', 'postal', 'state', 'code', 'geometry',
       'total_confirmed_cases', 'total_covid_vax_7_20_2021', 'cni',
       'gini_index', 'latin_pop', 'black_pop', 'white_pop', 'asian_pop', 'lat',
       'lng', 'population', 'density', 'recovered', 'death', 'households',
       'poverty_households', 'ALICE_households', 'above_ALICE',
       'poverty_and_ALICE', 'poverty_households_pct', 'ALICE_households_pct',
       'above_ALICE_pct', 'poverty_and_ALICE_pct'],
      dtype='object')
'''

def main():

    df = pd.read_csv('~/Documents/hon4355/covid_data_project/zip_maps/nov_30_main.csv')
    
    # Convert geometry column to shapely objects
    df['geometry'] = df['geometry'].apply(wkt.loads)
    df = gdp.GeoDataFrame(df, geometry='geometry')

    names = {
        'latin_pop': 'Latino',
        'black_pop': 'Black',
        'asian_pop': 'Asian',
        'white_pop': 'White',
        'population': 'Total Population',
        'density': 'Density',
        'total_confirmed_cases': 'Total Confirmed Cases',
        'total_covid_vax_7_20_2021': 'COVID Vaccination Rate Up to 7/2021',
        'gini_index': 'Gini Index',
        'recovered': 'Recovered',
        'death': 'Death',
        'above_ALICE': 'Households above the ALICE threshold in 2021',
        'ALICE_households': 'Households with income above poverty but below ALICE threshold in 2021',
        'poverty_and_ALICE': 'Households with income below poverty and ALICE threshold in 2021',
        'poverty_households': 'Households below poverty level in 2021',
        'poverty_households_pct': 'Percentage of Households below poverty level in 2021',
        'ALICE_households_pct': 'Percentage of households above poverty but below ALICE in 2021',
        'above_ALICE_pct': 'Percentage of households above the ALICE threshold in 2021',
        'poverty_and_ALICE_pct': 'Percentage of households with income below poverty and ALICE threshold in 2021'
        #'cni': 'CNI (Community Need Index)'
    }

    output_folder = "plots_img"
    os.makedirs(output_folder, exist_ok=True)

    # Plot population data
    for i in ['latin_pop', 'black_pop', 'asian_pop', 'white_pop']:
        output_file = os.path.join(output_folder, f"race_{i}.png")
        plot_data(df, column=i, title='Total ' + names[i] + ' Population', output_file=output_file)

    # Plot covid data
    for i in ['population', 'density', 'total_confirmed_cases', 'total_covid_vax_7_20_2021', 'recovered', 'death']:
        output_file = os.path.join(output_folder, f"{i}.png")
        plot_data(df, column=i, title=names[i], output_file=output_file)

    # Plot other data
    for i in ['gini_index', 'above_ALICE', 'ALICE_households', 'poverty_and_ALICE', 'poverty_households']:
        output_file = os.path.join(output_folder, f"{i}.png")
        plot_data(df, column=i, title=names[i], output_file=output_file)

    # Percentage of ALICE data
    for i in ['poverty_households_pct', 'ALICE_households_pct','above_ALICE_pct', 'poverty_and_ALICE_pct']:
        output_file = os.path.join(output_folder, f"pct_ALICE_{i}.png")
        plot_data(df, column=i, title=names[i], output_file=output_file)

def plot_data(df, column, title, output_file):
    """
    Plots the population data for a given column and title, and saves the plot to a file.

    Parameters:
        df (GeoDataFrame): The GeoDataFrame containing the data.
        column (str): The column to plot.
        title (str): The title for the plot.
        output_file (str): The file path to save the plot.
    """
    # Create border plot
    ax = df.boundary.plot(color='black', linewidth=0.2, figsize=(10, 5))
    
    # Plot the data with a color map
    df.plot(ax=ax, column=column, legend=True, cmap='inferno')

    # Hide x and y axis values
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Hide plot edges
    for edge in ['right', 'bottom', 'top', 'left']:
        ax.spines[edge].set_visible(False)

    # Set the title
    ax.set_title(title, size=12, weight='bold')

    # Save the plot
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()  # Close the plot to free memory

if __name__ == "__main__":
    main()
