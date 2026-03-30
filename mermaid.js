import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";

mermaid.initialize({ startOnLoad: true });

const diagram = `
classDiagram
    class Owner {
        +String name
        +List~Pet~ pets_owned
        +List~String~ preferences
        +add_pet(Pet pet)
        +remove_pet(Pet pet)
    }

    class Pet {
        +String name
        +Owner owner
        +String type_breed
    }

    class Task {
        +List~Pet~ pets
        +String task_type
        +String importance
        +DateTime due_date
        +Boolean is_done
        +String recurrence
        +int duration_minutes
        +add_pet(Pet pet)
        +mark_done()
        -_reset_for_next_occurrence()
    }

    class Schedule {
        +Owner owner
        +List~Task~ tasks
        +generate_schedule()
        +sort_by_time()
        +filter_by_priority(String priority)
        +detect_conflicts() List~Conflict~
        +get_conflict_warnings() List~String~
        +has_conflicts() Boolean
    }

    class Conflict {
        +Task task1
        +Task task2
        +Pet pet
        +String message
        +__str__() String
    }

    Owner "1" --> "many" Pet : owns
    Owner "1" --> "1" Schedule : has
    Pet "many" --> "many" Task : assigned to
    Schedule "1" --> "many" Task : contains
    Schedule ..> Conflict : creates
    Conflict --> "2" Task : references
    Conflict --> "1" Pet : involves

    note for Task "importance: low | medium | high\nrecurrence: daily | weekly | monthly | None"
`;

const container = document.getElementById("diagram");
if (container) {
  const { svg } = await mermaid.render("pawpal-uml", diagram);
  container.innerHTML = svg;
}
