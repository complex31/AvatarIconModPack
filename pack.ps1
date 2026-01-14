python .\generate_ini.py
Remove-Item ".\AvatarIconModPack.zip"
$compress = @{
  Path = ".\mod.ini", ".\resources"
  DestinationPath = ".\AvatarIconModPack.zip"
}
Compress-Archive @compress
