#!/usr/bin/env python3
"""Build Homebrew index from actual native IPK; never invent artifact hashes."""
import hashlib, io, json, pathlib, subprocess, sys, tarfile
ipk=pathlib.Path(sys.argv[1]).resolve()
repo, tag, dest=sys.argv[2],sys.argv[3],pathlib.Path(sys.argv[4])
assert ipk.is_file() and ipk.stat().st_size>100000, "Invalid IPK"
assert repo.count("/")==1 and "/" not in tag
data=subprocess.check_output(["ar","p",str(ipk),"data.tar.gz"])
with tarfile.open(fileobj=io.BytesIO(data),mode="r:gz") as tar:
    apps=[m for m in tar.getmembers() if m.name.endswith("/appinfo.json")]
    assert len(apps)==1,"Expected one appinfo"
    info=json.load(tar.extractfile(apps[0]))
    assert info["id"]=="space.nuvio.stable" and info["type"]=="native" and info["title"]=="Nuvio Stable"
    bins=[m for m in tar.getmembers() if m.name.endswith("/nuvio-proto")]
    assert len(bins)==1 and bins[0].mode&0o111,"Executable missing"
    assert b"space.nuvio.stable" in tar.extractfile(bins[0]).read(),"Native runtime app ID mismatch"
sha=hashlib.sha256(ipk.read_bytes()).hexdigest()
base=f"https://github.com/{repo}/releases/download/{tag}"
icon="https://raw.githubusercontent.com/iqui27/nuvio-native-legacy/master/deploy/app/icon-large-20.png"
m={"id":info["id"],"version":info["version"],"type":"native","title":"Nuvio Stable",
   "appDescription":"Nuvio Stable native LG webOS preview (player and TV Guide). UI in progress.",
   "iconUri":icon,"sourceUrl":f"https://github.com/{repo}/tree/nuvio-stable",
   "rootRequired":False,"ipkUrl":f"{base}/{ipk.name}",
   "ipkHash":{"sha256":sha},"ipkSize":ipk.stat().st_size}
index={"paging":{"page":1,"count":1,"maxPage":1,"itemsTotal":1,"prevUrl":None,"nextUrl":None},
       "packages":[{"id":m["id"],"title":m["title"],"iconUri":icon,
                    "manifestUrl":f"{base}/webosbrew.manifest.json",
                    "manifest":m,"pool":"main","shortDescription":m["appDescription"]}]}
dest.mkdir(parents=True,exist_ok=True)
(dest/"repo.json").write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(dest/"webosbrew.manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(dest/(ipk.name+".sha256")).write_text(sha+"  "+ipk.name+"\n",encoding="utf-8")
print(f"Created Homebrew metadata: {base}/repo.json")
