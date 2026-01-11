"""
PATRON PROXY - Acceso a Base de Datos con Permisos

Analogia: Un guardia de seguridad en la entrada de un edificio. El guardia
(proxy) verifica tu identificacion antes de dejarte pasar al edificio real.
No puedes acceder directamente, siempre pasas por el guardia.

PROBLEMA: Quieres controlar el acceso a un objeto (base de datos). No todos
los usuarios deberian poder hacer todas las operaciones. Un usuario normal
no deberia poder borrar datos, solo un admin.

SOLUCION: Crear un proxy que tiene la misma interfaz que el objeto real.
El proxy intercepta las llamadas, verifica permisos, y solo entonces
delega al objeto real si esta permitido.

VENTAJA: Controlas el acceso sin modificar el objeto real. Puedes añadir
logging, cache, validacion, etc. de forma transparente.

Conceptos OOP usados:
- Composicion: Proxy CONTIENE referencia al objeto real
- Herencia: Proxy y Real implementan la misma interfaz
- Polimorfismo: El cliente no distingue entre proxy y real
"""

from abc import ABC, abstractmethod


# =============================================================================
# INTERFAZ: Define las operaciones de la base de datos
# =============================================================================

class Database(ABC):
    """
    Interfaz comun para la base de datos real y el proxy.
    El cliente trabaja con esta interfaz sin saber si es proxy o real.
    """
    
    @abstractmethod
    def read(self, query: str) -> str:
        """Lee datos de la base de datos."""
        pass
    
    @abstractmethod
    def write(self, query: str) -> bool:
        """Escribe datos en la base de datos."""
        pass
    
    @abstractmethod
    def delete(self, query: str) -> bool:
        """Elimina datos de la base de datos."""
        pass


# =============================================================================
# OBJETO REAL: La base de datos real
# =============================================================================

class RealDatabase(Database):
    """
    Objeto real: La base de datos que queremos proteger.
    Ejecuta las operaciones sin verificar permisos.
    """
    
    def __init__(self):
        # Simulamos datos en memoria
        self._data = {
            "users": ["ana", "luis", "maria"],
            "products": ["laptop", "mouse", "keyboard"],
            "orders": ["order_001", "order_002"]
        }
        print("[RealDB] Base de datos inicializada")
    
    def read(self, query: str) -> str:
        print(f"[RealDB] Ejecutando lectura: {query}")
        # Simulamos una consulta simple
        table = query.replace("SELECT * FROM ", "")
        if table in self._data:
            return f"Resultados: {self._data[table]}"
        return "Tabla no encontrada"
    
    def write(self, query: str) -> bool:
        print(f"[RealDB] Ejecutando escritura: {query}")
        return True
    
    def delete(self, query: str) -> bool:
        print(f"[RealDB] Ejecutando eliminacion: {query}")
        return True


# =============================================================================
# PROXY: Controla el acceso a la base de datos
# =============================================================================

