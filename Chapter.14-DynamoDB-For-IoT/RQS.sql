SELECT *, floor(timestamp()/1E3 + 1E5) as ttlExpireOn FROM 'iot/#'
