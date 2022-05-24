"""
filename: merge-sort.py
"""

def merge(a, b):
  """merges two arrays together in ascending order"""
  c = []
  n = len(a) + len(b)
  i = j = 0
  while i < len(a) and j < len(b):
    if a[i] < b[j]:
      c.append(a[i])
      i += 1
    else:
      c.append(b[j])
      j += 1
  while i < len(a):
    c.append(a[i])
    i += 1
  while j < len(b):
    c.append(b[j])
    j += 1
  return c

def merge_sort_aux(lhs, rhs):
  """merge sort auxiliary function"""
  if len(lhs) <= 1 and len(rhs) <= 1:
    return merge(lhs, rhs)
  else:
    l = len(lhs) // 2
    r = len(rhs) // 2
    return merge(merge_sort_aux(lhs[:l], lhs[l:]), merge_sort_aux(rhs[:r], rhs[r:]))

def merge_sort_recursive(arr):
  """merge sort implementation"""
  n = len(arr) // 2
  sorted_array = merge_sort_aux(arr[:n], arr[n:])
  return sorted_array

def merge_sort_recursive_2(arr):
  """merge sort without auxiliary"""
  if len(arr) <= 1:
    return arr
  else:
    n = len(arr) // 2
    return merge(merge_sort_recursive_2(arr[:n]), merge_sort_recursive_2(arr[n:]))

def merge_sort_in_place(arr):
  """merge sort without using new memory"""
  if len(arr) > 1:
    n = len(arr) // 2
    lhs = arr[:n]
    rhs = arr[n:]
    merge_sort_in_place(lhs)
    merge_sort_in_place(rhs)

    i = j = k = 0
    while i < len(lhs) and j < len(rhs):
      if lhs[i] < rhs[j]:
        arr[k] = lhs [i]
        i += 1
      else:
        arr[k] = rhs[j]
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


def main():
  """main function"""
  arr = [5,4,1,8,7,2,6,3]
  sorted_array = merge_sort_recursive(arr)
  print(sorted_array)
  print(merge_sort_recursive_2(arr))
  merge_sort_in_place(arr)
  print(arr)


if __name__ == "__main__":
  main()