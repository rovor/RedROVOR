function addClickableLI(list,contents){
    var elem = $("<li class='clickable'>"+contents+"</li>");
    list.append(elem);
    elem.click(changeSelected);
    return elem;
}


function changeSelected(eventObj) {
    $(this).siblings().removeClass("selected");
    $(this).addClass("selected");
}


//class for the browser window

function BrowserWindow(id,initialPath){
    this.id = id;
    if( initialPath){
        this.topPath = initialPath;
    } else {
        this.topPath = '';
    }

    this.flist = $("#"+id+ " .folderList");
    this.clist = $("#"+id+" .fileList");
    this.leftSelected = '.';
    this.populateLeft('');
}

BrowserWindow.prototype.populateLeft = function(path){
    var li;
    var browser = this; //rename so closures can use it
    this.flist.empty();
    if(path){
        this.topPath += path + "/";
    }
    
    li = addClickableLI(this.flist,".");
    li.click(function(){ 
        browser.populateRight(".");
    });
    li.click(); //trigger a click event
    

    $.getJSON('json/'+this.topPath,{},function(data){
       for(var i=0,len=data.contents.length; i !== len; ++i){
            //$(".pathTitle").text(data.path);
            if( data.contents[i].isDir ){
                li = addClickableLI(browser.flist,data.contents[i].file);
                li.click(function(){
                    browser.populateRight($(this).text());
                    browser.leftSelected = $(this).text();
                });
                li.dblclick(function(){
                    browser.populateLeft($(this).text())
                });
            }
       }
    });

}

BrowserWindow.prototype.populateRight = function (path){
    var browser = this;
    $.getJSON('json/'+this.topPath+path,{},function(data){
        browser.clist.empty();
        for(var i=0, len=data.contents.length; i!== len; ++i){
            var elem = addClickableLI(browser.clist,data.contents[i].file);
            elem.prepend($("<img src='"+data.contents[i].icon+"'/>"))
        }
    });
}

/**
 *  get the path to the folder selected on the left
 */
BrowserWindow.prototype.getSelectedFolder = function(){
    return this.topPath + this.leftSelected;
}

/**
 *  get the path to the file selected on the right
 */
BrowserWindow.prototype.getSelectedFile = function(){
    return this.getSelectedFolder() + "/" + this.clist.find(".selected").text();
}

