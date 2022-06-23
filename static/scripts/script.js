var stat_divs = [];
var buttons = [];
var current_id = 1;

const data = JSON.parse(json_data);
var footprint_data_boxes =[];
var footprint_title_boxes =[];
// console.log(document.getElementById('footprint_data_3'));

for(let i=0;i<4;i++){     
    footprint_data_boxes.push(document.getElementById('footprint_data_'+String(i+1)))
    footprint_title_boxes.push(document.getElementById('footprint_title_'+String(i+1)))
}
// console.log(footprint_data_boxes);
for(let i=0;i<4;i++){     
    footprint_data_boxes[i].innerHTML=data.EBS[i]
    footprint_title_boxes[i].innerHTML=data["Volume Type"][i]
}


setTimeout(()=>{
    console.log("time over");
    for(let i=1;i<=5;i++){
        stat_divs.push(document.getElementById('stat_'+i));
        buttons.push(document.getElementById('button_'+i));
        if(i!=1) stat_divs[i-1].style.display='none';
        else { buttons[i-1].classList.add('selectedBorder'); }
    }
},3000);

setTimeout(()=>{
    console.log("time over 2");
    document.getElementById('loading_screen').style.display='none'
},3000);


const changeTo = (id) => {
    buttons[current_id-1].classList.remove('selectedBorder');
    buttons[id-1].classList.add('selectedBorder');
    stat_divs[current_id-1].style.display='none';
    stat_divs[id-1].style.display='block';
    current_id=id;
}

