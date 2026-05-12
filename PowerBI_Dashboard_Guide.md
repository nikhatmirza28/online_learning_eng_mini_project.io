# Power BI Dashboard for Online Learning Engagement Analysis

## Overview
This guide helps you create a Power BI dashboard to visualize the online learning engagement dataset and model results. Since Power BI is primarily GUI-based, we'll focus on the steps and key configurations rather than traditional "code". However, we'll include relevant DAX measures and M code snippets where applicable.

## Prerequisites
- Power BI Desktop (free download from Microsoft)
- The CSV file: `mini_project_dataset_200_rows.csv`

## Step 1: Import Data
1. Open Power BI Desktop
2. Click "Get Data" > "Text/CSV"
3. Select `mini_project_dataset_200_rows.csv`
4. Click "Load" (or "Transform Data" if you need to clean the data)

### Power Query (M Code) for Data Cleaning
If you open the Power Query Editor, here's the basic M code generated for CSV import:

```
let
    Source = Csv.Document(File.Contents("C:\Users\Admin\FinalProjects2026\mini_project_dataset_200_rows.csv"),[Delimiter=",", Columns=12, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Student_ID", type text}, {"Student_Name", type text}, {"Age", Int64.Type}, {"Gender", type text}, {"Subject", type text}, {"Hours_Studied_Per_Week", Int64.Type}, {"Attendance_Percentage", Int64.Type}, {"Assignments_Completed", Int64.Type}, {"Quiz_Score", Int64.Type}, {"Final_Exam_Score", Int64.Type}, {"Internship_Completed", type text}, {"Placement_Interest", type text}})
in
    #"Changed Type"
```

## Step 2: Create Key Measures (DAX)
In Power BI, create these measures in the "Modeling" tab or by right-clicking the table:

### Basic Statistics Measures
```
Average Final Exam Score = AVERAGE('Table'[Final_Exam_Score])

Standard Deviation Exam Score = STDEV.P('Table'[Final_Exam_Score])

Total Students = COUNTROWS('Table')

Average Hours Studied = AVERAGE('Table'[Hours_Studied_Per_Week])

Average Attendance = AVERAGE('Table'[Attendance_Percentage])
```

### Model-Related Measures
Since Power BI can't run the regression model directly, we'll create measures to display the model metrics you calculated in Python:

```
Model MSE = 42.75613506205529

Model R-Squared = 0.7447690151538872

RMSE = SQRT([Model MSE])
```

## Step 3: Create Visualizations

### 1. Student Distribution by Subject (Bar Chart)
- Drag "Subject" to X-axis
- Drag "Student_ID" to Y-axis (count)
- Title: "Number of Students by Subject"

### 2. Hours Studied by Subject (Box and Whisker Plot)
- Use the "Box and Whisker" visual from AppSource if needed
- X-axis: Subject
- Y-axis: Hours_Studied_Per_Week

### 3. Attendance Percentage by Subject (Box Plot)
- Similar to above, X: Subject, Y: Attendance_Percentage

### 4. Age Distribution by Subject (Box Plot)
- X: Subject, Y: Age

### 5. Assignments Completed by Subject (Box Plot)
- X: Subject, Y: Assignments_Completed

### 6. Scatter Plot: Hours vs Final Exam Score
- X-axis: Hours_Studied_Per_Week
- Y-axis: Final_Exam_Score
- Add trend line: Format > Analytics > Trend line

### 7. Scatter Plot: Attendance vs Final Exam Score
- X-axis: Attendance_Percentage
- Y-axis: Final_Exam_Score
- Add trend line

### 8. Model Performance Card
- Use "Card" visual to display:
  - Model MSE
  - Model R-Squared
  - RMSE

### 9. Key Insights Cards
- Create cards showing:
  - Total Students
  - Average Final Exam Score
  - Average Hours Studied
  - Average Attendance

### 10. Gender and Subject Distribution
- Stacked bar chart: X-axis Subject, Y-axis count, Legend: Gender

### 11. Internship and Placement Interest
- Pie charts for Internship_Completed and Placement_Interest

## Step 4: Add Filters and Slicers
- Add slicers for Subject, Gender, Age range
- This allows interactive filtering of all visuals

## Step 5: Dashboard Layout
- Arrange visuals in a logical flow:
  - Top: Key metrics cards
  - Middle: Subject distributions and box plots
  - Bottom: Scatter plots and model performance
- Use containers or backgrounds for grouping

## Step 6: Advanced Features

### Add Regression Line (Manual Approximation)
Since Power BI doesn't have built-in linear regression visualization, you can approximate the trend line using the scatter plot's built-in trend line feature.

### Using Python Visual for Custom Analysis
If you want to run Python code within Power BI:
1. Enable Python in Power BI Options
2. Add a "Python visual"
3. Use code like:

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Assuming dataset is loaded
df = dataset
X = df[['Hours_Studied_Per_Week', 'Attendance_Percentage', 'Age', 'Assignments_Completed']]
y = df['Final_Exam_Score']

model = LinearRegression()
model.fit(X, y)

plt.scatter(df['Hours_Studied_Per_Week'], y)
plt.plot(df['Hours_Studied_Per_Week'], model.predict(X), color='red')
plt.show()
```

## Step 7: Publish and Share
- Save as .pbix file
- Publish to Power BI Service if needed
- Share with stakeholders

## Limitations
- Power BI can't directly replicate the exact Python model or all statistical tests
- For complex ML models, consider using Power BI's integration with Azure ML or keeping Python separate
- Box plots may require custom visuals from the marketplace

This setup will give you an interactive dashboard that complements your Python analysis!