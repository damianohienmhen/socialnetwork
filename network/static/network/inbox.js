
function addlikes(id) { 

fetch(`/likeposts/${id}`)
.then(response => response.json())
.then(newcount => {

document.querySelector(`#likesbutton_${newcount.postid}`).innerHTML = newcount.likescount;


})
}; 

function edit(id) { 

fetch(`/edit/${id}`)
.then(response => response.json())
.then(edit => {

 r =     `<form enctype="multipart/form-data" onsubmit="submit(${edit.id})" action ="/submit/${edit.postid}" method ="POST" >
          <input type='hidden' name='csrfmiddlewaretoken' value="${ csrftoken }"/>
          <input type="text" name = "updatepost" class="form-control" id="compose-body" placeholder="Body" value="${edit.post_content}" ></input>
          <button type="submit" name= "update" value ="update" class="btn btn-primary">Update</button>
          </form>`;

document.querySelector(`#thepost_${edit.postid}`).innerHTML =  r;



})
};

function submit(id) { 

fetch(`/submit/${id}`)
.then(response => response.json())
.then(post => {

document.querySelector(`#thepost_${post.postid}`).innerHTML =  `<div id = "thepost_${post.id}" class="containerborder">
    				                                                  <div style="font-size:30px;">${post.user}</div>
    				    											  <br>
                    												  ${post.post_content}<br>
                        											  ${post.created}<br>
                        											  <button onclick="addlikes(${post.id})" id="likesbutton_${post.id}">${post.nolikes}</button><i class="em em-heart" aria-role="presentation" aria-label="HEAVY BLACK HEART"></i>
                   													  </div>`;
console.log(post)


})
}; 

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

