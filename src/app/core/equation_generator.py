import random


def _join_terms(terms):
    """Joins mathematical terms into a formatted string, handling signs."""
    if not terms:
        return "0"
    out = ""
    first = True
    for sign, body in terms:
        if first:
            out += (f"-{body}" if sign == "-" else f"{body}")
            first = False
        else:
            out += f" {sign} {body}"
    return out


def _format_coef_var(coef, var="x", power=1):
    """Formats a single term of a polynomial (e.g., '5x^2' or '-3')."""
    if coef == 0:
        return None
    abs_coef = abs(coef)
    if power == 0:
        body = f"{abs_coef}"
    elif power == 1:
        body = f"{var}" if abs_coef == 1 else f"{abs_coef}{var}"
    else:
        body = f"{var}^{power}" if abs_coef == 1 else f"{abs_coef}{var}^{power}"
    sign = "-" if coef < 0 else "+"
    return sign, body


def _format_linear(a, b):
    """Formats a linear equation (ax + b)."""
    terms = []
    t = _format_coef_var(a, power=1)
    if t:
        terms.append(t)
    t = _format_coef_var(b, power=0)
    if t:
        terms.append(t)
    return _join_terms(terms)


def _format_quadratic(a, b, c):
    """Formats a quadratic equation (ax^2 + bx + c)."""
    terms = []
    t = _format_coef_var(a, power=2)
    if t:
        terms.append(t)
    t = _format_coef_var(b, power=1)
    if t:
        terms.append(t)
    t = _format_coef_var(c, power=0)
    if t:
        terms.append(t)
    return _join_terms(terms)


def _format_cubic(a, b, c, d):
    """Formats a cubic equation (ax^3 + bx^2 + cx + d)."""
    terms = []
    t = _format_coef_var(a, power=3)
    if t:
        terms.append(t)
    t = _format_coef_var(b, power=2)
    if t:
        terms.append(t)
    t = _format_coef_var(c, power=1)
    if t:
        terms.append(t)
    t = _format_coef_var(d, power=0)
    if t:
        terms.append(t)
    return _join_terms(terms)


def generate_random_equation():
    """Generates a random equation of various types (polynomial, exponential, etc.)."""
    equation_types = [
        "polynomial", "exponential", "fractional",
        "radical", "logarithmic", "trigonometric",
        "exponential_polynomial", "log_polynomial", "radical_polynomial",
        "composite"
    ]
    weights = [0.2, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.1]
    eq_type = random.choices(equation_types, weights=weights, k=1)[0]
    if eq_type == "polynomial":
        return generate_polynomial()
    elif eq_type == "exponential":
        return generate_exponential()
    elif eq_type == "fractional":
        return generate_fractional()
    elif eq_type == "radical":
        return generate_radical()
    elif eq_type == "logarithmic":
        return generate_logarithmic()
    elif eq_type == "trigonometric":
        return generate_trigonometric()
    elif eq_type == "exponential_polynomial":
        return generate_exponential_polynomial()
    elif eq_type == "log_polynomial":
        return generate_log_polynomial()
    elif eq_type == "radical_polynomial":
        return generate_radical_polynomial()
    else:
        return generate_composite()


def generate_polynomial():
    """Generates a random polynomial equation."""
    if random.random() < 0.3:
        root1 = random.randint(-5, 5)
        root2 = random.randint(-5, 5)

        def factor(r):
            if r == 0:
                return "(x)"
            if r > 0:
                return f"(x - {r})"
            return f"(x + {abs(r)})"
        if root1 == root2:
            return f"$({factor(root1)})^2 = 0$".replace("($(", "(")
        else:
            return f"${factor(root1)}{factor(root2)} = 0$"
    elif random.random() < 0.65:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-10, 10)
        d = random.randint(-5, 5)
        e = random.randint(-10, 10)
        if a == 0 and d == 0: a = random.randint(1, 5) # Avoid 0 = constant
        if a == d: d += random.choice([-1, 1]) or 1
        left = _format_quadratic(a, b, c)
        right = _format_linear(d, e)
        return f"${left} = {right}$"
    else:
        a = random.randint(1, 3)
        b = random.randint(-3, 3)
        c = random.randint(-5, 5)
        d = random.randint(-5, 5)
        poly = _format_cubic(a, b, c, d)
        return f"${poly} = 0$"


def generate_exponential():
    """Generates a random exponential equation."""
    bases = [2, 3, 5]
    base1 = random.choice(bases)
    exponent_coeff = random.randint(1, 4)
    left_exp = "x" if exponent_coeff == 1 else f"{exponent_coeff}x"
    x_sol = random.randint(1, 3)
    result = base1 ** (exponent_coeff * x_sol)
    return f"${base1}^{{{left_exp}}} = {result}$"


def generate_fractional():
    """Generates a random fractional equation."""
    numerator_coeff = random.randint(1, 3)
    denominator = random.randint(2, 9)
    constant = random.randint(1, 5)
    numerator_term = "x" if numerator_coeff == 1 else f"{numerator_coeff}x"
    if random.random() < 0.5:
        return f"$\frac{{{numerator_term}}}{{{denominator}}} = {constant}$"
    else:
        numerator_const = random.randint(1, 5)
        return f"$\frac{{{numerator_term} + {numerator_const}}}{{{denominator}}} = {constant}$"


def generate_radical():
    """Generates a random radical (square root) equation."""
    coefficient = random.randint(1, 3)
    radicand_coeff = random.randint(1, 3)
    constant = random.randint(2, 5)
    radicand_term = "x" if radicand_coeff == 1 else f"{radicand_coeff}x"
    outside = "" if coefficient == 1 else f"{coefficient}"
    if random.random() < 0.5:
        return rf"${outside}\sqrt{{{radicand_term}}} = {constant}$"
    else:
        offset = random.randint(1, 5)
        return rf"$\sqrt{{{radicand_term} + {offset}}} = {constant}$"


