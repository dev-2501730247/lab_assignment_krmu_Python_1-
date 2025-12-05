# Name-Dev Kaushik, Date-21/10/25 ,Title- DAILY CALORIE TRACKER
print("Welcome! This Python tool helps you easily track and monitor your daily calorie intake.")


#ALL FUNCTIONS HERE
def do_you_want_permission(question_prompt):
    while True:
        user_input = input(f"{question_prompt} (yes/no)? - ").lower().strip()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Please enter a valid answer (Yes or No)")

def calc_avg_calorie():
    avg_calorie = calorie_sum / num_MEALS
    rounded_avg_calorie = round(avg_calorie,2)
    return rounded_avg_calorie



Meal = []
Calories = []
num_MEALS = int(input("Enter the number of meals you want to add - "))
for i in range(1,num_MEALS + 1):
    Meal_name = input("Enter the name of your meal - ")
    Meal.append(Meal_name)
    calorie_amt = float(input("Enter the amount of your calorie intake - "))
    Calories.append(calorie_amt)


calorie_sum = sum(Calories)
print("Total amount of your calorie intake is - ", float(calorie_sum))



if do_you_want_permission("Do you want to see the average calories per meal?"):
    print("Calculating your data...") 
    print(calc_avg_calorie())
else:
    print("Action cancelled")



#daily calorie limit according to google it was 3000 for an avg healthy human so i set it to this
daily_limit = 3000



if do_you_want_permission("Do you want to save today's report"):
    print("Proceeding with action")
    filename = input("Enter the name of the file to be created! - ").strip()
    Date = input("Enter today's date in any format - ").strip()

    # Create filename safely
    full_filename = f"{filename}_{Date}.txt"

    with open(full_filename, "a") as report:
        report.write(f"{Date}\n")
        report.write("Meal name\tCalories\n")
        report.write("--------------------------\n")
        for j in range(num_MEALS):
            report.write(f"{Meal[j]}\t\t{Calories[j]}\n")
        report.write(f"Total calorie\t{calorie_sum}\n")
        report.write(f"Average calorie\t{calc_avg_calorie()}\n")

    print(f"Report saved as '{full_filename}' successfully!")
else:
    print("Action Cancelled!")
