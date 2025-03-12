import streamlit as st

def show_page():
    st.write("### FAQ")
    st.write("Here you will see frequently asked questions. And also the answers for those questions.")

    st.write("""
    **Q: What is fraud detection?**

    A: Fraud detection is the process of identifying suspicious or unauthorized activities that could indicate fraud. This can include things like credit card fraud, insurance fraud, or even fake online reviews.

    **Q: How does using a large dataset help detect fraud?**

    A: Large datasets contain a lot of information about past transactions and activities. By analyzing this data, we can identify patterns and anomalies that might indicate fraudulent behavior. The more data we have, the more accurate our detection can be.

    **Q: What kind of data is used for fraud detection?**

    A: It depends on the type of fraud, but it can include:
    - Transaction details (date, time, amount, location)
    - User behavior (login times, browsing history)
    - Demographic information (age, location)
    - Device information (IP address, device ID)

    **Q: How does a computer know what is fraud and what isn't?**

    A: We use machine learning algorithms to train computers to recognize patterns of fraud. These algorithms learn from past examples of fraudulent and non-fraudulent activity. When a new transaction comes in, the computer can assess the likelihood of it being fraudulent based on what it has learned.

    **Q: Is it possible to detect all fraud?**

    A: Unfortunately, no. Fraudsters are constantly developing new techniques. However, by using large datasets and advanced analytics, we can significantly reduce the amount of fraud that goes undetected.

    **Q: What are some examples of fraud that can be detected?**

    A:
    - Credit card fraud (unauthorized transactions)
    - Insurance fraud (false claims)
    - Identity theft (using someone else's information)
    - Online scams (phishing, fake websites)

    **Q: How is my personal information protected?**

    A: We use strict security measures to protect your data, including encryption and access controls. We also comply with all relevant data privacy regulations.
    """)
