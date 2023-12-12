function createChatMessage(content=null, avatar=null, who=null, when=null, add=true, edited=false) {
    var image = null; 
    var image_type = null; 
    if(who == "Jack"){ 
        image = './images/avatar_jack.webp';
    }else if(who == "nick"){
        image = './images/avatar_nick.webp';
    }else if(who == "zain"){
        image = './images/avatar_zain.webp';
    }else if(who == "diyor"){
        image = './images/avatar_zain.webp';
    }else{
        // image = './images/default.svg';
        image = '<svg width="38px" height="38px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9 16C9.85038 16.6303 10.8846 17 12 17C13.1154 17 14.1496 16.6303 15 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/><path d="M21.6359 12.9579L21.3572 14.8952C20.8697 18.2827 20.626 19.9764 19.451 20.9882C18.2759 22 16.5526 22 13.1061 22H10.8939C7.44737 22 5.72409 22 4.54903 20.9882C3.37396 19.9764 3.13025 18.2827 2.64284 14.8952L2.36407 12.9579C1.98463 10.3208 1.79491 9.00229 2.33537 7.87495C2.87583 6.7476 4.02619 6.06234 6.32691 4.69181L7.71175 3.86687C9.80104 2.62229 10.8457 2 12 2C13.1543 2 14.199 2.62229 16.2882 3.86687L17.6731 4.69181C19.9738 6.06234 21.1242 6.7476 21.6646 7.87495" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/></svg>';
        image_type = 'svg'; 
    }
    var listItem = document.createElement('li');
    listItem.className = 'MessageListItem';
    var divItem = document.createElement('div');
    divItem.className = "MessageAvatar";
    if(image_type != 'svg'){
        var imageItem = document.createElement('img');
        imageItem.src = image; 
    }else{
        const fill = Math.floor(Math.random()*16777215).toString(16); 
        // console.log("Fill: " + fill);

        imageItem = document.createElement('div');
        imageItem.innerHTML = image; 
        imageItem.child
        // imageItem.style.backgroundColor = "#" + String(fill);
        // imageItem.style.backgroundColor = "rgb(166, 38, 63)";
        // imageItem.src = "./images/default.svg";
    }
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
        // console.log("Room: " + room + " Selected: " + selected);
        if(selected.length == 0){
            console.log("Not room");
            createChatMessage(content, null, who, when);  
        }else if(selected == room){
            // console.log("in the filter");
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
        try{
            if(checkRooms(element)){
                var clone = roomElement.cloneNode(true);
                clone.style.display = "block";
                clone.querySelector(".ChannelText").textContent = element; 
                // clone.textContent = element; 
                roomParent.append(clone);
            }

        }catch(error){
            console.log("Clone Error");
        }
    });

    /* Not good code could use dynamic programming to speed things up */
    let users = parsed["connected"];
    let numUsers = Object.keys(users).length;
    let keys = Object.keys(users); 

    var listElements = document.getElementsByClassName("Users");
    // console.log("List elements: ", listElements); 
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