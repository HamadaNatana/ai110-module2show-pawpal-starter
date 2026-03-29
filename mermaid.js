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
        +add_task()
        +mark_done()
    }

    class Schedule {
        +List~Task~ tasks
        +generate_schedule()
    }

    Owner "1" --> "many" Pet : owns
    Pet "many" --> "many" Task : assigned to
    Schedule "1" --> "many" Task : contains

    note for Task "importance: low | medium | high"
`;

const container = document.getElementById("diagram");
if (container) {
  const { svg } = await mermaid.render("pawpal-uml", diagram);
  container.innerHTML = svg;
}
