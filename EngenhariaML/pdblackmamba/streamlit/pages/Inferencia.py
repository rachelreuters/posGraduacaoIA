from matplotlib.patches import  Rectangle
import requests
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

st.markdown("## BLACK MAMBA Converteu a cesta??? ")
st.markdown("""
            ### Preencha o formulário e descubra!
            """)

col1, col2= st.columns(2)

lat =  col1.number_input("Posição do arremesso de latitude da quadra", 
                         step=0.0001, format="%.4f", min_value=33.2, max_value=34.2)

lon =  col1.number_input("Posição do arremesso de longitude da quadra" , 
                         step=0.0001, format="%.4f", min_value=-118.54  , max_value=-118.0)

minutes_remaining= col1.number_input("Minutos faltantes para fechar o quarto", step=1)

period= col2.number_input("Quarto no momento do arremesso", min_value=1, max_value=4, step=1)

playoffs =  1 if col2.checkbox("Etapa de playoffs?") else 0

shot_distance=   col2.number_input("Distância  da cesta em pés" , step=1) 

input_data = {
    "lat": lat,
    "lon": lon,
    "minutes_remaining": minutes_remaining,
    "period": period,
    "playoffs": playoffs,
    "shot_distance": shot_distance
    }

record = list(input_data.values())


if st.button("Converteu ? ",  icon= "🏀", key='custom_button', use_container_width= True):
    
    response = requests.post('http://127.0.0.1:5001/invocations', json= {'inputs': [record] }  )

    predict = response.json()['predictions'][0]

    st.markdown("## :green[Converteu 😀] " if predict else "## :red[Não converteu 😭 ]" )

    color = "green" if predict else "red" 

    fig, ax = plt.subplots(figsize=(10, 7))

    court = Rectangle((-118.54, 33.2), 0.6, 1, edgecolor="#B97E49", facecolor="none", linewidth=2)

    ax.add_patch(court)

    image = mpimg.imread("lakers.gif")

    ax.imshow(image, extent=[-118.54, -118 ,33.2, 34.2], aspect='auto', alpha=0.9,zorder=9)


    ax.scatter(lon, lat,s=280, c=color,marker='x' ,alpha=1, label='Arremesso',zorder=10, linewidths=5)
    plt.ticklabel_format(style="plain", axis="both",useOffset=False)
    plt.title('Arremesso na quadra', fontsize=15)
    plt.ylim(33.18, 34.22)
    plt.xlim(-118.55, -117.99)
    plt.xlabel('Lon')
    plt.ylabel('Lat')
    plt.legend('')
    st.pyplot(fig)


