import streamlit as st
from conditional_workflow import app

st.set_page_config(
    page_title="College Assistant",
    page_icon="🎓"
)

st.title("🎓 College Assistant")

programme = st.selectbox(
    "Which programme are you in?",
    ["BCA", "BBA", "B.Com (H)"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask your question...")

if user_query:
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = app.invoke({
                "programme": programme,
                "messages": [("human", user_query)]
            })

            answer = result["messages"][-1].content

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })