import daniel_pfp from '../assets/img/daniel.jpg'
import malainho_pfp from '../assets/img/malainho.jpg';
import simao_pfp from '../assets/img/simao.jpg';

import '../styles/AboutBody.css';


function AboutBody({t}) {
    
    return (
        <div className='about-container'>

            <div className="carousel">
                <div className="elements">
                    <div className="profile">
                        <img src={daniel_pfp} alt="Daniel" />
                        <span className="label">
                            <strong>Daniel Andrade</strong> 
                            <br />
                            <span>A100057</span>
                        </span>
                    </div>
                    <div className="profile">
                        <img src={malainho_pfp} alt="Malainho" />
                        <span className="label">
                            <strong>Pedro Malainho</strong>
                            <br />
                            <span>A100050</span>
                        </span>
                    </div>
                    <div className="profile">
                        <img src={simao_pfp} alt="Simao" />
                        <span className="label">
                            <strong>Simão Ribeiro</strong>
                            <br />
                            <span>A102877</span>
                        </span>
                    </div>
                </div>
            </div>


            <div className='statement'>
                <h2 className="statement-title">Enunciado</h2>
                <span style={{ color: 'black' }}>
                    <p style={{ textIndent: '20px' }}>
                        Dedução Natural designa um tipo de sistemas formais de prova, onde é permitido raciocinar no contexto de hipóteses e onde  coexistem regras para introdução e para eliminação dos conetivos da lógica em estudo. Por exemplo, este tipo de formalismo é estudado na UC de Lógica de LCC.
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        O objetivo deste projeto é o desenvolvimento de uma ferramenta computacional para a construção assistida de provas em Dedução Natural, no contexto das lógicas clássica e intuicionista. Tal ferramenta poderá ser um instrumento útil no ensino-aprendizagem de sistemas formais de prova.
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        No desenvolvimento da ferramenta tornar-se-á essencial modelar o conceito "estado da prova". Em particular, em cada momento, Em particular, em cada momento, o estado da prova deverá  permitir identificar os sub-problemas/sub-provas que ainda carecem de resolução.
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        Propõe-se que a ferramenta permita ainda representar as provas construídas através de termos-lambda, com recurso à  correspondência Curry-Howard (que relaciona Dedução Natural com  linguagens de programação com tipos funcionais).  Eventuais funcionalidades adicionais da ferramenta deverão ser  discutidas no decurso do projeto.
                        As  linguagens de programação a utilizar no desenvolvimento da ferramenta  serão escolhidas na fase inicial do projeto.
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        As  linguagens de programação a utilizar no desenvolvimento da ferramenta  serão escolhidas na fase inicial do projeto.
                    </p>
                </span>
            </div>
            
            <div className='misc-information'>
                <p>© 2025 Ferramenta para Construção de Provas em Dedução Natural — Todos os direitos reservados.</p>
            </div>

        </div>
    );
}

export default AboutBody;
