import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb


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
            print("Please wait a few minutes while we load the Miami housing model...")
            X, y = house_obj.preprocess_data(house_data)
            house_obj.train_model(X, y)

            while True:
                print("-------------------")
                print("CHOOSE THE FOLLOWING")
                print("1. Predict house price")
                print("2. Show correlations")
                print("3. explain each feature")
                print("click anything else to exit")
                user_choice = input("Press number and enter to continue...")
                if user_choice == '1':
                    house_obj.get_user_input_and_predict(house_data)
                elif user_choice == '2':
                    house_obj.show_correlations(house_data)
                elif user_choice == '3':
                    house_obj.show_explain_features()
                else:
                    break

    def preprocess_data(self, df):

        df.fillna(0, inplace=True)

        X = df.drop(columns=['SALE_PRC'])
        y = df['SALE_PRC']

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        return X_scaled, y

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.2,
                                                            random_state=42)

        models = {
            # "Random Forest":
            # RandomForestRegressor(random_state=50),
            # "Gradient Boosting":
            # GradientBoostingRegressor(random_state=50),
            "XGBoost":
            xgb.XGBRegressor(objective='reg:squarederror', random_state=50)
        }

        param_grids = {
            # "Random Forest": {
            #     'n_estimators': [100, 300, 500],
            #     'max_depth': [None, 10, 20]
            # },
            # "Gradient Boosting": {
            #     'n_estimators': [100, 300, 500],
            #     'learning_rate': [0.01, 0.1, 0.2],
            #     'max_depth': [3, 5, 7]
            # },
            "XGBoost": {
                'n_estimators': [100, 300, 500],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7]
            }
        }

        best_model = None
        best_mae = float("inf")
        best_r2 = float("-inf")

        for name, model in models.items():
            grid_search = GridSearchCV(model,
                                       param_grids[name],
                                       cv=5,
                                       scoring='neg_mean_absolute_error',
                                       n_jobs=-1)
            grid_search.fit(X_train, y_train)
            best_model_for_name = grid_search.best_estimator_
            y_pred = best_model_for_name.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"{name} - Mean Absolute Error: {mae}, R-squared: {r2}")

            if mae < best_mae:
                best_mae = mae
                best_r2 = r2
                best_model = best_model_for_name

        self.model = best_model
        print(
            f"Best Model: {self.model.__class__.__name__} - Mean Absolute Error: {best_mae}, R-squared: {best_r2}"
        )
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
                print(
                    f"{column}: Mean = {mean_value:.2f}, Median = {median_value:.2f}"
                )
                user_input[column] = float(
                    input(f"Enter value for {column}: "))

        new_house = pd.DataFrame(user_input, index=[0])
        prediction = self.predict(new_house)
        print(f"Predicted Sale Price: {prediction[0]}")
        print(
            f"Mean = {df['SALE_PRC'].mean():.2f}, Median = {df['SALE_PRC'].median():.2f}"
        )

    def show_correlations(self, df):
        correlations = df.corr()
        print(correlations['SALE_PRC'].sort_values(ascending=False))

    def show_explain_features(self):
        print("FEATURES")
        print("--------")
        file = open("scripts/houseres/features.txt", "r")
        content = file.read()
        print(content)
        file.close()
        while True:
            x = input("put anything to go back...")
            if x != "":
                break

if __name__ == "__main__":
    house_obj = Houses()
    house_obj.load_per()
