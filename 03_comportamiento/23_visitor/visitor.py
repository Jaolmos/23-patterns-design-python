"""
PATRON VISITOR - Analizador de Archivos

Analogia: Como un inspector de edificios. El inspector (visitor) visita
diferentes tipos de habitaciones (elementos) y hace inspecciones especificas
en cada una. El baño necesita revisar plomeria, la cocina revisa gas y
electricidad, etc. Cada habitacion acepta al inspector pero el inspector
decide que revisar.

PROBLEMA: Necesitas realizar diferentes operaciones sobre una estructura de
objetos sin modificar las clases de los objetos. Agregar operaciones directamente
a las clases las contamina con logica que no les corresponde.

SOLUCION: Separar las operaciones (visitors) de los objetos (elements). Los
elementos aceptan visitors, y cada visitor implementa la operacion especifica
para cada tipo de elemento. Puedes agregar nuevas operaciones sin modificar
los elementos.

VENTAJA: Agregas operaciones sin modificar elementos. Agrupa operaciones
relacionadas en un visitor. Separa operaciones de la estructura de datos.

Conceptos OOP usados:
- Abstraccion: Interfaces Visitor y Element
- Double Dispatch: El elemento decide que metodo del visitor ejecutar
- Polimorfismo: Diferentes visitors con misma interfaz
- Open/Closed: Agregas visitors sin modificar elementos
"""

from abc import ABC, abstractmethod
from typing import List
import os


# =============================================================================
# VISITOR: Interfaz para los visitantes
# =============================================================================

class FileVisitor(ABC):
    """
    Interfaz Visitor: Define una operacion para cada tipo de elemento.
    """

    @abstractmethod
    def visit_text_file(self, file: 'TextFile') -> None:
        """Visita un archivo de texto."""
        pass

    @abstractmethod
    def visit_image_file(self, file: 'ImageFile') -> None:
        """Visita un archivo de imagen."""
        pass

    @abstractmethod
    def visit_video_file(self, file: 'VideoFile') -> None:
        """Visita un archivo de video."""
        pass


# =============================================================================
# ELEMENT: Interfaz para los elementos visitables
# =============================================================================

class File(ABC):
    """
    Interfaz Element: Define el metodo accept que recibe un visitor.
    """

    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> int:
        return self._size

    @abstractmethod
    def accept(self, visitor: FileVisitor) -> None:
        """Acepta un visitor (double dispatch)."""
        pass


# =============================================================================
# ELEMENTOS CONCRETOS: Diferentes tipos de archivos
# =============================================================================

class TextFile(File):
    """
    Elemento concreto: Archivo de texto.
    """

    def __init__(self, name: str, size: int, lines: int):
        super().__init__(name, size)
        self._lines = lines

    def get_lines(self) -> int:
        return self._lines

    def accept(self, visitor: FileVisitor) -> None:
        """Acepta visitor y le dice que visite un TextFile."""
        # Double dispatch: el elemento llama al metodo especifico del visitor
        visitor.visit_text_file(self)


class ImageFile(File):
    """
    Elemento concreto: Archivo de imagen.
    """

    def __init__(self, name: str, size: int, width: int, height: int):
        super().__init__(name, size)
        self._width = width
        self._height = height

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def accept(self, visitor: FileVisitor) -> None:
        """Acepta visitor y le dice que visite un ImageFile."""
        visitor.visit_image_file(self)


class VideoFile(File):
    """
    Elemento concreto: Archivo de video.
    """

    def __init__(self, name: str, size: int, duration: int, fps: int):
        super().__init__(name, size)
        self._duration = duration  # segundos
        self._fps = fps

    def get_duration(self) -> int:
        return self._duration

    def get_fps(self) -> int:
        return self._fps

    def accept(self, visitor: FileVisitor) -> None:
        """Acepta visitor y le dice que visite un VideoFile."""
        visitor.visit_video_file(self)


# =============================================================================
# VISITORS CONCRETOS: Diferentes operaciones
# =============================================================================

class SizeAnalyzerVisitor(FileVisitor):
    """
    Visitor concreto: Analiza el tamaño de los archivos.
    """

    def __init__(self) -> None:
        # El visitor mantiene estado durante la visita
        self._total_size = 0

    def visit_text_file(self, file: TextFile) -> None:
        """Analiza archivo de texto."""
        self._total_size += file.get_size()
        print(f"  [Texto] {file.get_name()}: {file.get_size()} KB")

    def visit_image_file(self, file: ImageFile) -> None:
        """Analiza archivo de imagen."""
        self._total_size += file.get_size()
        print(f"  [Imagen] {file.get_name()}: {file.get_size()} KB")

    def visit_video_file(self, file: VideoFile) -> None:
        """Analiza archivo de video."""
        self._total_size += file.get_size()
        print(f"  [Video] {file.get_name()}: {file.get_size()} KB")

    def get_total_size(self) -> int:
        return self._total_size


