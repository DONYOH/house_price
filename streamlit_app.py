import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.ml.registry import Registry

# Connexion et chargement du modele
session = get_active_session()

@st.cache_resource
def load_model():
    reg = Registry(session = session)
    return reg.get_model("house_price_rf").version("v2")

model = load_model()

# Configuration de la page
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #E8E8E8;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    .result-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-label {
        font-size: 1rem;
        color: #888888;
        margin-bottom: 0.5rem;
    }
    .result-price {
        font-size: 2.8rem;
        font-weight: 700;
        color: #4FC3F7;
    }
    </style>
    """,
    unsafe_allow_html = True
)

st.markdown('<p class="main-title">House Price Predictor</p>', unsafe_allow_html = True)
st.markdown('<p class="subtitle">Estimation du prix d\'une maison a partir du modele RandomForest optimise</p>', unsafe_allow_html = True)

# Formulaire d'inputs
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Caracteristiques**")
    area = st.number_input("Surface (m2)", min_value = 500, max_value = 20000, value = 5000, step = 100)
    bedrooms = st.selectbox("Chambres", [1, 2, 3, 4, 5, 6], index = 2)
    bathrooms = st.selectbox("Salles de bain", [1, 2, 3, 4], index = 0)
    stories = st.selectbox("Etages", [1, 2, 3, 4], index = 1)

with col2:
    st.markdown("**Equipements**")
    mainroad = st.selectbox("Route principale", ["yes", "no"])
    guestroom = st.selectbox("Chambre d'amis", ["yes", "no"])
    basement = st.selectbox("Sous-sol", ["yes", "no"])
    hotwaterheating = st.selectbox("Chauffage eau chaude", ["yes", "no"])

with col3:
    st.markdown("**Confort et situation**")
    airconditioning = st.selectbox("Climatisation", ["yes", "no"])
    parking = st.selectbox("Places de parking", [0, 1, 2, 3], index = 1)
    prefarea = st.selectbox("Zone privilegiee", ["yes", "no"])
    furnishingstatus = st.selectbox("Ameublement", ["furnished", "semi-furnished", "unfurnished"])

# Prediction
if st.button("Estimer le prix", use_container_width = True):
    # Conversion yes/no en bool
    bool_map = {"yes": True, "no": False}

    input_data = pd.DataFrame([{
        "AREA": area,
        "BEDROOMS": bedrooms,
        "BATHROOMS": bathrooms,
        "STORIES": stories,
        "MAINROAD": bool_map[mainroad],
        "GUESTROOM": bool_map[guestroom],
        "BASEMENT": bool_map[basement],
        "HOTWATERHEATING": bool_map[hotwaterheating],
        "AIRCONDITIONING": bool_map[airconditioning],
        "PARKING": parking,
        "PREFAREA": bool_map[prefarea],
        "FURNISHINGSTATUS": furnishingstatus,
        "PRICE_PER_M2": 0
    }])

    input_sp = session.create_dataframe(input_data)
    prediction = model.run(input_sp, function_name = "predict")
    result = prediction.to_pandas()
    prix = result.iloc[0, -1]

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">Prix estime</div>
            <div class="result-price">{prix:,.0f} $</div>
        </div>
        """,
        unsafe_allow_html = True
    )
    # Recap des inputs
    st.markdown("---")
    st.markdown("**Recapitulatif des parametres**")
    recap_col1, recap_col2 = st.columns(2)
    with recap_col1:
        st.text(f"Surface : {area} m2")
        st.text(f"Chambres : {bedrooms}")
        st.text(f"Salles de bain : {bathrooms}")
        st.text(f"Etages : {stories}")
        st.text(f"Parking : {parking}")
        st.text(f"Ameublement : {furnishingstatus}")
    with recap_col2:
        st.text(f"Route principale : {mainroad}")
        st.text(f"Chambre d'amis : {guestroom}")
        st.text(f"Sous-sol : {basement}")
        st.text(f"Chauffage eau chaude : {hotwaterheating}")
        st.text(f"Climatisation : {airconditioning}")
        st.text(f"Zone privilegiee : {prefarea}")