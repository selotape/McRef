SET 7ZIP="C:\Program Files (x86)\Atlassian\SourceTree\tools\7za.exe"

cd "G:\Users\ronvis\Thesis_nondropbox\experiments\oxford"
FOR %%G IN (01 05 10 15) DO (
	FOR %%E IN (1 2 4) DO (
		
		REM echo %%G
		
		REM echo %%E
		
		SET simName=M3.%%G.migAC_%%E_0
		SET zipName=%simName%.zip
		SET traceName=trace.%simName%.tsv
		SET cladeName=clade.%simName%.tsv
		
		ECHO %simName%
		ECHO %zipName%
		ECHO %traceName%
		ECHO %cladeName%
		cd %simName%
		
		REM %7ZIP% e %zipName%
		
		REM rename %traceName%.dwn %traceName%
		REM rename %cladeName%.dwn %cladeName%		
		REM cd ..
	)
)
	
sleep 100
