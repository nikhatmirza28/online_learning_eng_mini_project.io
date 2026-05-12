import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="Online Learning Engagement Dashboard", layout="wide")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df['Internship_Completed'] = df['Internship_Completed'].astype('category')
    df['Placement_Interest'] = df['Placement_Interest'].astype('category')
    return df

@st.cache_data
def train_model(data: pd.DataFrame):
    features = ['Hours_Studied_Per_Week', 'Attendance_Percentage', 'Age', 'Assignments_Completed']
    X = data[features]
    y = data['Final_Exam_Score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    metrics = {
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'r2': r2_score(y_test, y_pred)
    }
    return model, X_test, y_test, y_pred, metrics

st.title("Online Learning Engagement Analysis")
st.markdown(
    "Use this dashboard to explore student engagement data, understand feature relationships, "
    "and predict final exam performance from study habits and attendance."
)

# Load data
DATA_PATH = 'mini_project_dataset_200_rows.csv'
df = load_data(DATA_PATH)

# Top summary cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Students", f"{df.shape[0]}")
col2.metric("Avg Final Score", f"{df['Final_Exam_Score'].mean():.1f}")
col3.metric("Avg Hours/Week", f"{df['Hours_Studied_Per_Week'].mean():.1f}")
col4.metric("Avg Attendance", f"{df['Attendance_Percentage'].mean():.1f}%")
col5.metric("Courses", f"{df['Subject'].nunique()}")

with st.expander("Dataset overview"):
    st.dataframe(df)
    st.write(df.describe())

# Visual exploration
st.header("Engagement Visualizations")

with st.container():
    c1, c2 = st.columns(2)
    subject_count = df['Subject'].value_counts().reset_index()
    subject_count.columns = ['Subject', 'Count']
    c1.plotly_chart(px.bar(subject_count, x='Subject', y='Count', color='Subject', title='Students by Subject'), use_container_width=True)

    corr = df[['Hours_Studied_Per_Week', 'Attendance_Percentage', 'Age', 'Assignments_Completed', 'Quiz_Score', 'Final_Exam_Score']].corr()
    c2.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', origin='lower', title='Correlation Matrix'), use_container_width=True)

with st.container():
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.box(df, x='Subject', y='Hours_Studied_Per_Week', color='Subject', title='Hours Studied Per Week by Subject'), use_container_width=True)
    c2.plotly_chart(px.box(df, x='Subject', y='Attendance_Percentage', color='Subject', title='Attendance Percentage by Subject'), use_container_width=True)

with st.container():
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.box(df, x='Subject', y='Age', color='Subject', title='Age Distribution by Subject'), use_container_width=True)
    c2.plotly_chart(px.box(df, x='Subject', y='Assignments_Completed', color='Subject', title='Assignments Completed by Subject'), use_container_width=True)

with st.container():
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.scatter(df, x='Hours_Studied_Per_Week', y='Final_Exam_Score', color='Subject', trendline='ols', title='Hours Studied vs Final Exam Score'), use_container_width=True)
    c2.plotly_chart(px.scatter(df, x='Attendance_Percentage', y='Final_Exam_Score', color='Subject', trendline='ols', title='Attendance vs Final Exam Score'), use_container_width=True)

st.header("Modeling & Prediction")
model, X_test, y_test, y_pred, metrics = train_model(df)

col1, col2, col3 = st.columns(3)
col1.metric("R-squared", f"{metrics['r2']:.3f}")
col2.metric("MSE", f"{metrics['mse']:.2f}")
col3.metric("RMSE", f"{metrics['rmse']:.2f}")

st.markdown(
    "### Actual vs Predicted Final Exam Score\n"
    "This section compares model predictions against the actual scores for the test set."
)
comparison = pd.DataFrame({
    'Hours_Studied_Per_Week': X_test['Hours_Studied_Per_Week'],
    'Attendance_Percentage': X_test['Attendance_Percentage'],
    'Age': X_test['Age'],
    'Assignments_Completed': X_test['Assignments_Completed'],
    'Actual Score': y_test,
    'Predicted Score': np.round(y_pred, 1)
}).reset_index(drop=True)
st.dataframe(comparison)

pred_fig = px.scatter(comparison, x='Actual Score', y='Predicted Score', trendline='ols', title='Actual vs Predicted Final Exam Score')
st.plotly_chart(pred_fig, use_container_width=True)

st.sidebar.header("Predict a Student's Final Exam Score")
pred_hours = st.sidebar.slider('Hours Studied Per Week', int(df['Hours_Studied_Per_Week'].min()), int(df['Hours_Studied_Per_Week'].max()), int(df['Hours_Studied_Per_Week'].median()))
pred_attendance = st.sidebar.slider('Attendance Percentage', int(df['Attendance_Percentage'].min()), int(df['Attendance_Percentage'].max()), int(df['Attendance_Percentage'].median()))
pred_age = st.sidebar.slider('Age', int(df['Age'].min()), int(df['Age'].max()), int(df['Age'].median()))
pred_assignments = st.sidebar.slider('Assignments Completed', int(df['Assignments_Completed'].min()), int(df['Assignments_Completed'].max()), int(df['Assignments_Completed'].median()))

user_input = np.array([[pred_hours, pred_attendance, pred_age, pred_assignments]])
predicted_score = model.predict(user_input)[0]

st.sidebar.markdown("### Prediction Result")
st.sidebar.metric("Estimated Final Exam Score", f"{predicted_score:.1f}")

st.sidebar.markdown("---")
st.sidebar.write("**Model coefficients**")
coefficients = pd.DataFrame({
    'Feature': ['Hours_Studied_Per_Week', 'Attendance_Percentage', 'Age', 'Assignments_Completed'],
    'Coefficient': np.round(model.coef_, 3)
})
st.sidebar.dataframe(coefficients)

st.markdown("### Feature Influence")
feature_importance = coefficients.copy()
feature_importance['abs_coeff'] = feature_importance['Coefficient'].abs()
st.bar_chart(feature_importance.set_index('Feature')['abs_coeff'])

st.markdown("---")
st.write("### Notes")
st.write(
    "- The model uses a simple linear regression with `Hours_Studied_Per_Week`, `Attendance_Percentage`, `Age`, and `Assignments_Completed` to predict `Final_Exam_Score`.\n"
    "- R-squared above 0.74 indicates strong explanatory power for this dataset.\n"
    "- Use the sidebar sliders to estimate how changes in student engagement factors affect the predicted final score."
)
