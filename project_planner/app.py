import streamlit as st
#from utils import run_master_agent, format_project_template
#from agents import master_agent
import asyncio

st.set_page_config(page_title="UseCase Generator", layout="wide")
 
st.title("UseCase Generator")
st.write("Please fill in the details below. Fields marked with * are mandatory.")
 
with st.form("usecase_form"):
    usecase_name = st.text_input("UseCase Name *")
    usecase_objectives = st.text_area("UseCase Objectives *", height=150)
    budget_constraints = st.number_input("Budget Constraints ($) *", min_value=0.0, step=1000.0)
    expected_timeline = st.text_input("Expected Timeline (e.g., '5 months') *")
    sensitivity_requirements = st.text_area("Sensitivity Requirements (Optional)", height=100)
    description = st.text_area("Description (Optional)", height=100)
 
    submitted = st.form_submit_button("Submit")
 
    if submitted:
        if not usecase_name or not usecase_objectives or not budget_constraints or not expected_timeline:
            st.error("Please fill all mandatory fields!")
        else:
            st.success("Form submitted successfully!")
            st.write("### Submitted Details:")
            st.write(f"**UseCase Name:** {usecase_name}")
            st.write(f"**UseCase Objectives:** {usecase_objectives}")
            st.write(f"**Budget Constraints:** ${budget_constraints:,.2f}")
            st.write(f"**Expected Timeline:** {expected_timeline}")
            if sensitivity_requirements:
                st.write(f"**Sensitivity Requirements:** {sensitivity_requirements}")
            if description:
                st.write(f"**Description:** {description}")
 
            #project_template = format_project_template(
            #    usecase_name, usecase_objectives, budget_constraints, expected_timeline, sensitivity_requirements, description
            #)
 
            st.write("### Agent Processing Output:")
            #asyncio.run(run_master_agent(master_agent, project_template, st))
 