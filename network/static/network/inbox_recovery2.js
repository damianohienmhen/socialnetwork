
window.addEventListener('load', function() {
load_posts()
});


function load_posts() {

 fetch('/myposts') 
.then(response => response.json())
.then(posts => {
    html = '';
    posts.forEach(post => {
    htmlSegment = `<div id = "thepost_${post.id}" class="containerborder">
    				    <div style="font-size:30px;">${post.user}</div>
    				    <br>
                    	${post.post_content}<br>
                        ${post.created}<br>
                        <button onclick="addlikes(${post.id})" id="likesbutton_${post.id}">${post.nolikes}</button><i class="em em-heart" aria-role="presentation" aria-label="HEAVY BLACK HEART"></i>
                   </div>`;
                  
        html += htmlSegment;
    });
    
    container = document.querySelector('#container')
    container.innerHTML = html;
    first()
  
    console.log(posts);
   
});
};

function addlikes(id) { 

fetch(`/likeposts/${id}`)
.then(response => response.json())
.then(newcount => {

document.querySelector(`#likesbutton_${newcount.postid}`).innerHTML = newcount.likescount;


})
 }; 

function first() {



document.querySelector('#proto').style.display = 'block';
document.querySelector('#container').style.display = 'block';

firsti = 11
secondi= 21


  for (i =0; i < firsti; i++) {

    if (c = (document.getElementById("thepost_" + i ))) {
    document.querySelector('#proto').append(c)
    
    // do stuff

}
 localStorage.setItem('firsti', 11);
 localStorage.setItem('secondi', 21);
}
document.querySelector('#container').style.display = 'none';
document.querySelector('#proto1').style.display = 'none';


};


function next() {

document.querySelector('#container').style.display = 'block';




  for (i = firsti; i < secondi; i++) {

    if (c = (document.getElementById("thepost_" + i ))) {
    const element = document.createElement('div');
        element.innerHTML = 'This is the content of the div.';
        
   document.querySelector('#proto1').append(c);
   
}

   } 
    
    // do stuff
document.querySelector('#container').style.display = 'none';
document.querySelector('#proto').style.display = 'none';
document.querySelector('#proto1').style.display = 'block';

firsti = parseInt(secondi)
secondi = parseInt(firsti) + 10
};

function previous() {

document.querySelector('#container').style.display = 'block';




  for (i = firsti-10; i < secondi-10; i++) {

    if (c = (document.getElementById("thepost_" + i ))) {
    const element = document.createElement('div');
        element.innerHTML = 'This is the content of the div.';
        
   document.querySelector('#proto1').append(c);
   
}

   } 
    
    // do stuff
document.querySelector('#container').style.display = 'none';
document.querySelector('#proto').style.display = 'none';
document.querySelector('#proto1').style.display = 'block';

};
