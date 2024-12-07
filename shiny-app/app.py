from shiny import App, render, ui
import altair as alt
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Load unemployment data
data_path = "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/Unemployment Rate Map & CPI Plot/state_yearly_unemployment_rate_with_state_name.csv"
unemployment_data = pd.read_csv(data_path)

# Rename columns for consistency
unemployment_data.rename(columns={'state_name': 'State', 'year': 'Year'}, inplace=True)

# Load GeoJSON data for US states
shape_url = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'
shape_data = gpd.read_file(shape_url)

# Directory to store generated maps
output_dir = "/tmp/maps"
os.makedirs(output_dir, exist_ok=True)

# Function to dynamically create maps
def create_map(year):
    # Filter data for the selected year
    filtered_data = unemployment_data[unemployment_data['Year'] == year]
    filtered_data = filtered_data.groupby('State', as_index=False)['unemployment_rate'].mean()
    filtered_data['unemployment_rate'] = filtered_data['unemployment_rate'] * 100 

    # Merge with shape data
    merged_data = shape_data.merge(filtered_data, left_on='name', right_on='State', how='left')
    merged_data['unemployment_rate'] = merged_data['unemployment_rate'].fillna(0)  

    # Plot map
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged_data.plot(
        column='unemployment_rate',
        cmap='Blues',
        linewidth=0.8,
        ax=ax,
        edgecolor='black',
        legend=True,
        legend_kwds={
            'shrink': 0.7,
            'orientation': "horizontal",
            'label': "Unemployment Rate (%)"
        }
    )
    ax.set_title(f"Unemployment Rate by State ({year})", fontsize=16)
    ax.set_axis_off()
    
    # Save map to file
    filepath = os.path.join(output_dir, f"map_{year}.png")
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath

# Define UI
app_ui = ui.page_fluid(
    # Dropdown for Time Period Selection
    ui.input_select(
        "time_period",
        "Select a Time Period:",
        choices=["2011-2015", "2016-2020"]
    ),
    # Dropdown for Visualization Selection
    ui.input_select(
        "visualization_type",
        "Select Visualization Type:",
        choices=["Plots", "NLP Analysis"]
    ),
    # Conditional rendering for data type (only for "Plots")
    ui.output_ui("data_type_buttons"),
    
    # Conditional rendering for CPI plots
    ui.panel_conditional(
        "input.visualization_type === 'Plots' && input.data_type === 'CPI'",
        ui.output_image("cpi_plot", width="100%", height="600px"),
    ),
    # Conditional rendering for unemployment maps (dynamic by year)
    ui.panel_conditional(
        "input.visualization_type === 'Plots' && input.data_type === 'Unemployment rate'",
        ui.input_slider("year_slider", "Select Year", min=2011, max=2020, value=2015, step=1),
        ui.output_image("dynamic_unemployment_map", width="100%", height="600px")
    ),
    # Conditional rendering for difference plot
    ui.panel_conditional(
        "input.visualization_type === 'Plots' && input.data_type === 'Differences'",
        ui.output_image("difference_plot", width="100%", height="600px")
    ),
    # Conditional rendering for NLP Analysis
    ui.panel_conditional(
        "input.visualization_type === 'NLP Analysis'",
        ui.output_image("nlp_plot1", width="100%", height="600px"),
        ui.br(),
        ui.output_image("nlp_plot2", width="100%", height="600px")
    ),
    # Outputs for selected dropdown and visualization type
    ui.output_text_verbatim("dropdown_total"),
    ui.output_text_verbatim("visualization_type_output")
)

# Define Server Logic
def server(input, output, session):
    @output
    @render.ui
    def data_type_buttons():
        # Render radio buttons dynamically for "Plots"
        if input.visualization_type() == "Plots":
            return ui.input_radio_buttons(
                "data_type",
                "Select Data Type:",
                choices=["Unemployment rate", "CPI", "Differences"]
            )
        return None

    @output
    @render.image
    def dynamic_unemployment_map():
        if input.visualization_type() == "Plots" and input.data_type() == "Unemployment rate":
            year = input.year_slider()
            map_path = create_map(year)
            return {"src": map_path, "alt": f"Unemployment Rate Map for {year}"}
        return None

    @output
    @render.image
    def difference_plot():
        # Render difference plot
        if input.visualization_type() == "Plots" and input.data_type() == "Differences":
            return {
                "src": "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/pictures/Difference_graph_2011-2019.png",
                "alt": "Differences in Unemployment Rate"
            }
        return None

    @output
    @render.image
    def cpi_plot():
        # Render CPI Analysis plot
        if input.visualization_type() == "Plots" and input.data_type() == "CPI":
            return {
                "src": "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/pictures/CPI_analysis.png",
                "alt": "CPI Analysis"
            }
        return None

    @output
    @render.image
    def nlp_plot1():
        # Render first NLP plot
        if input.visualization_type() == "NLP Analysis":
            return {
                "src": "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/pictures/Poliarity_Announcement.png",
                "alt": "FOMC Announcement Polarity"
            }
        return None

    @output
    @render.image
    def nlp_plot2():
        # Render second NLP plot
        if input.visualization_type() == "NLP Analysis":
            return {
                "src": "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/pictures/Polarity_Speech.png",
                "alt": "Fed Chair Speech Polarity"
            }
        return None

    @output
    @render.text
    def dropdown_total():
        return f"You selected: {input.time_period()}"

    @output
    @render.text
    def visualization_type_output():
        return f"Visualization Type: {input.visualization_type()}"

app = App(app_ui, server)
