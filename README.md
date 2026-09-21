# Authorised Redis Security Assessment

A sanitised case study of an authorised penetration test conducted in an isolated university lab. The assessment identified an exposed Redis service that accepted unauthenticated connections and permitted dangerous configuration changes.

The repository focuses on the assessment process, the security impact, and practical remediation. Real credentials, addresses, flags, and institution-specific material have been removed.

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
| Unauthenticated Redis administration | Critical | An unauthorised user could alter data and configuration and potentially write files with the Redis service account's permissions |

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
