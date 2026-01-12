"""
PATRON INTERPRETER - Conversor de Unidades

Analogia: Como un traductor que entiende frases en diferentes idiomas. Le dices
"10 km a metros" y el traductor entiende la estructura de la frase (numero, unidad
origen, palabra clave "a", unidad destino) y realiza la conversion. Cada palabra
o simbolo tiene un significado que se interpreta.

PROBLEMA: Necesitas evaluar o interpretar expresiones en un lenguaje especifico
(matematicas, consultas, conversiones). Sin un interprete, tendrias que parsear
y evaluar manualmente cada vez, con codigo complejo y dificil de mantener.

SOLUCION: Definir una gramatica del lenguaje y crear clases que interpreten
cada regla gramatical. Cada expresion es un objeto que sabe interpretarse a si
mismo en un contexto dado.

VENTAJA: Facil agregar nuevas reglas al lenguaje. La gramatica esta representada
explicitamente en el codigo. Cambiar o extender el lenguaje es mas simple.

Conceptos OOP usados:
- Abstraccion: Interfaz Expression con interpret()
- Herencia: Diferentes expresiones heredan de Expression
- Composicion: Expresiones complejas compuestas de expresiones simples
"""

from abc import ABC, abstractmethod
import re


# =============================================================================
# CONTEXT: Almacena informacion global necesaria para la interpretacion
# =============================================================================

class ConversionContext:
    """
    Contexto: Almacena las tasas de conversion entre unidades.
    Los interpretes usan este contexto para obtener la informacion necesaria.
    """

    def __init__(self):
        # Tasas de conversion a la unidad base (metros para distancia, dolares para moneda)
        self._distance_rates = {
            "m": 1.0,
            "km": 1000.0,
            "cm": 0.01,
            "mm": 0.001,
            "mi": 1609.34,  # millas
            "ft": 0.3048,   # pies
        }

        self._currency_rates = {
            "USD": 1.0,
            "EUR": 1.08,
            "GBP": 1.27,
            "JPY": 0.0067,
            "MXN": 0.059,
        }

    def get_distance_rate(self, unit: str) -> float:
        """Obtiene la tasa de conversion para una unidad de distancia."""
        return self._distance_rates.get(unit.lower())

    def get_currency_rate(self, currency: str) -> float:
        """Obtiene la tasa de conversion para una moneda."""
        return self._currency_rates.get(currency.upper())


# =============================================================================
# EXPRESSION: Interfaz abstracta para todas las expresiones
# =============================================================================

class Expression(ABC):
    """
    Expresion abstracta: Define la interfaz comun para interpretar expresiones.
    Cada expresion concreta sabe como interpretarse a si misma.
    """

    @abstractmethod
    def interpret(self, context: ConversionContext) -> str:
        """Interpreta la expresion en el contexto dado y retorna el resultado."""
        pass


# =============================================================================
# EXPRESIONES TERMINALES: Expresiones basicas (hojas del arbol)
# =============================================================================

class NumberExpression(Expression):
    """
    Expresion terminal: Representa un numero.
    """

    def __init__(self, value: float):
        self._value = value

    def interpret(self, context: ConversionContext) -> str:
        return str(self._value)

    def get_value(self) -> float:
        return self._value


# =============================================================================
# EXPRESIONES NO TERMINALES: Expresiones complejas (nodos del arbol)
# =============================================================================

class DistanceConversionExpression(Expression):
    """
    Expresion no terminal: Convierte una distancia de una unidad a otra.
    Ejemplo: "10 km a metros"
    """

    def __init__(self, value: float, from_unit: str, to_unit: str):
        self._value = value
        self._from_unit = from_unit
        self._to_unit = to_unit

    def interpret(self, context: ConversionContext) -> str:
        """
        Interpreta la conversion de distancia:
        1. Convierte el valor a la unidad base (metros)
        2. Convierte de la unidad base a la unidad destino
        """
        from_rate = context.get_distance_rate(self._from_unit)
        to_rate = context.get_distance_rate(self._to_unit)

        if from_rate is None or to_rate is None:
            return f"[ERROR] Unidad de distancia no reconocida"

        # Convertir a unidad base y luego a unidad destino
        base_value = self._value * from_rate
        result = base_value / to_rate

        return f"{self._value} {self._from_unit} = {result:.2f} {self._to_unit}"


