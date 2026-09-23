from pathlib import Path
import re, shutil, datetime

root=Path(r'C:\Users\guo\Desktop\article\ieee_template')
original=root/'revision_backup_20260906_205853'
archive=root/('abridged_revision_archive_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
archive.mkdir()
shutil.copytree(root/'sections',archive/'sections')
for name in ['main.tex','main_chinese.tex','main_standalone.tex','main.pdf','main_chinese.pdf','main_standalone.pdf','README.md','REVISION_NOTES.md']:
    if (root/name).exists(): shutil.copy2(root/name,archive/name)
for p in (original/'sections').glob('*.tex'):
    shutil.copy2(p,root/'sections'/p.name)
for name in ['main.tex','main_chinese.tex','main_standalone.tex','README.md']:
    shutil.copy2(original/name,root/name)

# Preserve each original variant independently, including the fuller standalone text.
def bibitems(text):
    return {m.group(1):m.group(0).strip() for m in re.finditer(r'\\bibitem\{([^}]+)\}.*?(?=\\bibitem|\\end\{thebibliography\})',text,re.S)}
catalog={}
for name in ['main_standalone.tex','main.tex','main_chinese.tex']:
    for key,value in bibitems((original/name).read_text(encoding='utf-8')).items():
        catalog.setdefault(key,value)

counts=[]
for name in ['main.tex','main_chinese.tex','main_standalone.tex']:
    p=root/name
    text=p.read_text(encoding='utf-8')
    expanded=re.sub(r'\\input\{([^}]+)\}',lambda m:(root/(m.group(1)+'.tex')).read_text(encoding='utf-8'),text)
    keys=bibitems(text)
    cited={key.strip() for group in re.findall(r'\\cite\{([^}]+)\}',expanded) for key in group.split(',')}
    missing=sorted(cited-keys.keys())
    assert all(key in catalog for key in missing),missing
    if missing:
        text=text.replace(r'\end{thebibliography}','\n\n'.join(catalog[key] for key in missing)+'\n\n'+r'\end{thebibliography}')
    # Font setup only; original prose, figures and section structure remain intact.
    if r'\usepackage{xeCJK}' not in text:
        text=text.replace(r'\usepackage{graphicx}',r'\usepackage{graphicx}'+'\n'+r'\usepackage{xeCJK}')
    text=text.replace(r'\begin{document}',r'\setmainfont{Times New Roman}'+'\n'+r'\begin{document}',1)
    p.write_text(text,encoding='utf-8')
    counts.append(f'{name}: 原有{len(keys)}条，恢复后{len(bibitems(text))}条，补齐原有引用键{len(missing)}个。')

changed=[]
for p in list((root/'sections').glob('*.tex'))+[root/'main_standalone.tex']:
    if p.name=='bibliography.tex': continue
    s=p.read_text(encoding='utf-8')
    t=s.replace('170 & 84.8','170 & 85.0')
    # Correct the formula itself without deleting its surrounding discussion.
    t=t.replace(r'''\text{CI}_{95\%} = \hat{p} \pm 1.96 \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}''',r'''\begin{aligned}
    D &= 1+z^2/n,\quad z=1.96,\\
    c &= (\hat p+z^2/(2n))/D,\\
    h &= \frac{z}{D}\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}},\\
    \text{CI}_{95\%} &= [c-h,c+h].
    \end{aligned}''')
    if t!=s: changed.append(p.name)
    p.write_text(t,encoding='utf-8')

# Confirm exact paragraph and figure retention apart from the two local corrections.
for p in (original/'sections').glob('*.tex'):
    before=p.read_text(encoding='utf-8')
    after=(root/'sections'/p.name).read_text(encoding='utf-8')
    assert re.findall(r'\\(?:sub)*section\{[^}]+\}',before)==re.findall(r'\\(?:sub)*section\{[^}]+\}',after)
    assert re.findall(r'\\includegraphics[^\n]+',before)==re.findall(r'\\includegraphics[^\n]+',after)

note='''# 完整原稿恢复与局部修改说明

当前已撤回上一轮大幅删改。各版本从最初备份分别恢复，保留各自正文、章节、公式推导、图片引用、实验表格、占位内容和参考文献；没有再用拆分稿覆盖较完整的单文件稿。

最初备份：revision_backup_20260906_205853/
上一轮精简版归档：'''+archive.name+'''

## 当前实际保留的修改

- 170/200对应百分比由84.8修正为85.0。
- 将误标为Wilson的正态近似公式修正为Wilson公式，不删去周围文字。
- 拆分稿缺失的引用条目从原有文献中补齐，未凭空新增文献；原条目保留。
- 英文字体设置及后续必要的编译排版修正。

## 参考文献数量

'''+ '\n'.join('- '+c for c in counts)+'''

## 独立修改意见，不直接删改原文

1. 核对Panda、固定UR3、移动UR3三种描述与真实硬件关系。
2. 核对姿态奖励坐标轴与负距离乘数问题；未擅自改变训练算法或套用旧结果。
3. 核对HSM与HRL高层学习的实际实现；中文额外方法与英文方法的差异仍保留供作者决定。
4. 核对82.7%、93.3%及全流程42/50、必要子步骤40/50的版本和统计口径。
5. 核对jerk定义、单位与轨迹数据；补充统计区间、随机种子及实验质量指标。
6. 文献条目已恢复，但尚未逐条验证书目信息真实性和引文匹配。
7. 无实图的占位图、空表及待补实验内容依原稿保留，投稿前需完善。

后续应按原稿逐段修改，在保留篇幅、图片、引用与研究主线的前提下处理问题。重大删改需要先明确说明。
'''
(root/'REVISION_NOTES.md').write_text(note,encoding='utf-8')
print('\n'.join(counts))
print('Original section structures and every image reference preserved.')
print('Local corrections:',', '.join(changed))
