function createChatMessage(content=null, avatar=null, who=null, when=null, add=true, edited=false) {
    var listItem = document.createElement('li');
    listItem.className = 'MessageListItem';
    var divItem = document.createElement('div');
    divItem.className = "MessageAvatar";
    var imageItem = document.createElement('img');
    imageItem.className = 'Avatar';
    var mBody = document.createElement('div');
    mBody.className = "MessageBody";
    var mHeader = document.createElement('div');
    mHeader.className = "MessageHeader";
    var mwho = document.createElement('src');
    mwho.className = "MsgWho"; 
    mwho.textContent = who;
    var mwhen = document.createElement('src');
    mwhen.className = "MsgWhen"; 
    mwhen.textContent = when;
    var medited = document.createElement('src');
    medited.className = "MsgEdited"; 
    medited.textContent=null;
    var mContent = document.createElement('div');
    mContent.className = 'MessageContent';
    mContent.textContent=content;
    listItem.appendChild(divItem);
    divItem.appendChild(imageItem);
    listItem.appendChild(mBody);
    mBody.appendChild(mHeader);
    mBody.appendChild(mContent);
    mHeader.appendChild(mwho);
    mHeader.appendChild(mwhen);
    mHeader.appendChild(medited);

    if (add == true){
        const ele = document.getElementsByClassName('MessageList')[0];
        ele.appendChild(listItem); 
        // listItem.scrollIntoView({behavior: 'smooth', block:"end", align:"true"}); 
        listItem.scrollIntoView(true); 
    }
    return listItem;
}
// console.log("working");



// Create messages from json 
function parseJSON(messages){
    var selected = document.getElementsByClassName("Selected"); 
    try{
        selected = selected[0].textContent;
    }catch(e){
        console.log("Nothing selected");
    }
    const keys = Object.keys(messages); 
    let id = 0; 
    let content = ""; 
    let when = ""; 
    let edited = false; 
    let who = ""; 
    let avatar = null; 
    let room = "";
    // console.log("Parsing message", messages); 
    for(let i = 0; i < keys.length; i++){
        content = messages[keys[i]]["content"];
        when = messages[keys[i]]["time"];
        who  =  messages[keys[i]]["from"];
        room = messages[keys[i]]["room"];
        console.log("Room: " + room + " Selected: " + selected);
        if(selected.length == 0){
            console.log("Not room");
            createChatMessage(content, null, who, when);  
        }else if(selected == room){
            console.log("in the filter");
            createChatMessage(content, null, who, when);  
        }else{
            console.log("Here in else");
        }
    }

}

function checkRooms(room){
    var currentRooms = document.getElementsByClassName("ChannelText");
    for(var i = 0; i < currentRooms.length; i++){
        if(currentRooms[i].textContent == room){
            return false; 
        }
    }
    return true;

}

function updateWindow(parsed){ 
    let onlineElement = document.getElementById("onlineTag");
    let listItem = document.getElementById("members-online")
    var roomElement = document.getElementsByClassName("ChannelItem")[0];
    var roomParent = document.getElementsByClassName("ChannelList")[0]; 
    let rooms = parsed["rooms"];
    rooms.forEach(element => {
        if(checkRooms(element)){
            var clone = roomElement.cloneNode(true);
            clone.style.display = "block";
            clone.querySelector(".ChannelText").textContent = element; 
            // clone.textContent = element; 
            roomParent.append(clone);
        }
    });

    /* Not good code could use dynamic programming to speed things up */
    let users = parsed["connected"];
    let numUsers = Object.keys(users).length;
    let keys = Object.keys(users); 

    var listElements = document.getElementsByClassName("Users");
    console.log("List elements: ", listElements); 
    for(var i = 0; i < listElements.length; i++){
        listElements[i].remove();
    }
    keys.forEach(element=>{
        /* If there is a difference in the number of users and number of elements clear elements */
        try{
            if(!document.getElementById(element)){
                var userName = users[element];
                var newListItem = document.createElement("li"); 
                newListItem.id = element; 
                newListItem.className = "Users"
                newListItem.textContent = userName;
                listItem.appendChild(newListItem);
            }

        }catch(error){
            console.log("Error in update window: ", error);
        }
    });

    


    onlineElement.innerHTML = "ONLINE - " + String(numUsers);


}




module.exports = {createChatMessage, parseJSON, updateWindow};