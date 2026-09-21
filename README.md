<div align="center">

# Authorised Redis Security Assessment

**A sanitised case study of an authorised Redis penetration test conducted in an isolated university lab.**

![Redis](https://img.shields.io/badge/Redis-Security_Assessment-DC382D?logo=redis&logoColor=white)
![Python](https://img.shields.io/badge/Python-Standard_Library-3776AB?logo=python&logoColor=white)
![Testing](https://img.shields.io/badge/Testing-Authorised_Only-2E8B57)

[Assessment report](docs/assessment-report.md) | [Python utility](src/vigenere_analysis.py) | [Tests](tests/test_vigenere_analysis.py)

</div>

## Overview

The assessment identified an exposed Redis service that accepted unauthenticated connections and permitted dangerous configuration changes.

This repository focuses on the assessment process, security impact and practical remediation. Real credentials, addresses, flags and institution-specific material have been removed.

> All testing was conducted within an isolated and authorised university environment.

## Project highlights

- Defined and respected a controlled testing scope
- Performed network and service enumeration
- Validated an exposed Redis service without authentication
- Demonstrated the security impact within the authorised lab
- Documented evidence, risk, remediation, and retesting guidance
- Used classical cipher analysis during the access challenge

## Main finding

| Finding | Risk | Impact |
|---|---|---|
| Unauthenticated Redis administration | **Critical** | An unauthorised user could alter data and configuration and potentially write files with the Redis service account's permissions |

The complete sanitised finding is available in [docs/assessment-report.md](docs/assessment-report.md).

## Cipher analysis utility

The lab began with a classical Vigenere cipher challenge. The included Python utility ranks likely key lengths using the average Index of Coincidence across each candidate period. It is an educational aid, not a guaranteed automatic solver.

Run it with a ciphertext file:

```bash
python src/vigenere_analysis.py path/to/ciphertext.txt --max-key-length 30 --top 5
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

The utility uses only the Python standard library.

## Key remediation

- Restrict Redis to trusted interfaces and networks.
- Enforce Redis ACLs and strong authentication.
- Block direct internet access with host and network firewalls.
- Run Redis as a dedicated, least-privileged service account.
- Prevent the service account from writing to SSH and other sensitive directories.
- Monitor Redis configuration changes, authentication failures, and unexpected persistence activity.
- Rotate any credentials or keys exposed during an incident.

## Ethics and limitations

All activity described here was performed against an intentionally vulnerable system in an authorised lab. Identifiers and operational details have been sanitised. The project demonstrates a focused assessment of one configuration weakness and is not a complete security review of Redis or the host.

This repository is for defensive education and authorised security testing only.

## Reference

- [Redis security documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/security/)
