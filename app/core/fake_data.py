from faker import Faker

from core.utils import get_logger

logger = get_logger()
fake = Faker()


def generate_users(n=5, start=100000, end=999999):
    users = []
    for _ in range(n):
        users.append({"telegram_id": fake.random_int(start, end, 1),
                      "name":        fake.first_name(),
                      "username":    fake.user_name(), })
    return users


if __name__ == '__main__':
    generate_users()
