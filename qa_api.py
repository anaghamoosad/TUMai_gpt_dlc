import os
import openai



def create_jsonlfile():

    #Paste the API KEY
    openai.api_key ="Your api key"   

    #Create the documents file as jsonl file
    file = openai.File.create(file=open("output.jsonl"), purpose='answers')
    return file

def generateAnswers(user_question,jsonl_file,temp = 0.1,maxtoken = 30):
   
   try:
    # Api for creating answers
    response =openai.Answer.create(
        search_model="ada", 
        model="davinci", 
        question=user_question,       
        
        file=jsonl_file["id"], 
        examples_context="Corruption is dishonest or illegal behavior, especially by people in power, typically involving bribery. It can also include other acts, such as fraud, embezzlement, favoritism, and nepotism. The most common form of corruption is bribery.For further information see Section G1 of the BCG.**Additional Information** : For further information, also about what the term gifts of money covers, see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption", 
        examples=[["Can I take my client on a holiday?", "No u cannot take your client on a holiday .**Additional Information** For further information, see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption"],["What is corruption?", "Corruption is dishonest or illegal behavior, especially by people in power, typically involving bribery **Additional Information** For further information , see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption"],["What is bribery?","Bribery  is the act of offering, promising, or giving money, gifts, or other benefit to a public official or public or private employee with the aim of receiving improper advantages. Bribery is a criminal offense worldwide. Siemens does not tolerate any form of bribery. **Additional Information** For further information check [BCG](https://compliance.siemens.cloud/bcg/responsibility.html#g)"],["What are the rules for cash payments?","Payments with Cash are specifically regulated in many jurisdictions according to money laundering or other laws. The governance for Anti-Money Laundering lies with Legal & Compliance (LC CO RFC / LC CO SFS) and supports the BizCos by appropriate processes. **Additional Information** More information can be found [Here](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,C.-Anti-Money-Laundering-(AML),5.-Cash-Handling-Rules)"],
        ["Was ist ein Geschenk?","Ein Geschenk ist eine freiwillige Überweisung von Geld oder anderen Vorteilen an Dritte ohne Gegenleistung. ** Zusätzliche Informationen ** Weitere Informationen finden Sie im [Compliance-Handbuch](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption"]], 
        max_rerank=10,
        max_tokens=maxtoken,
        temperature=temp,
        stop=["\n"]
    )

    return response
   
   except :
       response ={"answers":["I apologize I couldnot find an answer for your query. Please as questions related to complaince or please rephrase your question"] ,
                  "file":file }
       return response

print("Creating file !")
file =create_jsonlfile() 
print("File created!! File id: ",file["id"])   

user_ques =input("Chatbot :Enter your question :")
response =generateAnswers(user_ques,file)

print("Chatbot Answer :",response["answers"][0])



