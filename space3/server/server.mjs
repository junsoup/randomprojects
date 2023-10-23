import mysql from 'mysql';
import path from 'path';
import express from 'express';
import session from 'express-session';
import cookieParser from 'cookie-parser';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename); 
const oneDay = 86400000;
const gamePath = path.join(__dirname, '../game');
const connection = mysql.createConnection({
	host     : 'localhost',
	user     : 'root',
	password : 'root',
	database : 'nodelogin'
});

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(session({
	secret: 'authKey',
	resave: false,
	saveUninitialized: true,
	cookie: {maxAge: oneDay}
}));

import Game from './gameServer/Game.mjs';
const game = new Game();

// Request goes to login page or main game.
app.get('/',(req,res) =>{
	if(req.session.loggedin && req.session.username)
		res.sendFile('loggedin.html',{root:__dirname});
	else
		res.sendFile('login.html',{root:__dirname});
});

app.get('/login.css',(req,res) =>{
	res.sendFile('login.css',{root:__dirname});
});
app.get('/loggedin.js',(req,res) =>{
	res.sendFile('loggedin.js',{root:__dirname});
});

app.post('/auth', function(request, response) {
	let username = request.body.username;
	let password = request.body.password;

	if (request.body["logout"] == "Logout"){
		request.session.destroy();
		response.redirect('/');
		return;
	}

	if (request.body["start"] == "Start"){
		response.redirect('/game');
		return;
	}

	connection.query('SELECT * FROM accounts WHERE username = ? AND password = ?', [username, password], function(error, results, fields) {
		if (error) throw error;
		if (results.length > 0) {
			request.session.loggedin = true;
			request.session.username = username;
		}
		response.redirect('/');
		response.end();
	});
});

app.get('/loggedin', function (req, res) {
	return res.send(req.session.username);
});

app.get('/game',(req,res) =>{
	if(req.session.loggedin && req.session.username){
		res.sendFile(path.join(gamePath, 'main.html'));
		connection.query('SELECT id FROM accounts WHERE username = ?', [req.session.username], function(error, results, fields) {
			if (error) throw error;
			game.addPlayer(results[0]['id'])
		});
		
	}else
		res.redirect('/');
});

app.get('*', (req,res) =>{
	if(req.session.loggedin && req.session.username)
		res.sendFile(path.join(gamePath, req.url));
	else
		res.redirect('/');
})

app.use('/', express.static(__dirname));
app.use('*', express.static(gamePath));

var server = app.listen(80,function() {
    console.log("running on localhost:80")
});
