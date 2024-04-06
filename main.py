import os
import time

import streamlit as st
from datetime import datetime, timedelta

import config
from agents import FactsGenerator
from preprocess import process_data
added_color = "green"
removed_color = "red"


if 'question_answers' not in st.session_state:
    st.session_state['question_answers'] = []

if 'agent' not in st.session_state:
    st.session_state['agent'] = FactsGenerator()

# Instantiate FactsGenerator
# facts_generator = FactsGenerator()

def display(selected_date):
    for ques in st.session_state['question_answers']:
        data = ques['factsByDay']
        if str(selected_date) in data:
            # st.subheader(f"Facts for {ques['question']}")
            st.markdown(f"<h5>{ques['question']}", unsafe_allow_html=True)
            with st.container():
                for key, value in data[str(selected_date)].items():
                    if key == "added":
                        st.markdown(
                            f'<div style="border: 1px solid {added_color}; padding:10px; border-radius:5px; margin-top:10px;">'
                            f'<p style="color:{added_color};"><strong>{key.capitalize()}:</strong> {value}</p>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    elif key == "removed":
                        st.markdown(
                            f'<div style="border: 1px solid {removed_color}; padding:10px; border-radius:5px; margin-top:10px;">'
                            f'<p style="color:{removed_color};"><strong>{key.capitalize()}:</strong> {value}</p>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div style="border: 1px solid #f0f0f0; padding:10px; border-radius:5px; margin-top:10px;">'
                            f'<p><strong>{key.capitalize()}:</strong> {value}</p>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
        else:
            st.write("No facts available for the selected date.")



def create_container_with_border(question, added, removed, changed):
    st.markdown(f"<h2 style='border-bottom: 1px solid black;'>{question}</h2>", unsafe_allow_html=True)
    st.markdown(f'<ul><li style="color:{added_color};">{added[0]}</li></ul>', unsafe_allow_html=True)
    st.markdown(f'<ul><li style="color:{removed_color};">{removed[0]}</li></ul>', unsafe_allow_html=True)
    st.markdown(f'<ul><li>{changed[0]}</li></ul>', unsafe_allow_html=True)

def displayw(selected_date):
    for item in st.session_state['question_answers']:
        # print(selected_date)
        question = item["question"]
        facts = item["factsByDay"]
        if selected_date in facts:
            added = [facts[selected_date]['add']]
            removed = [facts[selected_date]['remove']]
            changed = [facts[selected_date]['change']]
            create_container_with_border(question, added, removed, changed)
        else:
            st.write("No facts available for the selected date.")


# Function to display Question and Answer Screen
def question_answer_screen():
    # global question_answers
    print(st.session_state['question_answers'])
    st.title("Question and Answer Screen")
    if len(st.session_state['question_answers']) > 0:
        start_date = datetime.strptime(list(st.session_state['question_answers'][0]['factsByDay'].keys())[0], "%Y-%m-%d")
        end_date = datetime.strptime(list(st.session_state['question_answers'][0]['factsByDay'].keys())[-1], "%Y-%m-%d")

        selected_date = st.slider("Select Date", start_date, end_date, value=start_date, format="YYYY-MM-DD").strftime("%Y-%m-%d")
        displayw(selected_date)


# Function to display Document Addition Screen
def document_addition_screen():
    # global question_answers
    st.title("Document Addition Screen")
    input_text = st.text_area("Enter some URL in every new line:")
    question = st.text_area("Enter Question")
    if st.button('Process'):
        if input_text:
            # Processing the data
            with st.spinner('Processing...'):
                url = input_text.split("\n")
                processed_result = st.session_state['agent'].process_data(url, question)
                for date, facts in processed_result.items():
                    st.subheader(f"Date: {date}")  # Display the date retrieved from the data

                    # Display facts with checkboxes and color coding
                    for category, fact in facts.items():
                        approved_status = st.checkbox(f"{category.capitalize()}: {fact}", key=time.time())

                st.session_state['question_answers'].append({"question":question, "factsByDay": processed_result})
                print(st.session_state.question_answers)
                # question_answer_screen(question_answers)

        else:
            st.warning("Please enter some text to process.")


# Main function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Document Addition", "Question and Answer"))

    if page == "Question and Answer":
        question_answer_screen()
    elif page == "Document Addition":
        document_addition_screen()


if __name__ == "__main__":
    main()
