import folium
import pandas as pd
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, request
import matplotlib.ticker as ticker
import numpy as np
plt.switch_backend('Agg')

# Hardcoded river data with specific colors
rivers_data = {
    "Broken River": {
        "locations": [
            {"Site ID": 404204, "Latitude": -36.1237777777778, "Longitude": 145.831916666667},
            {"Site ID": 404207, "Latitude": -36.6111666666667, "Longitude": 146.059194444444},
            {"Site ID": 404210, "Latitude": -35.9677777777778, "Longitude": 144.961888888889},
            {"Site ID": 404214, "Latitude": -36.0985277777778, "Longitude": 145.685166666667},
            {"Site ID": 404216, "Latitude": -36.4735277777778, "Longitude": 145.94175},
            {"Site ID": 404217, "Latitude": -36.4731388888889, "Longitude": 145.941444444444},
            {"Site ID": 404222, "Latitude": -36.4313888888889, "Longitude": 145.449777777778},
            {"Site ID": 404224, "Latitude": -36.4336666666667, "Longitude": 145.669194444444},
            {"Site ID": 404226, "Latitude": -36.6159722222222, "Longitude": 145.982861111111},
            {"Site ID": 404227, "Latitude": -36.6156388888889, "Longitude": 145.980777777778},
            {"Site ID": 404234, "Latitude": -36.7926388888889, "Longitude": 146.208694444444},
            {"Site ID": 404235, "Latitude": -36.8188055555556, "Longitude": 146.2185},
            {"Site ID": 404238, "Latitude": -36.0988333333333, "Longitude": 145.331777777778},
            {"Site ID": 404239, "Latitude": -36.2929444444444, "Longitude": 145.834277777778},
            {"Site ID": 404241, "Latitude": -36.4736388888889, "Longitude": 145.941416666667},
            {"Site ID": 404243, "Latitude": -36.8453611111111, "Longitude": 146.010694444444},
            {"Site ID": 404245, "Latitude": -36.7795555555556, "Longitude": 146.028972222222},
            {"Site ID": 404246, "Latitude": -36.7217222222222, "Longitude": 145.993111111111},
            {"Site ID": 404247, "Latitude": -36.7304166666667, "Longitude": 146.226138888889},
            {"Site ID": 404248, "Latitude": -36.0948333333333, "Longitude": 145.442611111111},
            {"Site ID": 404249, "Latitude": -36.1441388888889, "Longitude": 145.796888888889},
            {"Site ID": 404250, "Latitude": -36.09875, "Longitude": 145.594166666667},
            {"Site ID": 404251, "Latitude": -36.1310833333333, "Longitude": 145.486027777778},
            {"Site ID": 404713, "Latitude": -36.0550833333333, "Longitude": 145.489694444444},
            {"Site ID": 404714, "Latitude": -36.031, "Longitude": 145.759888888889},
            {"Site ID": 409202, "Latitude": -35.8135277777778, "Longitude": 145.556694444444},
            {"Site ID": 409216, "Latitude": -36.0089166666667, "Longitude": 146.000611111111},
            {"Site ID": 409217, "Latitude": -35.9148611111111, "Longitude": 145.668527777778},
            {"Site ID": 409224, "Latitude": -35.7366388888889, "Longitude": 144.944333333333},
            {"Site ID": 409225, "Latitude": -35.7913333333333, "Longitude": 145.091194444444},
            {"Site ID": 409226, "Latitude": -35.8167777777778, "Longitude": 145.162527777778},
            {"Site ID": 409228, "Latitude": -35.7721944444444, "Longitude": 144.968861111111},
            {"Site ID": 409229, "Latitude": -35.8313888888889, "Longitude": 145.003888888889},
            {"Site ID": 409230, "Latitude": -35.8358333333333, "Longitude": 144.946194444444},
            {"Site ID": 409232, "Latitude": -35.9558055555556, "Longitude": 144.950861111111},
            {"Site ID": 409391, "Latitude": -35.8416111111111, "Longitude": 145.151638888889},
            {"Site ID": 409392, "Latitude": -35.8689722222222, "Longitude": 145.099833333333},
            {"Site ID": 409393, "Latitude": -35.8804444444444, "Longitude": 145.074111111111},
            {"Site ID": 409394, "Latitude": -35.8851944444444, "Longitude": 145.042416666667},
            {"Site ID": 409395, "Latitude": -35.9147222222222, "Longitude": 145.140305555556},
            {"Site ID": 409396, "Latitude": -35.8951944444444, "Longitude": 145.003083333333},
            {"Site ID": 409397, "Latitude": -35.8954166666667, "Longitude": 145.005583333333},
            {"Site ID": 409398, "Latitude": -35.9358055555556, "Longitude": 144.967416666667},
            {"Site ID": 409710, "Latitude": -35.9984166666667, "Longitude": 145.823361111111},
            {"Site ID": 409711, "Latitude": -35.8399722222222, "Longitude": 145.495694444444},
            {"Site ID": 409712, "Latitude": -35.9081944444444, "Longitude": 145.332166666667},
            {"Site ID": 409722, "Latitude": -36.0131111111111, "Longitude": 145.9985}
        ],
        "color": "blue"
    },
    "Campaspe River": {
        "locations": [
            {"Site ID": 406200, "Latitude": -37.1914722222222, "Longitude": 144.380333333333},
            {"Site ID": 406201, "Latitude": -36.6292222222222, "Longitude": 144.5545},
            {"Site ID": 406202, "Latitude": -36.3319444444444, "Longitude": 144.700972222222},
            {"Site ID": 406207, "Latitude": -36.8433333333333, "Longitude": 144.530194444444},
            {"Site ID": 406208, "Latitude": -37.3877222222222, "Longitude": 144.450472222222},
            {"Site ID": 406210, "Latitude": -37.2509722222222, "Longitude": 144.380722222222},
            {"Site ID": 406212, "Latitude": -37.2226388888889, "Longitude": 144.418833333333},
            {"Site ID": 406213, "Latitude": -37.0151111111111, "Longitude": 144.540305555556},
            {"Site ID": 406214, "Latitude": -36.7735, "Longitude": 144.428111111111},
            {"Site ID": 406215, "Latitude": -36.9616111111111, "Longitude": 144.491555555556},
            {"Site ID": 406216, "Latitude": -36.8968888888889, "Longitude": 144.355611111111},
            {"Site ID": 406218, "Latitude": -36.4363888888889, "Longitude": 144.658972222222},
            {"Site ID": 406220, "Latitude": -37.1916666666667, "Longitude": 144.383333333333},
            {"Site ID": 406224, "Latitude": -36.5456666666667, "Longitude": 144.637694444444},
            {"Site ID": 406225, "Latitude": -36.8485, "Longitude": 144.533944444444},
            {"Site ID": 406226, "Latitude": -36.8803333333333, "Longitude": 144.652},
            {"Site ID": 406235, "Latitude": -36.9471666666667, "Longitude": 144.664694444444},
            {"Site ID": 406250, "Latitude": -37.3194722222222, "Longitude": 144.363944444444},
            {"Site ID": 406262, "Latitude": -36.8109166666667, "Longitude": 144.391222222222},
            {"Site ID": 406263, "Latitude": -36.0959166666667, "Longitude": 144.675361111111},
            {"Site ID": 406264, "Latitude": -36.1866944444444, "Longitude": 144.730527777778},
            {"Site ID": 406265, "Latitude": -36.1447222222222, "Longitude": 144.735333333333},
            {"Site ID": 406266, "Latitude": -37.33775, "Longitude": 144.5115},
            {"Site ID": 406273, "Latitude": -37.4072222222222, "Longitude": 144.355472222222},
            {"Site ID": 406276, "Latitude": -36.1504444444444, "Longitude": 144.737111111111},
            {"Site ID": 406280, "Latitude": -37.2895833333333, "Longitude": 144.433888888889},
            {"Site ID": 406281, "Latitude": -37.2389722222222, "Longitude": 144.339194444444},
            {"Site ID": 406700, "Latitude": -37.1932222222222, "Longitude": 144.376555555556},
            {"Site ID": 406704, "Latitude": -36.1286666666667, "Longitude": 144.769305555556},
            {"Site ID": 406731, "Latitude": -36.3210277777778, "Longitude": 144.918555555556},
            {"Site ID": 406744, "Latitude": -36.3335277777778, "Longitude": 144.644666666667},
            {"Site ID": 406756, "Latitude": -36.3286944444444, "Longitude": 144.980888888889},
            {"Site ID": 406758, "Latitude": -36.0405, "Longitude": 144.578833333333},
            {"Site ID": 406764, "Latitude": -36.3281111111111, "Longitude": 144.701},
            {"Site ID": 406766, "Latitude": -36.3186666666667, "Longitude": 144.684583333333},
            {"Site ID": 409200, "Latitude": -36.1197222222222, "Longitude": 144.747333333333},
            {"Site ID": 409222, "Latitude": -36.0943055555556, "Longitude": 144.683611111111}
        ],
        "color": "purple"
    },
    "Goulburn River": {
        "locations": [
            {"Site ID": 407202, "Latitude": -35.7032222222222, "Longitude": 143.919222222222},
            {"Site ID": 407203, "Latitude": -36.8311944444445, "Longitude": 143.891722222222},
            {"Site ID": 407205, "Latitude": -35.9243333333333, "Longitude": 143.871888888889},
            {"Site ID": 407209, "Latitude": -35.6565833333333, "Longitude": 144.124833333333},
            {"Site ID": 407210, "Latitude": -36.9851666666667, "Longitude": 143.967472222222},
            {"Site ID": 407211, "Latitude": -36.9222777777778, "Longitude": 143.74675},
            {"Site ID": 407213, "Latitude": -37.0843888888889, "Longitude": 143.811666666667},
            {"Site ID": 407214, "Latitude": -37.2966388888889, "Longitude": 143.789833333333},
            {"Site ID": 407215, "Latitude": -37.1090277777778, "Longitude": 144.058},
            {"Site ID": 407217, "Latitude": -37.1579444444444, "Longitude": 144.208416666667},
            {"Site ID": 407220, "Latitude": -36.9947777777778, "Longitude": 143.642583333333},
            {"Site ID": 407221, "Latitude": -37.2064166666667, "Longitude": 144.100361111111},
            {"Site ID": 407222, "Latitude": -37.2274444444444, "Longitude": 143.834083333333},
            {"Site ID": 407224, "Latitude": -36.3234166666667, "Longitude": 143.86525},
            {"Site ID": 407227, "Latitude": -37.3338333333333, "Longitude": 143.922527777778},
            {"Site ID": 407229, "Latitude": -36.4267777777778, "Longitude": 143.951222222222},
            {"Site ID": 407230, "Latitude": -37.1639166666667, "Longitude": 143.962472222222},
            {"Site ID": 407236, "Latitude": -36.1625, "Longitude": 144.285805555556},
            {"Site ID": 407237, "Latitude": -37.44125, "Longitude": 143.946333333333},
            {"Site ID": 407238, "Latitude": -37.4443333333333, "Longitude": 143.949444444444},
            {"Site ID": 407239, "Latitude": -37.13825, "Longitude": 143.913388888889},
            {"Site ID": 407240, "Latitude": -36.8338055555556, "Longitude": 143.891694444444},
            {"Site ID": 407241, "Latitude": -36.9890277777778, "Longitude": 143.968416666667},
            {"Site ID": 407244, "Latitude": -37.0929722222222, "Longitude": 143.863722222222},
            {"Site ID": 407246, "Latitude": -36.7289444444444, "Longitude": 144.136055555556},
            {"Site ID": 407248, "Latitude": -37.0904722222222, "Longitude": 143.865333333333},
            {"Site ID": 407249, "Latitude": -37.4042777777778, "Longitude": 144.003444444444},
            {"Site ID": 407251, "Latitude": -35.7101111111111, "Longitude": 143.910027777778},
            {"Site ID": 407252, "Latitude": -35.6046111111111, "Longitude": 143.931166666667},
            {"Site ID": 407253, "Latitude": -36.4519166666667, "Longitude": 144.469361111111},
            {"Site ID": 407254, "Latitude": -36.7453611111111, "Longitude": 144.290722222222},
            {"Site ID": 407255, "Latitude": -36.6331388888889, "Longitude": 144.364694444444},
            {"Site ID": 407260, "Latitude": -35.99, "Longitude": 143.841972222222},
            {"Site ID": 407283, "Latitude": -35.7577777777778, "Longitude": 144.105472222222},
            {"Site ID": 407284, "Latitude": -35.889, "Longitude": 144.043416666667},
            {"Site ID": 407285, "Latitude": -35.896, "Longitude": 143.995611111111},
            {"Site ID": 407286, "Latitude": -35.6947222222222, "Longitude": 143.87125},
            {"Site ID": 407287, "Latitude": -35.9225555555556, "Longitude": 144.1845},
            {"Site ID": 407288, "Latitude": -37.1877777777778, "Longitude": 143.522833333333},
            {"Site ID": 407289, "Latitude": -36.0977222222222, "Longitude": 143.924222222222},
            {"Site ID": 407290, "Latitude": -36.373, "Longitude": 144.137444444444},
            {"Site ID": 407293, "Latitude": -35.9308611111111, "Longitude": 144.262361111111},
            {"Site ID": 407294, "Latitude": -35.8851666666667, "Longitude": 144.176861111111},
            {"Site ID": 407295, "Latitude": -35.9141666666667, "Longitude": 144.203527777778},
            {"Site ID": 407300, "Latitude": -37.0166944444445, "Longitude": 144.14175},
            {"Site ID": 407301, "Latitude": -36.0110277777778, "Longitude": 143.826138888889},
            {"Site ID": 407302, "Latitude": -36.1216388888889, "Longitude": 143.833444444444},
            {"Site ID": 407311, "Latitude": -37.3898333333333, "Longitude": 144.174444444444},
            {"Site ID": 407312, "Latitude": -37.3861388888889, "Longitude": 144.239472222222},
            {"Site ID": 407314, "Latitude": -37.2839444444444, "Longitude": 143.648888888889},
            {"Site ID": 407315, "Latitude": -37.2573888888889, "Longitude": 143.631722222222},
            {"Site ID": 407319, "Latitude": -37.3656388888889, "Longitude": 143.990583333333},
            {"Site ID": 407323, "Latitude": -36.0532222222222, "Longitude": 143.829027777778},
            {"Site ID": 407324, "Latitude": -37.4447777777778, "Longitude": 143.93625},
            {"Site ID": 407326, "Latitude": -37.2793888888889, "Longitude": 143.54475},
            {"Site ID": 407336, "Latitude": -35.6564444444444, "Longitude": 144.14325},
            {"Site ID": 407337, "Latitude": -35.7018611111111, "Longitude": 144.193194444444},
            {"Site ID": 407338, "Latitude": -35.7646944444444, "Longitude": 144.232555555556},
            {"Site ID": 407339, "Latitude": -35.7369444444445, "Longitude": 144.190777777778},
            {"Site ID": 407340, "Latitude": -35.7108055555556, "Longitude": 144.178055555556},
            {"Site ID": 407366, "Latitude": -35.7666944444445, "Longitude": 144.268},
            {"Site ID": 407369, "Latitude": -35.8485555555556, "Longitude": 144.345888888889},
            {"Site ID": 407372, "Latitude": -35.7663611111111, "Longitude": 144.230888888889},
            {"Site ID": 407381, "Latitude": -37.3281944444445, "Longitude": 144.158083333333},
            {"Site ID": 407384, "Latitude": -35.7266666666667, "Longitude": 144.207527777778},
            {"Site ID": 407608, "Latitude": -35.8761111111111, "Longitude": 143.807888888889},
            {"Site ID": 407609, "Latitude": -37.4765833333333, "Longitude": 144.012638888889},
            {"Site ID": 407712, "Latitude": -36.0801944444444, "Longitude": 144.566583333333},
            {"Site ID": 407732, "Latitude": -35.8813333333333, "Longitude": 144.101416666667},
            {"Site ID": 407735, "Latitude": -35.87975, "Longitude": 144.147361111111},
            {"Site ID": 407779, "Latitude": -35.8549166666667, "Longitude": 144.333916666667},
            {"Site ID": 409207, "Latitude": -35.9425833333333, "Longitude": 144.464666666667},
            {"Site ID": 409214, "Latitude": -35.4235555555556, "Longitude": 143.764777777778},
            {"Site ID": 409399, "Latitude": -35.4085833333333, "Longitude": 143.619027777778},
            {"Site ID": 409701, "Latitude": -35.9926388888889, "Longitude": 144.5085}
        ],
        "color": "red"
    },
    "Loddon River": {
        "locations": [
    {"Site ID": 405306, "Latitude": -36.8626944444444, "Longitude": 145.733388888889},
    {"Site ID": 405307, "Latitude": -36.8798611111111, "Longitude": 145.619666666667},
    {"Site ID": 405308, "Latitude": -36.7839722222222, "Longitude": 145.570833333333},
    {"Site ID": 405310, "Latitude": -37.1816944444444, "Longitude": 145.368972222222},
    {"Site ID": 405321, "Latitude": -37.1056944444444, "Longitude": 146.369194444444},
    {"Site ID": 405323, "Latitude": -36.8252777777778, "Longitude": 145.084611111111},
    {"Site ID": 405325, "Latitude": -37.21675, "Longitude": 145.435388888889},
    {"Site ID": 405327, "Latitude": -36.8768888888889, "Longitude": 145.474666666667},
    {"Site ID": 405328, "Latitude": -37.5258055555556, "Longitude": 145.7735},
    {"Site ID": 405329, "Latitude": -37.1639444444444, "Longitude": 145.422166666667},
    {"Site ID": 405335, "Latitude": -37.2695833333333, "Longitude": 144.947805555556},
    {"Site ID": 405336, "Latitude": -36.8013888888889, "Longitude": 145.622527777778},
    {"Site ID": 405341, "Latitude": -37.2101388888889, "Longitude": 145.413083333333},
    {"Site ID": 405342, "Latitude": -37.1731388888889, "Longitude": 145.252388888889},
    {"Site ID": 405700, "Latitude": -36.7162777777778, "Longitude": 145.16925},
    {"Site ID": 405702, "Latitude": -36.5866666666667, "Longitude": 145.1275},
    {"Site ID": 405704, "Latitude": -36.6770833333333, "Longitude": 145.257944444444},
    {"Site ID": 405705, "Latitude": -36.5402777777778, "Longitude": 145.017416666667},
    {"Site ID": 405708, "Latitude": -36.5589444444444, "Longitude": 145.215666666667},
    {"Site ID": 405709, "Latitude": -36.5246944444444, "Longitude": 145.198166666667},
    {"Site ID": 405710, "Latitude": -36.5114166666667, "Longitude": 145.179416666667},
    {"Site ID": 405712, "Latitude": -36.5100277777778, "Longitude": 145.092444444444},
    {"Site ID": 405717, "Latitude": -36.538, "Longitude": 145.019888888889},
    {"Site ID": 405720, "Latitude": -36.1863055555556, "Longitude": 145.141083333333},
    {"Site ID": 405730, "Latitude": -36.5040833333333, "Longitude": 145.310916666667},
    {"Site ID": 405738, "Latitude": -36.1088055555556, "Longitude": 145.611777777778},
    {"Site ID": 405758, "Latitude": -36.1816944444444, "Longitude": 145.433555555556},
    {"Site ID": 405779, "Latitude": -36.1807222222222, "Longitude": 145.382472222222},
    {"Site ID": 409215, "Latitude": -36.0176111111111, "Longitude": 144.961027777778},    
            {"Site ID": 405200, "Latitude": -36.6170277777778, "Longitude": 145.219583333333},
            {"Site ID": 405201, "Latitude": -37.0916111111111, "Longitude": 145.2025},
            {"Site ID": 405202, "Latitude": -37.0198888888889, "Longitude": 145.108944444444},
            {"Site ID": 405203, "Latitude": -37.2468055555556, "Longitude": 145.889305555556},
            {"Site ID": 405204, "Latitude": -36.3797777777778, "Longitude": 145.393527777778},
            {"Site ID": 405205, "Latitude": -37.4136666666667, "Longitude": 145.564027777778},
            {"Site ID": 405209, "Latitude": -37.3177222222222, "Longitude": 145.712888888889},
            {"Site ID": 405212, "Latitude": -37.0989444444445, "Longitude": 145.056138888889},
            {"Site ID": 405214, "Latitude": -37.1583055555556, "Longitude": 146.113083333333},
            {"Site ID": 405215, "Latitude": -37.2295833333333, "Longitude": 146.207222222222},
            {"Site ID": 405217, "Latitude": -37.3827222222222, "Longitude": 145.473083333333},
            {"Site ID": 405218, "Latitude": -37.29125, "Longitude": 146.187833333333},
            {"Site ID": 405219, "Latitude": -37.3308888888889, "Longitude": 146.13075},
            {"Site ID": 405226, "Latitude": -36.6211111111111, "Longitude": 145.307194444444},
            {"Site ID": 405227, "Latitude": -37.3674722222222, "Longitude": 146.056944444444},
            {"Site ID": 405228, "Latitude": -36.9510833333333, "Longitude": 145.283638888889},
            {"Site ID": 405229, "Latitude": -36.6349166666667, "Longitude": 144.870861111111},
            {"Site ID": 405230, "Latitude": -36.6041388888889, "Longitude": 144.804777777778},
            {"Site ID": 405231, "Latitude": -37.3470555555556, "Longitude": 145.288361111111},
            {"Site ID": 405232, "Latitude": -36.1776944444444, "Longitude": 145.119055555556},
            {"Site ID": 405234, "Latitude": -36.887, "Longitude": 145.68275},
            {"Site ID": 405237, "Latitude": -36.7623611111111, "Longitude": 145.585833333333},
            {"Site ID": 405238, "Latitude": -37.1202777777778, "Longitude": 144.857277777778},
            {"Site ID": 405240, "Latitude": -37.0596388888889, "Longitude": 145.055055555556},
            {"Site ID": 405241, "Latitude": -37.2903611111111, "Longitude": 145.827555555556},
            {"Site ID": 405245, "Latitude": -37.0383055555556, "Longitude": 146.053583333333},
            {"Site ID": 405246, "Latitude": -36.5908333333333, "Longitude": 145.351138888889},
            {"Site ID": 405247, "Latitude": -36.5908611111111, "Longitude": 145.625777777778},
            {"Site ID": 405248, "Latitude": -36.8544444444445, "Longitude": 144.914583333333},
            {"Site ID": 405251, "Latitude": -36.9688333333333, "Longitude": 145.785444444444},
            {"Site ID": 405253, "Latitude": -36.7128333333333, "Longitude": 145.173944444444},
            {"Site ID": 405264, "Latitude": -37.5193888888889, "Longitude": 146.076083333333},
            {"Site ID": 405269, "Latitude": -36.4566944444444, "Longitude": 145.399055555556},
            {"Site ID": 405270, "Latitude": -36.4388333333333, "Longitude": 145.347444444444},
            {"Site ID": 405274, "Latitude": -37.1059444444445, "Longitude": 145.605138888889},
            {"Site ID": 405276, "Latitude": -36.2414444444445, "Longitude": 145.286944444444},
            {"Site ID": 405282, "Latitude": -36.7460277777778, "Longitude": 145.139722222222},
            {"Site ID": 405287, "Latitude": -37.36625, "Longitude": 145.13025},
            {"Site ID": 405288, "Latitude": -37.3733333333333, "Longitude": 145.127361111111},
            {"Site ID": 405290, "Latitude": -37.2872777777778, "Longitude": 145.049305555556},
            {"Site ID": 405291, "Latitude": -37.0320555555556, "Longitude": 145.208833333333},
            {"Site ID": 405294, "Latitude": -36.7121944444445, "Longitude": 145.760444444444},
            {"Site ID": 405297, "Latitude": -36.1044722222222, "Longitude": 144.858888888889}
        ],
        "color": "green"
    }
}

