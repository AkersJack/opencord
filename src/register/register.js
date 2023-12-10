var checkPassword = function(){
     if (document.getElementsByName('password')[0].value ==
    document.getElementsByName('confirm-password')[0].value) {
    document.getElementById('message').style.color = 'black';
    document.getElementById('message').innerHTML = 'Confirm Password';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'Confirm Password: Error Passwords do not match.';
  }
}