class DetailedInfoVisitor(FileVisitor):
    """
    Visitor concreto: Muestra informacion detallada de cada archivo.
    """

    def visit_text_file(self, file: TextFile) -> None:
        """Muestra info detallada de archivo de texto."""
        print(f"\n  [Archivo de Texto]")
        print(f"    Nombre: {file.get_name()}")
        print(f"    Tamaño: {file.get_size()} KB")
        print(f"    Lineas: {file.get_lines()}")

    def visit_image_file(self, file: ImageFile) -> None:
        """Muestra info detallada de archivo de imagen."""
        print(f"\n  [Archivo de Imagen]")
        print(f"    Nombre: {file.get_name()}")
        print(f"    Tamaño: {file.get_size()} KB")
        print(f"    Resolucion: {file.get_width()}x{file.get_height()} px")
        pixels = file.get_width() * file.get_height()
        print(f"    Total pixeles: {pixels:,}")

    def visit_video_file(self, file: VideoFile) -> None:
        """Muestra info detallada de archivo de video."""
        print(f"\n  [Archivo de Video]")
        print(f"    Nombre: {file.get_name()}")
        print(f"    Tamaño: {file.get_size()} KB")
        print(f"    Duracion: {file.get_duration()} segundos")
        print(f"    FPS: {file.get_fps()}")
        print(f"    Total frames: {file.get_duration() * file.get_fps()}")


class CompressionVisitor(FileVisitor):
    """
    Visitor concreto: Simula compresion de archivos.
    """

    def visit_text_file(self, file: TextFile) -> None:
        """Comprime archivo de texto."""
        compressed = file.get_size() * 0.3  # 70% de compresion
        print(f"  [Texto] {file.get_name()}: {file.get_size()} KB -> {compressed:.1f} KB")

    def visit_image_file(self, file: ImageFile) -> None:
        """Comprime archivo de imagen."""
        compressed = file.get_size() * 0.5  # 50% de compresion
        print(f"  [Imagen] {file.get_name()}: {file.get_size()} KB -> {compressed:.1f} KB")

    def visit_video_file(self, file: VideoFile) -> None:
        """Comprime archivo de video."""
        compressed = file.get_size() * 0.4  # 60% de compresion
        print(f"  [Video] {file.get_name()}: {file.get_size()} KB -> {compressed:.1f} KB")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON VISITOR - Analizador de Archivos")
    print("=" * 70)

    # --- Crear archivos ---
    print("\n[PASO 1] Crear estructura de archivos")
    print("-" * 70)
    files: List[File] = [
        TextFile("documento.txt", 50, 1000),
        TextFile("notas.txt", 30, 500),
        ImageFile("foto.jpg", 2048, 1920, 1080),
        ImageFile("logo.png", 512, 800, 600),
        VideoFile("presentacion.mp4", 102400, 180, 30),
        VideoFile("tutorial.avi", 51200, 90, 24),
    ]
    print(f"  {len(files)} archivos creados")

    # --- Usar visitor de analisis de tamaño ---
    print("\n[PASO 2] Analizar tamaño de archivos")
    print("-" * 70)
    size_analyzer = SizeAnalyzerVisitor()
    for file in files:
        file.accept(size_analyzer)
    print(f"\n  Tamaño total: {size_analyzer.get_total_size()} KB")

    # --- Usar visitor de informacion detallada ---
    print("\n[PASO 3] Mostrar informacion detallada")
    print("-" * 70)
    detail_visitor = DetailedInfoVisitor()
    for file in files:
        file.accept(detail_visitor)

    # --- Usar visitor de compresion ---
    print("\n[PASO 4] Simular compresion de archivos")
    print("-" * 70)
    compression_visitor = CompressionVisitor()
    for file in files:
        file.accept(compression_visitor)

    # --- Demostrar que podemos agregar nuevas operaciones ---
    print("\n[PASO 5] Agregar nueva operacion sin modificar archivos")
    print("-" * 70)
    print("  Se pueden agregar nuevos visitors (operaciones) sin modificar")
    print("  las clases TextFile, ImageFile, VideoFile")
    print("  Ejemplo: ExportVisitor, EncryptVisitor, BackupVisitor, etc.")

    """
    =========================================================================
    VENTAJAS DEL PATRON VISITOR
    =========================================================================
    1. OPEN/CLOSED: Agregas operaciones sin modificar elementos

    2. AGRUPACION: Operaciones relacionadas juntas en un visitor

    3. SEPARACION: Separa operaciones de estructura de datos

    4. FACIL EXTENSION: Nuevos visitors sin tocar elementos existentes

    5. ACCESO: El visitor accede a la estructura interna de elementos
    """
