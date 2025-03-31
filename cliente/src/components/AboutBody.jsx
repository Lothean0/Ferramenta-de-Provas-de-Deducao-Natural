import malainhopf from '../assets/img/malainho.jpg';
import simaopf from '../assets/img/simao.jpg';

import '../styles/AboutBody.css';


function AboutBody() {
    
    return (
        <div className='about-container'>

            <div className='enunciado'>
                <span style={{ color: 'black' }}>
                    Dedução Natural designa um tipo de sistemas formais de prova, onde é permitido raciocinar no contexto de hipóteses e onde  coexistem regras para introdução e para eliminação dos conetivos da lógica em estudo. Por exemplo, este tipo de formalismo é estudado na UC de Lógica de LCC.
                    O objetivo deste projeto é o desenvolvimento de uma ferramenta computacional para a construção assistida de provas em Dedução Natural, no contexto das lógicas clássica e intuicionista. Tal ferramenta poderá ser um instrumento útil no ensino-aprendizagem de sistemas formais de prova.
                    No desenvolvimento da ferramenta tornar-se-á essencial modelar o conceito "estado da prova". Em particular, em cada momento, Em particular, em cada momento, o estado da prova deverá  permitir identificar os sub-problemas/sub-provas que ainda carecem de resolução.
                    Propõe-se que a ferramenta permita ainda representar as provas construídas através de termos-lambda, com recurso à  correspondência Curry-Howard (que relaciona Dedução Natural com  linguagens de programação com tipos funcionais).  Eventuais funcionalidades adicionais da ferramenta deverão ser  discutidas no decurso do projeto.
                    As  linguagens de programação a utilizar no desenvolvimento da ferramenta  serão escolhidas na fase inicial do projeto.
                </span>

                <div className="quadrado">
                    <div className="cabeca">
                        
                        <img src={malainhopf}/>
                        <img src={simaopf}/>
                    </div>
                    <div className="tronco">

                    </div>
                </div>
            </div>

        </div>
    );
}

export default AboutBody;
