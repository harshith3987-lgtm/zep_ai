# Module 2: Analytics & Predictive Modeling

## 1. Overview
This module conducts an end-to-end exploratory analysis and machine learning study on the Titanic passenger cohort (simulating customer demographic behavior and survival/churn outcomes). The pipeline is structured across two primary notebooks:
1. `01_eda.ipynb` — Data ingestion, statistical profiling, missingness diagnosis, IQR outlier detection, correlation analysis, and data export.
2. `02_modeling.ipynb` — Leak-free preprocessing pipelines, baseline benchmarking, cross-validation, hyperparameter tuning, model persistence, and regression analysis.

---

## 2. Exploratory Data Analysis (EDA) Highlights
- **Missingness Strategy**:
  - `Age` (~19.87% missing): Imputed conditionally via passenger title medians (`Mr`, `Mrs`, `Miss`, `Master`) to prevent distribution distortion.
  - `Embarked` (2 missing rows): Imputed using the modal port (`'S'`).
  - `Cabin` (>77% missing): Dropped or engineered into a binary `Has_Cabin` deck indicator.
- **Outlier Mathematics (IQR Rule)**:
  - Fares were evaluated using $IQR = Q_3 - Q_1$. Extreme upper outliers above $Q_3 + 1.5 \times IQR$ were handled via scaling (`StandardScaler` and tree models resilient to skew).
- **Key Behavioral Insights**:
  - **Gender Effect**: Females had an overall survival rate of ~74.2% compared to ~18.9% for males.
  - **Socio-Economic Class**: 1st Class passengers experienced a ~62.9% survival rate versus ~24.2% for 3rd Class passengers.
  - **Family Dynamics**: Moderate family size (`SibSp + Parch = 1 to 3`) showed higher survival odds than solo travelers or large families (`> 4`).

---

## 3. Modeling & Evaluation Framework

### 3.1 Preprocessing & Leak-Free Pipelines
All transformations were encapsulated in Scikit-Learn `Pipeline` and `ColumnTransformer` objects:
- **Numerical Features**: Median imputation followed by `StandardScaler`.
- **Categorical Features**: Mode imputation followed by `OneHotEncoder(handle_unknown='ignore')`.
- All fit operations occurred strictly within training folds during cross-validation.

### 3.2 Classification Models Benchmarked
Models were evaluated using 5-Fold Stratified Cross-Validation on training data and tested on an unseen 20% holdout set:
- **Baseline Dummy Classifier**: Stratified majority rule (~61.6% accuracy).
- **Logistic Regression**: Linear decision boundary with L2 regularization.
- **Random Forest Classifier**: Ensemble of 100 decision trees.
- **Gradient Boosting Classifier**: Sequentially boosted decision trees with tuned learning rates.

### 3.3 Classification Metrics Summary (Holdout Set)
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Baseline (Dummy) | 0.616 | 0.000 | 0.000 | 0.000 | 0.500 |
| Logistic Regression | 0.804 | 0.771 | 0.730 | 0.750 | 0.852 |
| Random Forest | 0.816 | 0.789 | 0.743 | 0.765 | 0.864 |
| Gradient Boosting (Best) | **0.832** | **0.814** | **0.757** | **0.784** | **0.879** |

*Artifact Location*: `analytics/model_artifacts/best_titanic_pipeline.joblib`

### 3.4 Continuous Regression Benchmark
Predicting ticket fare (`Fare`) using passenger attributes:
- Evaluated with **RMSE** and **$R^2$**.
- Demonstrates regression capabilities using Ridge Regression and Gradient Boosting Regressor pipelines.

---

## 4. Execution Guide
To reproduce both notebooks from the project root:

```bash
# Run EDA Notebook
jupyter nbconvert --to notebook --execute analytics/01_eda.ipynb

# Run Modeling Pipeline & Save Model Artifact
jupyter nbconvert --to notebook --execute analytics/02_modeling.ipynb