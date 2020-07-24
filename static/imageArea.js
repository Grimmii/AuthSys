$( document ).ready(function() {
   $(".imgarea").on("click", function(e){
          e.preventDefault();
         addSelected(e.target.id);
      });
});

switchImage =  function(id,url){
   url = "url('" +url  + "')";
   document.getElementById("shownImg").style.backgroundImage = url;
   document.getElementById("selected-imageid").value = id;
   resetSelected();
}

addSelected = function(id){
   id = id.toString()
   selected = selectedStringtoList(document.getElementById("selected").value)
   if (selected.includes(id)){
      selected[selected.indexOf(id)] = ""
      // selected.pop(id);
      document.getElementById(id).style.borderColor = "black";
      // console.log('Removed : ' + id )
   }else if ( selected.length > 6){
      alert('Selected full');
   }else{
      selected.push(id);
      document.getElementById(id).style.borderColor = "red";
      // console.log('Added : ' + id )
   }
   document.getElementById("selected").value = selectListToString(selected);
   // console.log('Final : ' + document.getElementById("selected").value)
}

resetSelected = function(){
   selected = selectedStringtoList(document.getElementById("selected").value)
   var i;
   for (i=0; i < selected.length; i++){
      document.getElementById(selected[i]).style.borderColor = "black";
   }
   document.getElementById("selected").value = "";
   // console.log("selection reseted");

}

selectedStringtoList = function(string){
   return string.split("-").filter(Boolean);
}

selectListToString = function(list){
   return list.join('-');
}
