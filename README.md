# Patrones de Diseño en Python

Implementacion de los 23 patrones de diseño GoF (Gang of Four) con ejemplos practicos en Python.

## Que son los Patrones de Diseño

Los patrones de diseño son soluciones reutilizables a problemas comunes en el desarrollo de software. No son codigo que puedas copiar directamente, sino plantillas o guias que describen como resolver un problema de forma eficiente y mantenible.

Fueron popularizados por el libro "Design Patterns: Elements of Reusable Object-Oriented Software" (1994) escrito por cuatro autores conocidos como Gang of Four (GoF):

- **Erich Gamma** - Cientifico de computacion suizo, co-creador de JUnit y lider del diseño de Eclipse
- **Richard Helm** - Miembro del Object Technology Practice Group en IBM Consulting Group, Sydney
- **Ralph Johnson** - Profesor del Departamento de Ciencias de la Computacion de la Universidad de Illinois
- **John Vlissides** - Investigador de IBM, se autodenominaba "#4 del Gang of Four" (1961-2005)

Este libro es considerado fundamental en la ingenieria de software orientada a objetos.

## Categorias

Los 23 patrones se dividen en tres categorias segun su proposito:

### Patrones Creacionales

Se enfocan en **como crear objetos**. Abstraen el proceso de instanciacion, haciendo el sistema independiente de como se crean, componen y representan los objetos.

### Patrones Estructurales

Se enfocan en **como organizar objetos**. Describen como componer clases y objetos para formar estructuras mas grandes, manteniendo la flexibilidad y eficiencia.

### Patrones de Comportamiento

Se enfocan en **como se comunican los objetos**. Definen como los objetos interactuan y distribuyen responsabilidades entre si.

## Patrones Implementados

### Creacionales (5)

| # | Patron | Ejemplo | Descripcion |
|---|--------|---------|-------------|
| 1 | Singleton | Conexion a BD | Garantiza una unica instancia de una clase |
| 2 | Factory Method | Documentos PDF/MD/HTML | Delega la creacion de objetos a subclases |
| 3 | Abstract Factory | Muebles Modern/Classic | Crea familias de objetos relacionados |
| 4 | Builder | Personaje de videojuego | Construye objetos complejos paso a paso |
| 5 | Prototype | Clonar enemigos | Crea objetos clonando un prototipo existente |

### Estructurales (7)

| # | Patron | Ejemplo | Descripcion |
|---|--------|---------|-------------|
| 6 | Adapter | Reproductores de audio | Convierte una interfaz en otra compatible |
| 7 | Bridge | Dispositivos y controles | Separa abstraccion de implementacion |
| 8 | Composite | Sistema de archivos | Trata objetos individuales y grupos uniformemente |
| 9 | Decorator | Notificaciones Email/SMS | Agrega funcionalidad dinamicamente |
| 10 | Facade | Arranque de computadora | Proporciona interfaz simple a sistema complejo |
| 11 | Flyweight | Productos tienda online | Comparte datos comunes para ahorrar memoria |
| 12 | Proxy | Acceso BD con permisos | Controla acceso a un objeto |

### Comportamiento (11)

| # | Patron | Ejemplo | Descripcion |
|---|--------|---------|-------------|
| 13 | Chain of Responsibility | Sistema de soporte | Pasa solicitud por cadena de handlers |
| 14 | Command | Editor de texto | Encapsula operaciones como objetos |
| 15 | Interpreter | Conversor de unidades | Interpreta expresiones de un lenguaje |
| 16 | Iterator | Menu de restaurante | Recorre coleccion sin exponer estructura |
| 17 | Mediator | Chat grupal | Centraliza comunicacion entre objetos |
| 18 | Memento | Configuracion de app | Guarda y restaura estado de un objeto |
| 19 | Observer | Sistema de notificaciones | Notifica cambios a multiples objetos |
| 20 | State | Reproductor de musica | Cambia comportamiento segun estado interno |
| 21 | Strategy | Metodos de pago | Define algoritmos intercambiables |
| 22 | Template Method | Exportar documentos | Define esqueleto de algoritmo |
| 23 | Visitor | Analizador de archivos | Separa operaciones de estructura de objetos |

## Estructura del Proyecto

```
patrones-dis/
├── 01_creacionales/
│   ├── 01_singleton/
│   ├── 02_factory_method/
│   ├── 03_abstract_factory/
│   ├── 04_builder/
│   └── 05_prototype/
├── 02_estructurales/
│   ├── 06_adapter/
│   ├── 07_bridge/
│   ├── 08_composite/
│   ├── 09_decorator/
│   ├── 10_facade/
│   ├── 11_flyweight/
│   └── 12_proxy/
└── 03_comportamiento/
    ├── 13_chain_of_responsibility/
    ├── 14_command/
    ├── 15_interpreter/
    ├── 16_iterator/
    ├── 17_mediator/
    ├── 18_memento/
    ├── 19_observer/
    ├── 20_state/
    ├── 21_strategy/
    ├── 22_template_method/
    └── 23_visitor/
```

## Uso

Cada patron esta implementado en un archivo Python independiente que puede ejecutarse directamente:

```bash
python 01_creacionales/01_singleton/singleton.py
python 02_estructurales/10_facade/facade.py
python 03_comportamiento/19_observer/observer.py
```

Cada archivo incluye:
- Explicacion del patron con analogia
- Problema que resuelve
- Solucion que propone
- Implementacion con comentarios
- Demostracion ejecutable
- Resumen de ventajas

## Conceptos OOP Utilizados

Los patrones hacen uso extensivo de conceptos de programacion orientada a objetos:

- **Abstraccion**: Clases abstractas (ABC) e interfaces
- **Herencia**: Subclases que extienden comportamiento
- **Polimorfismo**: Diferentes implementaciones de una misma interfaz
- **Encapsulacion**: Ocultamiento de detalles internos
- **Composicion**: Objetos que contienen otros objetos
- **Delegacion**: Objetos que delegan trabajo a otros

## Referencias

- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
