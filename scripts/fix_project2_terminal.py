from pathlib import Path
from datetime import datetime
import shutil
import nbformat

p = Path(r'D:\Group_9\notebooks\Project2.ipynb')
n = nbformat.read(p, as_version=4)
nbformat.validate(n)
if len(n.cells) == 26 and 'scripts.run_spmf_fixed' in n.cells[14].source:
    print('Notebook already cleaned (26 cells)')
    raise SystemExit(0)
assert len(n.cells) == 34, f'Expected 34 cells, got {len(n.cells)}. Not changed.'
backup = p.with_name('Project2_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.ipynb')
shutil.copy2(p, backup)
c = n.cells
order = [0,1,2,4,5,6,7,8,9,10,11,12,13,18,14,19,20,21,22,25,26,27,29,30,23,24]
n.cells = [c[i] for i in order]

n.cells[0].source = '\n'.join(c[0].source.splitlines()[:5]) + '''

**Project:** Group_9 - Eclat (Python + Julia).
**Colab:** Python 3 runtime. Upload this notebook, then Group_9_Colab.zip in Step 1.
Run Steps 1-7, Step 7B (Julia), and finally Step 8 (download results).
**VS Code:** Run scripts via PowerShell in D:\\Group_9.
Runtime measurements on different machines are not directly comparable.
'''
for cell in n.cells:
    if cell.cell_type == 'markdown':
        cell.source = (cell.source
            .replace('Eclat_HCMUS_VSCode_Colab.zip', 'Group_9_Colab.zip')
            .replace('Eclat_Submission_VSCode', 'Group_9'))

# Correct optional JAR uploader and install Java 25 BEFORE launching SPMF.
n.cells[12].source = 'import importlib\n' + n.cells[12].source
n.cells[14].source = '''import csv
assert jar.is_file(), 'Missing tools/spmf.jar'
run_module('scripts.run_spmf_fixed', '--jar', 'tools/spmf.jar')
with (project / 'results/spmf_comparison.csv').open(
        encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
matched = [r for r in rows if r['status'] == 'ok'
           and r['exact_match'].lower() == 'true']
print(f'SPMF EXACT MATCH: {len(matched)}/{len(rows)}')
assert len(rows) == len(matched) == 25, 'SPMF comparison incomplete'
'''

# A PDF stored on Windows should not be treated as missing in a Colab-only export.
n.cells[18].source = n.cells[18].source.replace(
    "run_module('scripts.check_submission')",
    "if not Path('/content').is_dir():\n    run_module('scripts.check_submission')\nelse:\n    print('Report.pdf is kept on Windows, not in the Colab ZIP')")

# Mark new Julia measurements as originating in this Colab session.
n.cells[23].source += '''
import json, platform
from datetime import datetime, timezone
info = {
    'run_utc': datetime.now(timezone.utc).isoformat(),
    'platform': platform.platform(),
    'julia': subprocess.check_output([JULIA, '--version'], text=True).strip(),
    'colab': Path('/content').is_dir()
}
(ROOT / 'results/julia_execution_environment.json').write_text(
    json.dumps(info, indent=2), encoding='utf-8')
print('Julia environment:', info)
'''

# Export only after all checks, updating the old BMS warning without mangling accents.
n.cells[25].source = '''from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import csv, unicodedata

with (project / 'results/spmf_comparison.csv').open(
        encoding='utf-8-sig', newline='') as f:
    spmf = list(csv.DictReader(f))
assert len(spmf) == 25 and all(
    r['status'] == 'ok' and r['exact_match'].lower() == 'true'
    for r in spmf), 'SPMF must be 25/25'

with (project / 'results/julia_benchmark.csv').open(
        encoding='utf-8-sig', newline='') as f:
    julia_rows = list(csv.DictReader(f))
assert len(julia_rows) == 48 and all(
    r['count_match'].lower() == 'true'
    and r['backend_exact_match'].lower() == 'true'
    for r in julia_rows), 'Julia must be 48/48'

readme = project / 'results/README.md'
if readme.is_file():
    content = readme.read_text(encoding='utf-8')
    updated = []
    for line in content.splitlines():
        plain = ''.join(x for x in unicodedata.normalize('NFD', line.lower())
                        if unicodedata.category(x) != 'Mn').replace('đ', 'd')
        if 'bms_webview_1' in plain and 'trang thai loi' in plain:
            updated.append('SPMF Colab: 25/25 exact matches, including BMS_WebView_1 with ID remapping.')
        else:
            updated.append(line)
    readme.write_text('\\n'.join(updated) + '\\n', encoding='utf-8')

output = base / 'Eclat_Ket_Qua_Thuc_Nghiem_Colab.zip'
collected = [x for x in (project / 'results').rglob('*') if x.is_file()]
for rel in ('data/download_manifest.json', 'docs/generated/experiment_data.tex'):
    file = project / rel
    if file.is_file():
        collected.append(file)
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    for file in collected:
        archive.write(file, file.relative_to(project))
print('Created:', output)
if Path('/content').is_dir():
    from google.colab import files
    files.download(str(output))
'''

for cell in n.cells:
    if cell.cell_type == 'code':
        cell.outputs = []
        cell.execution_count = None
    cell.metadata.pop('execution', None)
nbformat.validate(n)
nbformat.write(n, p)
print('BACKUP:', backup)
print('CLEANED:', len(c), '->', len(n.cells), 'cells')
print('SPMF FIXED:', 'scripts.run_spmf_fixed' in n.cells[14].source)
print('JULIA BEFORE STEP 8:', n.cells[19].source.startswith('## ') and n.cells[24].source.startswith('## '))
print('OLD ERROR OUTPUTS REMOVED: True')
