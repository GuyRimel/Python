test_scores = [45, 23, 89, 78, 98, 55, 74, 87, 95, 75]

test_scores.sort(reverse = True)

input('hit the Enter key to get the top 3 test scores...')

for i in range(0, 3):
  print(test_scores[i])