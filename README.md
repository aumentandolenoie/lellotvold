# Nuvio Stable — preview nativa LG webOS

Questo ramo GitHub è **isolato**: il ramo `main` non viene modificato e non viene utilizzato alcun repository "Nuvio Legacy Custom".

## Obiettivo
Nuvio Stable mira a conservare l'esperienza di NuvioTVSmart (aspetto, settings, cloud, profili, progressi) con il motore nativo C/SDL2/OpenGL ES di Nuvio Native Legacy (player, audio, sottotitoli, guida TV).

## Stato della beta (importante)
Questa è una **preview tecnica del runtime nativo**, non la realizzazione completa della nuova UI:
- Identità indipendente `space.nuvio.stable`, installabile accanto a Nuvio ufficiale e Legacy.
- Motore grafico C e player di Legacy, inclusi sottotitoli e audio; guida EPG di Legacy.
- Collegamento cloud e profili basato sull'implementazione Legacy, con una salvaguardia per non interpretare automaticamente come film alcuni progressi di serie.
- La **replica estetica, delle schermate di impostazioni e delle sincronizzazioni della versione ufficiale non è stata ancora implementata**. Non è corretto indicare la beta come prodotto completo.
- Il motore torrent locale non è incluso nella prima build; riproduzione con fonti legittime HTTP/debrid. Compatibilità del player su LG C2 da verificare in condizioni reali.
- Non installa nulla sulla TV durante la compilazione.

## Sorgenti verificabili
- Runtime originale: https://github.com/iqui27/nuvio-native-legacy (commit `e3e21a590120ca283bcf7a96df1813ff5041eb66`).
- UI di riferimento (ancora da ricostruire nativamente): https://github.com/NuvioMedia/NuvioTVSmart.
- Packaging ufficiale: https://github.com/NuvioMedia/NuvioTVWebOS.

Il workflow scarica **soltanto l'originale pubblico** Legacy, applica `scripts/patch_native.py`, compila un IPK verificato e genera il manifest Homebrew dai byte effettivi del pacchetto. I file della build non contengono credenziali personali; la chiave anon/pubblica per il cloud è letta dalle configurazioni pubbliche del progetto Nuvio.

## Homebrew Channel
Dopo il successo della GitHub Action e la pubblicazione della release, aggiungere come repository:

https://github.com/aumentandolenoie/lellotvold/releases/download/nuvio-stable-beta/repo.json

**Non usare questo URL finché il file non esiste e la release non contiene un .ipk verificato**, un `repo.json` e un `webosbrew.manifest.json`. La presenza del workflow non prova che la compilazione sia riuscita.

Licenza sorgenti originali GNU GPL-3.0; attribuzione a NuvioMedia, iqui27 e relativi contributori. Progetto non ufficiale.
