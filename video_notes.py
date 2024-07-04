# import streamlit as st
# import requests
# import json
# import boto3
# import time
# import os
# from dotenv import load_dotenv
# load_dotenv()

# def get_presigned_url(folder_name, file_name, file_type):
#     # API Gateway URL
#     api_url = f"{os.environ['API_URL']}?folder_name={folder_name}&file_name={file_name}&file_type={file_type}"
    
#     response = requests.get(api_url)
#     response_data = response.json()
#     return response_data['upload_url']

# aws_access_key_id = os.environ["AWS_ACCESS_KEY"]
# aws_secret_access_key = os.environ["AWS_ACCESS_KEY_ID"]
# aws_region_name = os.environ["AWS_REGION"]
# def check_md_file(bucket_name, folder_name, file_name):
#     s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id,
#                       aws_secret_access_key=aws_secret_access_key,
#                       region_name=aws_region_name)
#     md_file_key = f"{folder_name}/{file_name}.md"
#     try:
#         s3.head_object(Bucket=bucket_name, Key=md_file_key)
#         return True
#     except:
#         return False
    
# def get_md_file_content(bucket_name, folder_name, file_name):
#     s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id,
#                       aws_secret_access_key=aws_secret_access_key,
#                       region_name=aws_region_name)
#     md_file_key = f"{folder_name}/{file_name}.md"
#     response = s3.get_object(Bucket=bucket_name, Key=md_file_key)
#     content = response['Body'].read().decode('utf-8')
#     content = content.strip('"').replace('\\"', '"').replace('\\n', '\n')
#     content = content.replace('\\t', '\t').replace('\\r', '\r')
#     return content

# st.title("Video TO Notes Generation")
# sidebar = st.sidebar
# uploaded_file = sidebar.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

# if uploaded_file is not None:
#     file_name = uploaded_file.name
#     file_type = uploaded_file.type
#     folder_name = uploaded_file.name.split(".")[0]
#     # Generating presigned url 
#     presigned_url = get_presigned_url(folder_name, file_name, file_type)
    
#     # Uploading file using presigned url
#     headers = {'Content-Type': uploaded_file.type}
#     with st.spinner(f'Uploading {file_name}...'):
#         start_time = time.time()
#         print(start_time,"start")
#         response = requests.put(presigned_url, data=uploaded_file.read(), headers=headers)
#         end_time = time.time()
#         print(end_time,"end")
#         print(end_time - start_time,"final")
#     if response.status_code == 200:
#         st.success(f"File '{file_name}' uploaded successfully!")
        
        
#         bucket_name = 'edtech-app-version-bucket'
#         md_file_found = False
#         # Max waiting time 5 minutes
#         max_wait_time = 300 
#         start_time = time.time()

#         # Checking for the .md file until we find it in the s3 bucket
#         with st.spinner("Generating Notes..."):
#             while not md_file_found and (time.time() - start_time) < max_wait_time: 
#                 # searching for .md file every 5 seconds
#                 time.sleep(5)  
#                 md_file_found = check_md_file(bucket_name, folder_name, file_name.split('.')[0])

#         # display notes once the file is found
#         if md_file_found:
#             md_content = get_md_file_content(bucket_name, folder_name, file_name.split('.')[0])
#             # st.write(md_content)
#             # st.write("//////////////////////////////////////////////////////////////////")
#             # cont = str(md_content)
#             st.markdown(md_content)
#         else:
#             st.error(f"Failed to find the file '{file_name}' within the wait time.")
#     else:
#         st.error(f"Failed to upload file. Status code: {response.status_code}")

# # # # api_url = f"https://par1ulposi.execute-api.us-east-1.amazonaws.com/default/edtech-s3-presigned-url?file_name={file_name}&file_type={file_type}"


