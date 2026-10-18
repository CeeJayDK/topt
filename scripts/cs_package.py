"""Ready-to-run timing package for TOPT_Bench_CS on the sopt Test Host.

    python -m scripts.cs_package --testhost Test-Host-0.7.0.zip --shaders <dir with ReShade.fxh> [--out dist]

The Test Host's sopt-timer add-on times `X_orig` / `X_sopt` technique pairs, each on the same input,
and writes both medians. This package gives every compute variant of TOPT_Bench_CS.fx (unchanged
shaders, `_sopt` added to the technique names) a plain composite as its `_orig`, so orig_us is the
composite floor and diff_us the marginal cost (the model's "us"). TOPT_C_PS_s<N> is the pixel-shader
reference: the same linear taps, horizontal pass to a texture, vertical pass fused with the composite.
One preset per sigma.

Writes <out>/TOPT-CS-Bench.zip: the Test Host (Test-Host.bat, bin\\, Docs\\, ...), TOPT-CS-Bench.bat,
bin\\topt-bench.ps1 (every API x resolution, results in one zip) and topt-cs\\ (presets + shaders).
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

from scripts.make_fx import cs_effect, cs_kernels

ROOT = Path(__file__).resolve().parent.parent
EFFECT = "TOPT_Bench_CS_Pairs.fx"

PS_BLOCK = """// ---- {NAME}: pixel-shader reference, sigma {SIGMA}: the same {NV} linear taps per axis,
// horizontal pass to a texture, vertical pass fused with the composite.
texture {NAME}_tH {{ Width = BUFFER_WIDTH; Height = BUFFER_HEIGHT; Format = TOPT_FORMAT; }};
sampler {NAME}_sH {{ Texture = {NAME}_tH; AddressU = MIRROR; AddressV = MIRROR; }};
sampler {NAME}_sBB {{ Texture = ReShade::BackBufferTex; AddressU = MIRROR; AddressV = MIRROR; }};
static const float2 {NAME}_v[{NV}] = {{ {V} }};

