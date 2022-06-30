reporting_sub_items = document.getElementsByClassName('reporting_sub_item');
let show = true;
const  toggleMenu = () => {
    show = !show;
    for(let i=0;i<reporting_sub_items.length;i++){
        if(show==false) reporting_sub_items[i].style.display='None';
        else reporting_sub_items[i].style.display='block';
    }
}

