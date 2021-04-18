import os
import time
from textwrap import dedent

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from PIL import Image
import openai
#import configuration

def create_jsonlfile():

    #Paste the API KEY
    openai.api_key ="your key"   

    #Create the documents file as jsonl file
    document_path = "jsonlfiles/finaldoc.jsonl"
    file = openai.File.create(file=open(document_path), purpose='answers')
    return file

def generateAnswers(user_question,jsonl_file,temp = 0.1,maxtoken = 50):
   
#    try:
    # Api for creating answers
    response =openai.Answer.create(
        search_model="ada", 
        model="davinci", 
        question=user_question,       
        
        file=jsonl_file["id"], 
        examples_context="Corruption is dishonest or illegal behavior, especially by people in power, typically involving bribery. It can also include other acts, such as fraud, embezzlement, favoritism, and nepotism. The most common form of corruption is bribery.For further information see Section G1 of the BCG.**Additional Information** : For further information, also about what the term gifts of money covers, see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption", 
        examples=[["Can I take my client on a holiday?", "No, you cannot take your client on a holiday .**Additional Information** For further information, see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption"],["What is corruption?", "Corruption is dishonest or illegal behavior, especially by people in power, typically involving bribery **Additional Information** For further information , see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption"],["What is bribery?","Bribery  is the act of offering, promising, or giving money, gifts, or other benefit to a public official or public or private employee with the aim of receiving improper advantages. Bribery is a criminal offense worldwide. Siemens does not tolerate any form of bribery. **Additional Information** For further information check [BCG](https://compliance.siemens.cloud/bcg/responsibility.html#g)"],["What are the rules for cash payments?","Payments with Cash are specifically regulated in many jurisdictions according to money laundering or other laws. The governance for Anti-Money Laundering lies with Legal & Compliance (LC CO RFC / LC CO SFS) and supports the BizCos by appropriate processes. **Additional Information** More information can be found [Here](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,C.-Anti-Money-Laundering-(AML),5.-Cash-Handling-Rules)"]
        ],
        max_rerank=10,
        max_tokens=maxtoken,
        temperature=temp,
        stop=["\n"]
    )

    return response
   
#    except :
#        response ={"answers":["I apologize I couldnot find an answer for your query. Please as questions related to complaince or please rephrase your question"] ,
#                 "file":file }
#        return response

print("Creating file !")
file =create_jsonlfile() 
print("File created!! File id: ",file["id"])   


def Header(name, app):
    title = html.H1(name, style={"margin-top": 20})
    logo = html.Img(
        src=app.get_asset_url("logo.jpeg"), style={"float": "left", "height": 100}
    )
    return dbc.Row([ dbc.Col(logo, md=4),dbc.Col(title, md=8)])


def textbox(text, box="AI", name="Philippe"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        # thumbnail = html.Img(
        #     src=app.get_asset_url("Philippe.jpg"),
        #     style={
        #         "border-radius": 50,
        #         "height": 36,
        #         "margin-right": 5,
        #         "float": "left",
        #     },
        # )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        return html.Div([textbox])

    else:
        raise ValueError("Incorrect option for `box`.")


description = """
Philippe is the principal architect at a condo-development firm in Paris. He lives with his girlfriend of five years in a 2-bedroom condo, with a small dog named Coco. Since the pandemic, his firm has seen a  significant drop in condo requests. As such, he’s been spending less time designing and more time on cooking,  his favorite hobby. He loves to cook international foods, venturing beyond French cuisine. But, he is eager  to get back to architecture and combine his hobby with his occupation. That’s why he’s looking to create a  new design for the kitchens in the company’s current inventory. Can you give him advice on how to do that?
"""

# Authentication
#openai.api_key = os.getenv("OPENAI_KEY")

# Define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Load images
#IMAGES = {"Philippe": app.get_asset_url("Philippe.jpg")}


# Define Layout
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)

controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text"),
        dbc.InputGroupAddon(dbc.Button("Submit", id="submit"), addon_type="append"),
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("Digital Legal and Compliance Officer", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        conversation,
        controls,
        dbc.Spinner(html.Div(id="loading-component")),
    ],
)


@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        textbox(x, box="user") if i % 2 == 0 else textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]


@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks == 0 and n_submit is None:
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    name = "Philippe"

    prompt = dedent(
        f"""
    {description}
    You: Hello {name}!
    {name}: Hello! Glad to be talking to you today.
    """
    )

    # First add the user input to the chat history
    chat_history += f"You: {user_input}<split>{name}:"

    model_input = prompt + chat_history.replace("<split>", "\n")

   

    #user_ques =input("Chatbot - Enter your question :")
    response = generateAnswers(user_input, file)
    #full_answer = check_scores(model_input, response)
    # # print("Chatbot Answer :", response["answers"][0])
    # print("Chatbot Answer :", full_answer.answer)
    # if full_answer.additional:
    #     print("Additionally:\n")
    #     print(full_answer.additional)

    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=model_input,
    #     max_tokens=250,
    #     stop=["You:"],
    #     temperature=0.9,
    # )
    #model_output = response.choices[0].text.strip()
    model_output=response["answers"][0]
    chat_history += f"{model_output}<split>"

    return chat_history, None


if __name__ == "__main__":
    app.run_server(debug=False)