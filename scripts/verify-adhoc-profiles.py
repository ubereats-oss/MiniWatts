#!/usr/bin/env python3
"""Fail early if the app/widget Ad Hoc profiles do not contain the right App Groups."""
import glob
import os
import plistlib
import subprocess
import sys
from datetime import datetime, timezone

targets = {
    "com.ubereatsoss.miniwatts": "app",
    "com.ubereatsoss.miniwatts.Widget": "widget",
}
expected_group = "group.com.ubereatsoss.miniwatts"
paths = glob.glob(os.path.expanduser("~/Library/MobileDevice/Provisioning Profiles/*.mobileprovision"))
paths += glob.glob(os.path.expanduser("~/Library/Developer/Xcode/UserData/Provisioning Profiles/*.mobileprovision"))
if not paths:
    sys.exit("ERROR: nenhum provisioning profile foi disponibilizado pelo Codemagic")

found = {}
for path in paths:
    try:
        result = subprocess.run(
            ["security", "cms", "-D", "-i", path], capture_output=True, check=True
        )
        p = plistlib.loads(result.stdout)
        ent = p.get("Entitlements", {})
        appid = ent.get("application-identifier", ent.get("com.apple.application-identifier", ""))
        bundle = next((item for item in targets if appid.endswith("." + item)), None)
        if bundle is None:
            continue
        groups = ent.get("com.apple.security.application-groups", [])
        devices = p.get("ProvisionedDevices", [])
        expires = p.get("ExpirationDate")
        name = p.get("Name", "(sem nome)")
        valid = (expected_group in groups and bool(devices)
                 and not p.get("ProvisionsAllDevices", False)
                 and (expires is None or expires.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)))
        print(f"{targets[bundle]}: profile={name!r}, bundle={bundle}, app_group={expected_group in groups}, ad_hoc_devices={len(devices)}, valid={valid}")
        if valid:
            found[bundle] = path
    except (subprocess.CalledProcessError, ValueError, OSError) as err:
        print(f"Warning: perfil nao legivel: {path}: {err}", file=sys.stderr)

missing = [v for k, v in targets.items() if k not in found]
if missing:
    sys.exit("ERROR: perfis Ad Hoc com App Groups ausentes/incompativeis para: "
             + ", ".join(missing) + ". Recrie os perfis depois de habilitar App Groups nos dois App IDs e reimporte-os no Codemagic.")
print("PASS: perfis App e Widget com App Groups compativeis encontrados")
