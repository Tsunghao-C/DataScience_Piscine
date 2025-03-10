## **📌 Statistical Differences**
| Feature           | **Standardization (Z-score Scaling)** | **Normalization (Min-Max Scaling)** |
|------------------|--------------------------------------|-----------------------------------|
| **Formula** | \( x = (x - x_min) / x_std \) | \( x = (x - x_min) / (x_max - x_min) \) |
| **Resulting Distribution** | Mean = 0, Std = 1 (keeps original shape) | Transformed values in the range **[0,1]** (or [-1,1]) |
| **Effect on Outliers** | Less sensitive to outliers (but doesn’t remove them) | Very sensitive to outliers (they can skew the scaling) |
| **Keeps Shape of Data?** | Yes, maintains the distribution | No, rescales values within a fixed range |
| **Handles Different Units?** | Yes, removes unit dependency | Yes, but may distort distributions |
| **Works Well With?** | Data following a **normal distribution** | Data that is **not normally distributed** or has known fixed bounds |

---

## **📌 Use Cases**
### **🔹 When to Use Standardization (Z-score Scaling)**
👉 **Works well with algorithms that assume normally distributed data** (e.g., linear regression, logistic regression, PCA, SVM, etc.).  
👉 **Good for datasets where the distribution is unknown or contains negative values.**  
👉 **Best when the dataset has outliers** since it doesn’t distort the range too much.

### **🔹 When to Use Normalization (Min-Max Scaling)**
👉 **Useful when the data has known bounds** (e.g., image pixel values [0,255], percentages [0,100]).  
👉 **Works well for deep learning models (e.g., neural networks)** since it speeds up training (activations are often between 0 and 1).  
👉 **Best for algorithms that compute distances (e.g., k-NN, K-Means, DBSCAN, etc.)** because it ensures fair weight contribution.

---

## **📌 Simple Rule of Thumb**
✔ **If the data follows (or is assumed to follow) a normal distribution → Use STANDARDIZATION**  
✔ **If the data has varying scales and you want values between [0,1] → Use NORMALIZATION**  
✔ **If you're unsure → Try both and compare model performance** 🎯  
