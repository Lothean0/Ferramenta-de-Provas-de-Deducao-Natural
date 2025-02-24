import { React, useState } from 'react';
import { Link } from 'react-router-dom';

import '../styles/TruthTableBody.css';

/*

const TruthTableBody = () => {

    const [isLoading, setIsLoading] = useState(false);

    { //const errors = validateTruthTableInput(inputValue)}
    if (errors) {
        alert(errors);
        return;
    } else {
        setIsLoading(true)
    }

    return (
        <div className='truth-table-container'>
            <button onClick={handleSubmit}>
                Test-Button
            </button>
        </div>
    )
}

*/
function TruthTableBody() {
  
    return (
        <header className="header-container">
            <h1 className="title"> 
                Ferramenta Dedução de Provas Naturais
            </h1>
        </header>  
    )
  }



export default TruthTableBody;