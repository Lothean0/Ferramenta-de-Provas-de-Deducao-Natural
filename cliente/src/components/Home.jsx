import '../styles/Home.css';
import Card from './Card';

import landscape1 from '../assets/img/landscape-1.png';
import landscape2 from '../assets/img/landscape-2.png';
import landscape3 from '../assets/img/landscape-3.png';

function Home() {
    return (
        <div className='home-container'>
            <div className='card__container'>

                <Card
                    image={landscape1}
                    altText="Propositional Logic"
                    description="Propositional Logic"
                    title="Propositional Logic"
                    link="/Propositional-Logic"
                />

                <Card
                    image={landscape2}
                    altText="Truth Table"
                    description="Truth Table"
                    title="Truth Table"
                    link="/Truth-Table"
                />

                <Card
                    image={landscape3}
                    altText="About"
                    description="About"
                    title="About"
                    link="/About"
                />

            </div>
        </div>  
    );
}

export default Home;