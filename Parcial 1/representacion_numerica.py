import math

THRESHOLD_PRINT = 1000  # Si la cantidad total excede este umbral, no se genera la lista.
# Para evitar listas gigantescas de mantisas.
MAX_MANT_LIMIT = 2 ** 16  # 65536

def obtener_parametros():
    print("=== Parámetros de la máquina (representación en punto flotante) ===")
    base = int(input("Ingrese la base (β) (ej.: 2 para binario, 10 para decimal, 16 para hexadecimal): "))
    total_bits = int(input("Ingrese la cantidad total de bits: "))
    sign_bits = int(input("Ingrese la cantidad de bits para el signo (generalmente 1): "))
    exp_bits = int(input("Ingrese la cantidad de bits para el exponente: "))
    mant_bits = int(input("Ingrese la cantidad de bits para la mantisa: "))
    if sign_bits + exp_bits + mant_bits != total_bits:
        print("Error: La suma de los bits asignados no coincide con la cantidad total.")
        return None
    norm_flag = input("¿La mantisa debe ser normalizada? (s/n): ").strip().lower()
    return base, total_bits, sign_bits, exp_bits, mant_bits, norm_flag

def calcular_sesgo(exp_bits):
    # Sesgo = 2^(exp_bits - 1)
    return 2 ** (exp_bits - 1)

def obtener_info_exponentes(exp_bits, sesgo):
    max_field = (2 ** exp_bits) - 1
    total_exponentes = max_field + 1
    N = 0 - sesgo
    M = max_field - sesgo
    return 0, max_field, total_exponentes, N, M

def generar_mantisas(mant_bits, normalizada, base):
    # La mantisa se ingresa en forma binaria.
    if normalizada == 's':
        # Valores posibles: desde 2^(mant_bits - 1) hasta 2^(mant_bits) - 1.
        start = 2 ** (mant_bits - 1)
        end = 2 ** mant_bits
    else:
        start = 0
        end = 2 ** mant_bits
    num_vals = end - start
    if num_vals > MAX_MANT_LIMIT:
        print("La cantidad de valores de mantisa es demasiado grande (" + str(num_vals) + "), no se generará la lista completa.")
        return None
    mant_list = []
    for i in range(start, end):
        # Valor de la mantisa = entero / (2^(mant_bits))
        mantissa = float(i) / (2 ** mant_bits)
        mant_list.append(mantissa)
    return mant_list

def generar_numeros(base, exp_reales, mant_list):
    numeros = []
    for n in exp_reales:
        for m in mant_list:
            numeros.append(m * (base ** n))
    return numeros

def convertir_registro(reg, exp_bits, mant_bits, sesgo, normalizada, base):
    # Se espera que reg tenga longitud igual a total_bits.
    signo_bit = reg[0]
    exp_str = "".join([reg[i] for i in range(1, 1 + exp_bits)])
    mant_str = "".join([reg[i] for i in range(1 + exp_bits, 1 + exp_bits + mant_bits)])
    signo_val = 1 if signo_bit == '0' else -1
    e_field = int(exp_str, 2)
    # La mantisa se interpreta como fracción: entero en binario / (2^(mant_bits))
    mant_val = int(mant_str, 2) / (2 ** mant_bits)
    exp_real = e_field - sesgo
    numero = signo_val * (base ** exp_real) * mant_val
    return signo_val, exp_str, mant_str, exp_real, numero

def calcular_gap(base, exp_real, mant_bits):
    return (base ** exp_real) / (2 ** mant_bits)

