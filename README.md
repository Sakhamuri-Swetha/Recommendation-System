# 🎬 K-Drama Recommendation System

Welcome to the **K-Drama Recommendation System**! This project helps users discover new K-Dramas based on the similarity of their features such as **genre**, **actors**, **directors**, and **plot**. Using **TF-IDF Vectorization** and **Cosine Similarity**, this system provides recommendations based on the user's input K-Drama title.

## 📑 Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [References](#references-used)

## 💻 Installation

### 📦 Prerequisites:
- Python 3.x
- pip (Python package installer)

### 🔽 Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/kdrama-recommendation.git
cd kdrama-recommendation
```

### ⚙️ Step 2: Create a Virtual Environment
1. To create a virtual environment, run the following command:
```bash
python -m venv venv
```
2. Activate the virtual environment: (Windows)
```bash
.\venv\Scripts\activate 
```
## 🚀 Usage

1. To run the K-Drama Recommendation System, use **Streamlit**:
```bash
   streamlit run app.py
```
2. Once the app is running, open the local URL in your browser.

- Enter the title of a K-Drama in the input field to get similar recommendations.
- Select a title from the filtered list and see recommendations based on similarity.
-The app will show the title, poster image, genre, rating, and a summary of the recommended K-Dramas.

## 🛠️ Technologies Used

- **Python 3.x** 🐍
- **Streamlit** 🌐 – For creating the web interface
- **Pandas** 📊 – For data handling
- **Scikit-learn** 🔧 – For TF-IDF Vectorization and Cosine Similarity
- **HTML/CSS** 🎨 – For styling the UI of the Streamlit app
- **Selenium** 🧑‍💻 – For web scraping and data collection
- **Excel** 📈 – For storing and organizing collected data
## 📚 References

- [Netflix Recommender System GitHub Repository](https://github.com/aravind0402/netflix_recommender)
- [K-Drama Presentation on Google Slides](https://docs.google.com/presentation/d/1L2oTeLCcCUhKpN-N1U_s9oXZq3NeXnXy9SNoO9Nekig/edit#slide=id.gd109d3e046_0_100)
- [List of Korean Dramas - Wikipedia](https://en.wikipedia.org/wiki/List_of_Korean_dramas)
