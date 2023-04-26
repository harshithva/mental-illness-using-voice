import streamlit as st
import speech_recognition as sr
import numpy as np
import pickle

loaded_model = pickle.load(open('C:/Users/Harshith/Documents/codes/python/mental-illness/trained_model.sav', 'rb'))



def mental_illness_prediction(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)

    if (prediction[0] == 0):
        return 'Mental Health is good'
    else:
        return 'Mental Health is not good'
# Define questions and corresponding keywords
questions = [
    "In the past week, how often have you experienced a lack of interest or pleasure in your usual activities?",
    "In the past week, how often have you felt sad, down, or blue?",
    "In the past week, how often have you had difficulty falling asleep or staying asleep?",
    "In the past week, how often have you felt hopeless about the future?",
    "In the past week, how often have you had difficulty concentrating or making decisions?",
    "In the past week, how often have you experienced a significant change in appetite or weight?",
    "In the past week, how often have you felt fatigued or low on energy?",
    "In the past week, how often have you experienced feelings of worthlessness or excessive guilt?",
    "In the past week, how often have you had thoughts of death or suicide?"
]

keywords = {
    0: ["not at all", "none", "never"],
    1: ["a little bit", "rarely", "slightly"],
    2: ["moderately", "sometimes", "occasionally"],
    3: ["quite a bit", "often", "frequently"],
    4: ["extremely", "always", "constantly","yes"]
}



# Define Streamlit app
def app():
    st.set_page_config(page_title="Questionnaire", page_icon=":clipboard:", layout="wide")
    # Initialize question index if not already set
    if 'question_idx' not in st.session_state:
        st.session_state.question_idx = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = []
    if 'completed' not in st.session_state:
        st.session_state.completed= False

    # Start button
    if st.button("Start"):
        st.write("Recording audio...")

        # Record audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        
        # Convert audio to text
        text = r.recognize_google(audio)

        # Display recorded text
        st.write("Recorded Text: ", text)

        # Assign score based on keywords
        score = 0
        for key, value in keywords.items():
            for keyword in value:
                if keyword in text:
                    score = key
                    break
        
        # Display score
            # Append score to scores array
        st.session_state.scores.append(score)
        st.write("Score: ", score)

    # Next button
    if st.button("Next"):
        # Increment question index
        st.session_state.question_idx += 1

        # Check if all questions have been answered
        if st.session_state.question_idx >= len(questions):
            print(st.session_state.scores)
            # st.write(mental_illness_prediction(scores))
            # st.write("All questions answered. Thank you!")
            st.session_state.question_idx = 0  # Reset question index
            st.session_state.completed = True   
        else:
            # Display next question
            question = questions[st.session_state.question_idx]
            # st.markdown(f"<h1 style='text-align: center;'>{question}</h1>", unsafe_allow_html=True)

    # Display initial question

    if st.session_state.completed == True:
        st.markdown(f"<h1 style='text-align: center;'>{mental_illness_prediction(st.session_state.scores)}</h1>", unsafe_allow_html=True)
    else:
        question = questions[st.session_state.question_idx]
        st.markdown(f"<h1 style='text-align: center;'>{question}</h1>", unsafe_allow_html=True)
        


if __name__ == '__main__':
    app()
