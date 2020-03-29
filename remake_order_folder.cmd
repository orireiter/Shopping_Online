sc stop colbomain
sc stop colboshoppingbag
sc stop colbosender

rmdir /s /q "C:\ColBo\orders"
md "C:\ColBo\orders"

sc start colbomain
sc start colboshoppingbag
sc start colbosender