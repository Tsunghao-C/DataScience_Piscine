# Feature Selection using VIF and PCA


## Principal Component Analysis (PCA)

- PCA is often used to reduce the dimensions of features. It leaves only uncorrelated features.
- The method of PCA is by using axes transformation. It find the **most efficient** axes that captures the most variances, and then find the 2nd efficient axes, and so on.


## Variable Inflation Factor (VIF)

- VIF is a widely used *diagnostic* tool in regression analysis to detect **multicollinearity**, which is known to affect the stability and interpretability of regression coefficients.
- In short, VIF is a quantifying metric to show how much the variance of a regression coefficient is infalted due to correlations among predictors.


## Compare PCA and VIF

| Metric        | What id Does  | High Value meaning | What it Helps with | When to Use |
|---------------|---------------|--------------------|--------------------|-------------|
|VIF|Detects multicollinearity in original features|Feature is redundant, likely highly correlated with others|Improves interpretability, reduces redundancy|When using linear models, when feature importance matters|
|PCA|Creates new uncorrelated features (PCs)|More variance is explained, fewer components may be needed|Reduces dimensionality, retains variance|When you don’t need interpretability, want to capture variance efficiently|

### Key Difference: PCA changes the features, while VIF helps remove redundant original features.
- PCA **transforms** data-> Original features are replaced with **principal components** (which are combinations of original features)
- VIF **removes redundant features** -> Keeps the original features but remove collinearity.

## When to use What?

### 1. Use PCA Alone When:
- You **don't care about feature interpretability** (e.g. deep learning, clustering,... the original feature value doesn't matter)
- You **want to keep all variance** but in a lower-dimensional space.
- Your model can work with transformed features (e.g. SVM, KNN, Neural Networks).
- Example: Image processing, speech recognition, clustering

### 2. Use VIF Before PCA When:
- You need **interpretable features** (e.g., linear regression, decision trees)
- You want to reduce redundancy **before** applying PCA.
- You want ot improve stability before using a model sensitive to collinearity.
- Example: Economic forecasting, medical research, financial modeling.

### 3. Use VIF Alone When:
- You need **interpretable features**
- You want to reduce redundancy but don't need to reduce dimensionality.


## Reference
1. https://medium.com/@sahin.samia/principal-component-analysis-pca-made-easy-a-complete-hands-on-guide-e26a3680c0bc
2. https://www.datacamp.com/tutorial/variance-inflation-factor

