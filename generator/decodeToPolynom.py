def make_polynom(coefficients):
    terms = []
    degree = len(coefficients) - 1

    for i, coeff in enumerate(coefficients):
        exp = degree - i

        if coeff == 0:
            continue

        if coeff > 0:
            if not terms:
                term = f"{coeff}" if coeff != 1 else ""
            else:
                term = f"+ {coeff}" if coeff != 1 or exp == 0 else "+ "

        elif coeff < 0:
            term = f"- {-coeff}" if coeff != -1 or exp == 0 else "- "

        if exp > 1:
            term += f"x^{exp}"
        elif exp == 1:
            term += "x"
        
        terms.append(term)

    polynomial = " ".join(terms)

    return polynomial if polynomial else "0"
def find_coefficients(bits, batch_size = 5):
    degree_bits = bits[:batch_size]
    degree = int(''.join(map(str, degree_bits)), 2)
    
    coefficients = []
    
    for i in range(batch_size, len(bits), batch_size):
        if len(coefficients) == degree:
            break
        batch = bits[i:i+batch_size]
        binary_str = ''.join(map(str, batch)) 
        coefficients.append(int(binary_str, 2))
    
    return coefficients

input_bits = [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
coefficients = find_coefficients(input_bits)
polynomial = make_polynom(coefficients)
print(polynomial)
