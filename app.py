import streamlit as st
import pickle
import numpy as np

# Initialize session state
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = False

# Ticket History Storage
if "ticket_history" not in st.session_state:
    st.session_state.ticket_history = []
if len(st.session_state.ticket_history) > 5:
    st.session_state.ticket_history.pop(0)
# ==============================
# PAGE CONFIG 
# ==============================
st.set_page_config(
    page_title="Customer Support Ticket Intelligence",
    page_icon="🎧",
    layout="wide"
)
st.markdown("""
<style>
.metric-card{
    padding:20px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-size:18px;
    font-weight:500;
}

.metric-value{
    font-size:30px;
    font-weight:bold;
}
.accuracy{
    background: linear-gradient(135deg,#36d1dc,#5b86e5);
}
.precision{
    background: linear-gradient(135deg,#ff7e5f,#feb47b);
}
.recall{
    background: linear-gradient(135deg,#43cea2,#185a9d);
}
.f1{
    background: linear-gradient(135deg,#f7971e,#ffd200);
}
</style>
""", unsafe_allow_html=True)
# ==============================
# LOAD MODEL + VECTORIZER
# ==============================
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ==============================
# MODEL METRICS
# ==============================
accuracy = 0.72
precision = 0.71
recall = 0.70
f1_score = 0.70

