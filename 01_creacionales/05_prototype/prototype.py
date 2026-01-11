"""
PATRON PROTOTYPE
================
Crea nuevos objetos clonando un objeto existente, en lugar de crearlos
desde cero.

Analogia: Clonar enemigos en un videojuego. En lugar de configurar cada
enemigo desde cero, tienes plantillas base y las clonas cuando necesitas.

PROBLEMA: Crear objetos desde cero puede ser costoso o repetitivo.
Si ya tienes un objeto configurado, es mas facil copiarlo.

SOLUCION: Definir un metodo clone() que devuelva una copia del objeto.
Usamos copy.deepcopy() para copiar todo, incluyendo objetos anidados.

VENTAJA: Clonar es mas rapido que crear desde cero. Puedes tener
prototipos base y crear variaciones a partir de ellos.
"""

import copy


class Enemy:
    """
    Clase que representa un enemigo en un videojuego.
    Puede clonarse para crear copias rapidamente.
    """
    
    def __init__(self, name, health, damage, speed, loot):
        self.name = name
        self.health = health
        self.damage = damage
        self.speed = speed
        self.loot = loot  # Lista de objetos que suelta al morir
    
    def clone(self):
        """
        Crea y devuelve una copia profunda de este enemigo.
        Usamos deepcopy para que la lista 'loot' tambien se copie.
        """
        return copy.deepcopy(self)
    
    def show_info(self):
        """Muestra la informacion del enemigo."""
        print(f"\n  [{self.name}]")
        print(f"  Salud: {self.health} | Dano: {self.damage} | Velocidad: {self.speed}")
        print(f"  Loot: {self.loot}")
        print(f"  ID en memoria: {id(self)}")


class EnemyRegistry:
    """
    Registro de prototipos de enemigos.
    Guarda enemigos base que pueden clonarse cuando se necesiten.
    """
    
    def __init__(self):
        self._prototypes = {}
    
    def register(self, name, prototype):
        """Registra un prototipo con un nombre."""
        self._prototypes[name] = prototype
    
    def create(self, name):
        """Crea un nuevo enemigo clonando el prototipo registrado."""
        if name not in self._prototypes:
            print(f"[ERROR] Prototipo '{name}' no encontrado")
            return None
        return self._prototypes[name].clone()


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON PROTOTYPE")
    print("=" * 60)
    
    # Crear prototipos base (enemigos "plantilla")
    print("\n[1] CREANDO PROTOTIPOS BASE:")
    
    orc_prototype = Enemy(
        name="Orco",
        health=100,
        damage=15,
        speed=5,
        loot=["oro", "pocion"]
    )
    
    goblin_prototype = Enemy(
        name="Goblin",
        health=50,
        damage=8,
        speed=10,
        loot=["moneda"]
    )
    
    dragon_prototype = Enemy(
        name="Dragon",
        health=500,
        damage=50,
        speed=8,
        loot=["tesoro", "escama", "espada legendaria"]
    )
    
    print("    - Prototipo Orco creado")
    print("    - Prototipo Goblin creado")
    print("    - Prototipo Dragon creado")
    
    # Registrar prototipos
    print("\n[2] REGISTRANDO PROTOTIPOS:")
    registry = EnemyRegistry()
    registry.register("orco", orc_prototype)
    registry.register("goblin", goblin_prototype)
    registry.register("dragon", dragon_prototype)
    print("    Prototipos registrados en el registry")
    
    # Clonar enemigos usando el registry
    print("\n[3] CLONANDO ENEMIGOS:")
    
    orco1 = registry.create("orco")
    orco2 = registry.create("orco")
    goblin1 = registry.create("goblin")
    dragon_boss = registry.create("dragon")
    
    print("\n    Enemigos clonados:")
    orco1.show_info()
    orco2.show_info()
    goblin1.show_info()
    dragon_boss.show_info()
    
    # Demostrar que son objetos diferentes
    print("\n" + "=" * 60)
    print("VERIFICACION: Son objetos diferentes?")
    print("=" * 60)
    print(f"\n    orco1 is orco2: {orco1 is orco2}")  # False
    print(f"    orco1 is orc_prototype: {orco1 is orc_prototype}")  # False
    print("\n    Cada clon tiene su propio ID en memoria (son independientes)")
    
    # Demostrar deep copy (loot independiente)
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Deep Copy (loot independiente)")
    print("=" * 60)
    
    print("\n    Modificamos el loot de orco1:")
    orco1.loot.append("hacha")
    print(f"    orco1.loot: {orco1.loot}")
    print(f"    orco2.loot: {orco2.loot}")
    print(f"    prototipo.loot: {orc_prototype.loot}")
    print("\n    Solo orco1 cambio! (deep copy funciona)")
    
    # Demostrar personalizacion de clones
    print("\n" + "=" * 60)
    print("PERSONALIZACION: Modificar clones")
    print("=" * 60)
    
    print("\n    Creamos un orco jefe (clon modificado):")
    orco_jefe = registry.create("orco")
    orco_jefe.name = "Orco Jefe"
    orco_jefe.health = 200
    orco_jefe.damage = 30
    orco_jefe.loot.append("llave del calabozo")
    
    orco_jefe.show_info()
    
    print("\n    El prototipo original no cambio:")
    orc_prototype.show_info()
    
    """
    =========================================================================
    VENTAJAS DEL PATRON PROTOTYPE
    =========================================================================
    1. RAPIDEZ: Clonar es mas rapido que crear desde cero
    
    2. SIMPLICIDAD: No necesitas conocer la clase concreta
       registry.create("orco") funciona sin saber que es Enemy
    
    3. FLEXIBILIDAD: Puedes modificar clones sin afectar el original
    
    4. PROTOTIPOS: Guardas "plantillas" y creas variaciones
    """

