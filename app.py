import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from graph import workflow as app


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Academic Assistant",
    page_icon="🎓",
    layout="centered",
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
        /* Main container */
        .block-container {
            max-width: 850px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Header */
        .app-header {
            text-align: center;
            padding: 1rem 0 1.5rem 0;
        }

        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .app-subtitle {
            color: #6b7280;
            font-size: 1rem;
        }

        /* Subject selector */
        .subject-label {
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        /* Cleanly hide Streamlit header and footer */
        header[data-testid="stHeader"] {
            display: none;
        }
        footer {
            display: none;
        }
        #MainMenu {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">Academic Assistant</div>
        <div class="app-subtitle">
            Ask questions about academic policies, programs, fees, and more.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Initialize Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Subject Selection
# --------------------------------------------------

st.markdown(
    '<div class="subject-label">Select your academic program</div>',
    unsafe_allow_html=True,
)

subject = st.selectbox(
    "Academic Program",
    options=[
        "CSIT",
        "BCA",
        "BBA",
    ],
    key="subject",
    index=None,
    placeholder="Choose your program",
    label_visibility="collapsed",
)


# --------------------------------------------------
# Display Conversation History
# --------------------------------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

user_input = st.chat_input(
    "Ask a question about your academic program..."
)


# --------------------------------------------------
# Process User Query
# --------------------------------------------------

if user_input:

    # Make sure a subject has been selected
    if not st.session_state.get("subject"):

        st.warning(
            "Please select your academic program before starting a conversation."
        )

    else:

        # Add user message to session history
        human_message = HumanMessage(
            content=user_input
        )

        st.session_state.messages.append(
            human_message
        )

        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare graph state
        state = {
            "subject": st.session_state.subject,
            "query_type": "general",
            "messages": st.session_state.messages,
        }

        # Run LangGraph
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    result = app.invoke(state)

                    # Get latest AI response
                    assistant_message = result["messages"][-1]

                    # Display response
                    st.markdown(
                        assistant_message.content
                    )

                    # Update conversation history
                    st.session_state.messages = result[
                        "messages"
                    ]

                except Exception as e:

                    st.error(
                        "Something went wrong while processing your request."
                    )

                    st.exception(e)