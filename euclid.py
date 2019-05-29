def ex_euclid(a, b):
    """
    The extended Euclidean algorithm yields the
    gcd of inputs a and b, and also two numbers
    x and y such that a*x + b*y = gcd(a,b).
    """
    last_remainder = a
    current_remainder = b
    last_s = 1
    current_s = 0
    last_t = 0
    current_t = 1

    while current_remainder > 0:
        quotient, new_remainder = divmod(last_remainder, current_remainder)
        new_s = last_s - quotient*current_s
        new_t = last_t - quotient*current_t
        current_remainder, last_remainder = new_remainder, current_remainder
        current_s, last_s = new_s, current_s
        current_t, last_t = new_t, current_t

    return last_remainder, last_s, last_t

