import streamlit as st
import pickle

# Modelni yuklash
model_path = "or.pkl"  # Yuklangan fayl bilan bir xil joyda saqlang
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error(f"Model fayli topilmadi: {model_path}. Iltimos, faylni to'g'ri joylashtiring.")
    st.stop()
except Exception as e:
    st.error(f"Modelni yuklashda xato: {str(e)}")
    st.stop()

st.set_page_config(page_title="Predictive Maintenance", page_icon="🔧", layout="centered")
st.markdown(
    """
    <style>
    /* Custom background */
    .stApp {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #34495E;
        font-family: 'Arial', sans-serif;
    }
    /* Card-like layout for the input form */
    .main {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.2);
        max-width: 750px;
        margin: 20px auto;
        border: 2px solid #f39c12;
    }
    /* Button styling */
    .stButton>button {
        background-color: #e74c3c !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 15px 35px !important;
        font-size: 20px !important;
        font-weight: bold;
        border: none;
        box-shadow: 0px 8px 15px rgba(231, 76, 60, 0.4);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #c0392b !important;
        box-shadow: 0px 12px 20px rgba(192, 57, 43, 0.4);
        transform: scale(1.05);
    }
    /* Section header */
    h1 {
        color: #2E4053;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 25px;
        text-shadow: 2px 2px 5px #f39c12;
    }
    /* Prediction result styling */
    .result-section {
        background-color: #f7f1e3;
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
    }
    .result-section h3 {
        font-size: 1.7rem;
        color: #34495E;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .result-section p {
        font-size: 1.2rem;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .icon {
        font-size: 1.8rem;
        margin-right: 10px;
        color: #2980b9;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Mashinani Bashoratli Texnik Xizmat Ko'rsatishni Bashorat Qilish")
st.markdown("<h3 style='color:#34495E;'>🔧 Bashorat qilish uchun qurilma ma'lumotlarini kiritish</h3>", unsafe_allow_html=True)
udi = st.text_input("UDI (Unique Device Identifier)", "")  
product_id = st.text_input("Product ID (e.g., L47181)", "")  
type_value = st.text_input("Type (e.g., 1)", "")  
air_temp = st.number_input("Air Temperature (K)", min_value=0.0, max_value=500.0)
process_temp = st.number_input("Process Temperature (K)", min_value=0.0, max_value=500.0)
rotational_speed = st.number_input("Rotational Speed (rpm)", min_value=0.0, max_value=3000.0)
torque = st.number_input("Torque (Nm)", min_value=0.0, max_value=1000.0)
tool_wear = st.number_input("Tool Wear (min)", min_value=0.0, max_value=500.0)
if st.button("Predict Maintenance Needs"):
    try:
        product_id_numeric = int(product_id[1:])  
    except ValueError:
        product_id_numeric = 0  
    try:
        type_value_numeric = int(type_value)
    except ValueError:
        type_value_numeric = 0  
    input_data = [[udi, product_id_numeric, type_value_numeric, air_temp, process_temp, rotational_speed, torque, tool_wear]]
    prediction = model.predict(input_data)
    st.markdown(f"<div class='result-section'><h3>🔧 Prediction: {'Failure Expected' if prediction[0] == 1 else 'No Failure Expected'}</h3></div>", unsafe_allow_html=True)
