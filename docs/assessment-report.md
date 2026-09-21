# Sanitised Penetration Testing Report

## Engagement overview

This assessment was completed in an isolated university environment containing an intentionally vulnerable Linux host. Testing was limited to the supplied lab infrastructure and the objectives defined for the exercise.

All addresses, credentials, keys, flags, and institution-specific details have been removed or replaced with documentation values.

## Executive summary

Service enumeration identified a remotely accessible Redis instance. The service accepted connections without authentication and exposed administrative configuration functionality.

Within the authorised exercise, this access was sufficient to demonstrate that an unauthorised user could modify Redis data and configuration and abuse the service account's file permissions. The weakness created a credible path to operating-system account compromise.

The issue was rated **Critical** because exploitation required no valid Redis credentials and could affect the confidentiality, integrity, and availability of the host.

## Scope

| Item | Detail |
|---|---|
| Environment | Isolated university cyber range |
| Example target | `192.0.2.25` (documentation address) |
| Assessment type | Authorised, black-box lab assessment |
| Primary focus | Network services and access controls |
| Out of scope | Public systems, denial of service, persistence outside the exercise |

## Methodology

### 1. Access challenge

A classical Vigenere cipher was analysed to recover information required to enter the lab. Cipher material and recovered access details are omitted from this public version.

### 2. Host and service discovery

The assigned network range was enumerated to identify the target and its reachable TCP services. Service detection was then used to prioritise exposed administrative services for manual validation.

### 3. Redis validation

The Redis service accepted a remote connection without requesting authentication. Low-impact commands confirmed that the service was responsive and exposed administrative functionality.

### 4. Controlled impact demonstration

The assessment verified that Redis configuration and persistence behaviour could be abused to write attacker-controlled data using the Redis service account's filesystem permissions. The demonstration was restricted to the steps required by the lab objective.

### 5. Cleanup and reporting

Evidence was recorded, the security impact was assessed, and defensive recommendations were prepared. No testing was performed outside the authorised environment.

## Finding PT-01: Unauthenticated Redis administration

| Attribute | Value |
|---|---|
| Risk | Critical |
| Affected service | Redis |
| Category | Missing authentication and unsafe service exposure |
| Status | Confirmed in the lab |

### Description

The Redis instance was reachable from an untrusted network segment and did not require authentication. Administrative configuration commands were available to the unauthenticated connection.

Redis is designed for trusted environments and can perform persistence operations using the permissions of its operating-system account. Exposing these capabilities without effective network restrictions, ACLs, and filesystem isolation can allow a remote user to move beyond database access and affect the host.

### Sanitised evidence

- A TCP connection to the Redis service succeeded from the assessment host.
- The service responded to unauthenticated commands.
- Administrative configuration values were readable and changeable.
- Persistence functionality could write data to a location accessible to the Redis service account.
- The controlled lab objective demonstrated the resulting host-level impact.

Exact commands, addresses, usernames, credentials, key material, and flags are intentionally excluded.

### Impact

An attacker with network access to the service could potentially:

- Read, modify, or delete Redis data.
- Change security-sensitive Redis configuration.
- Write files to locations permitted for the Redis service account.
- Establish unauthorised access to a local account when permissions are unsafe.
- Disrupt applications that depend on the Redis instance.

### Root causes

- Redis was exposed beyond a trusted application network.
- Authentication and ACL controls were not enforced.
- Administrative commands were available remotely.
- The service account had access to a security-sensitive filesystem location.
- Network filtering did not prevent access from the assessment segment.

### Recommendations

1. Bind Redis only to required private interfaces and retain protected mode where applicable.
2. Use Redis ACLs to create named users with strong credentials and only the commands each application requires.
3. Restrict the Redis port with host and network firewalls so that only approved application hosts can connect.
4. Run Redis as a dedicated, non-privileged operating-system account.
5. Remove write access from the Redis account to SSH directories, web roots, scheduled-task locations, and other sensitive paths.
6. Restrict or disable dangerous administrative commands where operationally appropriate, while treating this only as defence in depth.
7. Store configuration and persistence files in dedicated directories with restrictive ownership and permissions.
8. Monitor authentication failures, ACL changes, configuration changes, and unexpected persistence operations.
9. Rotate any credentials or keys that may have been exposed and review the host for unauthorised files or accounts.

### Retest guidance

A successful retest should confirm that:

- Connections from unauthorised network segments are blocked.
- Unauthenticated Redis commands are rejected.
- Approved clients use a least-privileged ACL identity.
- Administrative commands are unavailable to application identities.
- The Redis service account cannot write to security-sensitive directories.
- Monitoring records rejected access and administrative changes.

## Limitations

This was a focused educational assessment of a deliberately vulnerable host. It did not include source-code review, social engineering, denial-of-service testing, physical testing, or a complete review of every host and application control.

## Ethical-use statement

The techniques discussed in this report must only be used on systems you own or have explicit permission to test.

## Reference

- [Redis security documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/security/)
