"""
PATRON ABSTRACT FACTORY
=======================
Crea familias de objetos relacionados sin especificar sus clases concretas.

Analogia: Una tienda de muebles con estilos. Si eliges estilo moderno,
todos los muebles (silla, mesa) seran modernos y combinaran entre si.

PROBLEMA: Necesitas crear varios objetos que deben ser compatibles entre
si (misma familia). Si mezclas elementos de diferentes familias, no combinan.

SOLUCION: Una fabrica abstracta que define metodos para crear TODOS los
productos de una familia. Cada fabrica concreta crea productos compatibles.

DIFERENCIA CON FACTORY METHOD:
- Factory Method: 1 fabrica → 1 producto
- Abstract Factory: 1 fabrica → familia de productos relacionados
"""

from abc import ABC, abstractmethod


# =============================================================================
# PRODUCTOS ABSTRACTOS: Interfaces que definen los tipos de productos
# =============================================================================

class Chair(ABC):
    """
    Interfaz para todas las sillas.
    Todas las sillas deben poder 'sentarse' en ellas.
    """

    @abstractmethod
    def sit_on(self) -> str:
        """Metodo que deben implementar todas las sillas."""
        pass


class Table(ABC):
    """
    Interfaz para todas las mesas.
    Todas las mesas deben poder 'colocar cosas' encima.
    """

    @abstractmethod
    def place_on(self) -> str:
        """Metodo que deben implementar todas las mesas."""
        pass


# =============================================================================
# PRODUCTOS CONCRETOS - FAMILIA MODERNA
# =============================================================================

class ModernChair(Chair):
    """Silla de estilo moderno."""

    def sit_on(self) -> str:
        return "Sentado en una silla MODERNA (minimalista, metal y vidrio)"


class ModernTable(Table):
    """Mesa de estilo moderno."""

    def place_on(self) -> str:
        return "Colocando objetos en una mesa MODERNA (lineas rectas, cristal)"


# =============================================================================
# PRODUCTOS CONCRETOS - FAMILIA CLASICA
# =============================================================================

class ClassicChair(Chair):
    """Silla de estilo clasico."""

    def sit_on(self) -> str:
        return "Sentado en una silla CLASICA (madera tallada, terciopelo)"


class ClassicTable(Table):
    """Mesa de estilo clasico."""

    def place_on(self) -> str:
        return "Colocando objetos en una mesa CLASICA (madera maciza, ornamentos)"


# =============================================================================
# FABRICA ABSTRACTA: Define la interfaz para crear familias de productos
# =============================================================================

class FurnitureFactory(ABC):
    """
    Interfaz de la fabrica abstracta.
    Define metodos para crear CADA tipo de producto de la familia.
    """

    @abstractmethod
    def create_chair(self) -> Chair:
        """Crea una silla del estilo de esta fabrica."""
        pass

    @abstractmethod
    def create_table(self) -> Table:
        """Crea una mesa del estilo de esta fabrica."""
        pass


# =============================================================================
# FABRICAS CONCRETAS: Cada una crea una familia completa de productos
# =============================================================================

class ModernFactory(FurnitureFactory):
    """
    Fabrica que crea muebles de estilo MODERNO.
    Todos los productos creados combinan entre si.
    """

    def create_chair(self) -> ModernChair:
        # Esta fabrica SIEMPRE crea sillas modernas
        return ModernChair()

    def create_table(self) -> ModernTable:
        # Esta fabrica SIEMPRE crea mesas modernas
        return ModernTable()


class ClassicFactory(FurnitureFactory):
    """
    Fabrica que crea muebles de estilo CLASICO.
    Todos los productos creados combinan entre si.
    """

    def create_chair(self) -> ClassicChair:
        # Esta fabrica SIEMPRE crea sillas clasicas
        return ClassicChair()

    def create_table(self) -> ClassicTable:
        # Esta fabrica SIEMPRE crea mesas clasicas
        return ClassicTable()


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON ABSTRACT FACTORY")
    print("=" * 60)
    
    # Crear las fabricas
    print("\n[1] Creando las fabricas:")
    modern_factory = ModernFactory()
    classic_factory = ClassicFactory()
    print("    - ModernFactory creada")
    print("    - ClassicFactory creada")
    
    # Amueblar con estilo moderno
    print("\n[2] Amueblando habitacion MODERNA:")
    modern_chair = modern_factory.create_chair()
    modern_table = modern_factory.create_table()
    print(f"    Silla: {modern_chair.sit_on()}")
    print(f"    Mesa:  {modern_table.place_on()}")
    
    # Amueblar con estilo clasico
    print("\n[3] Amueblando habitacion CLASICA:")
    classic_chair = classic_factory.create_chair()
    classic_table = classic_factory.create_table()
    print(f"    Silla: {classic_chair.sit_on()}")
    print(f"    Mesa:  {classic_table.place_on()}")
    
    """
    =========================================================================
    VENTAJAS DEL PATRON ABSTRACT FACTORY
    =========================================================================
    1. COHERENCIA: Los productos de una familia siempre combinan entre si
    
    2. AISLAMIENTO: El cliente no conoce las clases concretas, solo la fabrica
    
    3. INTERCAMBIABLE: Cambiar de familia es cambiar una sola linea (la fabrica)
    
    4. PRINCIPIO ABIERTO/CERRADO: Agregar familias sin modificar codigo existente
    """

