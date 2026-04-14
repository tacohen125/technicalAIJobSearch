"""Test helper: apply long bullets (>130c) to simulate old overflow mistake."""
import sys, re
sys.path.insert(0, 'scripts')
from para_utils import split_doc, join_doc, rebuild_para, arial_run

xml_path = sys.argv[1]
with open(xml_path, encoding='utf-8') as f:
    content = f.read()
paras, tail = split_doc(content)

paras[19] = rebuild_para(paras[19], arial_run(
    'Engineered test specifications and defined detailed acceptance criteria for optomechanical '
    'and automation teams developing pilot-scale optical characterization systems.'
))
paras[20] = rebuild_para(paras[20], arial_run(
    'Developed RCWA and ray-tracing simulations to comprehensively link inline measurement data '
    'to component-level optical performance, supporting design validation against all specifications.'
))

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(join_doc(paras, tail))

p19 = len(re.sub(r'<[^>]+>', '', paras[19]))
p20 = len(re.sub(r'<[^>]+>', '', paras[20]))
print(f'Para 19: {p19}c, Para 20: {p20}c')
