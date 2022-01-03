# flaav

Flask- Applikation im Docker-Container um kalender-Informationen aus CalDav via API zur Verfügung zu stellen.
Ich hab das nur für den iCloud-Kalender getestet. Theoretisch sollten auch andere CalDav-Server funktionieren.

## build 

```bash
docker build -t dudanski/flaav:latest .
```

Der Build datuert auf meinem Raspberry relativ ewig. Wäre ein guter Plan das Image bei Bedarf in ein Repo zu laden.


## run

## Vorbereitung 

Anwendungspezifisches Passwort erstellen:
https://support.apple.com/de-de/HT204397


### Mit .env -File

```
caldav_url=<<your CalDav Server URL Bsp: https://caldav.icloud.com:443>>
caldav_username=<<your User Name/AppleID>>
caldav_passwd=<<your app specific password>>
look_ahead_days=<<30>>
```

```bash
docker run --env-file .env \
           --name flaav \
           --detach \
           --publish 5000:5000 \ 
          dudanski/flaav:latest
```

### Oder environment -Parameter

```bash
docker run --env-file .env \
           --name flaav \
           --detach \
           --publish 5000:5000 \
           --env caldav_url=<<your CalDav Server URL Bsp: https://caldav.icloud.com:443>>
           --env caldav_username=<<your User Name/AppleID>>
           --env caldav_passwd=<<your application Password>>
           --env look_ahead_days=<<30>>
          dudanski/flaav:latest
```

## Konfiguration

* caldav_url
Url zum CalDav-Server (incl. Port) in meinem Fall https://caldav.icloud.com:443

* caldav_username
User-Name zur Authentifizierung am CalDav-Server in meinem Fall die Apple Id

* caldav_passwd
Passwort zum user-name für iCloud ein Anwenungdspezifisches Passwort

* look_ahead_days
Die API fragt bei jedem Call den Kalender ab. Aus Perormance-Sicht kann es sinnvol sein hier nur den notwendigen Zeitraum zu wählen.

# API Dokumentation

### Verfügbare Kalender

als Root zeit die API alle verfügbaren Kalender an

´´´bash
$ curl http://loxberry:5000/flaav/api/v0.1

> Reminders ⚠️
> Müllabfuhr ROW
> Kalender
> Packen ⚠️
> Family
> Einkauf
> Wochenmarkt
> Baumarkt
´´´

### Events

Die ist auch der nächste zu wählende Knotenpunkt. Der Knoten nach Auswahl des Kalenders zeigt alle verfügbaren Events im CalDav-Format. Das ist relativ unübersichtlich. Hilft aber beim Debuggen.

Theoretisch könnten verschiedene Objekte in einem Kalender stecken (Events, Tasks ... ). Bisher gibts nur Events:

´´´bash
$ curl http://loxberry:5000/flaav/api/v0.1/<calenda name>/events
´´´

*Beipsiel:*

´´´bash
$ curl http://loxberry:5000/flaav/api/v0.1/Family/events

