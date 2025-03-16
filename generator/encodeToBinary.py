import re

def find_coefficients(polynom):
    polynom = polynom.replace(' ', '')
    
    if polynom[0] not in '+-':
        polynom = '+' + polynom
    
    terms = re.findall(r'[+-][^+-]+', polynom)
    variable_match = re.search(r'[a-zA-Z]', polynom)
    variable = variable_match.group(0)

    
    coefficients = {}
    
    for term in terms:
        sign = 1 if term[0] == '+' else -1
        term = term[1:]
        
        if variable in term:
            parts = term.split(variable)
            coef = int(parts[0]) if parts[0] != '' else 1
            coef *= sign 
            
            if '^' in term:
                exponent = int(parts[1].replace('^', ''))
            else:
                exponent = 1
        else:
            coef = int(term) * sign
            exponent = 0
        
        coefficients[exponent] = coef
    
    max_exp = max(coefficients.keys()) if coefficients else 0

    result = [coefficients.get(exp, 0) for exp in range(max_exp, -1, -1)]
    return result

def polynomial_to_binary(coefficients, bits=5):
    binary_sequence = []

    length_binary = format(len(coefficients), f'0{bits}b')
    binary_sequence.extend([int(bit) for bit in length_binary])
    
    for coeff in coefficients:
        binary_coeff = format(coeff, f'0{bits}b')
        binary_sequence.extend([int(bit) for bit in binary_coeff])
    
    return binary_sequence

input_polynom = "5x^5 + 3x^7 + x + 0"
coefficients = find_coefficients(input_polynom)
binary_sequence = polynomial_to_binary(coefficients)
print(binary_sequence)
