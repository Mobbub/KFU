points = input().split()
points = [int(point) for point in points]
from_b = abs(points[1]-points[0])
from_c = abs(points[2]-points[0])
if from_b < from_c:
  print(f"B {from_b}")
else:
  print(f"C {from_c}")
