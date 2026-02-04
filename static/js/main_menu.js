
window.addEventListener('DOMContentLoaded', selectionHandler);

function selectionHandler() {
    let selection = document.getElementById('mainMenuList');
    selection.addEventListener('change', changeContent(selection));
}

function changeContent(choice){
    console.log("Entered changeContent()");
    console.log(choice.value);
    const importForm = document.getElementById('import_form');
    //const processForm = document.getElementById('process_form');

    const forms = document.querySelectorAll('.form-container');
    forms.forEach(form => {
        form.style.display = 'none';
    });
    
    switch(choice.value){
        case 'mainChoice1':
            importForm.style.display = 'block';
            break;
        // case 'mainChoice2':
        //     processForm.style.display = 'block';
        //     break;
        default:
            break;
    }
    
}