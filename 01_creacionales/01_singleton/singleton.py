"""
PATRON SINGLETON
================
Garantiza que una clase tenga UNA SOLA instancia y proporciona
un punto de acceso global a ella.

Analogia: Como el presidente de un pais - solo puede haber uno.

PROBLEMA: Crear multiples instancias de algo que deberia ser unico
(conexiones BD, configuracion, logs) desperdicia recursos y causa
inconsistencias.

SOLUCION: Controlar la creacion para que siempre se devuelva la misma
instancia.

COMO: En Python usamos __new__ (que CREA el objeto) en lugar de __init__
(que lo INICIALIZA). Guardamos la instancia en una variable de clase.
"""


class DatabaseConnection:
    """
    Clase que simula una conexion a base de datos.
    Implementa el patron Singleton para garantizar una unica instancia.
    """
    
    # Variable de clase que guarda la unica instancia
    # Al principio no existe ninguna instancia
    _instance = None
    
    def __new__(cls):
        """
        __new__ es el metodo que CREA el objeto (antes de __init__).
        Aqui controlamos si ya existe una instancia o no.
        """
        # Si NO existe una instancia previa...
        if cls._instance is None:
            print("[CREAR] Creando la UNICA instancia de DatabaseConnection...")
            # Creamos la instancia usando el __new__ de la clase padre (object)
            cls._instance = super().__new__(cls)
            # Inicializamos atributos de la instancia
            cls._instance.connected = False
        else:
            print("[REUSAR] Reutilizando la instancia existente...")
        
        # Siempre devolvemos la MISMA instancia
        return cls._instance
    
    def connect(self):
        """Simula conectar a la base de datos."""
        if not self.connected:
            self.connected = True
            print("[OK] Conectado a la base de datos")
        else:
            print("[INFO] Ya estabas conectado")
    
    def disconnect(self):
        """Simula desconectar de la base de datos."""
        if self.connected:
            self.connected = False
            print("[OK] Desconectado de la base de datos")
        else:
            print("[INFO] Ya estabas desconectado")
    
    def execute_query(self, query):
        """Simula ejecutar una consulta."""
        if self.connected:
            print(f"[QUERY] Ejecutando: {query}")
        else:
            print("[ERROR] No estas conectado a la base de datos")


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON SINGLETON")
    print("=" * 60)
    
    # Intentamos crear "varias" conexiones
    print("\n[1] Creando primera 'conexion':")
    db1 = DatabaseConnection()
    
    print("\n[2] Creando segunda 'conexion':")
    db2 = DatabaseConnection()
    
    print("\n[3] Creando tercera 'conexion':")
    db3 = DatabaseConnection()
    
    # Verificamos que todas son LA MISMA instancia
    print("\n" + "=" * 60)
    print("VERIFICACION: Son la misma instancia?")
    print("=" * 60)
    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"db2 is db3: {db2 is db3}")  # True
    print(f"ID de db1: {id(db1)}")
    print(f"ID de db2: {id(db2)}")
    print(f"ID de db3: {id(db3)}")
    
    # Demostracion de uso compartido
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Estado compartido")
    print("=" * 60)
    
    print("\n[PASO] Conectamos usando db1:")
    db1.connect()
    
    print("\n[PASO] Ejecutamos query usando db2 (misma conexion):")
    db2.execute_query("SELECT * FROM usuarios")
    
    print("\n[PASO] Desconectamos usando db3 (misma conexion):")
    db3.disconnect()
    
    print("\n[PASO] Intentamos ejecutar query con db1 (ya desconectado):")
    db1.execute_query("SELECT * FROM productos")
