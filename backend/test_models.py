
from app.db import Base, engine
from app import models


def main():
    Base.metadata.create_all(bind=engine)

    print("¡Tablas creadas correctamente!")

    print("Tablas disponibles:")
    for table in Base.metadata.sorted_tables:
        print(f"- {table.name}")


if __name__ == "__main__":
    main()
