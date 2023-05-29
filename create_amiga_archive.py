import subprocess,zipfile,os

# JOTD path for cranker, adapt to wh :)
os.environ["PATH"] += os.pathsep+r"K:\progs\cli"

cmd_prefix = ["make","-f","../makefile.am"]

subprocess.check_call(cmd_prefix+["clean"],cwd="src")

subprocess.check_call(cmd_prefix+["RELEASE_BUILD=1"],cwd="src")
# create archive
with zipfile.ZipFile("Galaxian500_HD.zip","w",compression=zipfile.ZIP_DEFLATED) as zf:
    for file in ["readme.md","instructions.txt","galaxian","galaxian.slave"]: #,"Xevious.info"]:
        zf.write(file)

subprocess.check_output(["cranker_windows.exe","-f","galaxian","-o","galaxian.rnc"])