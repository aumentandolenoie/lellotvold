#!/usr/bin/env python3
"""Transform pristine original Legacy C sources into a separately installable Stable preview."""
import json, pathlib, sys
root=pathlib.Path(sys.argv[1]).resolve()
manifest=root/"deploy/app/appinfo.json"
info=json.loads(manifest.read_text())
assert info["type"]=="native" and info["id"]=="space.nuvio.native.legacy"
info.update(id="space.nuvio.stable",title="Nuvio Stable",version="2.0.5",
            vendor="Nuvio Stable Community",appDescription="Nuvio Stable, native LG webOS preview")
manifest.write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n")
header=root/"src/app_id.h"
src=header.read_text()
assert '#define NV_APP_ID_PRODUCTION "space.nuvio.native.legacy"' in src
src=src.replace('"space.nuvio.native.legacy"','"space.nuvio.stable"')
src=src.replace('"com.webos.media.client.nuvio"','"com.webos.media.client.nuvio.stable"')
header.write_text(src)
for f in (root/"src").rglob("*"):
    if f.is_file() and f.suffix in (".c",".h",".inc"):
        raw=f.read_text()
        if "space.nuvio.native.legacy" in raw:
            f.write_text(raw.replace("space.nuvio.native.legacy","space.nuvio.stable"))

# An incoming remote progress row can identify a series by content_type,
# even when it has no explicit season/episode pair.
f=root/"src/syncprog.c"
raw=f.read_text()
old='''    if (d->episodio <= 0) { d->temporada = 0; d->episodio = 0; }
    if (d->temporada < 0) d->temporada = 0;
    snprintf(d->tipo, sizeof d->tipo, "%s", d->episodio > 0 ? "series" : "movie");'''
new='''    /* Stable: recover episode coordinates from the standard synthetic video_id.
       If the server explicitly labels a series, do not turn it into a movie. */
    if (d->episodio <= 0) {
      char videoId[96] = "";
      int season = 0, episode = 0;
      if (js_texto(p, f, "video_id", videoId, sizeof videoId) &&
          sscanf(videoId, PREFIXO_EPISODIO "%d:%d", &season, &episode) == 2 &&
          season >= 0 && episode > 0) {
        d->temporada = season;
        d->episodio = episode;
      }
    }
    if (d->episodio <= 0) { d->temporada = 0; d->episodio = 0; }
    if (d->temporada < 0) d->temporada = 0;
    {
      char contentType[16] = "";
      int explicitSeries = js_texto(p, f, "content_type", contentType, sizeof contentType) &&
                           (!strcmp(contentType, "series") || !strcmp(contentType, "tv"));
      snprintf(d->tipo, sizeof d->tipo, "%s",
               d->episodio > 0 || explicitSeries ? "series" : "movie");
    }'''
assert raw.count(old)==1, "Upstream progress shape changed"
f.write_text(raw.replace(old,new))

# In a Continue Watching entry, known S/E coordinates take precedence
# over stale catalog type metadata.
f=root/"src/continuar.c"
raw=f.read_text()
old='if (idx >= 0 && !strcmp(ci->tipo, "series") && ci->temporada > 0 &&'
assert raw.count(old)==1
f.write_text(raw.replace(old,'if (idx >= 0 && (!strcmp(ci->tipo, "series") || ci->episodio > 0) && ci->temporada > 0 &&'))

# Do not offer Legacy updates for a distinct app identity; Homebrew manages updates.
f=root/"src/atualizacao.c"
raw=f.read_text()
old='#define AT_URL   "https://api.github.com/repos/iqui27/nuvio-native-legacy/releases/latest"'
assert raw.count(old)==1
f.write_text(raw.replace(old, '#define AT_URL   "https://api.github.com/repos/aumentandolenoie/lellotvold/releases/tags/nuvio-stable-beta"'))

# Legacy build requires webOS metadata and Tizen config version parity.
import re
f=root/"tools/tizen-config.xml"
raw=f.read_text()
raw,n=re.subn(r'(version=")[0-9]+\.[0-9]+\.[0-9]+(")',r'\g<1>2.0.5\2',raw,count=1)
assert n==1
f.write_text(raw)

assert "space.nuvio.stable" in header.read_text()
assert "explicitSeries" in (root/"src/syncprog.c").read_text()
assert (root/"src/epg.h").exists()
assert (root/"src/video.c").exists()
print("Nuvio Stable: native identity and series progress safeguards successfully applied.")
