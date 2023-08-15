import re
from datetime import date, datetime
import os
import base64
from typing import List, Union
import pandas as pd  # dataframe

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import requests
import urllib3
from dotenv import dotenv_values
import streamlit as st

from langchain import LLMChain, LLMMathChain
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, create_pandas_dataframe_agent, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI  # , GPT4All
from langchain.prompts import BaseChatPromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import AgentAction, AgentFinish, HumanMessage

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition)

import stapp  # file
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)
config = dotenv_values(".env")

activities_url = "https://www.strava.com/api/v3/athlete/activities"
os.environ["OPENAI_API_KEY"] = config.get('OPENAI_API_KEY')
os.environ["SENDGRID_API_KEY"] = config.get('SENDGRID_API_KEY')
llm = ChatOpenAI(model_name='gpt-4-32k', temperature=0.2)
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

def convert_to_miles(num):
    return ((num/m_conv_factor)*1000)/1000.0

def calc_days_btwn(training_start_date, marathon_date): 
    training_start_date = training_start_date.split(',')[1].strip()
    training_start_date = datetime.strptime(training_start_date, '%Y-%m-%d') 
    training_start_date = datetime.date(training_start_date)

    delta = marathon_date - training_start_date
    return delta.days-1

#number of workouts in Strava data
def num_rows_in_dataframe(df):
    return len(df.index)

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def validate_email(email):
    # pass the regular expression and the string into the fullmatch() method
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False

class CustomPromptTemplate(BaseChatPromptTemplate):
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)] 
    
