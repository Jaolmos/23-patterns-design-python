"""
PATRON TEMPLATE METHOD - Exportar Documentos

Analogia: Como una receta de cocina. La receta define los pasos generales
(preparar ingredientes, cocinar, servir) pero cada platillo implementa los
detalles especificos. Todos siguen la misma estructura, pero cada uno hace
las cosas a su manera en cada paso.

PROBLEMA: Tienes varios algoritmos que siguen los mismos pasos pero con
implementaciones diferentes en algunos pasos. Duplicar el flujo completo en
cada clase genera codigo repetido y dificil de mantener.

SOLUCION: Definir el esqueleto del algoritmo en un metodo template de la clase
base. Los pasos comunes se implementan en la base, y los pasos variables son
metodos abstractos que las subclases implementan.

VENTAJA: Reutiliza codigo comun. Define estructura clara del algoritmo.
Las subclases solo sobreescriben pasos especificos. Facil agregar nuevas
variantes.

Conceptos OOP usados:
- Abstraccion: Clase abstracta con template method
- Herencia: Subclases extienden la clase base
- Polimorfismo: Diferentes implementaciones de pasos
- Template Method: Metodo que define el algoritmo
"""

from abc import ABC, abstractmethod


# =============================================================================
# CLASE ABSTRACTA: Define el template method
# =============================================================================

class DocumentExporter(ABC):
    """
    Clase abstracta: Define el template method que exporta documentos.
    El flujo es el mismo para todos, pero los pasos varian.
    """

    def export(self, title: str, content: str) -> str:
        """
        Template Method: Define el algoritmo de exportacion.
        Los pasos se ejecutan en orden fijo. Algunos son comunes,
        otros son especificos de cada formato.
        """
        print(f"\n[{self.__class__.__name__}] Iniciando exportacion...")
        print("-" * 60)

        # Template Method: define el esqueleto del algoritmo
        # Paso 1: Preparar documento (metodo concreto, puede sobreescribirse)
        self._prepare_document()

        # Paso 2: Agregar encabezado (metodo abstracto, cada subclase lo implementa)
        result = self._add_header(title)

        # Paso 3: Agregar contenido (metodo abstracto)
        result += self._add_content(content)

        # Paso 4: Agregar pie de pagina (metodo abstracto)
        result += self._add_footer()

        # Paso 5: Finalizar documento (metodo concreto)
        self._finalize_document()

        return result

    def _prepare_document(self) -> None:
        """
        Paso comun: Preparacion inicial.
        Implementacion por defecto, puede sobreescribirse.
        """
        print("[1/5] Preparando documento...")

    @abstractmethod
    def _add_header(self, title: str) -> str:
        """Paso especifico: Agregar encabezado segun formato."""
        pass

    @abstractmethod
    def _add_content(self, content: str) -> str:
        """Paso especifico: Agregar contenido segun formato."""
        pass

    @abstractmethod
    def _add_footer(self) -> str:
        """Paso especifico: Agregar pie de pagina segun formato."""
        pass

    def _finalize_document(self) -> None:
        """
        Paso comun: Finalizacion.
        Implementacion por defecto, puede sobreescribirse.
        """
        print("[5/5] Documento finalizado")


# =============================================================================
# SUBCLASES CONCRETAS: Implementan los pasos especificos
# =============================================================================

class PDFExporter(DocumentExporter):
    """
    Exportador concreto: Genera documentos en formato PDF.
    """

    def _add_header(self, title: str) -> str:
        """Encabezado en formato PDF."""
        print("[2/5] Agregando encabezado PDF...")
        return f"%PDF-1.4\\n<< /Title ({title}) >>\\n"

    def _add_content(self, content: str) -> str:
        """Contenido en formato PDF."""
        print("[3/5] Agregando contenido PDF...")
        return f"<< /Content ({content}) >>\\n"

    def _add_footer(self) -> str:
        """Pie de pagina en formato PDF."""
        print("[4/5] Agregando pie de pagina PDF...")
        return "%%EOF\\n"


