"""
PATRON COMMAND - Editor de Texto con Deshacer

Analogia: El control remoto de tu TV. Cada boton (comando) encapsula una accion
(subir volumen, cambiar canal). El control remoto no sabe COMO funciona la TV,
solo guarda comandos y los ejecuta. Puedes guardar historial de comandos y
deshacerlos si quieres.

PROBLEMA: Necesitas encapsular operaciones como objetos para poder parametrizarlas,
ponerlas en cola, guardar historial y deshacerlas. Si las operaciones estan
hardcodeadas, no puedes hacer nada de eso.

SOLUCION: Encapsular cada operacion como un objeto Command con metodo execute()
y undo(). El invocador (Invoker) no conoce los detalles de la operacion, solo
ejecuta el comando. Puedes guardar historial de comandos para deshacer/rehacer.

VENTAJA: Desacopla el objeto que invoca la operacion del que sabe como ejecutarla.
Puedes parametrizar objetos con operaciones, ponerlas en cola, guardar historial,
implementar deshacer/rehacer facilmente.

Conceptos OOP usados:
- Abstraccion: Interfaz Command con execute() y undo()
- Encapsulacion: Cada comando encapsula su operacion
- Composicion: El editor contiene historial de comandos
"""

from abc import ABC, abstractmethod
from typing import List


# =============================================================================
# RECEIVER: El objeto que sabe como realizar las operaciones reales
# =============================================================================

class TextDocument:
    """
    Receiver: El documento de texto que contiene el contenido y sabe
    como modificarlo. Los comandos delegan el trabajo real a este objeto.
    """

    def __init__(self):
        self._content = ""

    def insert_text(self, text: str, position: int) -> None:
        """Inserta texto en una posicion especifica."""
        self._content = self._content[:position] + text + self._content[position:]
        print(f"  [TextDocument] Texto insertado: '{text}' en posicion {position}")

    def delete_text(self, position: int, length: int) -> str:
        """Elimina texto desde una posicion y devuelve el texto eliminado."""
        deleted = self._content[position:position + length]
        self._content = self._content[:position] + self._content[position + length:]
        print(f"  [TextDocument] Texto eliminado: '{deleted}' desde posicion {position}")
        return deleted

    def get_content(self) -> str:
        """Obtiene el contenido actual del documento."""
        return self._content

    def __str__(self) -> str:
        return f'"{self._content}"'


# =============================================================================
# COMMAND: Interfaz abstracta para todos los comandos
# =============================================================================

class Command(ABC):
    """
    Interfaz Command: Define la interfaz comun para todos los comandos.
    Cada comando debe implementar execute() y undo().
    """

    @abstractmethod
    def execute(self) -> None:
        """Ejecuta el comando."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Deshace el comando."""
        pass


# =============================================================================
# COMANDOS CONCRETOS
# =============================================================================

class InsertTextCommand(Command):
    """
    Comando concreto: Inserta texto en el documento.
    Guarda la informacion necesaria para poder deshacerse.
    """

    def __init__(self, document: TextDocument, text: str, position: int):
        # Encapsulacion: el comando guarda el receiver y los parametros
        self._document = document
        self._text = text
        self._position = position

    def execute(self) -> None:
        """Ejecuta: inserta el texto."""
        print(f"[InsertTextCommand] Ejecutando...")
        # Delegacion: el comando delega el trabajo real al receiver
        self._document.insert_text(self._text, self._position)

    def undo(self) -> None:
        """Deshace: elimina el texto que se inserto."""
        print(f"[InsertTextCommand] Deshaciendo...")
        self._document.delete_text(self._position, len(self._text))


class DeleteTextCommand(Command):
    """
    Comando concreto: Elimina texto del documento.
    Guarda el texto eliminado para poder restaurarlo al deshacer.
    """

    def __init__(self, document: TextDocument, position: int, length: int):
        # Encapsulacion: guarda receiver y parametros para ejecutar y deshacer
        self._document = document
        self._position = position
        self._length = length
        self._deleted_text = ""  # Se guardara al ejecutar

    def execute(self) -> None:
        """Ejecuta: elimina el texto y lo guarda."""
        print(f"[DeleteTextCommand] Ejecutando...")
        self._deleted_text = self._document.delete_text(self._position, self._length)

    def undo(self) -> None:
        """Deshace: reinserta el texto eliminado."""
        print(f"[DeleteTextCommand] Deshaciendo...")
        self._document.insert_text(self._deleted_text, self._position)


# =============================================================================
# INVOKER: El objeto que ejecuta los comandos
# =============================================================================