# ==============================
# MODERN CSS STYLING
# ==============================
st.markdown("""
<style>

/* Main Background */
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Headings */
h1, h2, h3 {
    color: #e2e8f0;
    font-weight: 600;
}

/* Text Area */
textarea {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#16a34a);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 600;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#16a34a,#15803d);
}

/* Result Card */
.result-card {
    background: #111827;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
    margin-top: 20px;
}

/* Prediction Box */
.prediction {
    background: linear-gradient(90deg,#14532d,#166534);
    padding: 15px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

/* Confidence Box */
.confidence {
    background: linear-gradient(90deg,#1e3a8a,#1d4ed8);
    padding: 15px;
    border-radius: 10px;
    font-size: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR (MODEL INFO)
# ==============================
with st.sidebar:
    st.header("📊 Model Insights")
    st.write("**Model:** Logistic Regression")
    st.write("**Accuracy:** 72%")
    st.write("**Features:** TF-IDF (Unigram + Bigram)")
    st.write(
        "This model classifies customer support tickets "
        "into company categories using NLP language patterns."
    )

# ==============================
# MAIN TITLE
# ==============================
st.title("🎧 Customer Support Ticket Intelligence")
st.caption("AI-powered NLP system for automatic ticket classification")

tab1, tab2 = st.tabs(["💬 Message", "📜 History"])
st.divider()
with tab1:
    st.divider()
    st.subheader("📊 Model Performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.markdown("""
      <div class="metric-card accuracy">
          Accuracy
          <div class="metric-value">72%</div>
      </div>
      """, unsafe_allow_html=True)

    with col2:
      st.markdown("""
      <div class="metric-card precision">
        Precision
        <div class="metric-value">71%</div>
    </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card recall">
            Recall
            <div class="metric-value">70%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card f1">
            F1 Score
            <div class="metric-value">70%</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# USER INPUT
# ==============================

# Clear textbox if reset was clicked
    if st.session_state.reset_trigger:
        st.session_state.user_text = ""
        st.session_state.reset_trigger = False

    user_input = st.text_area(
        "Enter Customer Support Message:",
        height=150,
        placeholder="Example: my order has not arrived yet",
        key="user_text"
    )

    def get_severity(text):
        urgent_words = [
            "urgent", "angry", "refund", "cancel",
            "not working", "worst", "complaint",
            "delay", "fraud", "error"
        ]

        score = sum(word in text.lower() for word in urgent_words)

        if score >= 2:
            return "🔴 High Priority"
        elif score == 1:
            return "🟠 Medium Priority"
        else:
            return "🟢 Low Priority"

# ==============================
# PREDICTION FUNCTION
# ==============================
    def predict_category(text):
        text_vector = vectorizer.transform([text])
        prediction = model.predict(text_vector)[0]
        probabilities = model.predict_proba(text_vector)
        confidence = np.max(probabilities) * 100
        return prediction, confidence

# ==============================
# SUGGESTION FUNCTION  
# ==============================
    def generate_suggestions(category, text):

        text = text.lower()

        suggestions = []

    # -------- AMAZON / ORDER ISSUES --------
        if "Amazon" in category or "order" in text:
            suggestions = [
                "📦 Check your order status in the Orders section.",
                "🔎 Verify delivery address and tracking details.",
                "📞 Contact delivery support if delayed more than 24 hrs."
            ]

    # -------- PAYMENT / BANK --------
        elif "PayPal" in category or "payment" in text or "refund" in text:
            suggestions = [
                "💳 Verify transaction status in payment history.",
                "🧾 Keep transaction ID ready before contacting support.",
                "⏳ Refunds may take 3–5 business days."
            ]

    # -------- TECH / DEVICE SUPPORT --------
        elif "Apple" in category or "device" in text or "app" in text:
            suggestions = [
                "🔄 Restart the application or device once.",
                "📲 Update the app to the latest version.",
                "⚙️ Check settings or reinstall if issue continues."
            ]

    # -------- TRAVEL / BOOKING --------
        elif "Air" in category or "flight" in text or "ticket" in text:
            suggestions = [
                "✈️ Check booking status using confirmation number.",
                "📧 Review confirmation email for updates.",
                "📞 Contact airline support for urgent travel issues."
            ]

    # -------- DEFAULT --------
        else:
            suggestions = [
                "📝 Provide more details about your issue.",
                "📷 Attach screenshots when contacting support.",
                "📞 Reach customer care for faster resolution."
            ]

        return suggestions

# ==============================
# BUTTON ACTION
# ==============================

    col1, col2 = st.columns(2)
# -------- ANALYZE BUTTON --------
    with col1:
        analyze = st.button("🚀 Analyze Ticket", key="analyze_btn")

# -------- RESET BUTTON --------
    with col2:
        reset = st.button("🔄 Reset")

# RESET ACTION
    if reset:
        st.session_state.reset_trigger = True
        st.rerun()

# ANALYZE ACTION
    if analyze:

        if user_input.strip() == "":
            st.warning("Please enter a message.")

        else:
            prediction, confidence = predict_category(user_input)
            suggestions = generate_suggestions(prediction, user_input)

        # Save to history
            ticket_data = {
                "text": user_input,
                "category": prediction,
                "confidence": round(confidence, 2),
                "status": "❌ Unsolved"
            }

            st.session_state.ticket_history.insert(0, ticket_data)

            # Keep only last 5
            st.session_state.ticket_history = st.session_state.ticket_history[:5]

            st.divider()

        # RESULT CARD
            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown("### 📌 Predicted Category")
            st.markdown(
                f'<div class="prediction">{prediction}</div>',
                unsafe_allow_html=True
            )

            st.markdown("### 📊 Confidence Score")
            st.markdown(
                f'<div class="confidence">{confidence:.2f}%</div>',
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

            severity = get_severity(user_input)

            st.markdown("### 🚨 Ticket Priority")
            st.info(severity)

            st.markdown("### 💡 Suggested Actions")

            for s in suggestions:
                st.write(s)
with tab2:

    st.header("📜 Ticket History")

    if len(st.session_state.ticket_history) == 0:
        st.info("No tickets analyzed yet.")

    else:

        # Table header
        col1, col2, col3 = st.columns([5,3,2])

        with col1:
            st.markdown("**Ticket**")

        with col2:
            st.markdown("**Category**")

        with col3:
            st.markdown("**Status**")

        st.divider()

        # Table rows
        for i, ticket in enumerate(st.session_state.ticket_history):

            col1, col2, col3 = st.columns([5,3,2])

            with col1:
                st.write(ticket["text"])

            with col2:
                st.write(ticket["category"])

            with col3:
                status_options = ["🔵 Open", "❌ Unsolved", "✅ Solved"]

                status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(ticket["status"]) if ticket["status"] in status_options else 0,
                    key=f"status_{i}",
                    label_visibility="collapsed"
    )

                ticket["status"] = status
st.divider()