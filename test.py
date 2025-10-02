# def get_letter_grade(grade):
#     grade_switch ={
#         90 : "A",
#         80: "B", 
#         70 : "C",
#         60 : "D"
#     }

#     for cutoff, letter in grade_switch.items():
#         if grade >= cutoff:
#             return letter
#     return "F"

# numerical_grade = int(input("ENter numerical grade: "))
# letter_grade = get_letter_grade(numerical_grade)

# print("Letter Grade: ", letter_grade)

for i in range(5):
    print(i)
else:
    print("loop completed without break")

fruits = ["apple", "banana", "cherry"]
for  index, fruit in enumerate(fruits, start=1):
    print(f"Item{index}:{fruit}")
    