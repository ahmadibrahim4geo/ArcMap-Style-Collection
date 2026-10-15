# Harvest true standard symbols (triangles/arrows/hydro/quarry) into Geomorphological.style
$ErrorActionPreference = "Stop"
$esri = "C:\Program Files (x86)\ArcGIS\Desktop10.8\Styles\ESRI.style"
$cadd = "C:\Program Files (x86)\ArcGIS\Desktop10.8\Styles\CADD GIS Center SDS 220.Style"
$target = "C:\Users\ahmad\Desktop\Styles ArcMap\Geomorphological Style\Geomorphological.style"
$CAT20 = "20-قمم وعلامات Peaks-Markers"
$CAT21 = "21-مقالع وأنشطة Quarries-Anthro"

function Get-Blob($dbPath, $id) {
  $cs = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" + $dbPath + ";"
  $c = New-Object System.Data.OleDb.OleDbConnection($cs)
  $c.Open()
  $cmd = $c.CreateCommand()
  $cmd.CommandText = "SELECT Object, Tags FROM [Marker Symbols] WHERE ID=" + $id
  $rd = $cmd.ExecuteReader()
  if (-not $rd.Read()) { throw "ID $id not found in $dbPath" }
  $sz = $rd.GetBytes(0, 0, $null, 0, 0)
  $buf = New-Object byte[] $sz
  [void]$rd.GetBytes(0, 0, $buf, 0, $sz)
  $tags = ""
  try { $tags = $rd.GetString(1) } catch {}
  $rd.Close(); $c.Close()
  return @{ Bytes = $buf; Tags = $tags; Len = $sz }
}

$jobs = @(
  @{ Src = $esri; ID = 3;   Name = "قمة رئيسية | Main Peak (triangle)"; Cat = $CAT20; Tags = "peak;main;triangle;ESRI" },
  @{ Src = $esri; ID = 93;  Name = "قمة ثانوية | Secondary Peak"; Cat = $CAT20; Tags = "peak;secondary;triangle;ESRI" },
  @{ Src = $esri; ID = 94;  Name = "قمة بركانية | Volcanic Peak"; Cat = $CAT20; Tags = "volcano;peak;triangle;ESRI" },
  @{ Src = $cadd; ID = 58;  Name = "اتجاه الرياح السائدة | Wind Direction"; Cat = $CAT20; Tags = "wind;direction;CADD" },
  @{ Src = $cadd; ID = 397; Name = "اتجاه هجرة الكثبان | Dune Migration"; Cat = $CAT20; Tags = "dune;migration;slope;CADD" },
  @{ Src = $cadd; ID = 328; Name = "عين / ينبوع | Spring (CADD)"; Cat = $CAT20; Tags = "spring;CADD" },
  @{ Src = $cadd; ID = 333; Name = "شلال | Waterfall"; Cat = $CAT20; Tags = "waterfall;CADD" },
  @{ Src = $cadd; ID = 332; Name = "مسار سريع | Rapids"; Cat = $CAT20; Tags = "rapids;CADD" },
  @{ Src = $cadd; ID = 391; Name = "مقلع | Quarry"; Cat = $CAT21; Tags = "quarry;CADD" },
  @{ Src = $cadd; ID = 381; Name = "حفرة اقتراض | Borrow Pit"; Cat = $CAT21; Tags = "borrowpit;CADD" },
  @{ Src = $cadd; ID = 396; Name = "موقع عينة رسوبية | Sediment Sample"; Cat = $CAT20; Tags = "sample;sediment;CADD" },
  @{ Src = $cadd; ID = 399; Name = "نقطة منسوب | Spot Elevation"; Cat = $CAT20; Tags = "elevation;spot;CADD" }
)

$csT = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" + $target + ";"
$cT = New-Object System.Data.OleDb.OleDbConnection($csT)
$cT.Open()
$cmdMax = $cT.CreateCommand()
$cmdMax.CommandText = "SELECT MAX(ID) FROM [Marker Symbols]"
$nextID = [int]$cmdMax.ExecuteScalar() + 1
Write-Host ("starting ID=" + $nextID)
foreach ($j in $jobs) {
  $b = Get-Blob $j.Src $j.ID
  $ins = $cT.CreateCommand()
  $ins.CommandText = "INSERT INTO [Marker Symbols] ([ID], [Name], [Category], [Object], [Tags]) VALUES (?,?,?,?,?)"
  $p1 = $ins.CreateParameter(); $p1.OleDbType = [System.Data.OleDb.OleDbType]::Integer; $p1.Value = $nextID; [void]$ins.Parameters.Add($p1)
  $p2 = $ins.CreateParameter(); $p2.OleDbType = [System.Data.OleDb.OleDbType]::VarWChar; $p2.Size = 255; $p2.Value = $j.Name; [void]$ins.Parameters.Add($p2)
  $p3 = $ins.CreateParameter(); $p3.OleDbType = [System.Data.OleDb.OleDbType]::VarWChar; $p3.Size = 255; $p3.Value = $j.Cat; [void]$ins.Parameters.Add($p3)
  $p4 = $ins.CreateParameter(); $p4.OleDbType = [System.Data.OleDb.OleDbType]::LongVarBinary; $p4.Value = $b.Bytes; [void]$ins.Parameters.Add($p4)
  $p5 = $ins.CreateParameter(); $p5.OleDbType = [System.Data.OleDb.OleDbType]::VarWChar; $p5.Size = 255; $p5.Value = $j.Tags; [void]$ins.Parameters.Add($p5)
  [void]$ins.ExecuteNonQuery()
  Write-Host ("  inserted " + $nextID + " <- srcID " + $j.ID + " blobBytes=" + $b.Len)
  $nextID++
}
$chk = $cT.CreateCommand()
$chk.CommandText = "SELECT COUNT(*) FROM [Marker Symbols]"
Write-Host ("Marker Symbols now=" + $chk.ExecuteScalar())
$cT.Close()
Write-Host "HARVEST DONE"
