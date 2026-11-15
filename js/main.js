(function(){
  var d=document,h=d.querySelector('.site-header'),root=d.documentElement;
  var mb=d.querySelector('.mobile-book');function onScroll(){var y=window.scrollY;if(h)h.classList.toggle('scrolled',y>24);if(mb)mb.classList.toggle('show',y>window.innerHeight*.7)}
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var t=d.querySelector('.nav-toggle');
  if(t){t.addEventListener('click',function(){var o=root.classList.toggle('nav-open');t.setAttribute('aria-expanded',o);d.body.style.overflow=o?'hidden':''});
    d.querySelectorAll('.nav-links a').forEach(function(a){a.addEventListener('click',function(){root.classList.remove('nav-open');t.setAttribute('aria-expanded','false');d.body.style.overflow=''})});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&root.classList.contains('nav-open')){t.click();t.focus()}});}
  var els=d.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});els.forEach(function(el){io.observe(el)})}else{els.forEach(function(el){el.classList.add('in')})}
  var links=d.querySelectorAll('.nav-links a[href^="#"]'),secs=[];
  links.forEach(function(a){var s=d.querySelector(a.getAttribute('href'));if(s)secs.push([s,a])});
  if('IntersectionObserver' in window&&secs.length){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){secs.forEach(function(p){p[1].removeAttribute('aria-current')});secs.forEach(function(p){if(p[0]===e.target)p[1].setAttribute('aria-current','true')})}})},{rootMargin:'-45% 0px -50% 0px'});secs.forEach(function(p){so.observe(p[0])})}
  var y=d.getElementById('year');if(y)y.textContent=new Date().getFullYear();
})();
