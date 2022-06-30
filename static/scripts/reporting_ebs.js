const data = JSON.parse(json_data);
var footprint_data_boxes =[];
var footprint_title_boxes =[];
// console.log(document.getElementById('footprint_data_3'));

for(let i=0;i<6;i++){     
    footprint_data_boxes.push(document.getElementById('footprint_data_'+String(i+1)))
    footprint_title_boxes.push(document.getElementById('footprint_title_'+String(i+1)))
}
// console.log(footprint_data_boxes);
for(let i=0;i<6;i++){     
    footprint_data_boxes[i].innerHTML=data.EBS[i]
    footprint_title_boxes[i].innerHTML=data["Volume Type"][i]
}