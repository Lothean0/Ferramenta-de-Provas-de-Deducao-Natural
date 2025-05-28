import daniel_pfp from '../assets/img/daniel.jpg'
import malainho_pfp from '../assets/img/malainho.jpg';
import simao_pfp from '../assets/img/simao.jpg';

import '../styles/AboutBody.css';


function AboutBody({translate}) {

    const t = translate
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
                <h2 className="statement-title">{t("statement_title")}</h2>
                <span style={{ color: 'black' }}>
                    <p style={{ textIndent: '20px' }}>
                        {t("p1")}
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        {t("p2")}
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        {t("p3")}
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        {t("p4")}
                    </p>
                    <p style={{ textIndent: '20px' }}>
                        {t("p5")}
                    </p>
                </span>
            </div>
            
            <div className='misc-information'>
                <p>{t("copyright")}</p>
            </div>

        </div>
    );
}

export default AboutBody;