float4 {NAME}_H(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{{
	float3 c = 0.0;
	[unroll] for (int i = 0; i < {NV}; i++)
		c += {NAME}_v[i].y * tex2Dlod({NAME}_sBB, float4(uv.x + {NAME}_v[i].x * BUFFER_RCP_WIDTH, uv.y, 0.0, 0.0)).rgb;
	return float4(c, 1.0);
}}

float4 {NAME}_V(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{{
	float3 c = 0.0;
	[unroll] for (int i = 0; i < {NV}; i++)
		c += {NAME}_v[i].y * tex2Dlod({NAME}_sH, float4(uv.x, uv.y + {NAME}_v[i].x * BUFFER_RCP_HEIGHT, 0.0, 0.0)).rgb;
	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(lerp(o, c, TOPT_Strength), 1.0);
}}

technique {NAME}_sopt < ui_tooltip = "Pixel-shader separable reference, sigma {SIGMA}"; >
{{
	pass {{ VertexShader = PostProcessVS; PixelShader = {NAME}_H; RenderTarget = {NAME}_tH; }}
	pass {{ VertexShader = PostProcessVS; PixelShader = {NAME}_V; }}
}}
"""

COMPOSITE = """// ---- plain composite: the _orig of every pair (read the back buffer, write it)
float4 TOPT_C_Composite_PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	return float4(tex2D(ReShade::BackBuffer, uv).rgb, 1.0);
}
"""

ORIG = """technique {STEM}_orig < ui_tooltip = "Plain composite (the floor {STEM}_sopt is timed against)"; >
{{
	pass {{ VertexShader = PostProcessVS; PixelShader = TOPT_C_Composite_PS; }}
}}
"""

BAT = r"""@echo off
rem TOPT compute-blur benchmark: times every technique pair in topt-cs\ with the Test Host on
rem Direct3D 11, Direct3D 12 and Vulkan at 1920x1080 and 3840x2160. Results go to Results\.
setlocal
cd /d "%~dp0"
echo.
echo   TOPT compute-blur benchmark (about 5 minutes; the test window opens and closes by itself).
echo   Close games and other GPU-heavy programs first.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0bin\topt-bench.ps1" %*
echo.
pause
"""

PS1 = r"""# TOPT compute-blur benchmark (started by TOPT-CS-Bench.bat): sopt-host + ReShade + the sopt-timer add-on time
# every _orig / _sopt technique pair of the topt-cs\ presets on each API and resolution; one zip with all CSVs.
# Uses the Test Host's common.ps1; everything stays inside this folder.
param(
  [string[]]$Apis = @("dx11", "dx12", "vulkan"),
  [string[]]$Sizes = @("1920x1080", "3840x2160"),
  [int]$Frames = 300,
  [string]$ReShade = ""
)
. (Join-Path $PSScriptRoot "common.ps1")
$ReShade = Find-ReShade $ReShade
$pkg = Join-Path $Here "topt-cs"
$presets = @(Get-ChildItem -Path (Join-Path $pkg "sopt-presets") -Filter "sopt-*.ini" | Sort-Object Name)
if ($presets.Count -eq 0) { Fail "topt-cs\sopt-presets has no sopt-*.ini presets." }

$stamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$results = Join-Path $Here "Results\topt-cs-$stamp"
$shots = Join-Path $results "screenshots"
New-Item -ItemType Directory -Force -Path $results, $shots | Out-Null
$run = New-RunFolder $ReShade
Write-ReShadeIni $run (Join-Path $pkg "reshade-shaders\Shaders") (Join-Path $pkg "reshade-shaders\Textures") `
  $presets[0].FullName $shots $false @{
  SOPT_TIMER = [ordered]@{ AutoRun = 1; ExitWhenDone = 1; Screenshots = 1; Frames = $Frames }
}

$summary = @()
foreach ($size in $Sizes) {
  $w, $h = $size -split "x"
  foreach ($api in (Resolve-Apis $Apis)) {
    $tag = "$api-$size"
    Write-Host ""
    Write-Host "=== $($ApiNames[$api]) $size : $($presets.Count) presets, $Frames frames each ===" -ForegroundColor Cyan
    $csv = Join-Path $run "sopt-timer.csv"
    Remove-Item $csv -ErrorAction SilentlyContinue
    Enable-ReShade $run $api
    $p = Start-Process -FilePath (Join-Path $run "sopt-host.exe") -WorkingDirectory $run -PassThru -Wait `
      -ArgumentList @("--api", $api, "--bench", "--width", $w, "--height", $h)
    Disable-ReShade $run
    $log = Join-Path $run "ReShade.log"
    if (Test-Path $log) { Copy-Item $log (Join-Path $results "ReShade-$tag.log") -Force }
    if (Test-Path $csv) {
      Move-Item $csv (Join-Path $results "sopt-timer-$tag.csv") -Force
      $summary += "$tag : OK"
    } else {
      $summary += "$tag : no sopt-timer.csv (exit code $($p.ExitCode)); see ReShade-$tag.log"
    }
    $dir = Join-Path $shots $tag
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Get-ChildItem -Path $shots -File | Move-Item -Destination $dir -Force
  }
}

Get-GpuInfo | Set-Content (Join-Path $results "gpu.txt")
$summary | Set-Content (Join-Path $results "summary.txt")
$zip = "$results.zip"
Compress-Archive -Path "$results\*" -DestinationPath $zip -Force
Write-Host ""
$summary | ForEach-Object { Write-Host $_ }
Write-Host ""
Write-Host "Done. Send this file: $zip" -ForegroundColor Green
"""

README = """TOPT compute-blur benchmark
===========================

1. Extract this zip into a folder of its own.
2. Double-click TOPT-CS-Bench.bat. It runs the Test Host (sopt-host + ReShade 6.8.0 with
   add-on support + the sopt-timer add-on) on Direct3D 11, Direct3D 12 and Vulkan at
   1920x1080 and 3840x2160. The test window opens and closes by itself, once per run.
3. Send Results\\topt-cs-<date>.zip.

