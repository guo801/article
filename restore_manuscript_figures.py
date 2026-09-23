from pathlib import Path
import re

root = Path(r'C:\Users\guo\Desktop\article\ieee_template')
backup = root / 'revision_backup_20260906_205853'
figures = [
    ('methodology', 'fig:sim_env', 'subsec:dt_construction',
     'Digital twin workspace in Isaac Sim, showing the robot and laboratory equipment used in the original environment design.',
     'Isaac Sim中的数字孪生工作空间，展示原环境设计中的机器人与实验器材。'),
    ('methodology', 'fig:sim_env_parallel', 'subsec:ppo',
     'Parallel simulation environments for robot policy training.',
     '用于机器人策略训练的并行仿真环境。'),
    ('methodology', 'fig:skill_library', 'subsec:hierarchical_skill',
     'Hierarchical state machine and reusable skill library for laboratory workflow coordination.',
     '用于实验室工作流协调的分层状态机与可复用技能库。'),
    ('experiments', 'fig:hardware_setup', 'subsec:exp_setup',
     'Physical laboratory platform and its digital twin, showing the solution preparation, contact-angle measurement, and serial dilution work areas.',
     '实验硬件平台及其数字孪生，展示配液、接触角测量与梯度稀释工作区域。'),
]

for suffix in ['', '_chinese']:
    for part, label, anchor, en, zh in figures:
        path = root / 'sections' / (part + suffix + '.tex')
        text = path.read_text(encoding='utf-8')
        if '\\label{' + label + '}' in text:
            continue
        original = (backup / 'sections' / (part + suffix + '.tex')).read_text(encoding='utf-8')
        block = next(m.group() for m in re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}', original, re.S) if '\\label{' + label + '}' in m.group())
        block = re.sub(r'\\caption\{[^\n]*\}', lambda m: '\\caption{' + (zh if suffix else en) + '}', block)
        reference = ('如图~\\ref{' + label + '}所示。' if suffix else 'See Fig.~\\ref{' + label + '}.')
        marker = '\\label{' + anchor + '}'
        assert text.count(marker) == 1
        text = text.replace(marker, marker + '\n' + reference + '\n' + block, 1)
        path.write_text(text, encoding='utf-8')

main = (root / 'main.tex').read_text(encoding='utf-8')
flat = re.sub(r'\\input\{([^}]+)\}', lambda m: (root / (m.group(1) + '.tex')).read_text(encoding='utf-8'), main)
(root / 'main_standalone.tex').write_text(flat, encoding='utf-8')

for suffix in ['', '_chinese']:
    contents = '\n'.join((root/'sections'/(part+suffix+'.tex')).read_text(encoding='utf-8') for part in ['methodology','experiments'])
    paths = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', contents)
    assert len(paths) == 5, paths
    assert all((root/p).is_file() for p in paths)
    print(('Chinese' if suffix else 'English') + ': all 5 original image references restored; image files exist.')

notes = root / 'REVISION_NOTES.md'
text = notes.read_text(encoding='utf-8')
text = text.replace('11. 移除空图、空结果章节及缺少结果的表格；原图只保留框架图并注明图内标签待确认。', '11. 移除没有图片文件的空图、空结果章节及缺少结果的表格；根据作者反馈恢复全部5张已有插图，包括框架、仿真环境、并行训练、技能库、虚实平台对照。图片文件未修改，图注保留必要的措辞修正。')
text += '\n## 插图恢复\n\n根据作者反馈，恢复此前从正文移出的4张实际插图，保留原图文件、原标签和原尺寸设置，并在相关小节添加引用。中英文及单文件英文同步更新。此前未实际提供图片的占位图不伪造补入。\n'
notes.write_text(text, encoding='utf-8')
