const AWS = require('aws-sdk');

exports.handler = async (event, context, callback) => {
    const output = event.records.map((record) => {

        let data = Buffer.from(record.data, 'base64').toString('utf8');
        console.log('data :', data);

        if (data) {
            try {
                data = JSON.parse(data);
                data.UUID = AWS.util.uuid.v4();
                data = JSON.stringify(data);
                data = data.replace(/\\n/g, '');
                data = data.replace('}', "},");   //add back trailing comma 
                console.log('formation done!', data);
            } catch (e) {
                console.log('e :', e);

            }
        }

        return {
            recordId: record.recordId,
            result: 'Ok',
           // data: new Buffer(data).toString('base64'),  //depreciated
           data: Buffer.alloc(Object.keys(data).length, data).toString('base64'),  //create a buffer of dynamoc size and place data object into buffer 
        };
    });

    callback(null, { records: output });
};