Nothing outside this folder is changed: every run uses its own run\\ folder and ReShade.ini.
Options (from a command prompt): TOPT-CS-Bench.bat -Apis dx11,vulkan,gl -Sizes 2560x1440 -Frames 600

What is timed (topt-cs\\reshade-shaders\\Shaders\\{EFFECT}, one preset per sigma 1 / 2 / 4):
every technique *_sopt against a plain composite *_orig on the same input, so orig_us is the
composite floor and diff_us what the blur adds.
  TOPT_C_Tile_s<N>     compute: tile + halo in groupshared memory, H and V there; composite pixel shader
  TOPT_C_TileComp_s<N> compute also does the composite; the pixel shader only copies
  TOPT_C_SplitHV_s<N>  compute H pass; pixel shader V pass fused with the composite
  TOPT_C_PS_s<N>       pixel-shader reference: the same taps, H pass + V pass fused with the composite

The Test Host itself (Test-Host.bat, README.html, bin\\, Docs\\) is the unchanged
Test-Host-{VERSION} release of sopt.
"""


def pairs_effect() -> tuple:
    """The pair-named effect and the technique stems per sigma."""
    src = cs_effect()
    stems = {}
    for name in re.findall(r"^technique (\w+) <", src, re.M):
        stems.setdefault(int(name.rsplit("_s", 1)[1]), []).append(name)
    src = re.sub(r"^technique (\w+) <", r"technique \1_sopt <", src, flags=re.M)
    blocks = [COMPOSITE]
    for sigma, r, w, v in cs_kernels():
        name = f"TOPT_C_PS_s{sigma}"
        blocks.append(PS_BLOCK.format(NAME=name, SIGMA=sigma, NV=len(v),
                                      V=", ".join(f"float2({o:.9g}, {w_:.9g})" for o, w_ in v)))
        stems[sigma].append(name)
    for sigma in stems:
        blocks += [ORIG.format(STEM=s) for s in stems[sigma]]
    head = src.rsplit("#endif", 1)[0]
    head = head.replace("// Auto-generated by topt - compute tile blur",
                        "// Auto-generated by topt (scripts/cs_package.py) - TOPT_Bench_CS.fx as _orig / _sopt pairs\n"
                        "// for the sopt-timer bench. Compute tile blur", 1)
    return head + "\n".join(blocks) + "#endif\n", stems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--testhost", required=True, type=Path, help="Test-Host-<version>.zip from the sopt releases")
    ap.add_argument("--shaders", required=True, type=Path, help="folder with ReShade.fxh")
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    a = ap.parse_args()
    version = re.search(r"Test-Host-([\d.]+)\.zip", a.testhost.name).group(1)
    fx, stems = pairs_effect()
    a.out.mkdir(parents=True, exist_ok=True)
    dst = a.out / "TOPT-CS-Bench.zip"
    with zipfile.ZipFile(a.testhost) as th, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for info in th.infolist():
            z.writestr(info, th.read(info))
        crlf = lambda s: s.replace("\r\n", "\n").replace("\n", "\r\n")
        z.writestr("TOPT-CS-Bench.bat", crlf(BAT))
        z.writestr("TOPT-CS-README.txt", crlf(README.replace("{EFFECT}", EFFECT).replace("{VERSION}", version)))
        z.writestr("bin/topt-bench.ps1", crlf(PS1))
        z.writestr(f"topt-cs/reshade-shaders/Shaders/{EFFECT}", crlf(fx))
        z.writestr("topt-cs/reshade-shaders/Shaders/ReShade.fxh", (a.shaders / "ReShade.fxh").read_bytes())
        z.writestr("topt-cs/reshade-shaders/Textures/.keep", "")
        for sigma, names in stems.items():
            techs = ",".join(f"{n}_{side}@{EFFECT}" for n in names for side in ("orig", "sopt"))
            z.writestr(f"topt-cs/sopt-presets/sopt-topt-cs-s{sigma}.ini",
                       f"Techniques={techs}\r\nTechniqueSorting={techs}\r\n")
    print("wrote", dst)


if __name__ == "__main__":
    main()
