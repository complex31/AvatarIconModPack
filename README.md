# Avatar Icon Mod Pack Generator
This set of scripts can be used to generate mod pack for a certain anime game. Refer to [this](https://gamebanana.com/mods/475764) for an example.

**Note**: This repository does not include source images for the above mod.

## Requirements
Python 3

PNG images for the custom icons

## How to use
Generate empty source folder

```
python generate_empty_source.py
```

Organize your PNG images into the empty folders inside the generated `source` folder.
Generate resources folder

```
python generate_resources.py
```

Generate mod INI file

```
python generate_ini.py
```

You can manually edit resource path for each icon in the generated `mod.ini` file for customization.

## Updating the mod with new icons
This repository will be updated with icon hashes as characters get added. Just download latest code (or use `git pull`). Then repeat above steps.

