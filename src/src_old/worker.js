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
    const keys = Object.keys(messages); 
    let id = 0; 
    let content = ""; 
    let when = ""; 
    let edited = false; 
    let who = ""; 
    let avatar = null; 
    // console.log("Parsing message", messages); 
    for(let i = 0; i < keys.length; i++){
        content = messages[keys[i]]["content"];
        when = messages[keys[i]]["time"];
        who  =  messages[keys[i]]["from"];
        createChatMessage(content, null, who, when);  
    }

}

module.exports = {createChatMessage, parseJSON};