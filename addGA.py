#!/usr/bin/env python3
import os
import streamlit as st
import re

code="""
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-07KGM1QX7N"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-07KGM1QX7N');
</script>
"""
a=os.path.dirname(st.__file__)+'/static/index.html'
with open(a, 'r') as f:
    data=f.read()
    if len(re.findall('UA-', data))==0:
        with open(a, 'w') as ff:
            newdata=re.sub('<head>','<head>'+code,data)
            ff.write(newdata)
