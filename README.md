# Customer_Support_Ticket
Project Overview
This project builds a Natural Language Processing (NLP) based system that automatically classifies customer support tickets into predefined categories. The system analyzes the text entered by the user and predicts the most relevant category using a trained machine learning model.
A Streamlit web application is used to provide an interactive interface where users can enter a support message and view the predicted category, confidence score, ticket priority, and suggested actions.
The application also maintains a history panel showing the last five analyzed tickets along with their status (Open, Solved, or Unsolved).

Features
- Automatic ticket classification using NLP
- Confidence score for predictions
- Ticket priority detection (High, Medium, Low)
- Suggested actions for resolving issues
- Ticket history panel
- Status management (Open, Solved, Unsolved)
- Interactive web interface using Streamlit

Project Structure
customer_support_ticket_project
│
├── app.py                # Streamlit web application
├── model.pkl             # Trained machine learning model
├── vectorizer.pkl        # TF-IDF vectorizer
├── dataset.csv           # Dataset used for training
├── notebook.ipynb        # Jupyter notebook for model training
└── README.md             # Project documentation

Requirements
Install the required Python libraries before running the project.
pip install streamlit
pip install scikit-learn
pip install pandas
pip install numpy

How to Run the Project
Step 1: Open the project folder in terminal or command prompt
Navigate to the project directory:
cd customer_support

Step 2: Run the Streamlit application
streamlit run app.py

Step 3: Open the web application
After running the command, Streamlit will automatically open the application in your browser.

If it does not open automatically, go to:
http://localhost:8501

How to Use the Application
- Enter a customer support message in the text box.
- Click Analyze Ticket.
- The system will display:
- Predicted ticket category
- Confidence score
- Ticket priority
- Suggested actions
- The ticket will be stored in the History panel.
- The ticket status can be updated as Open, Solved, or Unsolved.

Future Improvements
- Use larger datasets for better training
- Implement advanced NLP models such as transformer-based models
- Add real-time ticket monitoring
- Integrate with customer support platforms

## Author
Fiza Ansari
