import folium
import random
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, request, jsonify

# Setting the Matplotlib backend to a non-GUI one (Agg)
plt.switch_backend('Agg')

app = Flask(__name__)

# Define river data with accurate coordinates for each river and color
rivers_data = {
    "Broken River": {
        "coords": [
            [-36.674, 145.497],
            [-36.689, 145.510],
            [-36.704, 145.523],
            [-36.719, 145.536],
            [-36.734, 145.549]
        ],
        "color": "blue"
    },
    "Loddon River": {
        "coords": [
            [-36.850, 144.150],
            [-36.870, 144.175],
            [-36.890, 144.200],
            [-36.910, 144.225],
            [-36.930, 144.250]
        ],
        "color": "green"
    },
    "Goulburn River": {
        "coords": [
            [-37.059, 145.366],
            [-37.074, 145.381],
            [-37.089, 145.396],
            [-37.104, 145.411],
            [-37.119, 145.426]
        ],
        "color": "red"
    },
    "Yarra River": {
        "coords": [
            [-37.822, 145.013],
            [-37.834, 145.028],
            [-37.846, 145.043],
            [-37.858, 145.058],
            [-37.870, 145.073]
        ],
        "color": "purple"
    },
    "Thomson River": {
        "coords": [
            [-37.977, 146.627],
            [-37.997, 146.647],
            [-38.017, 146.667],
            [-38.037, 146.687],
            [-38.057, 146.707]
        ],
        "color": "darkblue"
    },
    "Macalister River": {
        "coords": [
            [-38.098, 146.911],
            [-38.108, 146.926],
            [-38.118, 146.941],
            [-38.128, 146.956],
            [-38.138, 146.971]
        ],
        "color": "orange"
    },
}

# Function to generate random data and chart for the selected date and time
def generate_chart(selected_date, selected_time):
    # Time points for 24 hours in 24-hour format
    time_points = list(range(1, 25))  # 1 to 24 for 24-hour format

    # Random data for height (mm), flow (cfs), and rainfall (mm)
    height_data = [random.uniform(100, 2500) for _ in time_points]  # in millimeters, starting from 100
    flow_data = [random.uniform(100, 300) for _ in time_points]  # in cubic feet per second (cfs)
    rainfall_data = [random.uniform(50, 2500) for _ in time_points]  # in millimeters

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot rainfall as a bar graph (increase bar width to enhance visibility)
    ax1.bar(time_points, rainfall_data, color='b', alpha=0.6, label='Rainfall (mm)', width=0.8, align='center')

    # Plot water height as a line graph
    ax1.plot(time_points, height_data, color='g', marker='o', linestyle='-', label='Water Height (mm)')
    ax1.set_xlabel('Time (hours)')
    ax1.set_xticks(time_points)
    ax1.set_xticklabels([f"{i:02d}" for i in time_points])  # Display hours in a clean 24-hour format
    ax1.set_ylabel('Rainfall / Water Height (mm)', color='black')
    ax1.set_ylim(0, 3000)  # Set y-axis to start from 0 and go up to 3000 for better scaling
    ax1.set_yticks([i for i in range(100, 3000, 100)])  # Increment y-axis labels by 100
    ax1.set_title(f'Water Data on {selected_date} at {selected_time}')

    # Create a second y-axis for water flow and plot it
    ax2 = ax1.twinx()
    ax2.plot(time_points, flow_data, color='r', marker='x', linestyle='--', label='Water Flow (cfs)')
    ax2.set_ylabel('Water Flow (cfs)', color='r')

    # Legends for both y-axes (Make legend smaller to avoid overlap)
    ax1.legend(loc='upper left', fontsize='small')
    ax2.legend(loc='upper right', fontsize='small')

    # Save the plot to a PNG image and encode it to base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Close the figure to free memory
    plt.close(fig)

    # Return the base64-encoded image to embed in the popup
    base64_image = base64.b64encode(image_png).decode('utf-8')
    html = f'''
    <div>
        <img src="data:image/png;base64,{base64_image}" style="width:600px;height:400px;">
    </div>
    '''
    return html

@app.route('/')
def index():
    # Initialize the map centered around Victoria using OpenStreetMap tiles
    victoria_map = folium.Map(
        location=[-37.4713, 144.7852],
        zoom_start=7,
        tiles="OpenStreetMap",  # Using OpenStreetMap for consistent display
        max_bounds=True
    )

    # Create individual feature groups for each river and add them to the map
    for river_name, river_info in rivers_data.items():
        river_group = folium.FeatureGroup(name=f"<span style='color:{river_info['color']};'>{river_name}</span>")
        for coord in river_info["coords"]:
            # Placeholder values for selected date and time
            selected_date = "2024-09-14"
            selected_time = "12:00"
            popup_html = generate_chart(selected_date, selected_time)

            folium.Marker(
                location=coord,
                popup=folium.Popup(popup_html, max_width=400),
                icon=folium.Icon(color=river_info["color"], icon="info-sign"),
            ).add_to(river_group)
        river_group.add_to(victoria_map)

    # Adjust map to fit all river points
    all_coords = [coord for river_info in rivers_data.values() for coord in river_info["coords"]]
    victoria_map.fit_bounds(all_coords)

    # Add layer control to allow toggling of river visibility with color-coded labels
    folium.LayerControl(position='topright', collapsed=False).add_to(victoria_map)

    # Custom Visualization Controls with date and time selection (Form-like static legend)
    legend_html = """
    <div style="position: fixed; top: 10px; left: 10px; width: 250px; height: 150px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                padding: 10px;">
        <b>Select Date and Time</b><br>
        Date: <input type='date' id='date_input' value='2024-09-14'/><br>
        Time: <input type='time' id='time_input' value='12:00'/><br>
        <button onclick="updateChart()">Update</button>
    </div>

    <script>
    function updateChart() {
        var date = document.getElementById('date_input').value;
        var time = document.getElementById('time_input').value;
        // Here you would pass the selected date and time to the backend for processing
        alert('You selected ' + date + ' ' + time + '. (Update functionality to be implemented)');
    }
    </script>
    """

    # Add the static form-like legend to the map
    victoria_map.get_root().html.add_child(folium.Element(legend_html))

    # Save the map to an HTML file
    victoria_map.save("templates/victoria_interactive_map.html")

    return render_template('victoria_interactive_map.html')

if __name__ == '__main__':
    app.run(debug=True)
