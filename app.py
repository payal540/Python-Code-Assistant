import streamlit as st
import openai
import google.generativeai as genai # type: ignore
from streamlit_feedback import streamlit_feedback # type: ignore

if 'feedback' not in st.session_state:
        st.session_state['feedback'] = {"score": None, "text": ""}


def gpt_prompt(prompt,user_api_key):
    openai.api_key = user_api_key
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.8 
    )
    return output.choices[0].message["content"].strip()

def gemini_prompt(prompt, user_api_key):
    genai.configure(api_key= user_api_key)
    model = genai.GenerativeModel('gemini-pro')
    output = model.generate_content(prompt,
                                  generation_config = genai.types.GenerationConfig(
                                  candidate_count = 1,
                                  top_p = 0.6,
                                  top_k = 5,
                                  temperature = 0.8)
                                )
    return output.text

# Function for code completion
def code_completion(code_completion_input,conditions,model_choice,user_api_key):
    prompt = f"""
    Complete the provided partial Python code to create a valid Python program:\n{code_completion_input}
    Assist according to the following conditions, ignore the condition part if nothing specified or "No" :\n{conditions}
    Return the completed code and also provide explanations wherever needed.
    """
    if(model_choice == "Gemini"):
        return gemini_prompt(prompt,user_api_key)
    elif(model_choice == "GPT-3"):
        return gpt_prompt(prompt,user_api_key)


# Function for debugging
def code_debugging_assitance(code_debug_input,conditions,model_choice,user_api_key):
    prompt = f"""Debug the following Python code and provide suggestions to fix the code : \n{code_debug_input}
    Assist according to the following conditions , ignore the condition part if nothing specified or "No" : \n{conditions}
    Return the corrected code and also provide comprehensive explanations.
    """
    if(model_choice == "Gemini"):
        return gemini_prompt(prompt,user_api_key)
    elif(model_choice == "GPT-3"):
        return gpt_prompt(prompt,user_api_key)

# Function for documentation retrieval
def documentation_retrieval(documentation_input,model_choice,user_api_key):
    prompt = f"You are a senior software teacher - Provide all information broken into sections and provide documentation for the following topic for me to build good understanding and give actionable steps to learn and use the mentioned Technology :\n{documentation_input}"
    if(model_choice == "Gemini"):
        return gemini_prompt(prompt,user_api_key)
    elif(model_choice == "GPT-3"):
        return gpt_prompt(prompt,user_api_key)



def main():
    st.title("Python Code Assistant")
    model_choice = st.sidebar.selectbox("Select the Model", ["Gemini", "GPT-3"])
    user_api_key = st.sidebar.text_input("Enter API Key")
    
    if model_choice and user_api_key:
        task = st.sidebar.selectbox("Select Task", ["Code Completion Assistance", "Code Debugging Assistance", "Documentation Retrieval and Assistance"])
        
        if task == "Code Completion Assistance":
            code_completion_input = st.text_area("Enter code for completion")
            conditions = st.text_area("Any other coments?")
            submit_button = st.button("Submit")
            if submit_button:
                output = code_completion(code_completion_input,conditions,model_choice,user_api_key)
                st.code(output, language='python') 
                streamlit_feedback(
                                    feedback_type="faces",
                                    optional_text_label="[Optional] Could you please provide us explanation or expected output for improvement ",
                                    key="feedback",
                                  )
            
        elif task == "Code Debugging Assistance":
            code_debug_input = st.text_area("Enter code for debugging")
            conditions = st.text_area("Any other comments?")
            submit_button = st.button("Submit")
            if submit_button:
                output = code_debugging_assitance(code_debug_input,conditions,model_choice,user_api_key)
                st.write("Code after debugging:", output) 
                streamlit_feedback(
                                    feedback_type="faces",
                                    single_submit=False,
                                    optional_text_label="[Optional] Could you please provide us explanation or expected output for improvement ",
                                    key="feedback",
                                  )
            
        elif task == "Documentation Retrieval and Assistance":
            documentation_input = st.text_area("Enter documentation request")
            submit_button = st.button("Submit")
            if submit_button:
                output = documentation_retrieval(documentation_input,model_choice,user_api_key)
                st.write("Documentation:", output) 
                streamlit_feedback(
                                    feedback_type="faces",
                                    single_submit=False,
                                    optional_text_label="[Optional] Could you please provide us explanation or expected output for improvement ",
                                    key="feedback",
                                  )

        user_feedback = {
            "feedback_score": st.session_state["feedback"]["score"],
            "feedback_text": st.session_state["feedback"]["text"],
        }    
    else:
        st.error("Please provide a valid API key.")

if __name__ == "__main__":
    main()

  