class HTMLExporter(DocumentExporter):
    """
    Exportador concreto: Genera documentos en formato HTML.
    """

    def _add_header(self, title: str) -> str:
        """Encabezado en formato HTML."""
        print("[2/5] Agregando encabezado HTML...")
        return f"<!DOCTYPE html>\\n<html>\\n<head>\\n  <title>{title}</title>\\n</head>\\n<body>\\n"

    def _add_content(self, content: str) -> str:
        """Contenido en formato HTML."""
        print("[3/5] Agregando contenido HTML...")
        return f"  <p>{content}</p>\\n"

    def _add_footer(self) -> str:
        """Pie de pagina en formato HTML."""
        print("[4/5] Agregando pie de pagina HTML...")
        return "</body>\\n</html>\\n"


class MarkdownExporter(DocumentExporter):
    """
    Exportador concreto: Genera documentos en formato Markdown.
    """

    def _add_header(self, title: str) -> str:
        """Encabezado en formato Markdown."""
        print("[2/5] Agregando encabezado Markdown...")
        return f"# {title}\\n\\n"

    def _add_content(self, content: str) -> str:
        """Contenido en formato Markdown."""
        print("[3/5] Agregando contenido Markdown...")
        return f"{content}\\n\\n"

    def _add_footer(self) -> str:
        """Pie de pagina en formato Markdown."""
        print("[4/5] Agregando pie de pagina Markdown...")
        return "---\\nGenerado automaticamente\\n"


class XMLExporter(DocumentExporter):
    """
    Exportador concreto: Genera documentos en formato XML.
    """

    def _prepare_document(self) -> None:
        """Sobreescribe preparacion para XML."""
        print("[1/5] Preparando documento XML (validando schema)...")

    def _add_header(self, title: str) -> str:
        """Encabezado en formato XML."""
        print("[2/5] Agregando encabezado XML...")
        return f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\\n<document>\\n  <title>{title}</title>\\n"

    def _add_content(self, content: str) -> str:
        """Contenido en formato XML."""
        print("[3/5] Agregando contenido XML...")
        return f"  <content>{content}</content>\\n"

    def _add_footer(self) -> str:
        """Pie de pagina en formato XML."""
        print("[4/5] Agregando pie de pagina XML...")
        return "</document>\\n"


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON TEMPLATE METHOD - Exportar Documentos")
    print("=" * 70)

    title = "Reporte Mensual"
    content = "Este es el contenido del reporte con datos importantes."

    # --- Exportar a PDF ---
    print("\n[CASO 1] Exportar documento a PDF")
    print("=" * 70)
    pdf_exporter = PDFExporter()
    pdf_result = pdf_exporter.export(title, content)
    print(f"\n[Resultado PDF]\\n{pdf_result}")

    # --- Exportar a HTML ---
    print("\n[CASO 2] Exportar documento a HTML")
    print("=" * 70)
    html_exporter = HTMLExporter()
    html_result = html_exporter.export(title, content)
    print(f"\n[Resultado HTML]\\n{html_result}")

    # --- Exportar a Markdown ---
    print("\n[CASO 3] Exportar documento a Markdown")
    print("=" * 70)
    md_exporter = MarkdownExporter()
    md_result = md_exporter.export(title, content)
    print(f"\n[Resultado Markdown]\\n{md_result}")

    # --- Exportar a XML ---
    print("\n[CASO 4] Exportar documento a XML")
    print("=" * 70)
    xml_exporter = XMLExporter()
    xml_result = xml_exporter.export(title, content)
    print(f"\n[Resultado XML]\\n{xml_result}")

    # --- Demostrar que todos siguen mismo flujo ---
    print("\n" + "=" * 70)
    print("[DEMO] Todos los exportadores siguen el mismo template:")
    print("=" * 70)
    print("1. Preparar documento")
    print("2. Agregar encabezado (especifico del formato)")
    print("3. Agregar contenido (especifico del formato)")
    print("4. Agregar pie de pagina (especifico del formato)")
    print("5. Finalizar documento")

    """
    =========================================================================
    VENTAJAS DEL PATRON TEMPLATE METHOD
    =========================================================================
    1. REUTILIZACION: El flujo comun esta en un solo lugar

    2. ESTRUCTURA CLARA: El algoritmo esta definido explicitamente

    3. FACIL EXTENSION: Agregas nuevos formatos sin cambiar el template

    4. CONTROL: La clase base controla el flujo, las subclases los detalles

    5. MANTENIMIENTO: Cambios en el flujo se hacen en un solo lugar
    """