# # # st.markdown('''## Counting and Addition\n\nCounting is the process of determining the number of elements or objects in a group or set. It is one of the fundamental mathematical skills that children learn from an early age. In the given text, the main focus is on counting penguins and introducing basic addition concepts.\n\n### Counting\n- Counting involves assigning a number to each object in a set, one by one, in a specific order.\n- In the text, Gwen asks the reader to count the penguins with her, starting from one and going up to three.\n- Counting helps children understand the concept of one-to-one correspondence between numbers and objects.\n\n### Introduction to Addition\n- Addition is the process of combining two or more quantities to find the total.\n- In the text, Gwen introduces addition by asking the reader to count the total number of penguins after adding two more penguins to the initial group.\n- The text starts with a simple addition problem: 3 + 2 = 5\n- It progresses to more complex additions, such as 5 + 2 = 7 and 7 + 3 = 10.\n\n### Step-by-Step Addition Process\n- Identify the first number (the starting point).\n- Identify the second number (the number to be added).\n- Count forward from the first number, adding the value of the second number.\n- The final number reached is the sum or the total.\n\nFor example, in the text:\n1. Start with 5 penguins.\n2. Add 2 more penguins.\n3. Count forward from 5: "5, 6, 7" (adding 2 counts).\n4. The total number of penguins is 7.\n\n### Applications\n- Counting and addition are fundamental skills used in everyday life, such as counting objects, measuring quantities, and performing basic calculations.\n- These skills lay the foundation for more advanced mathematical concepts and problem-solving abilities.\n\nThe text aims to introduce counting and addition concepts to young learners in a fun and engaging manner, using relatable characters and scenarios.''')

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
# s3 = boto3.client('s3')
def get_presigned_url(folder_name, file_name, file_type):
    # API Gateway URL
    api_url = f"https://par1ulposi.execute-api.us-east-1.amazonaws.com/default/edtech-s3-presigned-url?folder_name={folder_name}&file_name={file_name}&file_type={file_type}"
    
    response = requests.get(api_url)
    response_data = response.json()
    return response_data['upload_url']

def check_md_file(bucket_name, folder_name, file_name):
    # s3 = boto3.client('s3')
    md_file_key = f"{folder_name}/{file_name}.md"
    try:
        s3.head_object(Bucket=bucket_name, Key=md_file_key)
        return True
    except:
        return False
    
def get_md_file_content(bucket_name, folder_name, file_name):
    # s3 = boto3.client('s3')
    md_file_key = f"{folder_name}/{file_name}.md"
    response = s3.get_object(Bucket=bucket_name, Key=md_file_key)
    content = response['Body'].read().decode('utf-8')
    content = content.strip('"').replace('\\"', '"').replace('\\n', '\n')
    content = content.replace('\\t', '\t').replace('\\r', '\r')
    return content

st.title("Video TO Notes Generation")
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
        
        
        bucket_name = 'edtech-app-version-bucket'
        md_file_found = False
        # Max waiting time 5 minutes
        max_wait_time = 300 
        start_time = time.time()

        # Checking for the .md file until we find it in the s3 bucket
        with st.spinner("Generating Notes..."):
            while not md_file_found and (time.time() - start_time) < max_wait_time: 
                # searching for .md file every 5 seconds
                time.sleep(5)  
                md_file_found = check_md_file(bucket_name, folder_name, file_name.split('.')[0])

        # display notes once the file is found
        if md_file_found:
            md_content = get_md_file_content(bucket_name, folder_name, file_name.split('.')[0])
            # st.write(md_content)
            # st.write("//////////////////////////////////////////////////////////////////")
            # cont = str(md_content)
            st.markdown(md_content)
        else:
            st.error(f"Failed to find the file '{file_name}' within the wait time.")
    else:
        st.error(f"Failed to upload file. Status code: {response.status_code}")

# # # api_url = f"https://par1ulposi.execute-api.us-east-1.amazonaws.com/default/edtech-s3-presigned-url?file_name={file_name}&file_type={file_type}"


# # st.markdown('''## Counting and Addition\n\nCounting is the process of determining the number of elements or objects in a group or set. It is one of the fundamental mathematical skills that children learn from an early age. In the given text, the main focus is on counting penguins and introducing basic addition concepts.\n\n### Counting\n- Counting involves assigning a number to each object in a set, one by one, in a specific order.\n- In the text, Gwen asks the reader to count the penguins with her, starting from one and going up to three.\n- Counting helps children understand the concept of one-to-one correspondence between numbers and objects.\n\n### Introduction to Addition\n- Addition is the process of combining two or more quantities to find the total.\n- In the text, Gwen introduces addition by asking the reader to count the total number of penguins after adding two more penguins to the initial group.\n- The text starts with a simple addition problem: 3 + 2 = 5\n- It progresses to more complex additions, such as 5 + 2 = 7 and 7 + 3 = 10.\n\n### Step-by-Step Addition Process\n- Identify the first number (the starting point).\n- Identify the second number (the number to be added).\n- Count forward from the first number, adding the value of the second number.\n- The final number reached is the sum or the total.\n\nFor example, in the text:\n1. Start with 5 penguins.\n2. Add 2 more penguins.\n3. Count forward from 5: "5, 6, 7" (adding 2 counts).\n4. The total number of penguins is 7.\n\n### Applications\n- Counting and addition are fundamental skills used in everyday life, such as counting objects, measuring quantities, and performing basic calculations.\n- These skills lay the foundation for more advanced mathematical concepts and problem-solving abilities.\n\nThe text aims to introduce counting and addition concepts to young learners in a fun and engaging manner, using relatable characters and scenarios.''')

