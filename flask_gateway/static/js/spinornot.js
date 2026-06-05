var getinput = function(){
    var input1 = document.getElementById('projectname').value;
    var input2 = document.getElementById('authorname').value;
    if (input1 === '' || input2 === ''){
        return false
    }
    else{
        return true
    }
};