"""
PATRON FACADE - Arranque de Computadora

Analogia: El boton de encendido de un ordenador. Por detras hay un proceso
complejo (BIOS, CPU, memoria, disco), pero tu solo presionas un boton.
La fachada oculta toda esa complejidad.

PROBLEMA: Tienes un sistema con muchos subsistemas complejos. El cliente
tendria que conocer y coordinar todos: inicializar BIOS, arrancar CPU,
cargar memoria, activar disco... en el orden correcto.

SOLUCION: Crear una "fachada" que proporciona una interfaz simple.
El cliente solo llama a start() y la fachada coordina todo internamente.

VENTAJA: El cliente no necesita conocer los subsistemas ni su orden.
Solo usa la fachada. Los subsistemas pueden cambiar sin afectar al cliente.

Conceptos OOP usados:
- Composicion: La fachada CREA los subsistemas internamente
- Delegacion: La fachada delega el trabajo a los subsistemas
"""


# =============================================================================
# SUBSISTEMAS: Componentes complejos del sistema
# =============================================================================

class BIOS:
    """
    Subsistema: BIOS (Basic Input/Output System).
    Se encarga de inicializar y verificar el hardware.
    """

    def initialize(self) -> None:
        print("[BIOS] Inicializando BIOS...")

    def check_hardware(self) -> None:
        print("[BIOS] Verificando hardware... OK")

    def load_boot_sector(self) -> None:
        print("[BIOS] Cargando sector de arranque...")


class CPU:
    """
    Subsistema: Procesador.
    Se encarga de ejecutar instrucciones.
    """

    def freeze(self) -> None:
        print("[CPU] Congelando procesador...")

    def jump(self, address: int) -> None:
        print(f"[CPU] Saltando a direccion {address}")

    def execute(self) -> None:
        print("[CPU] Ejecutando instrucciones...")

    def stop(self) -> None:
        print("[CPU] Deteniendo procesador...")


class Memory:
    """
    Subsistema: Memoria RAM.
    Se encarga de cargar datos para acceso rapido.
    """

    def load(self, address: int, data: str) -> None:
        print(f"[Memory] Cargando '{data}' en direccion {address}")

    def free(self) -> None:
        print("[Memory] Liberando memoria...")


class HardDrive:
    """
    Subsistema: Disco duro.
    Se encarga de leer y escribir datos persistentes.
    """

    def read(self, sector: int, size: int) -> str:
        print(f"[HardDrive] Leyendo {size} bytes del sector {sector}")
        return f"datos_del_sector_{sector}"

    def spin_up(self) -> None:
        print("[HardDrive] Iniciando disco duro...")

    def spin_down(self) -> None:
        print("[HardDrive] Deteniendo disco duro...")


class CoolingSystem:
    """
    Subsistema: Sistema de refrigeracion.
    Se encarga de mantener la temperatura adecuada.
    """

    def start_fans(self) -> None:
        print("[Cooling] Iniciando ventiladores...")

    def stop_fans(self) -> None:
        print("[Cooling] Deteniendo ventiladores...")


# =============================================================================
# FACADE: Interfaz simple para el sistema complejo
# =============================================================================

class Computer:
    """
    Fachada: Proporciona una interfaz simple para el sistema complejo.
    El cliente solo necesita llamar a start() y shutdown().
    """

    def __init__(self) -> None:
        # Composicion: la fachada CREA todos los subsistemas
        self._bios = BIOS()
        self._cpu = CPU()
        self._memory = Memory()
        self._hard_drive = HardDrive()
        self._cooling = CoolingSystem()

    def start(self) -> None:
        """
        Enciende el ordenador.
        Coordina todos los subsistemas en el orden correcto.
        """
        print("\n" + "=" * 50)
        print("ENCENDIENDO ORDENADOR...")
        print("=" * 50)
        
        # 1. Iniciar refrigeracion
        self._cooling.start_fans()
        
        # 2. BIOS inicializa y verifica
        self._bios.initialize()
        self._bios.check_hardware()
        
        # 3. CPU se prepara
        self._cpu.freeze()
        
        # 4. Disco duro arranca y lee datos
        self._hard_drive.spin_up()
        boot_data = self._hard_drive.read(sector=0, size=1024)
        
        # 5. Memoria carga los datos del arranque
        self._memory.load(address=0x0000, data=boot_data)
        
        # 6. BIOS carga el sector de arranque
        self._bios.load_boot_sector()
        
        # 7. CPU salta a la direccion de inicio y ejecuta
        self._cpu.jump(address=0x0000)
        self._cpu.execute()
        
        print("=" * 50)
        print("ORDENADOR LISTO!")
        print("=" * 50 + "\n")

    def shutdown(self) -> None:
        """
        Apaga el ordenador.
        Coordina el apagado en orden inverso.
        """
        print("\n" + "=" * 50)
        print("APAGANDO ORDENADOR...")
        print("=" * 50)
        
        # Apagar en orden inverso
        self._cpu.stop()
        self._memory.free()
        self._hard_drive.spin_down()
        self._cooling.stop_fans()
        
        print("=" * 50)
        print("ORDENADOR APAGADO")
        print("=" * 50 + "\n")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PATRON FACADE - Arranque de Computadora")
    print("=" * 60)
    
    # --- Demostracion ---
    print("\n[1] Creando el ordenador (fachada):")
    print("    computer = Computer()")
    
    # El cliente solo conoce la fachada
    computer = Computer()
    
    # Encender es una sola llamada
    print("\n[2] Encendiendo con una sola llamada:")
    print("    computer.start()")
    computer.start()
    
    # Simular uso del ordenador
    print("[Usuario] Trabajando con el ordenador...")
    print("[Usuario] Guardando archivos...")
    
    # Apagar es una sola llamada
    print("\n[3] Apagando con una sola llamada:")
    print("    computer.shutdown()")
    computer.shutdown()
    
    """
    =========================================================================
    VENTAJAS DEL PATRON FACADE
    =========================================================================
    1. SIMPLICIDAD: El cliente solo conoce la fachada, no los subsistemas
    
    2. DESACOPLAMIENTO: El cliente no depende de los subsistemas directamente
    
    3. MANTENIBILIDAD: Puedes cambiar subsistemas sin afectar al cliente
    
    4. ORGANIZACION: Agrupa funcionalidad relacionada en una interfaz coherente
    """

