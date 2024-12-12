from faker import Faker

from core.utils import configure_logging

logger = configure_logging()
fake = Faker()


def generate_users(n=5, start=100000, end=999999) -> list[dict]:
    users = []
    for _ in range(n):
        users.append(
            {
                "telegram_id": fake.random_int(start, end, 1),
                "name":        fake.first_name(),
                "username":    fake.user_name(),
            }
        )
    logger.info(f"Generated {n} users")
    return users


if __name__ == "__main__":
    generate_users()
