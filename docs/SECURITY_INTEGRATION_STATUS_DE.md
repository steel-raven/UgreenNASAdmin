# Sicherheitsreview: gemeinsamer Stand vom 02.10.2026

Der Branch `codex/security-round5-integration` führt die elf eingereichten
Sicherheits-PRs #16 bis #26 gemeinsam zusammen. Er sichert den geprüften
Integrationsstand im Fork; die Übernahme der einzelnen PRs in das
Upstream-Projekt bleibt beim Maintainer.

Upstream-Basis: `f3ff0ad66b5d42e1787847d5fdd24e44d2551bc2`.
Integrationsstand nach Workflow-Korrektur und vor diesem Dokument:
`cc8dd345e7ccf3ffbe3de678c0b7095022877cf9`.

## Eingereichte Änderungen

Die folgenden veröffentlichten PR-Heads wurden am 02.10.2026 erneut mit
GitHub abgeglichen und sind im Integrationsbranch enthalten:

| PR | Inhalt | Veröffentlichter Commit |
|---|---|---|
| [#16](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/16) | Private Backup-Generationen, Sperre und atomare Cron-Aktivierung | `1e06072239e231f2cf72ee71cab196ff2828c3db` |
| [#17](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/17) | Öffentlicher Offline-Testlauf ohne private App-Metadaten | `bc43d025004927cc33f3fe426044b65556641ba1` |
| [#18](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/18) | Root-Dateien über stdin, feste Verzeichnisse und Ressourcengrenzen | `94d782e388cff2a87fa4a0ce6fa3ab1d75798cd3` |
| [#19](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/19) | Begrenzte Archivextraktion und atomare Einzeldateien | `6b2204e4c44667dcbcef2294896aa628c5e7c57f` |
| [#20](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/20) | Originale und unterstützte Metadaten beim Upload erhalten | `07647bdd86aa1a2e2ad0b7aaa372142db53168bd` |
| [#21](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/21) | Update-Downloads sowie signierte Version und Installer prüfen | `28fee7003ff6779dcfc07fb2ab64cc6e3f55d374` |
| [#22](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/22) | OS-Tresor, private Windows-Rechte und atomische Konfiguration | `35ffced2c5b1bbd9a77c596405058575bff07ee0` |
| [#23](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/23) | Release-Quellen, Build-Inventar und Sicherheitsworkflow | `537d7e914f1ce20706f385558110233e47d13a9f` |
| [#24](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/24) | UGOS-TLS-Erstkontakt vor dem Login bestätigen | `9c6c2db5ebeea9e8805acc420a37eb55bde60571` |
| [#25](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/25) | UGOS- und SMTP-Zugangsdaten nur verschlüsselt übertragen | `b1bb00c3274531109dbba2a26aff40bcd5b82704` |
| [#26](https://github.com/runlevel1977-del/UgreenNASAdmin/pull/26) | SSH-Rückfall vorab aktivieren und administrative Änderungen absichern | `45e4edd13fa84f7d5af54b95e9406312fa813f07` |

## Prüfung und Grenzen

Am 01.10.2026 bestanden **345 Offline-Tests** auf dem Integrationscommit
`577376b29dd3f2261d81a37b5bb0839b1609be8f`.
Zusätzlich wurden 146 versionierte Python-Dateien mit AST geparst.
Die Windows-DACL-Prüfung verwendete eine künstliche Datei; Linux-Eigentümer,
ACLs und Verzeichnisdeskriptoren wurden auf Windows simuliert.
Das belegt keine vollständige UGOS-Abnahme.

Der erste GitHub-Workflow wurde vor sämtlichen Jobs wegen ungültiger
YAML-Syntax abgelehnt:
[Lauf vom 01.10.2026](https://github.com/steel-raven/UgreenNASAdmin/actions/runs/36916678129).
Am 02.10.2026 wurde die Installationszeile als YAML-Block abgegrenzt.
Ein vorhandener YAML-Parser reproduzierte den ursprünglichen Fehler und
akzeptierte die Korrektur; Befehlsinhalt, Trigger und Windows/Linux-Matrix
wurden überprüft. Diese Nachprüfung änderte keinen Anwendungscode.
Ein vollständig erfolgreicher GitHub-Test- und Abhängigkeitsaudit steht aus.

Eine autorisierte, rein lesende UGOS-Verfügbarkeitsprüfung bestätigte die
benötigten systemd-Werkzeuge; die bisherige Alternative `at` war nicht
verfügbar. Es wurden dabei keine Root-Dateien geschrieben, Timer angelegt,
Dienste neu geladen oder echte Backup-/Restore-Vorgänge ausgeführt.

Weitere Grenzen bleiben ausdrücklich bestehen:

- Vollständiger Archivrollback und Systemrestore mit sämtlichen Metadaten
  benötigen ein eigenes Wiederherstellungskonzept. Die implementierten
  atomaren Einzeldateien ersetzen dieses nicht.
- Stromausfall, Neustart oder nicht kooperierende externe Konfigurationsänderungen
  können manuelle Wiederherstellung erfordern. Transiente SSH-Rückfalltimer
  überleben keinen Neustart.
- Alte Secret-Kopien und reale Zugangsdaten wurden nicht bereinigt oder rotiert.
- Reale Release-Lockdateien, zwei unabhängige Vergleichsbuilds, Zuordnung
  eingebetteter nativer Bibliotheken, Authenticode sowie Rotation und Widerruf
  des Release-Schlüssels benötigen die Mitwirkung des Release-Verantwortlichen.

## Hinweise zum Zusammenführen

Geprüfte Reihenfolge: **#17, #18, #16, #19, #20, #21, #22, #23, #24, #25, #26**.
#18 stellt den von #16 und #26 verwendeten Root-Transaktionseinstieg bereit;
#17 liefert den von #23 verwendeten Offline-Test-Runner.

Bei den Konfliktauflösungen wurden beide benötigten Änderungen erhalten:

1. `ugreen_app/mixin_transfer.py`: Imports aus `archive_commands` und `upload_stream`.
2. `packaging/UgreenNASAdmin.spec`: Ressourcen `ugreen_safe_extract.py` und `ssh_profile_guard.py`.

Vor einem produktiven Release muss der tatsächlich übernommene gemeinsame
Upstream-Stand einschließlich CI und erforderlicher UGOS-Abnahme geprüft werden.
Lokale Rohbelege, Geräteinformationen und temporäre Arbeitskopien sind nicht
Bestandteil dieser Veröffentlichung.
