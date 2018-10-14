const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/criminaldb', { useNewUrlParser : true });

const crimSchema = new mongoose.Schema({
    Name : String,
    score : Number,
    img : {
        data : Buffer,
        contentType : String
    }
});

var Crim = mongoose.model('Crim', crimSchema);
module.exports.Crim = Crim;