> BEGIN:VCALENDAR
> END:VCALENDAR
> BEGIN:VCALENDAR
> X-EXPANDED:True
> X-MASTER-DTSTART:20160731T180000
> X-MASTER-RRULE:FREQ=MONTHLY\;BYDAY=SU\;BYSETPOS=5
> BEGIN:VEVENT
> DTSTAMP:20220103T123212Z
> UID:0E25C87B-9961-4937-BC63-18492BD9EBCD
> LOCATION:Hainholzweg 52\, 21077 Hamburg
> SEQUENCE:0
> SUMMARY:Punkt 18 Gottesdienst
> LAST-MODIFIED:20160626T200825Z
> CREATED:20160626T200824Z
> TRANSP:OPAQUE
> X-APPLE-TRAVEL-ADVISORY-BEHAVIOR;ACKNOWLEDGED=20211031T163948Z:AUTOMATIC
> DTSTART;TZID=Europe/Berlin:20220130T180000
> DTEND;TZID=Europe/Berlin:20220130T190000
> RECURRENCE-ID:20220130T170000Z
> BEGIN:VALARM
> X-WR-ALARMUID:12DD00B8-470E-4EFF-8751-DF86DD5BD97D
> UID:12DD00B8-470E-4EFF-8751-DF86DD5BD97D
> TRIGGER:-PT15M
> ATTACH;VALUE=URI:Chord
> ACTION:AUDIO
> X-APPLE-DEFAULT-ALARM:TRUE
> ACKNOWLEDGED:20211031T155409Z
> END:VALARM
> BEGIN:VALARM
> X-WR-ALARMUID:89E25769-A9F4-47F3-9123-F304422BFD7B
> UID:89E25769-A9F4-47F3-9123-F304422BFD7B
> DESCRIPTION:Erinnerung
> ACKNOWLEDGED:20211031T155409Z
> TRIGGER:-PT30M
> ACTION:DISPLAY
> END:VALARM
> END:VEVENT
> END:VCALENDAR
> ...
...
´´´

### Verfügbare Events mit Namen

Der Nächste Knoten, nach dem Events gewählt werden können ist der Name. Dieser kann mittels Regex ermittelt werden.
Notwendig ist zu wählen ob jedes event, oder nur das nächste anstehende Event mit dem Namen zurückgegeben werden soll (any/next)

#### any: 
´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/<calenda name>/events/any/<event name>"
´´´


*Beispiel 1:*
´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/Family/events/any/Kita%20frei"

> BEGIN:VCALENDAR
> VERSION:2.0
> PRODID:-//PYVOBJECT//NONSGML Version 1//EN
> BEGIN:VEVENT
> UID:58FD33C8-358C-4FEE-8BC2-CDD82960DE32
> DTSTART;VALUE=DATE:20211222
> DTEND;VALUE=DATE:20220103
> CREATED:20210928T072630Z
> DTSTAMP:20210928T072631Z
> LAST-MODIFIED:20210928T072630Z
> SEQUENCE:0
> SUMMARY:Kita frei 
> URL;VALUE=URI:
> END:VEVENT
> END:VCALENDAR
´´´

*Beispiel 2:*
Dieses mal mit Regex
´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/Family/events/any/Kita.*"

> BEGIN:VCALENDAR
> VERSION:2.0
> PRODID:-//PYVOBJECT//NONSGML Version 1//EN
> BEGIN:VEVENT
> UID:58FD33C8-358C-4FEE-8BC2-CDD82960DE32
> DTSTART;VALUE=DATE:20211222
> DTEND;VALUE=DATE:20220103
> CREATED:20210928T072630Z
> DTSTAMP:20210928T072631Z
> LAST-MODIFIED:20210928T072630Z
> SEQUENCE:0
> SUMMARY:Kita frei 
> URL;VALUE=URI:
> END:VEVENT
> END:VCALENDAR
´´´

#### next:

auf dem gleichen Knoten aber mit "next" in er route gibt das Event zurück, dass als nächstes stattfindet

´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/<calenda name>/events/next/<event name>"
´´´

Beispiele wie bei "any"

#### today:

nur weils geht gibts den gleichen Knoten auch noch mit today. Dieser zeigt nur events von heute an.

´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/<calenda name>/events/today/<event name>"
´´´

### is_today

liefert einen einfach eine 1 bzw. eine 0 je nach dem ob das Event heute stattfinden oder nicht. Diese Funktion ist nur auf dem any-Knoten verfügbar

´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/<calenda name>/events/any/<event name>/is_today"
´´´

*Beispiel:*
Angenommen es ist heute Urlaub ;) 

´´´bash
$ curl "http://loxberry:1504/flaav/api/v0.1/Family/events/any/Urlaub/is_today"

> 1
´´´


## known issues

* is_today berücksichtigt auch ganztägige Termine, deren enddatum = Heute 00:00. Das ist leider immer so bei ganztägigen Terminen