(function() {
  //obtained from http://www.quirksmode.org/blog/archives/2005/10/_and_the_winner_1.html
  addEvent = function( obj, type, fn )
  {
    if (obj.addEventListener)
      obj.addEventListener( type, fn, false );
    else if (obj.attachEvent)
    {
      obj["e"+type+fn] = fn;
      obj[type+fn] = function() { obj["e"+type+fn]( window.event ); }
      obj.attachEvent( "on"+type, obj[type+fn] );
    }
  }

  removeEvent = function( obj, type, fn )
  {
    if (obj.removeEventListener)
      obj.removeEventListener( type, fn, false );
    else if (obj.detachEvent)
    {
      obj.detachEvent( "on"+type, obj[type+fn] );
      obj[type+fn] = null;
      obj["e"+type+fn] = null;
    }
  }

  convertTime = function(e) {
    var evt = e || window.event;
    var evtTarget = evt.target || evt.srcElement;

    if (evtTarget.id.indexOf('run.') > -1) {
      if (evtTarget.value.indexOf(':') >= 0) {
        time = evtTarget.value.split(':');
        evtTarget.value = parseInt(time[0],10)*60+parseInt(time[1]);
      }
    }
  }  

  addOnBlur = function() {
    var inputs = document.getElementsByTagName('INPUT');

    for(var i = 0; i < inputs.length; i++)
    {
      if(inputs[i].id.match(/_time$/))
      {
        addEvent( inputs[i], 'blur', convertTime );
      }
    }
  }
  
  addEvent( window, 'load' , addOnBlur );
})();
