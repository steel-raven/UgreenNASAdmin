# Prüfstand: aktualisierte PRs #5/#6 und fünf Folge-PRs

Basis: öffentlicher main `1c3f28b1fee243585c1ba9e6d134caaf457dfcb0`,
Quellstand 23.8.54 vom 01.10.2026. Der zuletzt abrufbare Binärrelease ist v23.8.49.

Dieser Referenzbranch kombiniert die aktualisierten Backup-/Administrations-PRs
#5/#6 mit den eng begrenzten Folgekorrekturen zu den geschlossenen #2, #3, #4,
#7 und #10. Die aktuellen Upstream-Funktionen bleiben erhalten: bestätigtes
SSH-Erstvertrauen, Skript-Whitelist und Cron-Grundprüfung, ausschließliche
Tresorablage von Passwort/Passphrase und nichtrekursives Docker-`chmod 755`.

Die für #8/#9 angekündigte Portierung nach 23.8.56 ist in diesem öffentlich
abrufbaren Basis-Commit noch nicht enthalten. Diese beiden geschlossenen PRs
werden hier nicht erneut eingebracht; die spätere Portierung benötigt einen
erneuten Codeabgleich.

## Bewusste Konfliktauflösung

#5 und der Folge-PR zur Backup-Cron-Validierung bearbeiten
`scheduled_backup_sync_to_nas`. Die kombinierte Funktion validiert zuerst die
vollständige Jobliste, liest die vorhandene Cron-Datei und ermittelt die
Quellen-/Mountidentität. Erst danach darf sie Verzeichnisse oder Dateien
schreiben. Die JSON enthält den erfassten Quellenstand (Schema-Version 2).
Nur bei Erfolg wird auch der UI-Zustand aktualisiert. Der private Root-Writer
aus dem früheren #8 ist in dieser Kombination nicht enthalten.

## Reproduzierbare Offline-Prüfung

Aus dem Repository-Wurzelverzeichnis:

```console
python -B tests/run_offline_suite.py
```

**170 ausgeführte Tests: 169 erfolgreich, ein bereits auf unverändertem main
reproduzierbarer Fehler.** Alle 110 zusätzlichen PR-/Integrationstests bestehen;
kein Test wird übersprungen. Upstream allein ergibt 60 Tests mit 59 Erfolgen.
`test_enrich_fills_missing_name` in `tests/test_runlevel_apps_scan.py` erwartet
lokale App-Metadaten, die im öffentlichen Checkout fehlen. Der Test bleibt
unverändert aktiv; der gesamte Lauf endet deshalb weiterhin mit Exitcode 1.

Der Runner ergänzt zu unittest die zehn parameterlosen `test_fan_curve`-Funktionen.
Geprüft auf Windows mit Python 3.12.14 und vorhandenen cryptography/OpenSSL-/Bash-/
tar-Komponenten. Keine Paketinstallation. Tests verwenden künstliche Dateien,
Geheimnisse und Zertifikate; SSH, sudo, OS-Tresor und UI-Dialoge sind simuliert.
TLS-Handshakes laufen über MemoryBIO ohne Netzwerk-Sockets.

Anwendungs-/Testsyntax und `git diff --check` sind ohne Befund. Das unveränderte
Upstream-Wartungswerkzeug `tools/split_ugreen_manager.py` ist UTF-16-kodiert und
nicht direkt mit Python ausführbar; nach expliziter Dekodierung ist sein AST
parsbar. Das Werkzeug wurde nicht gestartet.

## Weitere Prüfung

Reales UGOS, POSIX-Rechte/ACLs, SSH/SFTP, sudo, Credential Manager und EXE-Packaging
bleiben ungeprüft. Root-Restore braucht eigene Grenzen für Archivpfade, Links,
Spezialdateien und Überschreibungen. Runner/JSON/Cron und Tresor/JSON sind keine
gemeinsamen Transaktionen. Bestehende NAS-Jobs müssen nach den Migrationshinweisen
der einzelnen PRs geprüft und erneut synchronisiert werden. Das ist keine
Freigabe für ein produktives NAS.
