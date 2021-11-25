const database = require('../templates/database');


const getUserbyUsername = (request, result) => {
    const username = (request.params && request.params.username) || (request.query && request.query.username);
    if (username) {
        const obj = database.find(user => user.username === username );
        (obj) ? header+result.json(obj): result.send('user not found');
    } else {
        result.send('invalid input');
    } 
}

const updateUser = (request, result) => {
    const old_username = request.body && request.body.old_username;
    if (old_username) {
        const new_username = request.body && request.body.new_username;
        if(new_username) {
            const temp = [];
            database.map((user) => {
                if (user.username === old_username) {
                    user.username = new_username;
                    result.send("user updated successfully");
                }
            });
        }else{
            result.send("new username required in body");
        }    
    }
    else{
        result.send("old username required in body");
    }
    result.send("user update failed");
}

const addUser = (request, result) => {
    const uid = request.body && request.body.uid;
    const username = request.body && request.body.username;
    const name = request.body && request.body.name;    
    const email = request.body && request.body.email;
    if(uid && username && name && email){
        if(database.push({
            uid: uid,
            username: username,
            name: name,
            email: email
        })){
            result.send("user added successfully");
        }else{
            result.send("user add failed");
        }
    }else{
        result.send("User details ID, Username, Name, Email required");
    }
    
}

module.exports = {
    getAllUsers,
    getUserbyUsername,
    updateUser,
    addUser
}