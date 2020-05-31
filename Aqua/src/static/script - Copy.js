var yes_id = [];
var no_id = [];
var skip_id = [];
//Modal Data Content
function modal_fn() {
  document.getElementById("product-modal").innerHTML = document.getElementById("product-body").innerHTML;
  document.getElementById("solutions-modal").innerHTML = document.getElementById("solutions").innerHTML;
  document.getElementById("problems-modal").innerHTML = document.getElementById("myUL").innerHTML;
  document.getElementById("searchBar").innerHTML = '<input style="font-family:FontAwesome;" id="myInput" type="text"  onkeyup="search()" placeholder="&#xf002; Search for names.." title="Type in a name">';

  return document.getElementById("remote-modal").innerHTML = document.getElementById("remote-solutions").innerHTML;
}


function myFunction() {
  document.getElementById("myInput").value='';
  yes_id = [];
  no_id = [];
  skip_id = [];
  var api_var1 = document.getElementById("api_var1").innerHTML;
  var api_url = document.getElementById("api_url").innerHTML;
  //console.log(api_var1)
  document.getElementById("question").innerHTML = '<strong style="font-size:16px">What is the Problem?</strong>';
  document.getElementById("solutions").innerHTML = '<span class="badge" style="height: 20px;background-color:blue!important;">__%</span><strong style="font-size:16px;padding-left: 10px;">Fill in questions for solutions..</strong>'
  document.getElementById("remote-solutions").innerHTML = '';

  function postRequest(url, data) {
    return fetch(url, {
      credentials: 'same-origin', // 'include', default: 'omit'
      method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
      body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    })
    .then(response => response.json())
  };
  async function loadDoc(api_url,api_var1) {
  var slides = await postRequest(api_url+'/GetRootSymptoms', {UniqueProductIdentifier: api_var1})
  var str = '<ul id="test">'
  var str1 = ''

  slides.forEach(function(slide) {
  str += '<li><button style="background-color:black!important;padding: 12px 0 12px 0;border:none; color:white;" id='+(slide.symptomId)+'>'+ slide.symptomText + '</button></li>';
  });

  str1 += str+'</ul>';
  document.getElementById("myUL").innerHTML = str1;
  function getEventTarget(e) {
      e = e || window.event;
      return e.target || e.srcElement;
  }

  var ul = document.getElementById('test');
  ul.onclick = function(event) {
      var target = getEventTarget(event);
      //alert(target.innerHTML);}
    //.then(data => console.log(data)) // Result from the `response.json()` call
    //.catch(error => console.error(error))
    var api_var1 = document.getElementById("api_var1").innerHTML;
    var api_url = document.getElementById("api_url").innerHTML;

    function postRequest(url, data) {
      return fetch(url, {
        credentials: 'same-origin', // 'include', default: 'omit'
        method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
        body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
        headers: new Headers({
          'Content-Type': 'application/json'
        }),
      })
      .then(response => response.json())
    };
    document.getElementById("myUL").innerHTML = '<li><i class="fa fa-check-circle" style="color:green;" aria-hidden="true"></i>'+' '+document.getElementById(target.id).textContent+'</li>';
    document.getElementById("searchBar").innerHTML = '<input style="font-family: FontAwesome;" type="text" id="myInput" onkeyup="search()" placeholder="&#xf002; Search for names.." title="Type in a name">';
    document.getElementById("question").innerHTML ='<div class="spinner-border" role="status"><span class="sr-only">'+"Loading..."+'</span></div>'
    async function loadclick(api_url,api_var1,id) {
    var nextQuestion = await postRequest(api_url+'/GetNextSymptomQuestion', {UniqueProductIdentifier: api_var1,
                                                                              SymptomsThatArePresent: [parseInt(id)],
                                                                              SymptomsThatAreNOTPresent: [],
                                                                              SymptomsThatWereSkipped: []})


    //get solutions for third apnel
    //console.log(id)
    //console.log(nextQuestion)
    if (parseInt(id) != -1) {
    var solution = await postRequest(api_url+'/PredictPartsGivenSymptoms', {UniqueProductIdentifier: api_var1,
                                                                            SymptomsThatArePresent: [parseInt(id)],
                                                                            SymptomsThatAreNOTPresent: [],
                                                                            SymptomsThatWereSkipped: []})


let sols =  solution.partsRecommendation.map(function(sol) {
                              if ( sol.probablityPercentage > 75 ){
                                    return  '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:green!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                                    }
                                      return '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:blue!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'

                                      });
document.getElementById("solutions").innerHTML = sols.join("");//solution.partsRecommendation[0].partId

document.getElementById("remote-solutions").innerHTML = '<h4>Possible remote solutions:</h4>'
document.getElementById("remote-solutions").innerHTML += solution.remoteSolutions.remoteSolutions.map(function(r_sol) {
                    return  '<p style="padding-left:50px">*'+r_sol+'<p>';
}).join("");



}
yes_id.push(parseInt(id))
//no_id.push(parseInt(id))
//skip_id.push(parseInt(id))
//console.log(yes_id)
//console.log(no_id)
//console.log(skip_id)
//console.log(this.id)
if (nextQuestion.symptomId != -1){
document.getElementById("question").innerHTML = nextQuestion.symptomQuestion+'<p><button onclick = "click_yes('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px; color:gray!important; border-radius: 10px;">Yes</button><button onclick = "click_no('+id+','+nextQuestion.symptomId+')" style="width: 60px; color:gray!important; height: 30px;border-radius: 10px;">No</button><button onclick = "click_skip('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px; color:gray!important; border-radius: 10px;">Skip</button><p>';
}
if (nextQuestion.symptomId == -1) {
document.getElementById("question").innerHTML = nextQuestion.symptomQuestion;
}

};
loadclick(api_url,api_var1,target.id)



}
  };
loadDoc(api_url,api_var1)
};




function click_yes(previd, id) {
  yes_id.push(parseInt(id))
  var api_var1 = document.getElementById("api_var1").innerHTML;
  var api_url = document.getElementById("api_url").innerHTML;
  document.getElementById("question").innerHTML ='<div class="spinner-border" role="status"><span class="sr-only">'+"Loading..."+'</span></div>'
  //console.log(api_var1)
  function postRequest(url, data) {
    return fetch(url, {
      credentials: 'same-origin', // 'include', default: 'omit'
      method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
      body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    })
    .then(response => response.json())
  };
  async function loadyes(api_url,api_var1) {
  //var api_id = [];
  //api_id.push(previd,id);
  //console.log(api_id)
  //yes_id.push(parseInt(id))
  //console.log("click yes:-yes_id", yes_id)
  //console.log("click yes:-no_id",no_id)
  //console.log("click yes:-skip_id",skip_id)
  var nextQuestion = await postRequest(api_url+'/GetNextSymptomQuestion', {UniqueProductIdentifier: api_var1,
                                                                          SymptomsThatArePresent: yes_id,
                                                                          SymptomsThatAreNOTPresent: no_id,
                                                                          SymptomsThatWereSkipped: skip_id})

  var solution_yes = await postRequest(api_url+'/PredictPartsGivenSymptoms', {UniqueProductIdentifier: api_var1,
                                                                              SymptomsThatArePresent: yes_id,
                                                                              SymptomsThatAreNOTPresent: no_id,
                                                                              SymptomsThatWereSkipped: skip_id})


  let sols =  solution_yes.partsRecommendation.map(function(sol) {
                              if ( sol.probablityPercentage > 75 ){
                              return  '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:green!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                            }
                            return '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:blue!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                            })
document.getElementById("solutions").innerHTML = sols.join("");
document.getElementById("remote-solutions").innerHTML = '<h4>Possible remote solutions:</h4>'
document.getElementById("remote-solutions").innerHTML += solution_yes.remoteSolutions.remoteSolutions.map(function(r_sol) {
                    return  '<p style="padding-left:50px">*'+r_sol+'<p>';
}).join("");

if (nextQuestion.symptomId != -1) {
document.getElementById("question").innerHTML = '<span id='+nextQuestion.symptomId+'>'+nextQuestion.symptomQuestion+'</span><p><button onclick = "click_yes('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px;border-radius: 10px; color:gray!important;">Yes</button><button onclick = "click_no('+id+','+nextQuestion.symptomId+')" style="width: 60px;color:gray!important;height: 30px;border-radius: 10px;">No</button><button onclick = "click_skip('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px; color:gray!important; border-radius: 10px;">Skip</button><p>';
}
if (nextQuestion.symptomId == -1) {
document.getElementById("question").innerHTML = nextQuestion.symptomQuestion;
}




function postRequest(url, data) {
  return fetch(url, {
    credentials: 'same-origin', // 'include', default: 'omit'
    method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
    body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
    headers: new Headers({
      'Content-Type': 'application/json'
    }),
  })
  .then(response => response.json())
};
async function loadyesUI(api_url,api_var1,id) {
var slides = await postRequest(api_url+'/GetRootSymptoms', {UniqueProductIdentifier: api_var1})

slides.forEach(function(slide) {
  if (slide.symptomId == id) {
    document.getElementById("myUL").innerHTML += '<li style="padding-top:10px;"><i class="fa fa-check-circle" style="color:green;" aria-hidden="true"></i>'+slide.symptomText+'</li>'
  }
});
  //.then(data => console.log(data)) // Result from the `response.json()` call
  //.catch(error => console.error(error))
};
loadyesUI(api_url,api_var1,id)
//document.getElementById("myUL").innerHTML += '<li style="padding-top:10px;"><i class="fa fa-check-circle" aria-hidden="true"></i></li>'
}
loadyes(api_url,api_var1,previd,id)
};







function click_no(previd, id) {
  no_id.push(parseInt(id));
  var api_var1 = document.getElementById("api_var1").innerHTML;
  var api_url = document.getElementById("api_url").innerHTML;
  document.getElementById("question").innerHTML ='<div class="spinner-border" role="status"><span class="sr-only">'+"Loading..."+'</span></div>'
  function postRequest(url, data) {
    return fetch(url, {
      credentials: 'same-origin', // 'include', default: 'omit'
      method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
      body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    })
    .then(response => response.json())
  };
  async function loadno(api_url,api_var1,previd,id) {
    //console.log("click no-yes_id", yes_id)
    //console.log("click no-no_id",no_id)
    //console.log("click no-skip_id",skip_id)
  var nextQuestion = await postRequest(api_url+'/GetNextSymptomQuestion', {UniqueProductIdentifier: api_var1,
                                                                          SymptomsThatArePresent: yes_id,
                                                                          SymptomsThatAreNOTPresent: no_id,
                                                                          SymptomsThatWereSkipped: skip_id})




var solution_no = await postRequest(api_url+'/PredictPartsGivenSymptoms', {UniqueProductIdentifier: api_var1,
                                                                          SymptomsThatArePresent: yes_id,
                                                                          SymptomsThatAreNOTPresent: no_id,
                                                                          SymptomsThatWereSkipped: skip_id})


let sols =  solution_no.partsRecommendation.map(function(sol) {
                                if ( sol.probablityPercentage > 75 ){
                                        return  '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:green!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                                        }
                                        return '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:blue!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                                      })
document.getElementById("solutions").innerHTML = sols.join("");
document.getElementById("remote-solutions").innerHTML = '<h4>Possible remote solutions:</h4>'
document.getElementById("remote-solutions").innerHTML += solution_no.remoteSolutions.remoteSolutions.map(function(r_sol) {
                    return  '<p style="padding-left:50px">*'+r_sol+'<p>';
}).join("");
if (nextQuestion.symptomId != -1) {
document.getElementById("question").innerHTML = '<span id='+nextQuestion.symptomId+'>'+nextQuestion.symptomQuestion+'</span><p><button onclick = "click_yes('+id+','+nextQuestion.symptomId+')" style="width: 60px;color:gray!important;height: 30px;border-radius: 10px;">Yes</button><button onclick = "click_no('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px;color:gray!important;border-radius: 10px;">No</button><button onclick = "click_skip('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px;color:gray!important;border-radius: 10px;">Skip</button><p>';
}

if (nextQuestion.symptomId == -1) {
  document.getElementById("question").innerHTML = nextQuestion.symptomQuestion;
}

function postRequest(url, data) {
  return fetch(url, {
    credentials: 'same-origin', // 'include', default: 'omit'
    method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
    body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
    headers: new Headers({
      'Content-Type': 'application/json'
    }),
  })
  .then(response => response.json())
};
async function loadnoUI(api_url,api_var1,id) {
var slides = await postRequest(api_url+'/GetRootSymptoms', {UniqueProductIdentifier: api_var1})

slides.forEach(function(slide) {
  if (slide.symptomId == id) {
    document.getElementById("myUL").innerHTML += '<li style="padding-top:10px;"><i class="fas fa-times-circle" style="color:red;" aria-hidden="true"></i>'+slide.symptomText+'</li>'
  }
});
  //.then(data => console.log(data)) // Result from the `response.json()` call
  //.catch(error => console.error(error))
};
loadnoUI(api_url,api_var1,id)
}
//console.log(previd,id)
loadno(api_url,api_var1,previd,id)
};





function click_skip(previd, id) {
  skip_id.push(id)
  //console.log(id)
  var api_var1 = document.getElementById("api_var1").innerHTML;
  var api_url = document.getElementById("api_url").innerHTML;
  document.getElementById("question").innerHTML ='<div class="spinner-border" role="status"><span class="sr-only">'+"Loading..."+'</span></div>'
  function postRequest(url, data) {
    return fetch(url, {
      credentials: 'same-origin', // 'include', default: 'omit'
      method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
      body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    })
    .then(response => response.json())
  };
  async function loadskip(api_url,api_var1,previd,id) {
    //console.log("click skip-yes_id", yes_id)
    //console.log("click skip-no_id",no_id)
    //console.log("click skip-skip_id",skip_id)
  var nextQuestion = await postRequest(api_url+'/GetNextSymptomQuestion', {UniqueProductIdentifier: api_var1,
                                                                            SymptomsThatArePresent: yes_id,
                                                                            SymptomsThatAreNOTPresent: no_id,
                                                                            SymptomsThatWereSkipped: skip_id})

var solution_skip = await postRequest(api_url+'/PredictPartsGivenSymptoms', {UniqueProductIdentifier: api_var1,
                                                                              SymptomsThatArePresent: yes_id,
                                                                                SymptomsThatAreNOTPresent: no_id,
                                                                              SymptomsThatWereSkipped: skip_id})


let sols =  solution_skip.partsRecommendation.map(function(sol) {
                            if ( sol.probablityPercentage > 75 ){
                                return  '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:green!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                              }
                              return '<div style="margin:20px 20px 20px 20px;"><span class="badge" style="background-color:blue!important;width:50px;">'+sol.probablityPercentage+'%</span><span style="margin-left:20px;font-size:large;">'+sol.partName+'</span><div style="margin-left:70px;"><p style="font-size:small;">Suggested PartId: '+sol.partId+'</p></div></div>'
                          })
document.getElementById("solutions").innerHTML = sols.join("");
document.getElementById("remote-solutions").innerHTML = '<h4>Possible remote solutions:</h4>'
document.getElementById("remote-solutions").innerHTML += solution_skip.remoteSolutions.remoteSolutions.map(function(r_sol) {
                    return  '<p style="padding-left:50px">*'+r_sol+'<p>';
}).join("");

if (nextQuestion.symptomId != -1) {
document.getElementById("question").innerHTML = '<span id='+nextQuestion.symptomId+'>'+nextQuestion.symptomQuestion+'</span><p><button onclick = "click_yes('+id+','+nextQuestion.symptomId+')" style="width: 60px;color:gray!important;height: 30px;border-radius: 10px;">Yes</button><button onclick = "click_no('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px;color:gray!important;border-radius: 10px;">No</button><button onclick = "click_skip('+id+','+nextQuestion.symptomId+')" style="width: 60px;height: 30px;color:gray!important;border-radius: 10px;">Skip</button><p>';
}
if (nextQuestion.symptomId == -1) {
  document.getElementById("question").innerHTML = nextQuestion.symptomQuestion;
}


function postRequest(url, data) {
  return fetch(url, { // 'include', default: 'omit'
    method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
    body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
  })
  .then(response => response.json())
};
async function loadskipUI(api_url,api_var1,id) {
var slides = await postRequest(api_url+'/GetRootSymptoms', {UniqueProductIdentifier: api_var1})

slides.forEach(function(slide) {
  if (slide.symptomId == id) {
    document.getElementById("myUL").innerHTML += '<li style="padding-top:10px;"><i class="far fa-circle" aria-hidden="true"></i>'+slide.symptomText+'</li>'
  }
});
  //.then(data => console.log(data)) // Result from the `response.json()` call
  //.catch(error => console.error(error))
};
loadskipUI(api_url,api_var1,id)
}
loadskip(api_url,api_var1,previd,id)
};





function search() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("button")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
};
