
window.addEventListener('DOMContentLoaded', selectionHandler);

function selectionHandler() {
    let selection = document.getElementById('procMenuList');
    selection.addEventListener('change', changeContent(selection));
}

function changeContent(choice){
    console.log("Entered changeContent()");
    console.log(choice.value);

    const divs = document.querySelectorAll('.menu-div-container');
    divs.forEach(div=> {
        div.style.display = 'none';
    });
    
    const chart_div = document.getElementById("chart");
    
    switch(choice.value){
        case 'procChoice1':
            chart_div.style.display = 'block';
            break;
        case 'procChoice2':
            // chart_div.style.display = 'none';
            break;
        default:
            break;
    }
    
}