# Function to read dataset based on Site ID
def read_dataset_for_site_id(site_id):
    dataset_path = f"Datasets/{site_id}.csv"
    try:
        df = pd.read_csv(dataset_path)
        return df
    except FileNotFoundError:
        print(f"Dataset for Site ID {site_id} not found.")
        return None

# Function to generate chart data for a specific river and date
def generate_chart_for_river_and_date(river_name, site_id, selected_date):
    df = read_dataset_for_site_id(site_id)
    if df is None:
        return "<div>Data not available for the selected site.</div>"

    # Filtering the data for the selected date
    df_filtered = df[df['Date'] == selected_date]

    # Check if required columns exist
    # required_columns = ['Time', 'Flow', 'Height', 'Rainfall']
    required_columns = ['Time', 'Flow', 'Height']
    for column in required_columns:
        if column not in df_filtered.columns:
            return "<div>Data not available for the selected date.</div>"

    if df_filtered.empty:
        return "<div>No data available for the selected date.</div>"

    time_points = df_filtered['Time']
    flow_data = df_filtered['Flow'].replace(0, 10).fillna(10)
    height_data = df_filtered['Height'].replace(0, 10).fillna(10)
    # rainfall_data = df_filtered['Rainfall'].replace(0, 10).fillna(10)


    fig, ax1 = plt.subplots(figsize=(10, 6))
    # ax1.plot(time_points, rainfall_data, color='b', linewidth=2, marker='o', label=f'{river_name} Rainfall (mm)')
    ax1.plot(time_points, height_data, color='g', linewidth=2, marker='o', label=f'{river_name} Water Height (m)')
    
    # Setting the x-axis range to the time points from the dataset
    ### Changed this to 0-23, ignoring actual data availability to display all times
    ax1.set_xlim(0, 23)
    ax1.set_xlabel('Time (hours)')
    
    # Set x-axis ticks to display time from the dataset
    # ax1.set_xticks(time_points)  # Ensure all hours from the dataset are labeled
    ### Change this to 0-24, drawing ticks for all 24 hours
    ax1.set_xticks(range(0,24))
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):02d}'))  # Format labels as '01', '02', etc.
    
    # Setting the y-axis for Rainfall / Water Height (mm)
    ax1.set_ylabel('Rainfall / Water Height (mm)')
    ax1.set_ylim(0.01, 4)
    ax1.set_yticks(np.arange(0.01, 4.1, 0.5))  # Increment by 0.5
    
    ax1.set_title(f'{river_name} Data for {selected_date}')
    ax2 = ax1.twinx()
    
    # Setting the y-axis for Water Flow (cfs)
    ax2.plot(time_points, flow_data, color='r', linewidth=2, marker='o', label=f'{river_name} Water Flow (cfs)')
    ax2.set_ylabel('Water Flow (cfs)')
    ax2.set_ylim(0.01, 4)
    ax2.set_yticks(np.arange(0.01, 4.1, 0.5))  # Increment by 0.5
    
    # Display legends for both axes
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

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

    victoria_map = folium.Map(location=[-37.4713, 144.7852], zoom_start=7, tiles="OpenStreetMap")

    for river_name, river_info in rivers_data.items():
        river_group = folium.FeatureGroup(name=f"<span style='color:{river_info['color']};'>{river_name}</span>")
        for location in river_info["locations"]:
            site_id = location["Site ID"]
            popup_html = generate_chart_for_river_and_date(river_name, site_id, selected_date)
            folium.Marker(
                location=[location["Latitude"], location["Longitude"]],
                popup=folium.Popup(popup_html, max_width=400),
                icon=folium.Icon(color=river_info["color"], icon="info-sign"),
            ).add_to(river_group)
        river_group.add_to(victoria_map)

    all_coords = [loc for river_info in rivers_data.values() for loc in river_info["locations"]]
    if all_coords:
        victoria_map.fit_bounds([[loc["Latitude"], loc["Longitude"]] for loc in all_coords])

    folium.LayerControl().add_to(victoria_map)

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