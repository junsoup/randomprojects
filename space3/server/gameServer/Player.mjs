class Player{
    id = undefined;
    lastUpdate = undefined;
    position = undefined;
    constructor(id, time, position){
        this.id = id;
        this.lastUpdate = time;
        this.position = position
    }
    setPosition(newPosition){
        this.position = newPosition;
    }
};
export default Player;