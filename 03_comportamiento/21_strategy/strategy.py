"""
PATRON STRATEGY - Metodos de Pago

Analogia: Como pagar en una tienda online. Puedes elegir diferentes metodos de
pago (tarjeta, PayPal, transferencia) y cada uno procesa el pago diferente.
La tienda no necesita saber como funciona cada metodo internamente, solo usa
la estrategia elegida. Puedes cambiar de estrategia facilmente.

PROBLEMA: Necesitas usar diferentes algoritmos o comportamientos segun el contexto.
Usar if/else o switch para cada algoritmo hace el codigo rigido y dificil de
extender. Agregar nuevos algoritmos requiere modificar codigo existente.

SOLUCION: Definir una familia de algoritmos, encapsular cada uno en una clase
separada, y hacerlos intercambiables. El cliente puede elegir la estrategia
en tiempo de ejecucion sin cambiar el codigo que la usa.

VENTAJA: Algoritmos intercambiables. Elimina condicionales. Facil agregar nuevas
estrategias. El cliente elige cual estrategia usar.

Conceptos OOP usados:
- Abstraccion: Interfaz Strategy con metodo comun
- Herencia: Estrategias concretas heredan de Strategy
- Composicion: Context contiene referencia a la estrategia
- Polimorfismo: Diferentes estrategias con misma interfaz
"""

from abc import ABC, abstractmethod


# =============================================================================
# STRATEGY: Interfaz para las estrategias de pago
# =============================================================================

class PaymentStrategy(ABC):
    """
    Interfaz Strategy: Define como debe procesarse un pago.
    Cada estrategia concreta implementa su propio algoritmo.
    """

    @abstractmethod
    def pay(self, amount: float) -> None:
        """Procesa el pago usando esta estrategia."""
        pass


# =============================================================================
# ESTRATEGIAS CONCRETAS
# =============================================================================

class CreditCardStrategy(PaymentStrategy):
    """
    Estrategia concreta: Pago con tarjeta de credito.
    """

    def __init__(self, card_number: str, cvv: str, expiry: str):
        self._card_number = card_number
        self._cvv = cvv
        self._expiry = expiry

    def pay(self, amount: float) -> None:
        """Procesa pago con tarjeta de credito."""
        # Ocultar parte del numero de tarjeta
        masked_card = "**** **** **** " + self._card_number[-4:]
        print(f"  [Tarjeta de Credito]")
        print(f"    Numero: {masked_card}")
        print(f"    Expiracion: {self._expiry}")
        print(f"    Procesando ${amount:.2f}...")
        print(f"    [OK] Pago con tarjeta aprobado")


class PayPalStrategy(PaymentStrategy):
    """
    Estrategia concreta: Pago con PayPal.
    """

    def __init__(self, email: str):
        self._email = email

    def pay(self, amount: float) -> None:
        """Procesa pago con PayPal."""
        print(f"  [PayPal]")
        print(f"    Cuenta: {self._email}")
        print(f"    Redirigiendo a PayPal...")
        print(f"    Procesando ${amount:.2f}...")
        print(f"    [OK] Pago via PayPal completado")


class BankTransferStrategy(PaymentStrategy):
    """
    Estrategia concreta: Pago por transferencia bancaria.
    """

    def __init__(self, account_number: str, bank_name: str):
        self._account_number = account_number
        self._bank_name = bank_name

    def pay(self, amount: float) -> None:
        """Procesa pago por transferencia bancaria."""
        # Ocultar parte del numero de cuenta
        masked_account = "*" * (len(self._account_number) - 4) + self._account_number[-4:]
        print(f"  [Transferencia Bancaria]")
        print(f"    Banco: {self._bank_name}")
        print(f"    Cuenta: {masked_account}")
        print(f"    Generando referencia de pago...")
        print(f"    Procesando ${amount:.2f}...")
        print(f"    [OK] Transferencia iniciada (pendiente de confirmacion)")


class CryptoStrategy(PaymentStrategy):
    """
    Estrategia concreta: Pago con criptomoneda.
    """

    def __init__(self, wallet_address: str, crypto_type: str = "Bitcoin"):
        self._wallet_address = wallet_address
        self._crypto_type = crypto_type

    def pay(self, amount: float) -> None:
        """Procesa pago con criptomoneda."""
        # Ocultar parte de la direccion
        masked_wallet = self._wallet_address[:6] + "..." + self._wallet_address[-4:]
        print(f"  [{self._crypto_type}]")
        print(f"    Wallet: {masked_wallet}")
        print(f"    Convirtiendo ${amount:.2f} a {self._crypto_type}...")
        print(f"    Esperando confirmacion en blockchain...")
        print(f"    [OK] Transaccion enviada")


