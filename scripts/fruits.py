import pandas as pd
import numpy as np

class Fruits:

    def __init__(self):
        pass

    def load_nut(self):
        foodCSV = 'scripts/fruitsres/nutrition.csv'
        try:
            food = pd.read_csv(foodCSV)
        except FileNotFoundError:
            print(f"Error: The file {foodCSV} does not exist.")
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
        except pd.errors.ParserError:
            print("Error: Error parsing the file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        else:
            food.drop(columns=['Unnamed: 0', 'serving_size'], inplace=True)
            food.fillna(0, inplace=True)

            # Convert relevant columns to floats
            for i in food:
                if i != 'name' and i != 'calories':
                    food[i] = self.clean_nutrients(food[i])

            # Print highest and lowest for each column
            self.print_highest_and_lowest(food)

    def clean_nutrients(self, column):
        def convert_value(value):
            value = str(value)
            if 'mg' in value:
                return float(value.replace('mg', ''))
            elif 'mcg' in value:
                return float(value.replace('mcg', '')) / 1000
            elif 'g' in value:
                return float(value.replace('g', '')) * 1000
            elif 'IU' in value:
                if column.name == 'vitamin_d' or column.name == 'vitamin_a':
                    return float(value.replace(' IU', ''))
            else:
                return float(value)

        # Apply the conversion to each value in the column
        column = column.apply(convert_value)
        return column

    def print_highest_and_lowest(self, df):
                    for col in df.columns:
                        if col != 'name':
                            max_value = df[col].max()
                            min_value = df[col].min()

                            max_names = df[df[col] == max_value]['name'].tolist()
                            min_names = df[df[col] == min_value]['name'].tolist()

                            if len(max_names) > 100:
                                max_names_str = "many items"
                            else:
                                max_names_str = ', '.join(max_names[:-1]) + ' and ' + max_names[-1] if len(max_names) > 1 else max_names[0]

                            if len(min_names) > 100:
                                min_names_str = "many items"
                            else:
                                min_names_str = ', '.join(min_names[:-1]) + ' and ' + min_names[-1] if len(min_names) > 1 else min_names[0]

                            print(f"For {col}:")
                            print(f"  Highest: {max_names_str} with {max_value}")
                            print(f"  Lowest: {min_names_str} with {min_value}")
                            print()


# Usage example
if __name__ == "__main__":
    fruit_obj = Fruits()
    fruit_obj.load_nut()
