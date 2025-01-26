import sys
import os

iniSeparator = ";"+("-"*20)

def fixName(name):
    parts = name.split("-")
    for i in range(len(parts)):
        parts[i] = parts[i].title()
    return ''.join(parts)

def extractHash(name):
    filename = os.listdir(f"original/{name}")[0]
    return filename.split("-")[0]

def getResourcePath(name):
    files = os.listdir(f"resources/{name}")
    if(len(files)>0):
        return f".\\resources\\{name}\\{files[0]}"
    return ''

def generateIniSection(name):
    sectionName = fixName(name)
    hash = extractHash(name)
    resourcePath = getResourcePath(name)
    if (resourcePath == ''):
        lines = [
            f";[TextureOverride{sectionName}]",
            f";hash = {hash}",
            f";ps-t0 = Resource{sectionName}",
            ";",
            f";[Resource{sectionName}]",
            f";filename = {resourcePath}",
        ]
    else:
        lines = [
            f"[TextureOverride{sectionName}]",
            f"hash = {hash}",
            f"ps-t0 = Resource{sectionName}",
            "",
            f"[Resource{sectionName}]",
            f"filename = {resourcePath}",
        ]
    return lines

def findDuplicateSection(sections, section):
    override = ""
    for line in section:
        if "TextureOverride" in line:
            override = line.strip().replace(";", "")
    for s in sections:
        for line in s:
            if override.strip() in line:
                #print("preserving section "+override)
                trimmed = []
                for l in s:
                    sl = l.strip()
                    if len(sl) > 1:
                        trimmed.append(l.strip())
                trimmed = trimmed[0:3]+[""]+trimmed[3:]
                return trimmed
    print("adding new section "+override)
    return section

def parseFile(file):
    section = []
    sections = []
    for line in file:
        if iniSeparator in line:
            sections.append(section)
            section = []
        else:
            section.append(line)
    print(f"found {len(sections)} sections")
    return sections
    

original_names = os.listdir("original")
args = sys.argv
if (len(args)>1):
    print("selective mode");
    original_names = args[1:]

files = os.listdir(".")
isFirst = True
if "mod.ini" in files:
    print("updating old file")
    iniFile = open("mod.ini", "r")
    oldsections = parseFile(iniFile)
    iniFile.close()
    os.remove("mod.ini")
    iniFile = open("mod.ini", "a")
    for name in original_names:
        section = generateIniSection(name)
        section = findDuplicateSection(oldsections, section)
        if not isFirst:
            iniFile.write('\n')
        for line in section:
            iniFile.write(line+'\n')
        iniFile.write('\n'+iniSeparator+'\n')
        isFirst = False
else:
    print("generating new file")
    iniFile = open("mod.ini", "a")
    for name in original_names:
        section = generateIniSection(name)
        if not isFirst:
            iniFile.write('\n')
        for line in section:
            iniFile.write(line+'\n')
        iniFile.write('\n'+iniSeparator+'\n')
        isFirst = False