# =============================================================================
# CONTEXT: La tienda online que usa las estrategias
# =============================================================================

class ShoppingCart:
    """
    Context: El carrito de compras que usa una estrategia de pago.
    Puede cambiar la estrategia dinamicamente.
    """

    def __init__(self):
        self._items = []
        self._payment_strategy: PaymentStrategy = None

    def add_item(self, name: str, price: float) -> None:
        """Agrega un item al carrito."""
        self._items.append({"name": name, "price": price})
        print(f"  [Carrito] Agregado: {name} - ${price:.2f}")

    def get_total(self) -> float:
        """Calcula el total del carrito."""
        return sum(item["price"] for item in self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Establece la estrategia de pago a usar."""
        self._payment_strategy = strategy
        print(f"\n[Carrito] Metodo de pago seleccionado: {strategy.__class__.__name__.replace('Strategy', '')}")

    def checkout(self) -> None:
        """Realiza el pago usando la estrategia seleccionada."""
        if not self._payment_strategy:
            print("[ERROR] No se ha seleccionado un metodo de pago")
            return

        total = self.get_total()
        print(f"\n[Checkout] Total a pagar: ${total:.2f}")
        print("-" * 50)
        self._payment_strategy.pay(total)


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON STRATEGY - Metodos de Pago")
    print("=" * 70)

    # --- Crear carrito y agregar items ---
    print("\n[PASO 1] Crear carrito y agregar productos")
    print("-" * 70)
    cart = ShoppingCart()
    cart.add_item("Laptop", 1200.00)
    cart.add_item("Mouse", 25.00)
    cart.add_item("Teclado", 75.00)

    # --- Pagar con tarjeta de credito ---
    print("\n[PASO 2] Pagar con tarjeta de credito")
    print("-" * 70)
    credit_card = CreditCardStrategy("1234567890123456", "123", "12/25")
    cart.set_payment_strategy(credit_card)
    cart.checkout()

    # --- Crear nuevo carrito ---
    print("\n" + "=" * 70)
    print("[PASO 3] Nuevo carrito con diferentes productos")
    print("-" * 70)
    cart2 = ShoppingCart()
    cart2.add_item("Monitor", 350.00)
    cart2.add_item("Webcam", 80.00)

    # --- Pagar con PayPal ---
    print("\n[PASO 4] Pagar con PayPal")
    print("-" * 70)
    paypal = PayPalStrategy("usuario@example.com")
    cart2.set_payment_strategy(paypal)
    cart2.checkout()

    # --- Crear otro carrito ---
    print("\n" + "=" * 70)
    print("[PASO 5] Otro carrito")
    print("-" * 70)
    cart3 = ShoppingCart()
    cart3.add_item("Smartphone", 800.00)

    # --- Pagar con transferencia bancaria ---
    print("\n[PASO 6] Pagar con transferencia bancaria")
    print("-" * 70)
    bank_transfer = BankTransferStrategy("1234567890", "Banco Nacional")
    cart3.set_payment_strategy(bank_transfer)
    cart3.checkout()

    # --- Cambiar estrategia dinamicamente ---
    print("\n" + "=" * 70)
    print("[PASO 7] Cambiar metodo de pago dinamicamente")
    print("-" * 70)
    print("\n  Cliente decide cambiar de transferencia a crypto:")
    crypto = CryptoStrategy("1A2b3C4d5E6f7G8h9I0j", "Bitcoin")
    cart3.set_payment_strategy(crypto)
    cart3.checkout()

    """
    =========================================================================
    VENTAJAS DEL PATRON STRATEGY
    =========================================================================
    1. INTERCAMBIABLE: Puedes cambiar algoritmos en tiempo de ejecucion

    2. ELIMINA CONDICIONALES: No necesitas if/else para cada estrategia

    3. OPEN/CLOSED: Agregas nuevas estrategias sin modificar codigo existente

    4. ENCAPSULACION: Cada estrategia encapsula su algoritmo

    5. TESTEABLE: Cada estrategia se prueba independientemente
    """
