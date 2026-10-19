import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="My AI Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 The Groq Chatbot")
st.write("AI assistant with Web Search, Calculator and Chat Memory.")

# ------ 1. Sidebar: Configuration -------
with st.sidebar:
    st.header("⚙️ Configuration")

    user_api_key = st.text_input(
        "Enter your Groq API Key:",
        type="password"
    )

    st.info("Your Groq API key powers the AI and its tools.")

    st.header("🎭 Persona")

    persona = st.text_area(
        "System Prompt:",
        value=(
            "You are a helpful AI assistant. "
            "Use browser search for current information, recent news, "
            "and questions requiring online research. "
            "Use code execution for accurate mathematical calculations. "
            "Include source URLs when answering from web search. "
            "Never claim you searched the web if you did not."
        )
    )

    if st.button("Reset Chat & Apply Persona"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("🧰 Available Tools")
    st.write("🔎 Groq Built-in Web Search")
    st.write("🧮 Groq Code Interpreter")

# ------ 2. Memory Vault -------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------ 3. Display Chat History -------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------ 4. Chat Input and Logic -------
if user_query := st.chat_input("Ask anything or search the web..."):

    if not user_api_key:
        st.error("Please enter your Groq API key in the sidebar.")

    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)

        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        try:
            # Initialize Groq client
            client = Groq(api_key=user_api_key)

            # Prepare conversation with system persona
            api_messages = [
                {
                    "role": "system",
                    "content": persona
                }
            ]

            api_messages.extend(st.session_state.messages)

            with st.chat_message("assistant"):
                with st.spinner("Thinking and using tools..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=api_messages,
                        tools=[
                            {"type": "browser_search"},
                            {"type": "code_interpreter"}
                        ],
                        temperature=0.2
                    )

                    bot_answer = (
                        response.choices[0].message.content
                        or "No text response was returned."
                    )

                    st.markdown(bot_answer)

            # Save response for conversation memory
            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_answer
            })

        except Exception as e:
            st.error(f"Groq API error: {e}")
            st.info(
                "Check your API key, model availability, "
                "and whether built-in tools are supported for your account."
            )
