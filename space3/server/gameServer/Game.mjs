import Player from "./Player.mjs";
import mysql from 'mysql';
const connection = mysql.createConnection({
	host     : 'localhost',
	user     : 'root',
	password : 'root',
	database : 'nodelogin'
});

const d = new Date();
class Game{
    players = []
    objects = []
    constructor(){
        console.log("game: starting");
    }
    addPlayer(playerID){
        if(this.players.some(player => player.id === playerID) == false){
            this.players.push(new Player(playerID, d.getTime(), [0,0,0]));
            console.log("game: adding " + playerID);
        }
    }
    removePlayer(playerID){
        // save player into database
        const index = this.players.findIndex(player => player.id === playerID);
        if (index !== -1) {
            players.splice(index, 1);
        }
    }
};
export default Game;