import folium
import pandas as pd
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, request
import matplotlib.ticker as ticker
import numpy as np
plt.switch_backend('Agg')

# Function to read metadata from CSV
def read_metadata():
    metadata_path = f"Datasets/metadata.csv"
    try:
        metadata_raw = pd.read_csv(metadata_path)
        # print(metadata.head(10)) testing code, can be deleted
        return metadata_raw
    except FileNotFoundError:
        print("Metadata could not be read.")
        return None

# Read metadata and create site list
metadata = read_metadata()
basin_list = sorted(set(metadata.Basin))
colors = ['red', 'purple', 'blue', 'green', 'orange', 'pink', 'darkred', 'darkpurple',  'darkblue', 'darkgreen', 'lightred', 'lightblue', 'lightgreen']
rivers_data = {}
for i, basin in enumerate(basin_list):
    locations_df = metadata.loc[metadata['Basin'] == basin]
    locations = locations_df.to_dict('records')
    rivers_data.update({basin: {
        "locations": locations,
        "color": colors[i]
    }})

# Function to read dataset based on Site ID
def read_dataset_for_site_id(site_id):
    dataset_path = f"Datasets/{site_id}.csv"
    try:
        df = pd.read_csv(dataset_path)
        return df.sort_values(['Date', 'Time'], ascending=[True, True])
    except FileNotFoundError:
        print(f"Dataset for Site ID {site_id} not found.")
        return None

# Function to generate chart data for a specific river and date
def generate_chart_for_river_and_date(river_name, site_id, selected_date, site_name):
    df = read_dataset_for_site_id(site_id)
    if df is None:
        return "<div>No data available for the selected site.</div>"

    # Filtering the data for the selected date
    df_filtered = df[df['Date'] == selected_date]

    # Checks if data exists for the selected date, returns error message if not
    if df_filtered.empty:
        return "<div>No data available for the selected date.</div>"
    # If data exists for the selected date, graphs available variables
    else: 
        # Reading times
        time_points = df_filtered['Time']
        # Drawing plot
        fig, ax1 = plt.subplots(figsize=(10, 6), layout='constrained')
        # Setting/labelling x-axis as 0-23 hours
        ax1.set_xlim(0, 23)
        ax1.set_xlabel('Time (hours)')
        ax1.set_xticks(range(0,24))
        ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):02d}'))  # Format time labels as '01', '02', etc.
        ax1.grid(axis='x')

        # Twin x-axis plots for flow and rainfall
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        # Setting graph title
        ax1.set_title(f'Data for {site_name} ({site_id} in {river_name} River basin) on {selected_date}')

        # Variables used to set legend location
        height = False
        flow = False
        rainfall = False

        # Graphing height data if available
        if 'Height' in df_filtered.columns:
            height_data = df_filtered['Height']
            p1 = ax1.plot(time_points, height_data, color='darkgreen', linewidth=2, marker='o', label='Water Height (m)')
            ax1.autoscale_view()
            ax1.set_ylabel('Water Height (m)')
            height = True
        else:
            ax1.axis('off')

        # Graphing flow data if available
        if 'Flow' in df_filtered.columns:
            flow_data = df_filtered['Flow']
            p2 = ax2.plot(time_points, flow_data, color='darkmagenta', linewidth=2, marker='o', label='Water Flow (ML/day)')
            ax2.autoscale_view()
            ax2.set_ylabel('Water Flow (ML/day)')
            flow = True
        else:
            ax2.axis('off')

        # Graphing rainfall data if available
        if 'Rainfall' in df_filtered.columns:
            rainfall_data = df_filtered['Rainfall']
            p3 = ax3.plot(time_points, rainfall_data, color='darkblue', linewidth=2, marker='o', label='Rainfall (mm)')
            ax3.spines['right'].set_position(('outward', 60))
            ax3.autoscale_view()   
            ax3.set_ylabel('Rainfall (mm)')  
            rainfall = True
        else:
            ax3.axis('off')

    # Setting legend locations based on available data
    if (height & flow & rainfall):   
        ax1.legend(handles=p1+p2+p3, loc='best')
    elif (flow & rainfall):
        ax1.legend(handles=p2+p3, loc='best')  
    elif (height & flow):
        ax1.legend(handles=p1+p2, loc='best')
    elif (height & rainfall):
        ax1.legend(handles=p1+p3, loc='best')
    elif (height):
        ax1.legend(handles=p1, loc='best')
    elif (flow):
        ax1.legend(handles=p2, loc='best')
    elif (rainfall):
        ax1.legend(handles=p3, loc='best')

    # Saving the image to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)

    base64_image = base64.b64encode(image_png).decode('utf-8')
    return f'<div><img src="data:image/png;base64,{base64_image}" style="width:600px;height:400px;"></div>'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_date = request.form.get('date_input', '2014-08-28')

    # Instantiate map
    victoria_map = folium.Map(location=[-37.4713, 144.7852], zoom_start=7, tiles="OpenStreetMap")

    # Loops through all sites, adds marker to map, generates chart
    for river_name, river_info in rivers_data.items():
        river_group = folium.FeatureGroup(name=f"<span style='color:{river_info["color"]};'>{river_name}</span>")
        for location in river_info["locations"]:
            site_id = location["SiteID"]
            site_name = location["Location"]
            popup_html = generate_chart_for_river_and_date(river_name, site_id, selected_date, site_name)
            folium.Marker(
                location=[location["Latitude"], location["Longitude"]],
                tooltip=f"{site_name}",
                popup=folium.Popup(popup_html, max_width=600),
                icon=folium.Icon(color=river_info["color"], icon="info-sign"),
            ).add_to(river_group)
        river_group.add_to(victoria_map)
        # Prints to console as rendering progresses
        print(f"Data successfully processed for {river_name}")

    # Prints to console once rendering complete
    total = len(rivers_data.items())
    print(f"Total river basins in processed data: {total}")

    all_coords = [loc for river_info in rivers_data.values() for loc in river_info["locations"]]
    if all_coords:
        victoria_map.fit_bounds([[loc["Latitude"], loc["Longitude"]] for loc in all_coords])

    folium.LayerControl().add_to(victoria_map)

    # Date selection
    legend_html = f"""
    <div style="position: fixed; top: 10px; left: 10px; width: 200px; height: 120px;
                background-color: white; border:2px solid grey; z-index:9999; font-size:12px;
                padding: 10px;">
        <form method='POST' action='/'>
            <b>Select Date</b><br>
            Date: <input type='date' name='date_input' value='{selected_date}'/><br><br>
            <input type='submit' value='Update'/>
        </form>
    </div>
    """
    victoria_map.get_root().html.add_child(folium.Element(legend_html))
    victoria_map.save("templates/victoria_interactive_map.html")

    return render_template('victoria_interactive_map.html')

if __name__ == '__main__':
    app.run(debug=True)