from faker import Faker

fake = Faker("ru_RU")


def email_param(domain: str | None = None):
    return fake.email(domain=domain)

