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
    var li, newPath;
    var browser = this; //rename so closures can use it
    this.flist.empty();
    if(path){
        newPath = this.topPath + path + "/";
        this.topPath += path + "/";
    } else {
        newPath = this.topPath;
    }
    
    li = addClickableLI(this.flist,".");
    li.click(function(){ 
        browser.populateRight(".");
        browser.leftSelected = "";
    });
    li.click(); //trigger a click event
    

    $.getJSON('/files/json/'+newPath,{},function(data){
       browser.topPath = data.path; //set to normalized path
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
       browser.flist.click(); //temporary fix to let the client know that the selected folder has been updated
    });

}

BrowserWindow.prototype.populateRight = function (path){
    var browser = this;
    $.getJSON('/files/json/'+this.topPath+path,{},function(data){
        browser.clist.empty();
        for(var i=0, len=data.contents.length; i!== len; ++i){
            //only show files that aren't directories
            if( ! data.contents[i].isDir){
                var elem = addClickableLI(browser.clist,data.contents[i].file);
                elem.prepend($("<img src='"+data.contents[i].icon+"'/>"))
            }
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

/**
 * add a handler for when the path is updated, i.e. when the user selects a new
 * folder on the left, the handler is passed the new path
 */
BrowserWindow.prototype.pathUpdated = function(handler){
    var br = this;
    this.flist.click(function(){
        handler(br.getSelectedFolder());
    });
    
}

/*
 * same as pathUpdated, but for top path
 */
BrowserWindow.prototype.topPathUpdated = function(handler){
    var br = this;
    this.flist.dblclick(function(){
        handler(br.topPath);
    });
}

/*
 *  the selectetion on the right has been updated
 */
BrowserWindow.prototype.selectionUpdated = function(handler){
    var br = this;
    this.clist.click(function(){
        handler(br.getSelectedFile());
    });
}

/**
 *  set the top level path
 */
BrowserWindow.prototype.setPath = function(newPath){
    this.topPath = newPath;
    this.populateLeft('');
}

