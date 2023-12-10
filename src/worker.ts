
function createChatMessage(){
    const listItem = document.createElement('li');
    listItem.className = 'MessageListItem';

    const divItem = document.createElement('div');
    divItem.className = "MessageAvatar";

    const imageItem = document.createElement('img');
    imageItem.className = 'Avatar';

    const mBody = document.createElement('div');
    mBody.className = "MessageBody";

    const mHeader = document.createElement('div');
    mHeader.className = "MessageHeader";

    const mContent = document.createElement('div');
    mContent.className = 'MessageContent';

    listItem.appendChild(divItem);
    divItem.appendChild(imageItem);
    listItem.appendChild(mBody);
    mBody.appendChild(mHeader);
    mBody.appendChild(mContent);

    return listItem;
}
