number_1 = int(input('enter the first number: '))
number_2 = int(input('enter the second number: '))
operator = input('plus or minus? ("+" or "-"): ')

if operator == '+':
  print(number_1, 'PLUS',number_2,'EQUALS:',number_1 + number_2)

elif operator == '-':
  print(number_1, 'MINUS',number_2,'EQUALS:',number_1 - number_2)

else:
  print('plus or minus, "+" or "-" only!!!!')