data = JSON.parse(json_data)
console.log(data)
let table = document.getElementById('backup_table')
// let is_modal_open = false

var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
var btn = document.getElementById("myBtn");
var modal_vol_id = document.getElementById('modal_vol_id');
var modal_vol_region = document.getElementById('modal_vol_region');
var cost_ebs = document.getElementById('cost_ebs');
var cost_onprem = document.getElementById('cost_onprem');
var iops_ebs = document.getElementById('iops_ebs');
var iops_onprem = document.getElementById('iops_onprem');
var time_ebs = document.getElementById('time_ebs');
var time_onprem = document.getElementById('time_onprem');
var creating_popup = document.getElementById('creating_popup');
span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

const show_created_popup = (type) => {
    creating_popup.innerHTML="Creating an "+type+" backup for the selected volume"
    creating_popup.style.display='block';
    modal.style.display = "none";
    setTimeout(()=>{
        creating_popup.style.display='none';
    },5000)
}

const show_modal = ( i) => {
    modal.style.display = "block";
    modal_vol_id.innerHTML = data[i]['volumeId']
    modal_vol_region.innerHTML = data[i]['region']
    cost_ebs.innerHTML = Math.round(data[i]['cost_estimate'][0] / 10) * 10
    cost_onprem.innerHTML = Math.round(data[i]['cost_estimate'][1] / 10) * 10
    if(data[i]['cost_estimate'][0]>data[i]['cost_estimate'][1])
    {iops_ebs.innerHTML = data[i]['iops'];
    iops_onprem.innerHTML = Math.round(data[i]['iops']*4/7 /10) * 10;}
    else{iops_ebs.innerHTML = Math.round(data[i]['iops']*4/7 / 10) * 10;
    iops_onprem.innerHTML = data[i]['iops'];}
    time_ebs.innerHTML = data[i]['backup_time'][0]
    time_onprem.innerHTML = data[i]['backup_time'][1]
}
data.forEach((item,index) => {
    let curPar = document.createElement('div');
    curPar.classList.add('backup_table_row')
    for([key,value] of Object.entries(item)){
        if(key=='iops' || key=='backup_time') continue;
        let curChild = document.createElement('div');
        curChild.classList.add('backup_table_item');
        curChild.innerHTML=value;
        if(key=='creation_time'){
            curChild.innerHTML=value.substring(0,10);
        }
        if(key=='cost_estimate'){
            curChild.innerHTML=''
            let recBtn = document.createElement('button');
            recBtn.innerHTML='View';
            recBtn.classList.add('rec_btn')
            recBtn.onclick= ()=>{show_modal(index)};
            curChild.appendChild(recBtn);
        }
        curPar.appendChild(curChild);          
    }
    table.appendChild(curPar);          
})