class TextEditor:
    """
    Invoker: El editor de texto que ejecuta comandos y mantiene un historial
    para poder deshacer/rehacer operaciones.
    """

    def __init__(self, document: TextDocument):
        self._document = document
        # Composicion: el editor contiene listas de comandos
        self._history: List[Command] = []  # Historial de comandos ejecutados
        self._redo_stack: List[Command] = []  # Pila para rehacer

    def execute_command(self, command: Command) -> None:
        """
        Ejecuta un comando y lo guarda en el historial.
        Limpia la pila de rehacer porque la historia cambio.
        """
        # 1. Ejecutar el comando (polimorfismo: no sabe que comando es)
        command.execute()
        # 2. Guardar en historial para poder deshacer
        self._history.append(command)
        # 3. Limpiar redo porque la historia cambio
        self._redo_stack.clear()  # Al hacer nueva accion, se pierde el redo

    def undo(self) -> None:
        """Deshace el ultimo comando ejecutado."""
        if not self._history:
            print("[TextEditor] No hay comandos para deshacer")
            return

        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)  # Lo guarda para poder rehacer

    def redo(self) -> None:
        """Rehace el ultimo comando deshecho."""
        if not self._redo_stack:
            print("[TextEditor] No hay comandos para rehacer")
            return

        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)

    def show_content(self) -> None:
        """Muestra el contenido actual del documento."""
        print(f"\n[CONTENIDO] {self._document}")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON COMMAND - Editor de Texto con Deshacer")
    print("=" * 70)

    # --- Crear el documento y el editor ---
    print("\n[PASO 1] Creando documento y editor")
    print("-" * 70)
    document = TextDocument()
    editor = TextEditor(document)
    editor.show_content()

    # --- Ejecutar comandos de insercion ---
    print("\n[PASO 2] Insertando texto con comandos")
    print("-" * 70)

    cmd1 = InsertTextCommand(document, "Hola", 0)
    editor.execute_command(cmd1)
    editor.show_content()

    cmd2 = InsertTextCommand(document, " mundo", 4)
    editor.execute_command(cmd2)
    editor.show_content()

    cmd3 = InsertTextCommand(document, "!", 10)
    editor.execute_command(cmd3)
    editor.show_content()

    # --- Ejecutar comando de eliminacion ---
    print("\n[PASO 3] Eliminando texto con comando")
    print("-" * 70)

    cmd4 = DeleteTextCommand(document, 4, 6)  # Eliminar " mundo"
    editor.execute_command(cmd4)
    editor.show_content()

    # --- Deshacer comandos ---
    print("\n[PASO 4] Deshaciendo comandos (Undo)")
    print("-" * 70)

    print("\nDeshacer ultima operacion (delete):")
    editor.undo()
    editor.show_content()

    print("\nDeshacer otra vez (insert '!'):")
    editor.undo()
    editor.show_content()

    print("\nDeshacer otra vez (insert ' mundo'):")
    editor.undo()
    editor.show_content()

    # --- Rehacer comandos ---
    print("\n[PASO 5] Rehaciendo comandos (Redo)")
    print("-" * 70)

    print("\nRehacer (insert ' mundo'):")
    editor.redo()
    editor.show_content()

    print("\nRehacer (insert '!'):")
    editor.redo()
    editor.show_content()

    # --- Hacer nueva accion despues de undo ---
    print("\n[PASO 6] Nueva accion despues de undo (pierde el redo)")
    print("-" * 70)

    print("\nDeshacer una vez:")
    editor.undo()
    editor.show_content()

    print("\nEjecutar nuevo comando (insert ' Python'):")
    cmd5 = InsertTextCommand(document, " Python", 10)
    editor.execute_command(cmd5)
    editor.show_content()

    print("\nIntentar rehacer (no hay nada porque se perdio al hacer nueva accion):")
    editor.redo()

    """
    =========================================================================
    VENTAJAS DEL PATRON COMMAND
    =========================================================================
    1. DESACOPLAMIENTO: Separa el objeto que invoca la operacion del que
       la ejecuta

    2. PARAMETRIZACION: Puedes parametrizar objetos con operaciones

    3. COLA DE OPERACIONES: Puedes encolar comandos y ejecutarlos mas tarde

    4. DESHACER/REHACER: Facil implementar undo/redo guardando historial

    5. MACRO COMANDOS: Puedes crear comandos compuestos de otros comandos

    6. REGISTRO: Puedes registrar comandos para recuperacion de fallos
    """
