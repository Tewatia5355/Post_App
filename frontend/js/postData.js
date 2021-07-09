
//Check the given url is correct or not by regex
function checkImgUrl(url) {

    var expression = /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi;
    var regex = new RegExp(expression);
    var t = url;

    if (t.match(regex)) {
        return true

    }
    else {
        return false
    }
}

//function to add new meme by Post request
async function newMeme() {
    let name = document.querySelector("#newMemeName").value;
    let caption = document.querySelector("#newMemeCaption").value;
    let memeUrl = document.querySelector("#newMemeUrl").value;

    //checking if all fields are present
    if (name === "" || caption === "" || url === "") {
        alert("Fill all fields please and then proceed")
        return;
    }

    //checking Url using Regex
    var checkImgUrlBool = checkImgUrl(memeUrl)

    if (-1 === memeUrl.indexOf('://')) {
        var str1 = "http://";
        memeUrl = str1.concat(memeUrl);
        // console.log(memeUrl)
    }

    //alert if given url is having errors
    if (!checkImgUrlBool) {
        alert("error in url")
    } else {

        //Sending POST request
        var xhr = new XMLHttpRequest();

        var url = "https://xmemeshare.herokuapp.com/memes";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {

                //Error Handling with Status Codes
                if (xhr.status === 406) {
                    alert(`Response Status : 406 --> Url is not of an image`)
                }
                else if (xhr.status === 400) {
                    alert('Response Status : 400 --> Incorrect POST request Parameters')
                }
                else if (xhr.status === 409) {
                    alert('Response Status : 409 --> url already present in Database')
                }
                else if (xhr.status === 201) {
                    var json = JSON.parse(xhr.responseText);
                    document.querySelector("#allMemes").innerHTML = "";
                    getData()
                    alert(`Response Status : 201 --> Your Meme is Successfully uploaded with unique ID -> ${json.id}`)

                }
                else {
                    alert(`Response Status : ${xhr.status} --> Internal Server Issue, please check Logs`)
                }
            }
        };

        //Formatting the given data for Json response
        var data = JSON.stringify({
            name: `${name}`,
            caption: `${caption}`,
            url: `${memeUrl}`,
        });
        xhr.send(data);
    }

    //Marking form fields as Null again 
    document.querySelector("#newMemeName").value = null;
    document.querySelector("#newMemeCaption").value = null;
    document.querySelector("#newMemeUrl").value = null;
}

async function updateMeme() {

    let id = document.querySelector("#uniqueId").innerHTML;
    let caption = document.querySelector("#updateCaption").value;
    let memeUrl = document.querySelector("#updateUrl").value;


    //Check if both the URL and Caption are Not NULL
    if (caption === "" && memeUrl === "") {
        alert("Fill any of one field please and then proceed")
        return;
    }

    //If Url is given, Check for Regex
    if (memeUrl != "") {
        if (-1 === memeUrl.indexOf('://')) {
            var str1 = "http://";
            memeUrl = str1.concat(memeUrl);
        }
    }
    if (memeUrl && !checkImgUrl(memeUrl)) {
        alert("error in url")
        return;
    }

    //Send Patch Request
    var xhr = new XMLHttpRequest();
    var url = `https://xmemeshare.herokuapp.com/memes/${id}`;
    xhr.open("PATCH", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {

            //Error Handling with Status Codes
            if (xhr.status === 406) {
                alert(`Response Status : 406 --> Url is not of an image`)
            }
            else if (xhr.status === 400) {
                alert('Response Status : 400 --> Incorrect POST request Parameters')
            }
            else if (xhr.status === 409) {
                alert('Response Status : 409 --> url already present in Database')
            }
            else if (xhr.status === 404) {
                alert('Response Status : 404 --> No Meme With Given Id')
            }
            else if (xhr.status === 204) {
                document.querySelector("#allMemes").innerHTML = "";
                getData()
                alert(`Response Status : 204 --> Updated Successfully`)
            } else {
                alert(`Response Status : ${xhr.status}`)
            }

        }
    };

    //Formatting variables to Json Data for Patch Request 
    var data = JSON.stringify({ caption: `${caption}`, url: `${memeUrl}` });
    xhr.send(data);

    //Marking form fields as Null again
    document.querySelector("#updateCaption").value = null;
    document.querySelector("#updateUrl").value = null;
}

//When Update Button is clicked, send the Id number to form
function updateMemeButton(id) {
    var x = id.toString();
    document.querySelector("#uniqueId").innerHTML = x;
}

//When Html load, fetch memes from given Url

function getData() {
    fetch(`https://xmemeshare.herokuapp.com/memes`)
        .then((response) => response.json())
        .then((data) => {

            //Using for loop to parse and Append Memes to Div
            for (var i = 0; i < data.length; i++) {
                let name = data[i].name;
                let caption = data[i].caption;
                let url = data[i].url;
                document.querySelector(
                    "#allMemes"
                ).innerHTML += `<div class="col"><div class="card border-info  px-4 py-4 mx-1 my-2 text-dark bg-light" ><div class="card-header"><strong>Meme No :</strong> ${data[i].id}</div><div class="card-body"><h5 class="card-title mb-4"><strong>Name : </strong> ${name}</h5><img src="${url}" class="card-img-top img-fluid"><p class="card-text text-center mt-2"><strong>Caption : </strong>${caption}</p></div><button onclick="updateMemeButton(${data[i].id})" class="upd btn btn-success" data-bs-toggle="modal" data-bs-target="#updateModal">Update this Meme</button></div></div>`;
            }
        });
}

document.addEventListener("DOMContentLoaded", getData());