class CurrencyConversionExpression(Expression):
    """
    Expresion no terminal: Convierte una cantidad de una moneda a otra.
    Ejemplo: "100 USD a EUR"
    """

    def __init__(self, amount: float, from_currency: str, to_currency: str):
        self._amount = amount
        self._from_currency = from_currency
        self._to_currency = to_currency

    def interpret(self, context: ConversionContext) -> str:
        """
        Interpreta la conversion de moneda:
        1. Convierte el monto a la moneda base (USD)
        2. Convierte de la moneda base a la moneda destino
        """
        from_rate = context.get_currency_rate(self._from_currency)
        to_rate = context.get_currency_rate(self._to_currency)

        if from_rate is None or to_rate is None:
            return f"[ERROR] Moneda no reconocida"

        # Convertir a moneda base (USD) y luego a moneda destino
        base_amount = self._amount * from_rate
        result = base_amount / to_rate

        return f"{self._amount} {self._from_currency} = {result:.2f} {self._to_currency}"


# =============================================================================
# PARSER: Analiza la entrada y construye el arbol de expresiones
# =============================================================================

class ConversionParser:
    """
    Parser: Analiza la entrada de texto y construye las expresiones apropiadas.
    Actua como el "compilador" que transforma texto en objetos Expression.
    """

    # Unidades de distancia conocidas
    DISTANCE_UNITS = ["m", "km", "cm", "mm", "mi", "ft", "metros", "kilometros"]

    # Monedas conocidas
    CURRENCIES = ["USD", "EUR", "GBP", "JPY", "MXN"]

    def parse(self, input_text: str) -> Expression:
        """
        Parsea el texto de entrada y construye la expresion correspondiente.
        Formato esperado: "<valor> <unidad_origen> a <unidad_destino>"
        """
        # Limpiar y normalizar entrada
        input_text = input_text.strip()

        # Pattern: numero unidad_origen a unidad_destino
        # Ejemplo: "10 km a metros" o "100 USD a EUR"
        pattern = r'(\d+\.?\d*)\s+([a-zA-Z]+)\s+a\s+([a-zA-Z]+)'
        match = re.match(pattern, input_text, re.IGNORECASE)

        if not match:
            return None

        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)

        # Determinar si es conversion de distancia o moneda
        if self._is_distance_unit(from_unit):
            return DistanceConversionExpression(value, from_unit, to_unit)
        elif self._is_currency(from_unit):
            return CurrencyConversionExpression(value, from_unit, to_unit)
        else:
            return None

    def _is_distance_unit(self, unit: str) -> bool:
        """Verifica si es una unidad de distancia."""
        return unit.lower() in [u.lower() for u in self.DISTANCE_UNITS]

    def _is_currency(self, currency: str) -> bool:
        """Verifica si es una moneda."""
        return currency.upper() in self.CURRENCIES


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON INTERPRETER - Conversor de Unidades")
    print("=" * 70)

    # --- Crear contexto y parser ---
    print("\n[PASO 1] Creando contexto con tasas de conversion y parser")
    print("-" * 70)
    context = ConversionContext()
    parser = ConversionParser()
    print("  Contexto y parser listos")

    # --- Conversiones de distancia ---
    print("\n[PASO 2] Interpretando conversiones de distancia")
    print("-" * 70)

    distance_queries = [
        "10 km a m",
        "5000 m a km",
        "100 cm a m",
        "2 mi a km",
    ]

    for query in distance_queries:
        print(f"\n  Expresion: '{query}'")
        expression = parser.parse(query)
        if expression:
            result = expression.interpret(context)
            print(f"  Resultado: {result}")
        else:
            print(f"  [ERROR] No se pudo parsear la expresion")

    # --- Conversiones de moneda ---
    print("\n[PASO 3] Interpretando conversiones de moneda")
    print("-" * 70)

    currency_queries = [
        "100 USD a EUR",
        "50 EUR a USD",
        "1000 JPY a USD",
        "200 MXN a EUR",
    ]

    for query in currency_queries:
        print(f"\n  Expresion: '{query}'")
        expression = parser.parse(query)
        if expression:
            result = expression.interpret(context)
            print(f"  Resultado: {result}")
        else:
            print(f"  [ERROR] No se pudo parsear la expresion")

    # --- Expresion invalida ---
    print("\n[PASO 4] Probando expresion invalida")
    print("-" * 70)

    invalid_queries = [
        "abc xyz",
        "10 foo a bar",
    ]

    for query in invalid_queries:
        print(f"\n  Expresion: '{query}'")
        expression = parser.parse(query)
        if expression:
            result = expression.interpret(context)
            print(f"  Resultado: {result}")
        else:
            print(f"  [ERROR] Expresion no valida")

    """
    =========================================================================
    VENTAJAS DEL PATRON INTERPRETER
    =========================================================================
    1. GRAMATICA EXPLICITA: La gramatica del lenguaje esta representada
       en clases, facil de entender

    2. FACIL EXTENSION: Agregar nuevas reglas es agregar nuevas clases

    3. REUTILIZACION: Expresiones complejas compuestas de expresiones simples

    4. MANTENIMIENTO: Cada regla gramatical esta encapsulada en su clase

    5. FLEXIBILIDAD: Puedes cambiar la interpretacion sin cambiar la gramatica
    """