class DatabaseProxy(Database):
    """
    Proxy de proteccion: Verifica permisos antes de acceder a la BD real.
    Tiene la misma interfaz que RealDatabase.
    """
    
    # Definimos los permisos por rol
    PERMISSIONS = {
        "guest": ["read"],           # Solo lectura
        "user": ["read", "write"],   # Lectura y escritura
        "admin": ["read", "write", "delete"]  # Todo
    }
    
    def __init__(self, user: str, role: str):
        self._user = user
        self._role = role
        # Composicion: el proxy CONTIENE la base de datos real
        # Lazy loading: solo se crea cuando se necesita
        self._real_database = None
    
    def _get_database(self) -> RealDatabase:
        """Obtiene la base de datos real (lazy loading)."""
        if self._real_database is None:
            print(f"[Proxy] Creando conexion a BD para '{self._user}'")
            self._real_database = RealDatabase()
        return self._real_database
    
    def _check_permission(self, operation: str) -> bool:
        """Verifica si el usuario tiene permiso para la operacion."""
        allowed = self.PERMISSIONS.get(self._role, [])
        has_permission = operation in allowed
        
        if has_permission:
            print(f"[Proxy] Permiso OK: '{self._user}' ({self._role}) -> {operation}")
        else:
            print(f"[Proxy] DENEGADO: '{self._user}' ({self._role}) no puede -> {operation}")
        
        return has_permission
    
    def _log_access(self, operation: str, query: str):
        """Registra el acceso (logging adicional del proxy)."""
        print(f"[Proxy] LOG: {self._user} ejecuto {operation}")
    
    def read(self, query: str) -> str:
        if not self._check_permission("read"):
            return "ERROR: Permiso denegado para lectura"
        
        result = self._get_database().read(query)
        self._log_access("read", query)
        return result
    
    def write(self, query: str) -> bool:
        if not self._check_permission("write"):
            print("ERROR: Permiso denegado para escritura")
            return False
        
        result = self._get_database().write(query)
        self._log_access("write", query)
        return result
    
    def delete(self, query: str) -> bool:
        if not self._check_permission("delete"):
            print("ERROR: Permiso denegado para eliminacion")
            return False
        
        result = self._get_database().delete(query)
        self._log_access("delete", query)
        return result


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PATRON PROXY - Acceso a Base de Datos con Permisos")
    print("=" * 60)
    
    # --- Usuario invitado (solo lectura) ---
    print("\n[1] Usuario INVITADO (guest) - solo puede leer:")
    print("-" * 50)
    
    guest_db = DatabaseProxy(user="visitante", role="guest")
    
    print("\n  Intentando LEER:")
    result = guest_db.read("SELECT * FROM users")
    print(f"  Resultado: {result}")
    
    print("\n  Intentando ESCRIBIR:")
    guest_db.write("INSERT INTO users VALUES ('nuevo')")
    
    print("\n  Intentando ELIMINAR:")
    guest_db.delete("DELETE FROM users WHERE name='ana'")
    
    # --- Usuario normal (lectura y escritura) ---
    print("\n" + "=" * 60)
    print("[2] Usuario NORMAL (user) - puede leer y escribir:")
    print("-" * 50)
    
    user_db = DatabaseProxy(user="empleado_juan", role="user")
    
    print("\n  Intentando LEER:")
    result = user_db.read("SELECT * FROM products")
    print(f"  Resultado: {result}")
    
    print("\n  Intentando ESCRIBIR:")
    user_db.write("INSERT INTO products VALUES ('monitor')")
    
    print("\n  Intentando ELIMINAR:")
    user_db.delete("DELETE FROM products WHERE name='mouse'")
    
    # --- Administrador (todo permitido) ---
    print("\n" + "=" * 60)
    print("[3] Usuario ADMIN (admin) - puede hacer todo:")
    print("-" * 50)
    
    admin_db = DatabaseProxy(user="admin_carlos", role="admin")
    
    print("\n  Intentando LEER:")
    result = admin_db.read("SELECT * FROM orders")
    print(f"  Resultado: {result}")
    
    print("\n  Intentando ESCRIBIR:")
    admin_db.write("INSERT INTO orders VALUES ('order_003')")
    
    print("\n  Intentando ELIMINAR:")
    admin_db.delete("DELETE FROM orders WHERE id='order_001'")
    
    # --- Demostrar que es transparente ---
    print("\n" + "=" * 60)
    print("DEMOSTRACION: El cliente usa la misma interfaz")
    print("=" * 60)
    
    print("\n[4] Misma operacion, diferentes permisos:")
    print(f"  Guest: {guest_db.read('SELECT * FROM users')}")
    print(f"  Admin: {admin_db.read('SELECT * FROM users')}")
    
    """
    =========================================================================
    VENTAJAS DEL PATRON PROXY
    =========================================================================
    1. CONTROL DE ACCESO: Verificas permisos antes de ejecutar
    
    2. LAZY LOADING: La BD real solo se crea cuando se necesita
    
    3. LOGGING: Registras todas las operaciones automaticamente
    
    4. TRANSPARENCIA: El cliente no sabe que usa un proxy
    """

