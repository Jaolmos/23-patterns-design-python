"""
PATRON COMPOSITE - Sistema de Archivos

Analogia: Una caja con productos. La caja puede contener productos sueltos
u otras cajas mas pequenas. Para saber el precio total, sumas todo lo de
dentro, sin importar si es un producto o una caja llena de cosas.

PROBLEMA: Tienes estructuras de arbol (carpetas con archivos y subcarpetas).
Quieres tratar archivos individuales y carpetas de la misma forma, por ejemplo
calcular el tamaño total sin importar si es un archivo o una carpeta con 100 archivos.

SOLUCION: Definir una interfaz comun (Component) que implementan tanto los
elementos simples (Leaf/File) como los contenedores (Composite/Folder).

VENTAJA: El cliente no necesita saber si trabaja con un archivo o una carpeta.
Llama a get_size() y funciona igual en ambos casos.

Conceptos OOP usados:
- Composicion: Folder CONTIENE una lista de FileSystemItem
- Herencia: File y Folder heredan de FileSystemItem
- Polimorfismo: get_size() funciona diferente en File y Folder
- Recursion: Folder llama a get_size() de sus hijos
"""

from abc import ABC, abstractmethod


# =============================================================================
# COMPONENT: Interfaz comun para archivos y carpetas
# =============================================================================

class FileSystemItem(ABC):
    """
    Componente base.
    Define la interfaz que comparten archivos y carpetas.
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def get_size(self) -> int:
        """Retorna el tamaño en bytes."""
        pass
    
    @abstractmethod
    def show(self, indent: int = 0):
        """Muestra el item con indentacion."""
        pass


# =============================================================================
# LEAF: Elemento simple (no tiene hijos)
# =============================================================================

class File(FileSystemItem):
    """
    Hoja del arbol: un archivo.
    No puede contener otros elementos.
    """
    
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size  # Tamaño en bytes
    
    def get_size(self) -> int:
        # Un archivo simplemente retorna su tamaño
        return self.size
    
    def show(self, indent: int = 0):
        # Muestra el archivo con su tamaño
        spaces = "  " * indent
        print(f"{spaces}[Archivo] {self.name} ({self.size} bytes)")


# =============================================================================
# COMPOSITE: Elemento compuesto (puede tener hijos)
# =============================================================================

class Folder(FileSystemItem):
    """
    Compuesto: una carpeta.
    Puede contener archivos y otras carpetas.
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        # Composicion: la carpeta CONTIENE una lista de items
        self._children: list[FileSystemItem] = []
    
    def add(self, item: FileSystemItem):
        """Agrega un archivo o carpeta."""
        self._children.append(item)
    
    def remove(self, item: FileSystemItem):
        """Elimina un archivo o carpeta."""
        self._children.remove(item)
    
    def get_size(self) -> int:
        # Una carpeta suma el tamaño de todos sus hijos (recursivo)
        total = 0
        for child in self._children:
            total += child.get_size()  # Polimorfismo: funciona con File o Folder
        return total
    
    def show(self, indent: int = 0):
        # Muestra la carpeta y su contenido
        spaces = "  " * indent
        print(f"{spaces}[Carpeta] {self.name}/ ({self.get_size()} bytes)")
        
        # Muestra cada hijo con mas indentacion
        for child in self._children:
            child.show(indent + 1)


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PATRON COMPOSITE - Sistema de Archivos")
    print("=" * 60)
    
    # --- Crear estructura de archivos ---
    print("\n[1] Creando estructura de archivos:")
    
    # Archivos sueltos
    readme = File("README.md", 1500)
    gitignore = File(".gitignore", 200)
    
    # Carpeta src con archivos
    src = Folder("src")
    src.add(File("main.py", 3000))
    src.add(File("utils.py", 1200))
    src.add(File("config.py", 800))
    
    # Carpeta tests dentro de src
    tests = Folder("tests")
    tests.add(File("test_main.py", 2500))
    tests.add(File("test_utils.py", 1800))
    src.add(tests)  # tests dentro de src
    
    # Carpeta docs
    docs = Folder("docs")
    docs.add(File("manual.pdf", 50000))
    docs.add(File("api.html", 8000))
    
    # Carpeta raiz del proyecto
    proyecto = Folder("mi_proyecto")
    proyecto.add(readme)
    proyecto.add(gitignore)
    proyecto.add(src)
    proyecto.add(docs)
    
    print("    Estructura creada!")
    
    # --- Mostrar estructura ---
    print("\n[2] Estructura del proyecto:")
    print("-" * 40)
    proyecto.show()
    
    # --- Demostrar polimorfismo ---
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Polimorfismo con get_size()")
    print("=" * 60)
    
    print("\n[3] Tamaño de elementos individuales:")
    print(f"    readme.get_size()    = {readme.get_size()} bytes")
    print(f"    tests.get_size()     = {tests.get_size()} bytes (suma de sus archivos)")
    print(f"    src.get_size()       = {src.get_size()} bytes (incluye tests/)")
    print(f"    proyecto.get_size()  = {proyecto.get_size()} bytes (todo el proyecto)")
    
    # --- La magia del Composite ---
    print("\n[4] La magia: tratar todo igual")
    
    def mostrar_info(item: FileSystemItem):
        """
        Esta funcion NO sabe si recibe un File o un Folder.
        Solo sabe que tiene get_size() y show().
        """
        print(f"    '{item.name}' ocupa {item.get_size()} bytes")
    
    # Funciona igual con archivos y carpetas
    mostrar_info(readme)      # Un archivo
    mostrar_info(tests)       # Una carpeta
    mostrar_info(proyecto)    # Carpeta raiz
    
    # --- Modificar estructura ---
    print("\n[5] Modificando estructura:")
    print(f"    Tamaño antes: {src.get_size()} bytes")
    
    nuevo_archivo = File("helpers.py", 500)
    src.add(nuevo_archivo)
    print(f"    Agregado helpers.py (500 bytes)")
    print(f"    Tamaño despues: {src.get_size()} bytes")
    
    """
    =========================================================================
    VENTAJAS DEL PATRON COMPOSITE
    =========================================================================
    1. UNIFORMIDAD: Tratas archivos y carpetas con la misma interfaz
    
    2. SIMPLICIDAD: El cliente no necesita distinguir entre hoja y compuesto
    
    3. EXTENSIBILIDAD: Facil agregar nuevos tipos (ej: Link, Shortcut)
    
    4. RECURSION NATURAL: Las operaciones en carpetas se propagan automaticamente
    """

