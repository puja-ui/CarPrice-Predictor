import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def cut_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def cut_categories1(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
    return categorical_map

@st.cache
def load_data():
    df = pd.read_csv("cardata1.csv")
    
    spec_chars = ["kmpl",'km/kg']
    for char in spec_chars:
        df['mileage'] = df['mileage'].str.replace(char, '')
    
    spec_chars = ["bhp"]
    for char in spec_chars:
        df['max_power'] = df['max_power'].str.replace(char, '')

    spec_chars = ["CC"]
    for char in spec_chars:
        df['engine'] = df['engine'].str.replace(char, '')

    df = df[["brand","year","selling_price","km_driven","fuel","owner","mileage","engine","max_power","seats"]]
    df=df.rename({"mileage":"mileage_kmpl", "engine":"engine_CC","max_power":"max_power_bhp"}, axis=1)
    df = df[df["selling_price"].notnull()]
    df = df.dropna()
    brand_map = cut_categories(df.brand.value_counts(), 15)
    df['brand'] = df['brand'].map(brand_map)
    owner_map = cut_categories1(df.owner.value_counts(), 10)
    df['owner'] = df['owner'].map(owner_map)
    seats_map = cut_categories1(df.seats.value_counts(), 10)
    df['seats'] = df['seats'].map(seats_map)
    df = df.dropna()
    df['max_power_bhp'] = df['max_power_bhp'].apply(pd.to_numeric, errors='coerce')
    df['engine_CC'] = df['engine_CC'].apply(pd.to_numeric, errors='coerce')
    df['mileage_kmpl'] = df['mileage_kmpl'].apply(pd.to_numeric, errors='coerce')
    return df

df = load_data()

def explore_page():
    st.title("Explore Car-prices")

    data = df["fuel"].value_counts()
    explode = (0, 0,  0,  0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(data,explode=explode, labels= data.index, autopct="%1.1f",  startangle=90, textprops={'fontsize': 7})
    ax1.axis("equal")
    st.write("""Number of cars sold with different kind of fuels""")

    st.pyplot(fig1)

    st.title(""" """)
    st.title(""" """)
    st.title(""" """)
    st.write("""Mean Price based on Brands""")
    data = df.groupby(["brand"])["selling_price"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.title(""" """)
    st.title(""" """)
    st.title(""" """)
    st.write("""Mean Price based on Seat numbers""")
    data = df.groupby(["seats"])["selling_price"].mean().sort_values(ascending=True)
    st.line_chart(data)