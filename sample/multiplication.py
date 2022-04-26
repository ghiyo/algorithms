"""
filename: multiplication.py
"""


def elementary(n_1, n_2):
  """Elementary method of integer multiplication"""
  mult_results = []
  first_num = str(n_1)
  second_num = str(n_2)
  carry = 0
  result = 0
  for i in range(len(second_num), 0, -1):
    product = ''
    for j in range(len(first_num), 0, -1):
      mul_op = str(int(second_num[i - 1]) * int(first_num[j - 1]) + carry)
      if len(mul_op) > 1:
        carry = int(mul_op[0])
        product = mul_op[1] + product
      else:
        carry = 0
        product = mul_op + product
    if carry != 0:
      product = str(carry) + product
      carry = 0
    mult_results.append(product)
  for i in range(len(mult_results)):
    result += int(mult_results[i] + '0' * i)
  return result


def recursive(n_1, n_2):
  """Recusrive method of integer multiplication"""
  result = 0
  return result


def karatsuba(n_1, n_2):
  """Karatsuba method of integer multiplication"""
  result = 0
  return result


def main():
  """main function"""
  result = elementary(
      3141592653589793238462643383279502884197169399375105820974944592, 2718281828459045235360287471352662497757247093699959574966967627)
  print(result)


if __name__ == "__main__":
  main()
