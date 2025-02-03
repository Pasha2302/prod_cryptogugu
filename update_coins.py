import psycopg
from psycopg.rows import dict_row
import os
import django

# 1. Указываем путь к настройкам Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

# 2. Инициализируем Django
django.setup()

from app.models import Airdrops


class PostgresDB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        """Создает подключение к базе данных."""
        if self.conn is None:
            self.conn = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                autocommit=True,
                row_factory=dict_row  # Возвращает результат в виде словаря
            )

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос и возвращает результат."""
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall() if cursor.description else None

    def execute_update(self, query, params=None):
        """Выполняет SQL-запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params or ())

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()
            self.conn = None


def extract_filename(old_path: str) -> str | None:
    """
    Извлекает имя файла из старого пути и формирует новый путь.
    """
    if not old_path:
        return None  # Если путь пустой, просто возвращаем None

    filename = os.path.basename(old_path)  # Достаем имя файла
    return f"airdrop_images/{filename}"  # Новый путь (Django сам добавит MEDIA_ROOT)


def save_data_airdrops(db: PostgresDB):
    """
    Переносит данные из старой базы в новую, корректируя путь к изображениям.
    """
    rows = db.execute_query("SELECT * FROM app_airdrops;")

    new_airdrops = []  # Список объектов для массовой вставки

    for row in rows:
        print(f"Обрабатываем: {row['name']}")

        new_airdrops.append(
            Airdrops(
                name=row["name"],
                status=row["status"],
                end_date=row["end_date"],
                reward=row["reward"],
                path_airdrop_img=extract_filename(row["path_coin_img"]),  # Конвертация пути
                created_at=row["created_at"],
            )
        )

    # Массовое создание записей в Django ORM
    Airdrops.objects.bulk_create(new_airdrops)
    print("✅ Данные успешно перенесены!")


def update_image_address_airdrops(db: PostgresDB):
    pass


def main():
    # 🔹 Использование класса
    db = PostgresDB(
        dbname="coin_cgugu_prod",
        user="pavelpc",
        password="1234",
        host="127.0.0.1",
        port="5432"
    )

    save_data_airdrops(db)

    db.close()


if __name__ == '__main__':
    main()
