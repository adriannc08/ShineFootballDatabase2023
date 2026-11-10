
from sqlalchemy import create_engine, text

from app.config import settings


def main():
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
    )

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT
                        current_database(),
                        current_user,
                        inet_server_port()
                """)
            )

            database, user, port = result.fetchone()

            print("¡Conexión correcta con PostgreSQL!")
            print(f"Base de datos: {database}")
            print(f"Usuario: {user}")
            print(f"Puerto: {port}")

    except Exception as error:
        print("Error de conexión:")
        print(error)

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
