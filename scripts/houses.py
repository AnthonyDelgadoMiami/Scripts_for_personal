import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

class Houses:
    def __init__(self):
        self.model = None
        self.scaler = None

    def load_data(self):
        houseCSV = 'scripts/houseres/miami-housing.csv'
        try:
            houses = pd.read_csv(houseCSV)
            return houses
        except FileNotFoundError:
            print(f"Error: The file {houseCSV} does not exist.")
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
        except pd.errors.ParserError:
            print("Error: Error parsing the file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def load_per(self):
        house_obj = Houses()
        house_data = house_obj.load_data()
        if house_data is not None:
            X, y = house_obj.preprocess_data(house_data)
            house_obj.train_model(X, y)
            house_obj.get_user_input_and_predict(house_data)

    def preprocess_data(self, df):
        # Handle missing values
        df.fillna(0, inplace=True)

        # Separate features and target variable
        X = df.drop(columns=['SALE_PRC'])
        y = df['SALE_PRC']

        # Normalize numerical features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        return X_scaled, y

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Trying different models
        models = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(alpha=1.0),
            "Lasso Regression": Lasso(alpha=0.1),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
        }

        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"{name} - Mean Absolute Error: {mae}, R-squared: {r2}")

        # Use the best model (for example, Gradient Boosting)
        self.model = models["Gradient Boosting"]
        self.model.fit(X_train, y_train)

    def predict(self, new_data):
        if self.model is None or self.scaler is None:
            print("Model is not trained yet.")
            return None

        new_data_scaled = self.scaler.transform(new_data)
        prediction = self.model.predict(new_data_scaled)
        return prediction

    def get_user_input_and_predict(self, df):
        user_input = {}
        for column in df.columns:
            if column != 'SALE_PRC':
                mean_value = df[column].mean()
                median_value = df[column].median()
                print(f"{column}: Mean = {mean_value:.2f}, Median = {median_value:.2f}")
                user_input[column] = float(input(f"Enter value for {column}: "))

        new_house = pd.DataFrame(user_input, index=[0])
        prediction = self.predict(new_house)
        print(f"Predicted Sale Price: {prediction[0]}")

# Usage example
if __name__ == "__main__":
    house_obj = Houses()
    house_obj.load_per()
