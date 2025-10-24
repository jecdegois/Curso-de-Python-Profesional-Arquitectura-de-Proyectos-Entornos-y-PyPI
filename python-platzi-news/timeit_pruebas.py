import timeit

NUMERO = 10_000_000


def suma_con_sum() -> int:
    return sum(range(NUMERO))


def suma_con_for() -> int:
    total = 0
    for i in range(NUMERO):
        total += i
    return total


print(f"Función: sum() {suma_con_sum()}")
print(f"Función: for() {suma_con_for()}")
print(f"Son iguales? {suma_con_sum() == suma_con_for()}")


repeticiones = 10

tiempo_sum = timeit.timeit(suma_con_sum, number=repeticiones)
timepo_for = timeit.timeit(suma_con_for, number=repeticiones)

print(f"Tiempo para sum {tiempo_sum:.6f}")
print(f"Tiempo para for {timepo_for:.6f}")
