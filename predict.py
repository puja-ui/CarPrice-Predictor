import streamlit as st
import pickle
import numpy as np

def get_model():
    with open('save_steps.pkl', 'rb') as file:
        save_data = pickle.load(file)
    return save_data

save_data = get_model()

regressor_loaded = save_data["model"]
leb_brand = save_data["leb_brand"]
leb_fuel = save_data["leb_fuel"]
leb_owner = save_data["leb_owner"]

def predict_page():
    st.title("Indian Cars price predictor")
    st.write(""" Fill out the information to get the possible car-price """)

    brands = ("Maruti", "Skoda", "Honda", "Hyundai", "Toyota", "Ford", "Renault",
       "Mahindra", "Tata", "Chevrolet", "Datsun", "Jeep", "Mercedes-Benz",
       "Other", "Audi", "Volkswagen", "BMW", "Nissan", "Lexus", "Jaguar",
       "Volvo", "Fiat")
    
    fuels = ("Diesel", "Petrol", "LPG", "CNG")

    owners = ("First Owner", "Second Owner", "Third Owner",
       "Fourth & Above Owner")

    seats = (5.,  4.,  7.,  8.,  6.,  9., 10.)
    
    brand = st.selectbox("Brands", brands)
    #weight = st.number_input("Enter your weight (in kgs)")
    year = st.slider("Year purchased", 1990, 2021, 1994)
    km_driven = st.slider("Kilometre Driven", 0, 2360500,250254)
    fuel = st.selectbox("fuels", fuels)
    owner = st.selectbox("owner", owners)
    mileage_kmpl = st.slider("Mileage(kmpl)", 0, 43, 7)
    engine_CC = st.slider("Engine(CC)", 600, 4000, 1715)
    max_power_bhp = st.slider("Maximum power(bhp)", 30, 400, 125)
    seat = st.selectbox("Seat number", seats)

    submited = st.button("Get price")
    if submited:
        inpt = np.array([[brand, year, km_driven,fuel, owner, mileage_kmpl, engine_CC, max_power_bhp, seat]])
        inpt[:,0] = leb_brand.transform(inpt[:,0])
        inpt[:,3] = leb_fuel.transform(inpt[:,3])
        inpt[:,4] = leb_owner.transform(inpt[:,4])
        inpt = inpt.astype(float)

        carprice = regressor_loaded.predict(inpt)
        st.info(f"The estimated Price is {carprice[0]:.2f}")