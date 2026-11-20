(function(){
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  var root=document.documentElement;
  document.querySelectorAll('[data-act]').forEach(function(b){
    b.addEventListener('click',function(){
      var a=b.getAttribute('data-act');
      if(a==='dark'){var d=document.body.classList.toggle('dark');set('lum-dark',d?'1':'0');return}
      var cur=parseInt(getComputedStyle(root).getPropertyValue('--fs'))||27;
      cur=Math.max(16,Math.min(44,cur+(a==='bigger'?1:-1)));
      root.style.setProperty('--fs',cur+'px');set('lum-fs2',cur);
    });
  });
  var reader=document.querySelector('.reader');
  var read={};try{read=JSON.parse(get('lum-read')||'{}')}catch(e){}
  if(reader){
    var slug=reader.getAttribute('data-slug');
    read[slug]=1;set('lum-read',JSON.stringify(read));
    set('lum-last',JSON.stringify({slug:slug,title:reader.getAttribute('data-title')}));
    document.addEventListener('keydown',function(e){
      if(e.altKey||e.ctrlKey||e.metaKey)return;
      var l=null;
      if(e.key==='ArrowLeft')l=document.querySelector('link[rel=prev]');
      if(e.key==='ArrowRight')l=document.querySelector('link[rel=next]');
      if(l)location.href=l.getAttribute('href');
    });
  }
  document.querySelectorAll('.toc a').forEach(function(a){
    if(read[a.getAttribute('href')])a.classList.add('read');
  });
  var r=document.getElementById('resume');
  if(r){var last=null;try{last=JSON.parse(get('lum-last')||'null')}catch(e){}
    if(last&&last.slug){r.href=last.slug;r.textContent='Continue: '+last.title.replace(/\u3000/g,' ');r.hidden=false}}
})();

