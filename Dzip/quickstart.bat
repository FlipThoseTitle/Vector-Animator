echo archive .\output\rename_this.dz>config.dcl
echo basedir .\input\>>config.dcl
FOR /F %%f IN ('dir /B input\') DO echo file %%f 0 dz>>config.dcl
dzip.exe config.dcl
pause