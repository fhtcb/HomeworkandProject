# CS3339: Machine Learning 2024 Fall Project

## File Structure
- `data_analysis.py` - Data preprocessing and analysis
- `logistic_regression.py` - Training and evaluation scripts for logistic regression models
- `SVM.py` - Training and evaluation scripts for SVM models
- `SVM_PCA_100.py` - Training and evaluation scripts of the SVM model after dimensionality reduction to 100 using PCA
- `neural_network.py` - Training and evaluation scripts for neural network models
- `best_neural_network.py` - Training and evaluation scripts for optimal neural network models
- `train_feature.pkl` - Training feature data
- `train_labels.npy` - Training labels data
- `test_feature.pkl` - Test feature data
- `requirements.txt` - Necessary Libraries
## Installation
Install the required dependencies
```
pip install -r requirements.txt
```

## Usage
1. Train and evaluate the logistic regression model
    ```
    python logistic_regression.py
    ```
2. Train and evaluate the support vector machine model
    ```
    python SVM.py
    ```
3. Train and evaluate the support vector machine model with PCA reduced to 100 dimensions
    ```
    python SVM_PCA_100.py
    ```
4. Train and evaluate the neural network model
    ```
    python neural_network.py
    ```
5. Train and evaluate the best neural network model
    ```
    python best_neural_network.py
    ```