def main():
    params = obtener_parametros()
    if params is None:
        return
    base, total_bits, sign_bits, exp_bits, mant_bits, norm_flag = params
    normalizada = norm_flag  # 's' o 'n'
    
    sesgo = calcular_sesgo(exp_bits)
    exp_min_field, exp_max_field, total_exp, N, M = obtener_info_exponentes(exp_bits, sesgo)
    
    # Generar exponentes reales: para e de 0 a (2^exp_bits - 1), restando el sesgo.
    exp_reales = [e - sesgo for e in range(0, 2 ** exp_bits)]
    
    # Intentar generar la lista de mantisas
    mant_list = generar_mantisas(mant_bits, normalizada, base)
    
    # Calcular la cantidad total de números representables según la fórmula:
    if normalizada == 's':
        num_mant = 2 ** (mant_bits - 1)
    else:
        num_mant = 2 ** mant_bits
    num_exp = 2 ** exp_bits
    count_pos = num_exp * num_mant
    count_total = count_pos * 2 + 1
    
    # Para calcular el menor y mayor número representable en positivos:
    # La menor mantisa (normalizada) es  (2^(mant_bits - 1))/(2^(mant_bits))
    # La mayor mantisa es  ((2^(mant_bits) - 1))/(2^(mant_bits))
    if normalizada == 's':
        mant_min = float(2 ** (mant_bits - 1)) / (2 ** mant_bits)
        mant_max = float((2 ** mant_bits) - 1) / (2 ** mant_bits)
    else:
        mant_min = 0.0
        mant_max = float((2 ** mant_bits) - 1) / (2 ** mant_bits)
    
    menor_pos = mant_min * (base ** N)
    mayor_pos = mant_max * (base ** M)
    menor_neg = -mayor_pos
    mayor_neg = -menor_pos

    print("\n=== RESULTADOS DE LA REPRESENTACIÓN NUMÉRICA EN MÁQUINAS ===")
    print("Base (β): " + str(base))
    print("Total de bits: " + str(total_bits))
    print("Distribución -> Signo: " + str(sign_bits) + ", Exponente: " + str(exp_bits) + ", Mantisa: " + str(mant_bits))
    print("Representación normalizada: " + ("Sí" if normalizada == 's' else "No"))
    
    print("\n--- Campo de Exponentes ---")
    print("Exponente mínimo (campo): 0")
    print("Exponente máximo (campo): " + str(exp_max_field))
    print("Total de exponentes posibles: " + str(2 ** exp_bits))
    print("N (menor exponente real): " + str(N))
    print("M (mayor exponente real): " + str(M))
    
    print("\n--- Números representables ---")
    print("Cantidad total (sin incluir 0): " + str(count_pos * 2))
    print("Cantidad total (incluyendo 0): " + str(count_total))
    print("Menor número representable (positivo): " + str(menor_pos))
    print("Mayor número representable (positivo): " + str(mayor_pos))
    print("Menor número representable (negativo): " + str(menor_neg))
    print("Mayor número representable (negativo): " + str(mayor_neg))
    
    print("\nZona de subdesbordamiento (underflow): Números con |x| < " + str(menor_pos))
    print("Zona de sobreflujo (overflow): Números con |x| > " + str(mayor_pos))
    
    if count_total > THRESHOLD_PRINT:
        print("\nLa cantidad total de números representables es muy grande (" + str(count_total) + ").")
        print("No se generará la lista completa de números representables.")
    else:
        pos_nums = generar_numeros(base, exp_reales, mant_list)
        pos_nums.sort()
        all_nums = []
        for val in pos_nums:
            all_nums.append(val)
        all_nums.append(0.0)
        for val in pos_nums:
            all_nums.append(-val)
        all_nums.sort()
        print("\nLista completa de números representables:")
        for n in all_nums:
            print(n)
    
    reg_flag = input("\n¿Desea ingresar un registro específico (cadena de dígitos)? (s/n): ").strip().lower()
    if reg_flag == 's':
        print("\n=== Ingreso de registro específico ===")
        ingresa_separado = input("¿Desea ingresar cada campo por separado? (s/n): ").strip().lower()
        if ingresa_separado == 's':
            signo = input("Ingrese el bit de signo (1 dígito): ").strip()
            exp_field = input("Ingrese el campo de exponente (en binario, " + str(exp_bits) + " dígitos): ").strip()
            mant_field = input("Ingrese el campo de mantisa (en binario, " + str(mant_bits) + " dígitos): ").strip()
            reg = signo + exp_field + mant_field
        else:
            reg = input("Ingrese la cadena completa (sin espacios): ").strip()
        if len(reg) != total_bits:
            print("Error: La longitud ingresada no coincide con " + str(total_bits) + " dígitos.")
        else:
            signo_val, exp_str, mant_str, exp_real, num_reg = convertir_registro(reg, exp_bits, mant_bits, sesgo, normalizada, base)
            print("\n--- Interpretación del Registro ---")
            print("Signo: " + str(signo_val) + " (campo: " + reg[0] + ")")
            print("Campo de exponente: " + exp_str + " (valor decimal: " + str(int(exp_str, 2)) + ")")
            print("Exp. real: " + str(int(exp_str, 2)) + " - " + str(sesgo) + " = " + str(exp_real))
            print("Campo de mantisa: " + mant_str)
            # Interpretar la mantisa como fracción binaria:
            mant_val = int(mant_str, 2) / (2 ** mant_bits)
            print("Mantisa (valor fraccional): " + str(mant_val))
            print("Número real representado: " + str(num_reg))
            gap = calcular_gap(base, exp_real, mant_bits)
            print("Gap (unidad en el último lugar): " + str(gap))
            siguiente = num_reg + gap
            anterior = num_reg - gap
            print("Número representable siguiente (aprox.): " + str(siguiente))
            print("Número representable anterior (aprox.): " + str(anterior))

if __name__ == '__main__':
    main()
