import streamlit as st
import requests
import json
import boto3
import time
import os
from dotenv import load_dotenv
load_dotenv()
aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
aws_region_name = os.environ["AWS_REGION"]
s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name="us-east-1")
 
def get_presigned_url(folder_name, file_name, file_type):
    # API Gateway URL
    api_url = os.environ["API_URL"]
    api_url = f"{api_url}?folder_name=videos&file_name={file_name}&file_type={file_type}"
   
    response = requests.get(api_url)
    response_data = response.json()
    return response_data['upload_url']
 
def check_md_file(bucket_name, folder_name, file_name):
    #
    md_file_key = f"{folder_name}/{file_name}.md"
    try:
        s3.head_object(Bucket=bucket_name, Key=md_file_key)
        return True
    except:
        return False
 
def get_md_file_content(bucket_name, folder_name, file_name):
   
    md_file_key = f"{folder_name}/{file_name}.md"
    response = s3.get_object(Bucket=bucket_name, Key=md_file_key)
    content = response['Body'].read().decode('utf-8')
    content = content.strip('"').replace('\\"', '"').replace('\\n', '\n')
    content = content.replace('\\t', '\t').replace('\\r', '\r')
    return content
 
def check_sqa_file(bucket_name, folder_name, file_name):
   
    sqa_file_key = f"{folder_name}/{file_name}_sqa.json"
    try:
        s3.head_object(Bucket=bucket_name, Key=sqa_file_key)
        return True
    except:
        return False
   
def get_sqa_file_content(bucket_name, folder_name,file_name):
    sqa_file_key = f"{folder_name}/{file_name}_sqa.json"
    response = s3.get_object(Bucket=bucket_name, Key=sqa_file_key)
    content = response['Body'].read().decode('utf-8')
    sqa_data = json.loads(content)
    return sqa_data
 
 
def display_data(data,notes):
    st.header("Summary")
    st.write(data["Summary"])
    st.header("Notes")
    st.markdown(notes)
    st.header("Questions")
    # Initialize session state to store user answers if not already done
    if 'user_answers' not in st.session_state:
        st.session_state['user_answers'] = [None] * len(data['Questions'])
 
    # Create a form for batch submission
    with st.form("questions_form"):
        for idx, q in enumerate(data["Questions"], 1):
            st.subheader(f"Question {idx}: {q['Question']}")
            st.session_state['user_answers'][idx-1] = st.radio(
                f"Select an option for Question {idx}:",
                options=q["Options"],
                index=None,
                key=f"question_{idx}"
            )
        submit = st.form_submit_button("Submit All")
 
    if submit:
        for idx, (q, user_answer) in enumerate(zip(data["Questions"], st.session_state['user_answers']), 1):
            if user_answer:
                correct_answer = q["CorrectAnswer"]
                if q["Options"].index(user_answer) + 1 == correct_answer:
                    st.success(f"Question {idx}: Correct! The answer is {q['Options'][correct_answer-1]}.")
                else:
                    st.error(f"Question {idx}: Incorrect. The correct answer is {q['Options'][correct_answer-1]}.")
            else:
                st.warning(f"Question {idx}: No option selected.")
 
 
st.title("Video TO Notes Generation, Summary, Q&A")
sidebar = st.sidebar
uploaded_file = sidebar.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
 
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    folder_name = uploaded_file.name.split(".")[0]
    # Generating presigned url
    presigned_url = get_presigned_url(folder_name, file_name, file_type)
   
    # Uploading file using presigned url
    headers = {'Content-Type': uploaded_file.type}
    with st.spinner(f'Uploading {file_name}...'):
        start_time = time.time()
        print(start_time,"start")
        response = requests.put(presigned_url, data=uploaded_file.read(), headers=headers)
        end_time = time.time()
        print(end_time,"end")
        print(end_time - start_time,"final")
    if response.status_code == 200:
        st.success(f"File '{file_name}' uploaded successfully!")
       
       
        bucket_name = os.environ["BUCKET_NAME"]
        md_file_found = False
        sqa_file_found = False
        # Max waiting time 5 minutes
        max_wait_time = 300
        start_time = time.time()
 
        # Checking for the .md file until we find it in the s3 bucket
        with st.spinner("Generating Summary, Notes and Q&A..."):
            while not md_file_found and not sqa_file_found and (time.time() - start_time) < max_wait_time:
                # searching for .md file every 5 seconds
                time.sleep(5)  
                md_file_found = check_md_file(bucket_name, folder_name, file_name.split('.')[0])
                sqa_file_found = check_sqa_file(bucket_name, folder_name, file_name.split('.')[0])
        # display notes once the file is found
        if md_file_found and sqa_file_found:
            md_content = get_md_file_content(bucket_name, folder_name, file_name.split('.')[0])
            sqa_content = get_sqa_file_content(bucket_name, folder_name, file_name.split('.')[0])
            display_data(sqa_content,md_content)
           
        else:
            st.error(f"Failed to find the file '{file_name}' within the wait time.")
       
    else:
        st.error(f"Failed to upload file. Status code: {response.status_code}")