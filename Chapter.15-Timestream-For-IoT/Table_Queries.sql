SELECT * FROM "myIotDB44"."myIoTDB44_table" WHERE time between ago(999m) and now() ORDER BY time DESC LIMIT 10 

Or a simplified query for small data tables:

SELECT * FROM "myIotDB44"."myIoTDB44_table"
