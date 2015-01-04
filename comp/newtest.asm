;Test assembly for new Terpstra CPU


.var X 5
.var Y 6

start:
   lda X
   ldb Y
   mult
   jmp start



