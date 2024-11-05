import re


def is_valid_domain(domain: str):
    domain_regex = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)([A-Za-z0-9-]{1,63}\.?)+$")
    return bool(domain_regex.match(domain)) and len(domain) <= 253


def is_subdomain(subdomain: str, domain: str):
    if not (is_valid_domain(subdomain) and is_valid_domain(domain)):
        return False

    return subdomain.endswith("." + domain) or subdomain == domain


# a.b.c.d.e -> a.b.c
def split_host(domain: str):
    if not is_valid_domain(domain):
        return None

    parts = domain.split(".")
    if len(parts) < 3:
        return None
    return ".".join(parts[:-2])


# a.b.c.d.e -> d.e
def split_zone(domain: str):
    if not is_valid_domain(domain):
        return None

    parts = domain.split(".")
    if len(parts) < 2:
        return None

    return ".".join(parts[-2:])
