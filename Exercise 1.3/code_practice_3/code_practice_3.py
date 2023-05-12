print('For Loop:')
for i in range(1, 7):
  if i < 6:
    print(i * 10)
  else:
    print("And we're done!\n\n")

i = 1

print('While loop')

while i < 7:
  if i < 6:
    print(i * 10)
  else:  
    print("And we're done!\n\n")
  i += 1

  text = input('Enter a string: ')

  chars = ['UPPER' if c.isupper() else 'Lower' if c.islower() else 'Other' for c in text]

  print(chars)