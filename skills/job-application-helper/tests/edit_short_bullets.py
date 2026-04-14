"""Test helper: apply short bullets (≤110c) + proactive pub cuts — correct approach."""
import sys, re
sys.path.insert(0, 'scripts')
from para_utils import split_doc, join_doc, rebuild_para, arial_run

xml_path = sys.argv[1]
with open(xml_path, encoding='utf-8') as f:
    content = f.read()
paras, tail = split_doc(content)

# Short bullets (≤110c)
paras[19] = rebuild_para(paras[19], arial_run(
    'Engineered optical test specifications for optomechanical and automation teams '
    'to build pilot-scale systems.'
))
paras[20] = rebuild_para(paras[20], arial_run(
    'Developed RCWA and ray-tracing models supporting measurement-driven '
    'metrology and design validation.'
))

# Proactive pub cuts + remove low-relevance bullet (reverse index order)
paras.pop(50)  # Thompson, Cohen - DiffCapAnalyzer (batteries, off-domain)
paras.pop(48)  # Huang, Cohen - Green Syntheses (organic dye, off-domain)
paras.pop(36)  # Led long-horizon NSF programs (low relevance)

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(join_doc(paras, tail))

p19 = len(re.sub(r'<[^>]+>', '', paras[19]))
p20 = len(re.sub(r'<[^>]+>', '', paras[20]))
total = sum(len(re.sub(r'<[^>]+>', '', p)) for p in paras if re.sub(r'<[^>]+>', '', p).strip())
print(f'Para 19: {p19}c, Para 20: {p20}c, Total chars: {total}')
