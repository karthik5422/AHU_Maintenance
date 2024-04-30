import time
import config
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from gen_resp import generate_response,common_response

st.set_page_config(page_title="AHU Performance", layout="wide")
st.markdown("<h1 style='text-align: center;'>Critical Air Handling Unit</h1>", unsafe_allow_html=True)
st.subheader("Current Status & Possible Actions for Maintenance")

render_area = st.empty()

kpi_list = []
render_list=[]


def render_ui(df,llm_output):
    st.write("Real Time Data of Last 5 Minutes")
    st.table(df)
    if llm_output:
        # st.write("Recommendations:")
        st.write(llm_output)
    else:
        st.write("**Current Status:**")
        st.write("**AHU Performance is Normal in state**")
    st.divider()



with open('ahu_5hour_data_anamoly.csv', 'r') as f ,open('kpi_list_output.csv','w') as f_out:
    next(f)
    for l in f:
        line = l.strip().split(',')

        # Convert values to integers where necessary
        fan_stat = int(line[1])
        filter_stat = int(line[2])
        uv_lamp_stat = int(line[3])
        uv_lamp_hours_stat = int(line[4])
        sa_temp_stat = float(line[5])
        sa_set_temp_stat = float(line[6])
        chw_inlet_temp_stat = float(line[7])
        chw_outlet_temp_stat = float(line[8])
        chw_delta_temp_stat = float(line[9])
        ra_co2_stat = int(line[10])
        ra_temp_stat = float(line[11])

        row_kpi_list = []

        if fan_stat == config.kpi_ranges['fan_status']['allowed']:
            row_kpi_list.append(0)
        elif fan_stat == config.kpi_ranges['fan_status']['warning']:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(2)

        if filter_stat in config.kpi_ranges['filter_status']['allowed']:
            row_kpi_list.append(0)
        elif filter_stat in config.kpi_ranges['filter_status']['warning']:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(2)

        if uv_lamp_stat == config.kpi_ranges['uv_lamp_status']['allowed']:
            row_kpi_list.append(0)
        elif uv_lamp_stat == config.kpi_ranges['uv_lamp_status']['warning']:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(2)

        if uv_lamp_hours_stat >= config.kpi_ranges['uv_lamp_hours']['allowed'][0] and uv_lamp_hours_stat <= config.kpi_ranges['uv_lamp_hours']['allowed'][1]:
            row_kpi_list.append(0)
        elif uv_lamp_hours_stat >= config.kpi_ranges['uv_lamp_hours']['warning'][0] and uv_lamp_hours_stat <= config.kpi_ranges['uv_lamp_hours']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(2)

        if sa_temp_stat < config.kpi_ranges['sa_temp']['critical'][0] or sa_temp_stat > config.kpi_ranges['sa_temp']['critical'][1]:
            row_kpi_list.append(2)
        elif sa_temp_stat < config.kpi_ranges['sa_temp']['warning'][0] or sa_temp_stat > config.kpi_ranges['sa_temp']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(0)

        if sa_set_temp_stat < config.kpi_ranges['sa_set_temp']['critical'][0] or sa_set_temp_stat > config.kpi_ranges['sa_set_temp']['critical'][1]:
            row_kpi_list.append(2)
        elif sa_set_temp_stat < config.kpi_ranges['sa_set_temp']['warning'][0] or sa_set_temp_stat > config.kpi_ranges['sa_set_temp']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(0)

        if chw_inlet_temp_stat < config.kpi_ranges['chw_inlet_temp']['critical'][0] or chw_inlet_temp_stat > config.kpi_ranges['chw_inlet_temp']['critical'][1]:
            row_kpi_list.append(2)
        elif chw_inlet_temp_stat < config.kpi_ranges['chw_inlet_temp']['warning'][0] or chw_inlet_temp_stat > config.kpi_ranges['chw_inlet_temp']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(0)

        if chw_outlet_temp_stat < config.kpi_ranges['chw_outlet_temp']['critical'][0] or chw_outlet_temp_stat > config.kpi_ranges['chw_outlet_temp']['critical'][1]:
            row_kpi_list.append(2)
        elif chw_outlet_temp_stat < config.kpi_ranges['chw_outlet_temp']['warning'][0] or chw_outlet_temp_stat > config.kpi_ranges['chw_outlet_temp']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(0)

        if chw_delta_temp_stat < config.kpi_ranges['chw_delta_temp']['critical'][0] or chw_delta_temp_stat > config.kpi_ranges['chw_delta_temp']['critical'][1]:
            row_kpi_list.append(2)
        elif chw_delta_temp_stat < config.kpi_ranges['chw_delta_temp']['warning'][0] or chw_delta_temp_stat > config.kpi_ranges['chw_delta_temp']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(0)

        if ra_co2_stat >= config.kpi_ranges['ra_co2']['allowed'][0] and ra_co2_stat <= config.kpi_ranges['ra_co2']['allowed'][1]:
            row_kpi_list.append(0)
        elif ra_co2_stat >= config.kpi_ranges['ra_co2']['warning'][0] and ra_co2_stat <= config.kpi_ranges['ra_co2']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(2)

        if ra_temp_stat < config.kpi_ranges['ra_temp']['critical'][0] or ra_temp_stat > config.kpi_ranges['ra_temp']['critical'][1]:
            row_kpi_list.append(2)
        elif ra_temp_stat < config.kpi_ranges['ra_temp']['warning'][0] or ra_temp_stat > config.kpi_ranges['ra_temp']['warning'][1]:
            row_kpi_list.append(1)
        else:
            row_kpi_list.append(0)

        count=row_kpi_list.count(1)

        count+=row_kpi_list.count(2)

        ahu_perf=''
        if count <2 :
            ahu_perf="Normal"
        elif count >=2 and count <5:
            ahu_perf="Low"
        elif count >=5 and count <7:
            ahu_perf="Medium"
        elif count >= 7:
            ahu_perf="High"

        new_line=l.strip() +','+ ahu_perf
        line.append(ahu_perf)
        
        if ahu_perf == "Normal":
            check_list=[]
        else:
            if len(check_list) < 5:
                check_list.append(line)
            else:
                check_list.pop(0)
                check_list.append(line)

        
        if len(check_list) ==5:
            data=""
            for i in check_list:
                list_str = ','.join([str(j) for j in i ])
                data+=list_str+"\n"

            llm_output= generate_response(data)
        elif ra_temp_stat < sa_temp_stat:
            llm_output= common_response("AHU Data return air temperature is lesser than the Supply air temperature, what are the actions can be performed on AHU? you should start with 'Observations: Return Air Temperature is lesser than the Supply Air Temperature'")

        elif chw_outlet_temp_stat < chw_inlet_temp_stat:
            llm_output= common_response("AHU Data Chilled water outlet temperature is lower than the chilled water inlet temperature, what are the actions can be performed on AHU? you should start with 'Observations: Chilled Water Outlet Temperature is Lower than Chilled Water Inlet Temperature'")
        
        elif ra_temp_stat < sa_set_temp_stat:
            llm_output= common_response("AHU Data return air temperature is lesser than the Supply air set temperature, what are the actions can be performed on AHU? you should start with 'Observations: Return Air Temperature is lesser than the Supply Air Set Temperature'")
        
        else:
            llm_output= ""

        if len(render_list) < 5:
            render_list.append(line)
        else:
            render_list.pop(0)
            render_list.append(line)
    

        f_out.write(new_line + '\n')
        
        # st.write("Real Time Data For Last 5 Minutes")
        df = pd.DataFrame(render_list[0:], columns=['Date','fan_status','filter_status','uv_lamp_status','uv_lamp_hours','sa_temp','sa_set_temp','chw_inlet_temp','chw_outlet_temp','chw_delta_temp','ra_co2','ra_temp','ahu_perf'])
        render_ui(df, llm_output)
        # st.table(df)

        # st.write("Recommendation")
        # st.write(llm_output)
        # time.sleep(1)
        # st.empty()
        time.sleep(1)
