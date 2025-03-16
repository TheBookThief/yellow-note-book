import sys
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

def polynomial_to_binary(coefficients, bits=8):
    binary_sequence = []
    
    for coeff in coefficients:
        binary_coeff = format(coeff, f'0{bits}b')
        binary_sequence.extend([int(bit) for bit in binary_coeff])
    
    return binary_sequence

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <pol> <audio_path>")
        sys.exit(1)
    
    pol = sys.argv[1]
    audio_path = sys.argv[2]
    
    print(f"Polinomial: {pol}")
    print(f"Audio Path: {audio_path}")
    print(f"Coefficients: {find_coefficients(pol)}")
    print(f"Binary: {polynomial_to_binary(find_coefficients(pol), bits=3)}")
    

if __name__ == "__main__":
    main()