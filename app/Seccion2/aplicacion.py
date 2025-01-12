class Conjunto100:
    def __init__(self):
        # Inicializa el conjunto con los primeros 100 números naturales
        self.numeros = set(range(1, 101))

    def extract(self, numero):
        """Método para extraer un número específico del conjunto."""
        if numero < 1 or numero > 100:
            raise ValueError("El número debe ser mayor que 0 y menor o igual a 100.")
        if numero in self.numeros:
            self.numeros.remove(numero)
        else:
            raise ValueError(f"El número {numero} no está en el conjunto.")

    def calcular_numero_extraido(self):
        """Calcula el número faltante utilizando la suma total y la suma de los números restantes."""
        suma_total = 100 * (100 + 1) // 2  # Suma de los primeros 100 números
        suma_restante = sum(self.numeros)  # Suma de los números restantes en el conjunto
        return suma_total - suma_restante  # El número faltante es la diferencia entre ambas sumas


def main():
    try:
        # Instanciamos la clase Conjunto100
        conjunto = Conjunto100()

        # Solicitar al usuario un número para extraer
        numero = int(input("Introduce el número que deseas extraer (entre 1 y 100): "))

        # Validación del input
        if numero < 1 or numero > 100:
            print("Por favor, ingresa un número entre 1 y 100.")
            return

        # Extraemos el número del conjunto
        conjunto.extract(numero)

        # Calculamos el número faltante
        numero_faltante = conjunto.calcular_numero_extraido()

        # Mostramos el resultado
        print(f"El número extraído fue: {numero_faltante}")

    except ValueError as e:
        print(f"Error: {e}")


# Ejecutamos la aplicación
if __name__ == "__main__":
    main()
