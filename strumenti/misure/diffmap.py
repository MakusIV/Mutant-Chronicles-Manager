import subprocess, re, sys

files = subprocess.run(["git","diff","--name-only","source/data_base_cards/"],capture_output=True,text=True).stdout.split()
for f in files:
    diff = subprocess.run(["git","diff","-U0",f],capture_output=True,text=True).stdout
    new = open(f,encoding="utf-8").read().split("\n")
    old = subprocess.run(["git","show","HEAD:"+f],capture_output=True,text=True).stdout.split("\n")
    def key_at(lines, idx):
        for i in range(min(idx,len(lines)-1), -1, -1):
            m = re.match(r'^    "(.+)": \{', lines[i])
            if m: return m.group(1)
        return "?"
    print("="*70); print(f)
    cur=None
    for line in diff.split("\n"):
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
        if m:
            oline=int(m.group(1)); nline=int(m.group(3))
            k = key_at(new, nline-1) if m.group(4)!="0" else key_at(old, oline-1)
            if k!=cur:
                print(f"\n--- CARTA: {k}")
                cur=k
            continue
        if line.startswith("+++") or line.startswith("---") or line.startswith("diff") or line.startswith("index"): continue
        if line.startswith("+") or line.startswith("-"):
            print(line.rstrip())
