# Define minimum and maximum values for each KPI
kpi_ranges = {
    'fan_status': {'allowed': 0, 'warning': 1, 'critical': 2},
    'filter_status': {'allowed': [0], 'warning': [1,2], 'critical': [3]},
    'uv_lamp_status': {'allowed': 0, 'warning': 1, 'critical': 2},
    'uv_lamp_hours': {'allowed': [0,9659], 'warning': [9660,9800], 'critical': [9800,100000]},
    'sa_temp': {'allowed': [17.0,23.0], 'warning': [17.0,23.0], 'critical': [15.0,25.0]},
    'sa_set_temp': {'allowed': [20.0,23.0], 'warning': [20.0,23.0], 'critical': [18.0,25.0]},
    'chw_inlet_temp': {'allowed': [8.0,12.0], 'warning': [8.0,12.0], 'critical': [6.0,14.0]},
    'chw_outlet_temp': {'allowed': [15.0,24.0], 'warning': [15.0,24.0], 'critical': [13.0,26.0]},
    'chw_delta_temp': {'allowed': [4.0,6.0], 'warning': [4.0,6.0], 'critical': [2.0,9.0]},
    'ra_co2': {'allowed': [0,949], 'warning': [950,1000], 'critical': [1000,10000]},
    'ra_temp': {'allowed': [24.0,26.0], 'warning': [24.0,26.0], 'critical': [23.0,28.0]},
}
