var stat_divs = [];
var buttons = [];
var current_id = 1;


setTimeout(()=>{
    console.log("time over");
    for(let i=1;i<=3;i++){
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

