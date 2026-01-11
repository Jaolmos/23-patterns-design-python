"""
PATRON FACTORY METHOD
=====================
Define una interfaz para crear objetos, pero deja que las subclases
decidan que clase instanciar.

Analogia: Diferentes fabricas de un mismo producto. Una fabrica hace
sillas, otra mesas, otra armarios. Todas son fabricas de muebles, pero
cada una esta especializada en crear una cosa concreta.

PROBLEMA: El codigo cliente usa if/elif para crear diferentes tipos
de objetos. Cada tipo nuevo requiere modificar ese codigo.

SOLUCION: Delegar la creacion a subclases (fabricas). Cada fabrica
sabe crear su tipo de producto.

VENTAJA: Agregar tipos nuevos = crear nueva fabrica, sin tocar codigo
existente. El cliente trabaja con interfaces, no clases concretas.
"""

# ABC = Abstract Base Class (clase base abstracta)
# abstractmethod = decorador que OBLIGA a implementar el metodo en subclases
from abc import ABC, abstractmethod


# =============================================================================
# PRODUCTO: La interfaz que define que deben hacer todos los documentos
# =============================================================================

class Document(ABC):
    """
    Clase abstracta que define la interfaz de todos los documentos.
    Todos los documentos deben poder 'generarse'.
    """
    
    @abstractmethod
    def generate(self):
        """
        Metodo abstracto: las subclases DEBEN implementarlo.
        Si no lo implementan, Python lanza error.
        """
        pass


# =============================================================================
# PRODUCTOS CONCRETOS: Las implementaciones reales de Document
# =============================================================================

class PDF(Document):
    """Documento PDF concreto."""
    
    def generate(self):
        return "Generando documento en formato PDF"


class Markdown(Document):
    """Documento Markdown concreto."""
    
    def generate(self):
        return "Generando documento en formato Markdown"


class HTML(Document):
    """Documento HTML concreto."""
    
    def generate(self):
        return "Generando documento en formato HTML"


# =============================================================================
# FABRICA: La interfaz que define como crear documentos
# =============================================================================

class DocumentFactory(ABC):
    """
    Clase abstracta que define la interfaz de todas las fabricas.
    Cada fabrica debe saber 'crear un documento'.
    """
    
    @abstractmethod
    def create_document(self):
        """
        Metodo factory: las subclases deciden QUE documento crear.
        Este es el corazon del patron.
        """
        pass
    
    def operation(self):
        """
        Metodo que USA el factory method.
        No sabe que tipo de documento se creara, solo que sera un Document.
        """
        # Llama al metodo factory (implementado en subclases)
        document = self.create_document()
        # Usa el documento sin saber su tipo concreto
        return document.generate()


# =============================================================================
# FABRICAS CONCRETAS: Cada una sabe crear un tipo especifico de documento
# =============================================================================

class PDFFactory(DocumentFactory):
    """Fabrica que crea documentos PDF."""
    
    def create_document(self):
        # Esta fabrica SIEMPRE crea PDFs
        return PDF()


class MarkdownFactory(DocumentFactory):
    """Fabrica que crea documentos Markdown."""
    
    def create_document(self):
        # Esta fabrica SIEMPRE crea Markdowns
        return Markdown()


class HTMLFactory(DocumentFactory):
    """Fabrica que crea documentos HTML."""
    
    def create_document(self):
        # Esta fabrica SIEMPRE crea HTMLs
        return HTML()


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON FACTORY METHOD")
    print("=" * 60)
    
    # Creamos las fabricas (cada una sabe crear su tipo de documento)
    print("\n[1] Creando las fabricas:")
    pdf_factory = PDFFactory()
    markdown_factory = MarkdownFactory()
    html_factory = HTMLFactory()
    print("    - PDFFactory creada")
    print("    - MarkdownFactory creada")
    print("    - HTMLFactory creada")
    
    # Usamos las fabricas para generar documentos
    print("\n[2] Generando documentos con cada fabrica:")
    print(f"    PDF:      {pdf_factory.operation()}")
    print(f"    Markdown: {markdown_factory.operation()}")
    print(f"    HTML:     {html_factory.operation()}")
    
    # Demostracion de polimorfismo: el codigo cliente no conoce el tipo concreto
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Polimorfismo")
    print("=" * 60)
    
    print("\n[3] Usando una funcion que acepta CUALQUIER fabrica:")
    
    def procesar_documento(factory: DocumentFactory):
        """
        Esta funcion no sabe que tipo de documento se creara.
        Solo sabe que recibe 'alguna fabrica' y llama a operation().
        """
        print(f"    Resultado: {factory.operation()}")
    
    # La misma funcion funciona con cualquier fabrica
    print("\n    Pasando PDFFactory:")
    procesar_documento(pdf_factory)
    
    print("\n    Pasando MarkdownFactory:")
    procesar_documento(markdown_factory)
    
    print("\n    Pasando HTMLFactory:")
    procesar_documento(html_factory)
    
    """
    =========================================================================
    VENTAJA: Extensibilidad
    =========================================================================
    Para agregar un nuevo tipo (ej: XML):
    
    1. Crear clase XML(Document) con su metodo generate()
    2. Crear clase XMLFactory(DocumentFactory) con su create_document()
    3. Listo! No tocas NADA del codigo existente
    """

