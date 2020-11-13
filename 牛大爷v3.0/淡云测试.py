from lib import sqlwork


sql= 'select * from gmtable where name="amu"'
sqldo=sqlwork.SQL("select",sql,'one')
print(sqldo)









