PRGAM1 START 0
	   USING * , 15
       SR 4 , INDEX
	   SR 5 , INDEX
	   L 3 , =F'5'
INDEX EQU 3
LOOP L 2 , SETUP
     A 2 , =F'49'
	 ST 2 , DATA
     A 4 , =F'4'
     LA 1 , TOTAL
     BNE LOOP		
	 BR 14
     LTORG
SETUP DC F'34'
TOTAL DC F'8'
DATA DS 10F
END						
