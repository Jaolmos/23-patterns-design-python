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
    def sit_on(self):
        """Metodo que deben implementar todas las sillas."""
        pass


class Table(ABC):
    """
    Interfaz para todas las mesas.
    Todas las mesas deben poder 'colocar cosas' encima.
    """
    
    @abstractmethod
    def place_on(self):
        """Metodo que deben implementar todas las mesas."""
        pass


# =============================================================================
# PRODUCTOS CONCRETOS - FAMILIA MODERNA
# =============================================================================

class ModernChair(Chair):
    """Silla de estilo moderno."""
    
    def sit_on(self):
        return "Sentado en una silla MODERNA (minimalista, metal y vidrio)"


class ModernTable(Table):
    """Mesa de estilo moderno."""
    
    def place_on(self):
        return "Colocando objetos en una mesa MODERNA (lineas rectas, cristal)"


# =============================================================================
# PRODUCTOS CONCRETOS - FAMILIA CLASICA
# =============================================================================

class ClassicChair(Chair):
    """Silla de estilo clasico."""
    
    def sit_on(self):
        return "Sentado en una silla CLASICA (madera tallada, terciopelo)"


class ClassicTable(Table):
    """Mesa de estilo clasico."""
    
    def place_on(self):
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
    def create_chair(self):
        """Crea una silla del estilo de esta fabrica."""
        pass
    
    @abstractmethod
    def create_table(self):
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
    
    def create_chair(self):
        # Esta fabrica SIEMPRE crea sillas modernas
        return ModernChair()
    
    def create_table(self):
        # Esta fabrica SIEMPRE crea mesas modernas
        return ModernTable()


class ClassicFactory(FurnitureFactory):
    """
    Fabrica que crea muebles de estilo CLASICO.
    Todos los productos creados combinan entre si.
    """
    
    def create_chair(self):
        # Esta fabrica SIEMPRE crea sillas clasicas
        return ClassicChair()
    
    def create_table(self):
        # Esta fabrica SIEMPRE crea mesas clasicas
        return ClassicTable()


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON ABSTRACT FACTORY")
    print("=" * 60)
    
    # Funcion cliente que usa la fabrica sin saber el estilo concreto
    def amueblar_habitacion(factory: FurnitureFactory, nombre_estilo: str):
        """
        Esta funcion NO sabe si recibe ModernFactory o ClassicFactory.
        Solo sabe que recibe 'alguna fabrica de muebles'.
        Todos los muebles creados combinaran porque vienen de la misma fabrica.
        """
        print(f"\n[AMUEBLANDO] Habitacion estilo {nombre_estilo}:")
        
        # Crear los muebles usando la fabrica
        silla = factory.create_chair()
        mesa = factory.create_table()
        
        # Usar los muebles
        print(f"    Silla: {silla.sit_on()}")
        print(f"    Mesa:  {mesa.place_on()}")
    
    # Crear las fabricas
    print("\n[1] Creando las fabricas:")
    modern_factory = ModernFactory()
    classic_factory = ClassicFactory()
    print("    - ModernFactory creada")
    print("    - ClassicFactory creada")
    
    # Amueblar habitaciones con diferentes estilos
    print("\n[2] Amueblando habitaciones:")
    amueblar_habitacion(modern_factory, "MODERNO")
    amueblar_habitacion(classic_factory, "CLASICO")
    
    # Demostracion de que los productos combinan
    print("\n" + "=" * 60)
    print("VENTAJA: Los productos siempre combinan")
    print("=" * 60)
    print("""
    Si usas ModernFactory:
        - Silla moderna + Mesa moderna = COMBINAN
    
    Si usas ClassicFactory:
        - Silla clasica + Mesa clasica = COMBINAN
    
    NUNCA tendras:
        - Silla moderna + Mesa clasica = NO COMBINAN
    
    La fabrica garantiza la coherencia de la familia.
    """)
    
    # Demostracion de extensibilidad
    print("=" * 60)
    print("EXTENSIBILIDAD: Agregar nueva familia")
    print("=" * 60)
    print("""
    Para agregar estilo RUSTICO:
    
    1. Crear RusticChair(Chair) y RusticTable(Table)
    2. Crear RusticFactory(FurnitureFactory)
    3. Listo! No tocas NADA del codigo existente
    
    Para agregar nuevo producto (ej: Lamp):
    
    1. Crear interfaz Lamp(ABC)
    2. Crear ModernLamp, ClassicLamp
    3. Agregar create_lamp() a FurnitureFactory y sus fabricas
    """)

