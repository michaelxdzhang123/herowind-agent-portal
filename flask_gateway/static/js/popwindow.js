var showalert = function(){
    var the_text = "请注意，为确保后台可以成功计算，上传文件及填写数据时请务必严格按照模板格式，否则可能无法正常计算，谢谢配合！\n\n" +
        "您是否确认数据格式正确？";
    var re = confirm(the_text);
    if (re===true){
        return true
    }
    else{
        return false
    }
};

// var makeinput = function(){
//     var the_input = document.getElementById('testing').value;
//     if (the_input===''){
//         alert("请输入相关信息！");
//         return false
//     }
//     else{
//         return true
//     }
//
// };
//
// var setinput = function(){
//     var the_input = document.getElementById('testing').value;
//     if (the_input===''){
//         return false
//     }
//     else{
//         return true
//     }
// };