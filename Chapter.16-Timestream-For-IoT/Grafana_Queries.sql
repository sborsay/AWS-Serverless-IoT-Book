Query for combined graph (single entry)

FROM $__database.$__table WHERE 'humidity' = "measure_name" OR 'temperature' = "measure_name" 

Use the query below to make two separate lines on your graph.  You will need to make a Query "A" and a Query "B" as two different entries.  Also make sure that the names and the data types match your data table (i.e., bigint or double).

Query A

SELECT CREATE_TIME_SERIES(time,measure_value::bigint) as temperature FROM $__database.$__table where $__timeFilter and measure_name = 'temperature'

Query B

SELECT CREATE_TIME_SERIES(time,measure_value::bigint) as humidity FROM $__database.$__table where $__timeFilter and measure_name = 'humidity'