class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Marathon Day" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Marathon Day:")[-1].strip()},
                log=llm_output,
            )
        elif marathon_date in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split(marathon_date)[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            try:
                action = match.group(1).strip()
                action_input = match.group(2)
                # Return the action and action input
                return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
            except ValueError as e:
                response = str(e)
                if not response.startswith("Could not parse LLM output: `"):
                    raise e
                response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")

st.title('Personal Marathon Training plan generator')
st.subheader('enter details below')
today = datetime.now()
jul_30 = date(today.year, 7, 30)
dec_31 = date(today.year, 12, 31)

with st.form('my_form'):
    strava_token_input = st.text_input('Strava API token')
    email = st.text_input('Email to send plan to')
    dates = st.date_input(
        "Select your training dates for the year: it should be from the first training date to the marathon date",
        (jul_30, date(today.year, 12, 10)),
        jul_30,
        dec_31
    )
    st.write('Training date: ', dates[0], "Marathon date: ", dates[1])
    training_start_date = dates[0]
    marathon_date = dates[1]
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not validate_email(email):
            st.error("invalid email", icon="🚨")
            st.cache_data()
            VALIDANSWERS = False
        elif training_start_date > marathon_date:
            st.error("Start date must be earlier than end date", icon="🚨")
            st.cache_data()
            VALIDANSWERS = False     
        try:
            r = requests.get('https://www.strava.com/api/v3/activities?access_token=' + strava_token_input)
            r.raise_for_status()
            VALIDANSWERS = True
        except requests.exceptions.HTTPError as e:
            print(e)
            st.error("Check Strava token")
            st.cache_data()
            VALIDANSWERS = False
        if VALIDANSWERS:
            header = {'Authorization': 'Bearer ' + strava_token_input} 
            params = {'per_page': 200, 'page': 1} #max 200 per page, can only do 1 page at a time
            my_dataset = requests.get(activities_url, headers=header, params=params).json() #activities 1st page
            page = 0
            for x in range(1,5): #loop through 4 pages of strava activities
                page +=1 
            params = {'per_page': 200, 'page': page}
            my_dataset += requests.get(activities_url, headers=header, params=params).json() 
        
            activities = pd.json_normalize(my_dataset)
            cols = ['name', 'type', 'distance', 'moving_time', 'total_elevation_gain', 'start_date']
            activities = activities[cols]
            activities = activities[activities["start_date"].str.contains("YEAR-YOU-WANT-TO-IGNORE-WORKOUTS") == False] 
            activities.to_csv('data_files/activities.csv', index=False)

            runs = activities.loc[activities['type'] == 'Run']
            runs.to_csv('data_files/runs.csv', index=False)
            data_run_df = pd.read_csv('data_files/runs.csv')
            data_activity_df = pd.read_csv('data_files/activities.csv')
            m_conv_factor = 1609

            data_run_df['distance'] = data_run_df['distance'].map(lambda x: convert_to_miles(x))
            data_activity_df['distance'] = data_activity_df['distance'].map(lambda x: convert_to_miles(x))
            #convert moving time secs to mins, hours
            data_run_df['moving_time'] = data_run_df['moving_time'].astype(str).map(lambda x: x[7:]) #slices off 0 days from moving_time
            data_run_df.to_csv('data_files/runs.csv')
            data_activity_df = pd.read_csv('data_files/activities.csv')
            tools = [
                Tool(
                    name = "rows in csv",
                    func = lambda df: num_rows_in_dataframe(df),
                    description="use to get the number of rows in csv file to calculate averages from running data"
                ),
                Tool(
                    name="Calculator",
                    func=llm_math_chain.run,
                    description="useful for when you need to answer questions about math"
                ),
                Tool(
                    name="days_between",
                    func=lambda day1, day2=marathon_date: calc_days_btwn(day1, day2),
                    description="useful for when you need to calculate the number of days between two dates of type date, like between the training start date and the marathon date"
                )
            ]
            pd_agent_run = create_pandas_dataframe_agent(OpenAI(temperature=0.3), data_run_df, verbose=True) 
            pd_agent_activity = create_pandas_dataframe_agent(OpenAI(temperature=0.3), data_activity_df, verbose=True)
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            num_workouts = agent.run(f'Calculate the number of days between these two dates representing the number of workouts in the plan: {marathon_date} and {training_start_date}. You have access to tools')
            pd_run_output = pd_agent_run.run("Calculate average distance and maximum distance in miles and average moving time and maximum moving time in minutes. Additionally, calculate any other running statistics from the data you think would be helpful to consider in marathon training.")
            coach_template = """training_start_date:{training_start_date}, marathon_date:{marathon_date}, pd_run_output: {pd_run_output}, num_workouts: {num_workouts}, plan: {plan}
            """
            example_prompt = PromptTemplate(input_variables=["training_start_date", "marathon_date", "pd_run_output", "num_workouts", "plan"], template=coach_template)
            prefix = """
            You are a marathon trainer tasked with crafting one personalized marathon training plan containing  according to your student's previous runs and activities.
            For each week you should recommend 2 cross-training activities and no more than one run greater than 14 miles per week. The longest run you recommend should be 20 miles around 2 weeks before {marathon_date}.
            There should be {num_workouts} workouts for {num_workouts} days, and there should be easy workouts and rest days in the week leading up to {marathon_date}.
            Slightly modify the following example marathon training plans based on your student and the days beginning on {training_start_date} up until {marathon_date} to create one personalized training plan with each workout on a new line: 
            """
            suffix = """
            training_start_date: {training_start_date}, marathon_date: {marathon_date}, pd_run_output: {pd_run_output}, num_workouts: {num_workouts}
            """
            few_shot_prompt_template = FewShotPromptTemplate(
                examples=stapp.examples, 
                example_prompt=example_prompt, 
                prefix=prefix,
                suffix=suffix, 
                input_variables=["marathon_date", "training_start_date", "pd_run_output", "num_workouts"]
            )
            output_parser = CustomOutputParser()
            #LLM chain consisting of the LLM and a prompt
            llm_chain = LLMChain(llm=llm, prompt=few_shot_prompt_template)
            tool_names = [tool.name for tool in tools]
            agent = LLMSingleActionAgent(
                llm_chain=llm_chain, 
                output_parser=output_parser,
                stop=["\Marathon Day:"], 
                allowed_tools=tool_names
            )
            agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
            plan = agent_executor({"marathon_date":marathon_date, "training_start_date": training_start_date, "pd_run_output": pd_run_output, "num_workouts": num_workouts})
            print('plan being print ', plan)
            plan = plan['output']
            plan = str(plan).replace('\n','<br />') #each workout on new line
            message = Mail(
                from_email='langchain_sendgrid_marathon_trainer@sf.com',
                to_emails=email,
                subject='Your AI-generated marathon training plan',
                html_content='<strong>Good luck at your marathon on %s</strong>!\n\nYour plan is attached.'%(marathon_date))
            styleN = getSampleStyleSheet()['Normal']
            story = []

            pdf_name = 'plan.pdf'
            doc = SimpleDocTemplate(
                pdf_name,
                pagesize=letter,
                bottomMargin=.4 * inch,
                topMargin=.6 * inch,
                rightMargin=.8 * inch,
                leftMargin=.8 * inch)
            P = Paragraph(plan, styleN)
            story.append(P)

            doc.build(
                story,
            )
            with open(pdf_name, 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()

            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName('personal_ai_generated_marathon_training_plan.pdf'),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.attachment = attachedFile
            sg = SendGridAPIClient()
            response = sg.send(message)
            if response.status_code == 202:
                st.success("Email sent! Check your email for your personal training plan")
                print(f"Response Code: {response.status_code} \n Message sent!")
            else:
                st.warning("Email not sent--check email")






