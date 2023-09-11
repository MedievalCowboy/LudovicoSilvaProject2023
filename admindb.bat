@echo off
FOR /f "tokens=2 delims==" %%a IN ('wmic OS Get localdatetime /value') DO SET "dt=%%a"
SET "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
SET "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
SET "datestamp=%YYYY%%MM%%DD%" & set "timestamp=%HH%%Min%%Sec%"
SET "fullstamp=%YYYY%-%MM%-%DD%_%HH%%Min%"
SET "mysql_bin_dir=C:\xampp\mysql\bin\"
SETLOCAL EnableDelayedExpansion
SET "db_dump_dir=.\dbDumps\"
IF NOT EXIST "%db_dump_dir%" MKDIR "%db_dump_dir%"

:MENU
CLS
ECHO.
ECHO ...............................................
ECHO Menu de administracion de db by RicardoAmun :)
ECHO ...............................................
ECHO.
ECHO 1 - Exportar db
ECHO 2 - Importar db
ECHO 3 - SALIR
ECHO ...............................................
ECHO Nota: por defecto la ruta para el mysql es C:\xampp\mysql\bin\
ECHO si llega a ocurrir un error esto es lo primero que debera verificar.
ECHO ...............................................
ECHO.


SET /P M=A donde vamos?:
IF %M%==1 GOTO EXPORT
IF %M%==2 GOTO IMPORT
IF %M%==3 GOTO EOF


:EXPORT
CLS
SET /P DB_NAME_IMPORT="Como se llama la db a exportar?: "
SET "startExportTime=%time: =0%"
"%mysql_bin_dir%mysqldump" --user=Ricardo --password=valeria2 --result-file="%db_dump_dir%%DB_NAME_IMPORT%_db_%fullstamp%.sql" "%DB_NAME_IMPORT%"

SET "endExportTime=%time: =0%"

REM Get Elapsed time:
SET "end=!endExportTime:%time:~8,1%=%%100)*100+1!"  &  set "start=!startExportTime:%time:~8,1%=%%100)*100+1!"
SET /A "elap=((((10!end:%time:~2,1%=%%100)*60+1!%%100)-((((10!start:%time:~2,1%=%%100)*60+1!%%100), elap-=(elap>>31)*24*60*60*100"

REM Convert elapsed time to HH:MM:SS:CC format:
SET /A "cc=elap%%100+100,elap/=100,ss=elap%%60+100,elap/=60,mm=elap%%60+100,hh=elap/60+100"
SET "elapsedExportTime=%hh:~1%%time:~2,1%%mm:~1%%time:~2,1%%ss:~1%%time:~8,1%%cc:~1%"

ECHO "Exportacion finalizada en %elapsedExportTime%."
PAUSE
GOTO MENU

:IMPORT
CLS
SET /P DB_NAME_IMPORT="Como se llama la base de datos objetivo?: "
SET /P FILE_NAME_IMPORT="Como se llama el archivo a importar?: "
SET "startimportTime=%time: =0%"

%mysql_bin_dir%mysql --user=Ricardo --password=valeria2 "%DB_NAME_IMPORT%" < "%FILE_NAME_IMPORT%"

SET "endImportTime=%time: =0%"
REM Get Elapsed time:
SET "end=!endImportTime:%time:~8,1%=%%100)*100+1!"  &  set "start=!startImportTime:%time:~8,1%=%%100)*100+1!"
SET /A "elap=((((10!end:%time:~2,1%=%%100)*60+1!%%100)-((((10!start:%time:~2,1%=%%100)*60+1!%%100), elap-=(elap>>31)*24*60*60*100"

REM Convert elapsed time to HH:MM:SS:CC format:
SET /A "cc=elap%%100+100,elap/=100,ss=elap%%60+100,elap/=60,mm=elap%%60+100,hh=elap/60+100"
SET "elapsedImportTime=%hh:~1%%time:~2,1%%mm:~1%%time:~2,1%%ss:~1%%time:~8,1%%cc:~1%"

ECHO "Exportacion finalizada en %elapsedImportTime%."
PAUSE
GOTO MENU

:EOF
CLS
EXIT




