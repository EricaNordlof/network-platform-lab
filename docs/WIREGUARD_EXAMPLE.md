# WireGuard site-to-site design example

This file documents the next implementation step without shipping real private keys.

## Malmö

```ini
[Interface]
Address = 10.200.0.1/30
PrivateKey = <MALMO_PRIVATE_KEY>
ListenPort = 51820

[Peer]
PublicKey = <LONDON_PUBLIC_KEY>
AllowedIPs = 10.200.0.2/32, 10.20.1.0/24
Endpoint = london.example.com:51820
PersistentKeepalive = 25
```

## London

```ini
[Interface]
Address = 10.200.0.2/30
PrivateKey = <LONDON_PRIVATE_KEY>
ListenPort = 51820

[Peer]
PublicKey = <MALMO_PUBLIC_KEY>
AllowedIPs = 10.200.0.1/32, 10.10.1.0/24
Endpoint = malmo.example.com:51820
PersistentKeepalive = 25
```

## Production considerations

- Store private keys in a secrets manager.
- Restrict firewall rules to the WireGuard UDP port.
- Rotate keys.
- Monitor handshake age and packet counters.
- Avoid overlapping routes.
- Document failover behavior.
