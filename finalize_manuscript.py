from pathlib import Path
import re
root=Path(r'C:\Users\guo\Desktop\article\ieee_template')
for suffix in ['', '_chinese']:
    p=root/('sections/methodology'+suffix+'.tex')
    s=p.read_text(encoding='utf-8')
    s=s.replace(r'''\begin{equation}
\min_{q(\cdot)}\int_0^T\|\dddot q(t)\|^2dt,
\quad |\phi-\phi_{target}|\le\epsilon_\phi,
\quad |\vartheta-\vartheta_{target}|\le\epsilon_\vartheta.
\end{equation}''',r'''\begin{gather}
\min_{q(\cdot)}\int_0^T\|\dddot q(t)\|^2dt,\\
|\phi-\phi_{target}|\le\epsilon_\phi,\qquad
|\vartheta-\vartheta_{target}|\le\epsilon_\vartheta.
\end{gather}''')
    p.write_text(s,encoding='utf-8')
    p=root/('sections/experiments'+suffix+'.tex')
    s=p.read_text(encoding='utf-8')
    a=s.index('\\begin{equation}')
    b=s.index('\\end{equation}',a)+len('\\end{equation}')
    s=s[:a]+r'''\begin{align}
 D&=1+z^2/n,\qquad z=1.96,\\
 c&=\frac{\hat p+z^2/(2n)}{D},\\
 h&=\frac{z}{D}\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}},\\
 [p_L,p_U]&=[c-h,c+h].
\end{align}'''+s[b:]
    s=s.replace('成功率为28.7、62.7和82.7个百分点','成功率分别为28.7\\%、62.7\\%和82.7\\%').replace('\\%','\\%')
    # Chinese literal percent must be TeX escaped without an extra backslash.
    p.write_text(s,encoding='utf-8')
    p=root/('main'+suffix+'.tex')
    s=p.read_text(encoding='utf-8')
    s=s.replace(r'\setCJKmainfont{SimSun}',r'\setmainfont{Times New Roman}'+'\n'+r'\setCJKmainfont[AutoFakeBold=2,AutoFakeSlant=0.2]{SimSun}')
    p.write_text(s,encoding='utf-8')
s=(root/'main.tex').read_text(encoding='utf-8')
flat=re.sub(r'\\input\{([^}]+)\}',lambda m:(root/(m.group(1)+'.tex')).read_text(encoding='utf-8'),s)
(root/'main_standalone.tex').write_text(flat,encoding='utf-8')
for main in ['main','main_chinese','main_standalone']:
    s=(root/(main+'.tex')).read_text(encoding='utf-8')
    expanded=re.sub(r'\\input\{([^}]+)\}',lambda m:(root/(m.group(1)+'.tex')).read_text(encoding='utf-8'),s)
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',expanded))
    cites={key for group in re.findall(r'\\cite\{([^}]+)\}',expanded) for key in group.split(',')}
    labels=re.findall(r'\\label\{([^}]+)\}',expanded)
    refs=set(re.findall(r'\\ref\{([^}]+)\}',expanded))
    assert not cites-keys,(main,cites-keys)
    assert not refs-set(labels),(main,refs-set(labels))
    assert len(labels)==len(set(labels)),main
    print(main, 'citation/reference checks passed')
