const express = require("express"),
bodyParser	  = require("body-parser"),
multer		  = require("multer"),
fs			  = require("fs"),
request	  	  = require("request"),
db			  = require("./models/db.js"),
app			  = express(),
upload		  = multer({ dest : "./tmp" });

app.use(express.static(__dirname + "/views"));
app.use(express.static(__dirname + "/public"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");

app.get("/", function(req, res){
	res.sendFile("index.html");
});

app.post("/api", upload.single("jpeg"), function(req,res){
	var newEntry = new db.Crim();
	var data = req.body;
	for (var property in data){
		newEntry[property] = data[property];
	}

	newEntry.img.data = fs.readFileSync(req.file.path);
	newEntry.img.contentType = req.file.mimetype;
	newEntry.save();
	fs.unlinkSync(req.file.path);

	res.send("Successfully send to DB");
	//res.render("data", {data})
});

app.get("/api", function(req, res){
	db.Crim.find({}, (err, data) => {
		if (err) res.send("Error");
		else {
			for (var i=0; i<data.length; i++){
				var ext = data[i].img.contentType.split("/");
				var path = "./tmp/" + data[i].Name + "." + ext[1];
				var file = path;
				fs.writeFileSync(file, data[i].img.data);
				data[i].img = file;
				fs.unlinkSync(path);
			}
			res.send("Success");
			request.post({
				url : "http://172.22.194.27:5000/api/predict/",
				json : true,
				body : data
			});
		}
	});
});

app.get("/clear", function(req, res){
	db.Crim.deleteMany({}, (err) => {
		if (err) console.log("Error");
		else res.send("Success");
	});
});

app.listen(8100, () => console.log("listening on 8100"));
