# Cartridge Domain Model

This artifact formally defines the `Cartridge` as a first-class Entity in the Domain Model, highlighting its Object-Oriented relationships.

```mermaid
classDiagram
    class Engine {
        +List~Cartridge~ cartridges
        +run()
        +load_cartridge(Cartridge)
    }

    class Cartridge {
        <<Abstract>>
        +String name
        +String description
        +String version
        +load_config() Dict
        +get_tool(String) Callable
        +init_db()
    }

    class HealthcareCartridge {
        +String domain_specific_attribute
        +validate_hipaa() bool
    }

    class FinanceCartridge {
        +connect_exchange()
    }

    class LegalCartridge {
        +conflict_check() bool
    }

    %% Relationships (HAS-A and IS-A)
    Engine "1" *-- "1..*" Cartridge : HAS-A
    Cartridge <|-- HealthcareCartridge : IS-A
    Cartridge <|-- FinanceCartridge : IS-A
    Cartridge <|-- LegalCartridge : IS-A
```

### Relationship Breakdown:
*   **HAS-A (Composition):** The core `Engine` HAS-A `Cartridge`. It cannot function without one loaded.
*   **IS-A (Inheritance):** A `HealthcareCartridge` IS-A `Cartridge`. It inherits all the base methods (like `load_config`), but extends it with its own domain-specific behaviors (like `validate_hipaa()`).
