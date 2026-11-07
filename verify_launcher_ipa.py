import zipfile, plistlib, struct, sys
z = zipfile.ZipFile(sys.argv[1])
names = z.namelist()
apps = sorted(set(n.split(chr(47))[1] for n in names if n.startswith(chr(80)+chr(97)+chr(121)+chr(108)+chr(111)+chr(97)+chr(100)+chr(47)) and len(n.split(chr(47))) > 2))
print("APPS", apps)
for n in names:
    print(n, z.getinfo(n).file_size)
plists = [n for n in names if n.count(chr(47)) == 2 and n.endswith("Info.plist")]
print("PLISTS", plists)
for pn in plists:
    d = plistlib.loads(z.read(pn))
    for k in ["CFBundleIdentifier", "CFBundleExecutable", "CFBundleDisplayName", "CFBundleName", "CFBundleShortVersionString", "UIFileSharingEnabled", "LSSupportsOpeningDocumentsInPlace"]:
        print(k, d.get(k))
    exe = "Payload/" + apps[0] + "/" + str(d.get("CFBundleExecutable", ""))
    print("EXE_IN_ZIP", exe in names)
    if exe in names:
        data = z.read(exe)
        print("EXE_SIZE", len(data))
        print("MACHO_MAGIC", data[:4].hex())
        print("CPU_TYPE", hex(struct.unpack("<I", data[4:8])[0]))