/* Read aloud: the browser's own speech synthesis */
(function(){
  var btn=document.getElementById('tts-btn'),bar=document.getElementById('tts-bar');
  var reader=document.querySelector('.reader');
  if(!btn||!bar||!reader||!('speechSynthesis' in window)||typeof SpeechSynthesisUtterance==='undefined')return;
  var ss=window.speechSynthesis;
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  btn.hidden=false;

  // What is read: book and volume titles, chapter title, epigraph, paragraphs and list items (not tables)
  var sel='.part-title,.vol-title,h1,blockquote p,article > p,article > h2,article > h3,article li,article figcaption';
  var units=[].slice.call(reader.querySelectorAll(sel)).filter(function(el){
    return el.textContent.replace(/\s/g,'').length>0 && !el.closest('table') && !el.closest('nav');
  });
  if(!units.length){btn.hidden=true;return}

  function clean(t){
    return t.replace(/[　\s]+/g,' ').replace(/\*/g,'').replace(/—/g,', ').replace(/…/g,'... ').trim();
  }
  // Split long paragraphs into sentences; some browsers stop part-way through long utterances
  function chunks(t){
    var out=[],buf='';
    t.split(/(?<=[.!?;:]["”’)]?\s)/).forEach(function(s){
      if((buf+s).length>220&&buf){out.push(buf);buf=s}else buf+=s;
    });
    if(buf)out.push(buf);
    var res=[];out.forEach(function(s){while(s.length>300){var k=s.lastIndexOf(', ',280);if(k<60)k=s.lastIndexOf(' ',280);if(k<60)k=280;res.push(s.slice(0,k+1));s=s.slice(k+1)}if(s.trim())res.push(s)});
    return res;
  }

  var rateSel=bar.querySelector('[data-tts=rate]'),voiceSel=bar.querySelector('[data-tts=voice]'),
      autoBox=bar.querySelector('[data-tts=auto]'),mainBtn=bar.querySelector('[data-tts=toggle]');
  var voices=[],voice=null;
  if(get('lum-tts-rate'))rateSel.value=get('lum-tts-rate');
  if(get('lum-tts-auto')==='0')autoBox.checked=false;

  function score(v){
    var n=v.name;
    if(/Natural|Online/i.test(n)&&/Aria|Guy|Jenny|Ryan|Sonia|Libby|Andrew|Emma|Brian|Ava/i.test(n))return 6;  // Edge natural voices
    if(/Daniel|Samantha|Karen|Moira|Serena|Arthur|Martha/i.test(n))return 5;                                // Apple
    if(/Google/i.test(n))return 4;
    if(/David|Zira|Mark|Hazel|George/i.test(n))return 3;                                                     // Windows local
    return /en[-_](GB|US)/i.test(v.lang)?2:1;
  }
  function loadVoices(){
    voices=ss.getVoices().filter(function(v){return /^en/i.test(v.lang)});
    voices.sort(function(a,b){return score(b)-score(a)||(/GB/.test(b.lang)-/GB/.test(a.lang))});
    voiceSel.innerHTML='';
    voices.forEach(function(v,i){var o=document.createElement('option');o.value=i;o.textContent=v.name.replace(/^Microsoft\s+/,'').split(/\s+Online|\s+-\s+|\s*\(/)[0].trim()+' · '+v.lang;voiceSel.appendChild(o)});
    var saved=get('lum-tts-voice'),idx=0;
    voices.forEach(function(v,i){if(v.name===saved)idx=i});
    voice=voices[idx]||null;
    if(voices.length)voiceSel.value=idx;
    voiceSel.parentNode.hidden=!voices.length;
  }
  loadVoices();
  if(ss.addEventListener)ss.addEventListener('voiceschanged',loadVoices);else ss.onvoiceschanged=loadVoices;

  var cur=0,part=0,parts=[],playing=false,token=0,keep=null;
  function mark(){
    units.forEach(function(u){u.classList.remove('tts-cur')});
    var el=units[cur];if(!el)return;
    el.classList.add('tts-cur');
    var r=el.getBoundingClientRect(),h=window.innerHeight;
    if(r.top<70||r.bottom>h-140)el.scrollIntoView({behavior:'smooth',block:'center'});
  }
  function setMain(){mainBtn.textContent=playing?'❚❚':'▶';btn.textContent=playing?'❚❚ Listening':'▶ Listen'}
  function speakPart(){
    var my=++token;
    if(cur>=units.length){finish();return}
    if(part===0){parts=chunks(clean(units[cur].textContent));mark()}
    if(!parts.length){cur++;part=0;speakPart();return}
    var u=new SpeechSynthesisUtterance(parts[part]);
    u.lang=voice?voice.lang:'en-GB';if(voice)u.voice=voice;
    u.rate=parseFloat(rateSel.value)||1;
    u.onend=function(){if(my!==token||!playing)return;part++;if(part>=parts.length){cur++;part=0;try{sessionStorage.setItem('lum-tts-pos',reader.dataset.slug+':'+cur)}catch(e){}}speakPart()};
    u.onerror=function(e){if(my!==token)return;if(e.error==='interrupted'||e.error==='canceled')return;part++;if(part>=parts.length){cur++;part=0}if(playing)setTimeout(speakPart,50)};
    ss.speak(u);
  }
  function play(from){
    ss.cancel();
    if(typeof from==='number'){cur=from;part=0}
    playing=true;document.body.classList.add('tts-on');bar.hidden=false;setMain();
    clearInterval(keep);
    // Chrome's online voices stall after ~15 s; nudge them periodically
    if(voice&&!voice.localService&&/Chrome/.test(navigator.userAgent)&&!/Edg\//.test(navigator.userAgent))
      keep=setInterval(function(){if(ss.speaking&&!ss.paused){ss.pause();ss.resume()}},10000);
    setTimeout(speakPart,60);
  }
  function pause(){playing=false;token++;ss.cancel();part=0;clearInterval(keep);setMain()}
  function stop(){pause();bar.hidden=true;document.body.classList.remove('tts-on');units.forEach(function(u){u.classList.remove('tts-cur')})}
  function finish(){
    playing=false;clearInterval(keep);setMain();
    var next=document.querySelector('link[rel=next]');
    if(autoBox.checked&&next){try{sessionStorage.setItem('lum-tts-go','1')}catch(e){}location.href=next.getAttribute('href')}
    else stop();
  }

  btn.addEventListener('click',function(){
    if(playing){pause();return}
    var first=units.findIndex(function(u){return u.getBoundingClientRect().bottom>80});
    play(bar.hidden?Math.max(0,first):cur);
  });
  bar.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    var a=b.getAttribute('data-tts');
    if(a==='toggle'){playing?pause():play(cur)}
    else if(a==='prev'){play(Math.max(0,cur-(part>0?0:1)))}
    else if(a==='next'){play(Math.min(units.length-1,cur+1))}
    else if(a==='stop'){stop()}
  });
  rateSel.addEventListener('change',function(){set('lum-tts-rate',rateSel.value);if(playing)play(cur)});
  voiceSel.addEventListener('change',function(){voice=voices[+voiceSel.value]||null;if(voice)set('lum-tts-voice',voice.name);if(playing)play(cur)});
  autoBox.addEventListener('change',function(){set('lum-tts-auto',autoBox.checked?'1':'0')});
  units.forEach(function(el,i){el.addEventListener('click',function(e){
    if(!document.body.classList.contains('tts-on')||e.target.closest('a'))return;
    if(window.getSelection&&String(window.getSelection()).length)return;
    play(i);
  })});
  window.addEventListener('pagehide',function(){ss.cancel()});

  // Carry on from the previous chapter
  var go=null;try{go=sessionStorage.getItem('lum-tts-go');sessionStorage.removeItem('lum-tts-go')}catch(e){}
  if(go){
    bar.hidden=false;document.body.classList.add('tts-on');cur=0;mark();setMain();
    setTimeout(function(){play(0);setTimeout(function(){if(!ss.speaking&&!ss.pending){pause();mainBtn.focus()}},2500)},300);
  }
})();
