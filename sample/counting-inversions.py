"""
filename: merge-sort.py
"""

def sort_and_count_inversions(arr):
  """merge sort without using new memory"""
  si_num = 0
  if len(arr) <= 1:
      return si_num
  else:
    n = len(arr) // 2
    lhs = arr[:n]
    rhs = arr[n:]
    si_num += sort_and_count_inversions(lhs)
    si_num += sort_and_count_inversions(rhs)

    i = j = k = 0
    while i < len(lhs) and j < len(rhs):
      if lhs[i] < rhs[j]:
        arr[k] = lhs [i]
        i += 1
      else:
        arr[k] = rhs[j]
        si_num += len(lhs[i:])
        j += 1
      k += 1

    while i < len(lhs):
      arr[k] = lhs[i]
      i += 1
      k += 1
    
    while j < len(rhs):
      arr[k] = rhs[j]
      j += 1
      k += 1
    return si_num


def main():
  """main function"""
  arr = [1,3,5,7,8,2,4,6]
  inversions = sort_and_count_inversions(arr)
  print(arr)
  print(inversions)


if __name__ == "__main__":
  main()