def generate_logarithmic():
    """Generates a random logarithmic equation."""
    coefficient = random.randint(1, 3)
    constant = random.randint(1, 5)
    term = "x" if coefficient == 1 else f"{coefficient}x"
    if random.random() < 0.5:
        return rf"$\ln({term}) = {constant}$"
    else:
        offset = random.randint(1, 3)
        return rf"$\ln({term} + {offset}) = {constant}$"


def generate_trigonometric():
    """Generates a random trigonometric equation."""
    func = random.choice([r"\sin", r"\cos", r"\tan"])
    coefficient = random.randint(1, 3)
    coeff_str = "" if coefficient == 1 else f"{coefficient}"

    if func in [r"\sin", r"\cos"]:
        # For sin/cos, the result must be in [-1, 1]
        possible_constants = ["0", "1", "-1", r"\frac{1}{2}", r"-\frac{1}{2}", r"\frac{\sqrt{2}}{2}", r"-\frac{\sqrt{2}}{2}", r"\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{3}}{2}"]
        constant = random.choice(possible_constants)
    else: # tan can have a wider range of results
        angles = ["0", "1", r"\frac{\sqrt{3}}{3}", r"\sqrt{3}"]
        constant = random.choice(angles)

    inside = "x" if coefficient == 1 else f"{coefficient}x"
    if random.random() < 0.5:
        return f"${func}({inside}) = {constant}$"
    else:
        offset_val = random.choice(["0", r"\frac{\pi}{6}", r"\frac{\pi}{4}", r"\frac{\pi}{3}"])
        if offset_val == "0":
            return f"${func}({inside}) = {constant}$"
        else:
            return f"${func}({inside} + {offset_val}) = {constant}$"


def generate_exponential_polynomial():
    """Generates a random equation with an exponential term on one side and a polynomial on the other."""
    base = random.choice([2, 3, 5])
    exponent_coeff = random.randint(1, 2)
    exponent_part = "x" if exponent_coeff == 1 else f"{exponent_coeff}x"
    poly_coeff = random.randint(1, 3)
    constant = random.randint(1, 5)
    rhs = _format_linear(poly_coeff, constant)
    return f"${base}^{{{exponent_part}}} = {rhs}$"


def generate_log_polynomial():
    """Generates a random equation with a logarithmic term on one side and a polynomial on the other."""
    log_coeff = random.randint(1, 2)
    poly_coeff = random.randint(1, 3)
    constant = random.randint(1, 5)
    left = "x" if log_coeff == 1 else f"{log_coeff}x"
    right = _format_linear(poly_coeff, constant)
    return rf"$\ln({left}) = {right}$"


def generate_radical_polynomial():
    """Generates a random equation with a radical term on one side and a polynomial on the other."""
    radical_coeff = random.randint(1, 2)
    poly_coeff = random.randint(1, 3)
    constant = random.randint(1, 5)
    rad = "x" if radical_coeff == 1 else f"{radical_coeff}x"
    rhs = _format_linear(poly_coeff, constant)
    return rf"$\sqrt{{{rad}}} = {rhs}$"


def generate_composite():
    num_operations = random.randint(2, 3)
    operations = set()
    while len(operations) < num_operations:
        op_type = random.choice(["exp", "log", "rad", "frac", "poly", "trig"])
        op_str = ""
        try:
            if op_type == "exp":
                base = random.choice([2, 3, 5])
                exp = random.randint(1, 2)
                exp_part = "x" if exp == 1 else f"{exp}x"
                op_str = f"{base}^{{{exp_part}}}"
            elif op_type == "log":
                coeff = random.randint(1, 2)
                left = "x" if coeff == 1 else f"{coeff}x"
                op_str = f"\\ln({left})"
            elif op_type == "rad":
                coeff = random.randint(1, 2)
                rad = "x" if coeff == 1 else f"{coeff}x"
                op_str = f"\\sqrt{{{rad}}}"
            elif op_type == "frac":
                num_coeff = random.randint(1, 2)
                den = random.randint(2, 5)
                num = "x" if num_coeff == 1 else f"{num_coeff}x"
                op_str = f"\\frac{{{num}}}{{{den}}}"
            elif op_type == "poly":
                coeff = random.randint(1, 3)
                const = random.randint(0, 3)
                op_str = _format_linear(coeff, const)
            else: # trig
                func = random.choice([r"\sin", r"\cos", r"\tan"])
                coeff = random.randint(1, 2)
                inside = "x" if coeff == 1 else f"{coeff}x"
                op_str = f"{func}({inside})"
            if op_str: operations.add(op_str)
        except: continue

    operators = [random.choice(["+", "-"]) for _ in range(num_operations - 1)]
    equation = list(operations)[0]
    for i in range(num_operations - 1):
        equation += f" {operators[i]} {list(operations)[i+1]}"
    constant = random.randint(1, 10)
    return f"${equation} = {constant}$"


def generate_multiple_equations(n):
    """Generates a specified number of unique random equations."""
    try:
        n = int(n)
        if n < 1:
            return "Error: Number must be at least 1"
        if n > 1000:
            return "Error: Maximum 10000 equations"
        equations = []
        generated_equations = set()
        for i in range(min(n, 10000)):
            for _ in range(10):
                eq = generate_random_equation()
                if eq not in generated_equations:
                    generated_equations.add(eq)
                    equations.append(f"Equation {i+1}: {eq}")
                    break
            else:
                equations.append(f"Equation {i+1}: {eq}")
        return "\n".join(equations)
    except ValueError:
        return "Error: Please enter a valid number"
    except Exception as e:
        return f"Error: {e}"