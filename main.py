import time
from machine import Pin
import anzeige

PIR_PIN = Pin(25, Pin.IN)
TEXT = "Hallo Gnom <3"   # <- hier ggf. den richtigen Text eintragen
ANZEIGE_DAUER = 5        # Sekunden volle Helligkeit nach letzter Bewegung
FADE_DAUER = 2           # Sekunden zum sanften Ausblenden
FADE_SCHRITTE = 20

anzeige.init()
anzeige.helligkeit(0)

sichtbar = False
letzte_bewegung = 0

while True:
    if PIR_PIN.value():
        letzte_bewegung = time.ticks_ms()
        if not sichtbar:
            anzeige.zeige_text(TEXT)
            anzeige.helligkeit(100)
            sichtbar = True

    elif sichtbar:
        wartezeit = time.ticks_diff(time.ticks_ms(), letzte_bewegung)
        if wartezeit > ANZEIGE_DAUER * 1000:
            for schritt in range(FADE_SCHRITTE, -1, -1):
                if PIR_PIN.value():
                    anzeige.helligkeit(100)
                    letzte_bewegung = time.ticks_ms()
                    break
                anzeige.helligkeit(int(100 * schritt / FADE_SCHRITTE))
                time.sleep_ms(int(FADE_DAUER * 1000 / FADE_SCHRITTE))
            else:
                anzeige.loeschen()
                sichtbar = False

    time.sleep_ms(100)
