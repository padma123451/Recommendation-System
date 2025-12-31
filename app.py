
import streamlit as st
from recommendation_system import new, recommend

       
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:cyan;padding:13px"> 
    <h1 style ="color:black;text-align:center;"> 🎬 Movie recommendation System</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    selected_movie = st.selectbox("Select a movie",new["title"].values) 
    number_of_recommendations = st.slider("Number of recommendations",1,10,5)
    result =""
    if st.button("Recommend"):
        recommendations = recommend(selected_movie)
        st.subheader("Recommended movies:")
        for movie in recommendations[:number_of_recommendations]:
            st.write(movie)

if __name__ == "__main__":
             main()


       