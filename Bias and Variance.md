## Bias
1. Bias is defined as the inability of the model because of that there is difference (or error) between predicted value and actual value.
2. In short, bias = y_estimate - y_actual
    - **Low Bias**: means fewer or less strong assumptions are taken to build the target function. The model will closely match the training data.
    - **High Bias**: means more and strong assumptions are taken to build target fucntion. The model will not match the training dataset closely. It is considerd **underfitting** model which has a high error rate. It is due to a very simplified algorithm.

3. A low-biased model does not restrict itself with strong assumptions about the data. For example, using simple linear regression model assumes that the relationship between variables is strickly linear, which itself is a strong assumption and can have high biases if the actual behaviour is non-linear.
4. Models with higher flexibilities like **neural network** or **decision tree** can learn highly complex patterns without assuming a strong predefined structure. This helps to reduce bias.
5. In a nutshell, Low bias model learn actual patterns instead of force itself into a simple assumption about the data.

## Variance
1. Variance is the measure of spread in data from its mean position.
2. In ML, variance, is the amount by which the performance of a predictive model CHANGES when it is trained on DIFFERENT subsets of trained data.
    - **Low variance**: means the model is less sensitive to changes in the training data. The estimate performance is consistent with different subsets of data from the same distribution.
    - **Hight variance**: means the model is very sensitive to changes in the training data and can result in significant changes in the estimate when trained on different subsets of data form the same distribution. This is the case of **overfitting** when model performs when on the training data but poorly on new, unseen test data.

## Reference
https://www.geeksforgeeks.org/bias-vs-variance-in-machine-learning/
