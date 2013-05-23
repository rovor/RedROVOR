function FileChooserDialog(ident,initialPath){
    this.id = ident;
    this.elem = $("#"+ident);
    this.initialPath = initialPath;
    this.path = initialPath;
    this.pathTitle = this.elem.find(".pathTitle");
    this.mylist = this.elem.find('.fileList');

    var proxy = this;
    this.elem.dialog({
        autoOpen: false,
        height: 500,
        width: 500,
        modal: true,
        title: "Choose a File",
        buttons: {
            "Open": function(){
                proxy.doSelect($(this).find(".selected"));
            },
            Cancel: function() {
                $(this).dialog("close");
            },
        }
    });
    this.populate();

}


FileChooserDialog.prototype = {
open: function(callback){
    this.path = this.initialPath;
    this.populate();
    this.callback = callback;
    this.elem.dialog("open");
},

close: function(){
    this.elem.dialog("close");
},

populate: function() {
    this.mylist.empty();
    var proxy = this;
    $.getJSON("/files/json/"+this.path,{},function(data){
        this.path = data.path;
        proxy.pathTitle.text(data.path);
        for(var i =0, len = data.contents.length; i !== len; ++i){
                var elem = $("<li class='clickable'>"+data.contents[i].file+"</li>");
                elem.data("isdir",data.contents[i].isDir);
                elem.prepend($("<img src='"+data.contents[i].icon+"'/>"));
                elem.click(function(){
                    $(this).addClass("selected");
                    $(this).siblings().removeClass("selected");
                });
                elem.dblclick(function(e){
                    proxy.doSelect($(this));
                });
                proxy.mylist.append(elem);
        }
    });
},

doSelect: function(item){
    if( !(item && item.length !== 0) ){
        alert("nothing to do");
        //nothing is selected
        return;
    }
    var newPath = this.path + item.text() + "/";
    if( item.data("isdir") ){
        this.path = newPath;
        this.populate();
    } else {
        this.elem.dialog("close");
        if( this.callback ){
            this.callback.call(null,newPath);
        }
    }
},
};
