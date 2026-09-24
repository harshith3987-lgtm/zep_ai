import requests
import streamlit as st

st.set_page_config(
    page_title="Zepto Support Assistant",
    layout="centered"
)

# ---------- Styling ----------
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }

    .title {
        text-align: center;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 15px;
        margin-bottom: 30px;
    }

    .answer-box {
        padding: 18px;
        border: 1px solid #dddddd;
        border-radius: 8px;
        margin-top: 20px;
        background-color: #fafafa;
    }

    .footer {
        text-align: center;
        color: #777777;
        font-size: 12px;
        margin-top: 35px;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Header ----------
st.markdown(
    '<div class="title">Zepto Support Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Support for Zepto policies and services</div>',
    unsafe_allow_html=True
)


# ---------- Input ----------
query = st.text_input(
    "Enter your question",
    placeholder="Example: What is the delivery time?"
)


# ---------- Button ----------
if st.button("Submit", use_container_width=True):

    if not query.strip():
        st.warning("Please enter a question.")

    else:
        st.markdown(
            '<div class="answer-box">',
            unsafe_allow_html=True
        )

        st.subheader("Answer")

        response = requests.post(
            "http://127.0.0.1:7860/ask",
            json={"query": query}
        )

        if response.status_code == 200:
            result = response.json()

            st.write(result["answer"])
            st.write("Sources:", ", ".join(result["sources"]))
            st.write("Confidence:", result["confidence"])

        else:
            st.error("Unable to process the request.")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- Footer ----------
st.markdown(
    '<div class="footer">Zepto Support Assistant</div>',
    unsafe_allow_html=True
)