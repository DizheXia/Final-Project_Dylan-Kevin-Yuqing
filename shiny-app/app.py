from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.panel_title("Hello Shiny!"),
    ui.input_slider("n", "N", 0, 100, 20),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app = App(app_ui, server)


from shiny import App, ui, render
import pandas as pd
import altair as alt

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
    # Conditional rendering for unemployment maps
    ui.panel_conditional(
        "input.visualization_type === 'Plots' && input.data_type === 'Unemployment rate'",
        ui.output_image("unemployment_map", width="100%", height="600px")
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
    def unemployment_map():
        # Render unemployment map based on time period
        if input.visualization_type() == "Plots" and input.data_type() == "Unemployment rate":
            if input.time_period() == "2011-2015":
                return {
                    "src": "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/pictures/Unemployment Rate 2011-2015.png",
                    "alt": "Unemployment Map (2011-2015)"
                }
            elif input.time_period() == "2016-2020":
                return {
                    "src": "/Users/alina./Desktop/Final-Project_Dylan-Kevin-Yuqing-main/pictures/Unemployment Rate 2016-2019.png",
                    "alt": "Unemployment Map (2016-2019)"
                }
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
